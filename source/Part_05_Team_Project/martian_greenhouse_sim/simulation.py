"""
Main simulation loop for the Martian greenhouse stress test.

The simulation runs for a configurable number of Martian sols at a fixed
time step (default 60 s).  Each run:

  1. Models external Martian conditions (diurnal temperature + solar).
  2. Schedules **one guaranteed global dust storm** (2 – 5 sols long, random
     start) to test whether the student controller compensates for sudden
     solar loss and temperature drop.
  3. Activates a **K30 CO₂ sensor freeze fault** (sensor stuck at 400 ppm)
     to verify that students implement sensor redundancy logic.
  4. Scores controller performance against Lettuce growth targets.

Usage
-----
Run as a script to execute a 30-sol simulation with the stub controller::

    python -m martian_greenhouse_sim.simulation

Or import and call programmatically::

    from martian_greenhouse_sim.simulation import run_simulation
    from martian_greenhouse_sim.controllers import StudentPIDController

    result = run_simulation(days=30, seed=42)
    print(result.summary())

    # Optional: dump per-step data to CSV
    with open("sim_log.csv", "w") as f:
        f.write(result.to_csv())   # requires log_records=True
"""

import csv
import importlib
import importlib.util
import io
import json
import random
import sys
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Type

from .actuators import VirtualActuators
from .constants import (
    CO2_TOXIC_DURATION_S,
    CO2_TOXIC_PPM,
    DEFAULT_DT_S,
    DEFAULT_SEED,
    LETTUCE_CO2_HIGH_PPM,
    LETTUCE_CO2_LOW_PPM,
    LETTUCE_CO2_SETPOINT_PPM,
    LETTUCE_RH_HIGH_PCT,
    LETTUCE_RH_LOW_PCT,
    LETTUCE_RH_SETPOINT_PCT,
    LETTUCE_TEMP_DAY_C,
    LETTUCE_TEMP_NIGHT_C,
    LETTUCE_VWC_SETPOINT,
    SCORING_MAX_POINTS,
    SCORING_TARGET_SOLS,
    SOL_SECONDS,
)
from .controllers import (
    ActuatorCommands,
    SensorReadings,
    Setpoints,
    StudentPIDController,
)
from .environment import MarsEnvironment
from .greenhouse import Greenhouse
from .plants import PlantCohort
from .sensors import VirtualSensors

# ---------------------------------------------------------------------------
# Per-step log record
# ---------------------------------------------------------------------------


@dataclass
class SimulationRecord:
    """One row of the per-step simulation log (populated when log_records=True)."""

    time_s: float
    sol: float
    t_out_c: float
    tau: float
    t_in_c: float
    rh_pct: float
    co2_ppm: float
    soil_vwc: float
    par_umol: float
    heater_pct: float
    led_pct: float
    co2_valve_pct: float
    pump_pct: float
    co2_k30_reading: float
    co2_scd41_reading: float
    co2_freeze_active: bool
    dust_storm_active: bool


# ---------------------------------------------------------------------------
# Simulation result
# ---------------------------------------------------------------------------


@dataclass
class SimulationResult:
    """
    Performance summary returned by :func:`run_simulation`.

    Attributes
    ----------
    mean_temp_error_c : float
        Mean absolute error between the internal temperature and the active
        setpoint (23 °C day / 18 °C night), averaged over all time steps.
    co2_in_range_fraction : float
        Fraction of time steps in which CO₂ was within [800, 1 000] ppm.
    rh_in_range_fraction : float
        Fraction of time steps in which RH was within [40, 60] %.
    co2_toxic_event : bool
        True if CO₂ exceeded 5 000 ppm for 30 or more continuous minutes.
    co2_toxic_duration_s : float
        Total accumulated seconds that CO₂ was above 5 000 ppm.
    records : list of SimulationRecord
        Per-step log (empty unless ``log_records=True`` was passed to
        :func:`run_simulation`).
    """

    days: int
    dt_seconds: float
    seed: int
    total_steps: int
    steps_run: int = 0

    mean_temp_error_c: float = 0.0
    co2_in_range_fraction: float = 0.0
    rh_in_range_fraction: float = 0.0
    co2_toxic_event: bool = False
    co2_toxic_duration_s: float = 0.0

    # Plant cohort results
    terminated_early: bool = False
    failure_sol: Optional[float] = None
    failure_cause: Optional[str] = None
    failure_snapshot: Optional[Dict[str, Any]] = None
    plant_health: float = 1.0
    sols_survived: float = 0.0

    records: List[SimulationRecord] = field(default_factory=list)

    def plant_survival_score(self, max_points: float = SCORING_MAX_POINTS) -> float:
        """Return the Gradescope score based on sols survived (0 – max_points)."""
        return round(max_points * min(self.sols_survived / SCORING_TARGET_SOLS, 1.0), 3)

    def failure_report(self) -> str:
        """Return a concise, student-readable failure report (fits in one screen)."""
        if not self.terminated_early:
            return (
                f"Plants survived the full {self.days}-sol mission.\n"
                f"Sols survived : {self.sols_survived:.2f} / {float(self.days):.2f}"
            )
        lines = [
            "PLANT COHORT FAILURE",
            f"  Survived      : {self.sols_survived:.2f} / {float(self.days):.2f} sols",
            f"  Cause         : {self.failure_cause}",
            f"  Failed at sol : {self.failure_sol:.3f}",
        ]
        if self.failure_snapshot:
            snap = self.failure_snapshot
            (lines.append("  Last readings :"),)
            lines.append(
                f"    T_in={snap.get('t_in_c', 0):.1f} °C  "
                f"VWC={snap.get('soil_vwc', 0):.3f}  "
                f"PAR={snap.get('par_umol', 0):.0f} µmol/m²/s"
            )
            lines.append("  Last commands :")
            lines.append(
                f"    heater={snap.get('heater_pct', 0):.0f}%  "
                f"LED={snap.get('led_pct', 0):.0f}%  "
                f"pump={snap.get('pump_pct', 0):.0f}%"
            )
        lines.append("")
        cause_hint = {
            "TEMP_LETHAL_LOW": "Hint: internal temperature dropped below 5 °C for over 2 hours.",
            "TEMP_LETHAL_HIGH": "Hint: internal temperature exceeded 40 °C for over 1 hour.",
            "SOIL_DROUGHT": "Hint: soil VWC stayed below 0.10 for over 1 sol.",
            "SOIL_WATERLOG": "Hint: soil VWC stayed above 0.70 for over 0.5 sol.",
            "LIGHT_INSUFFICIENT": (
                "Hint: PAR accumulated below 150 µmol/m²/s for over 2 cumulative sols. "
                "Check LED compensation during dust storms."
            ),
        }
        lines.append(cause_hint.get(self.failure_cause, ""))
        return "\n".join(lines)

    def to_gradescope_json(self, output_path: Optional[str] = None) -> dict:
        """
        Return (and optionally write) a Gradescope-compatible summary dict.

        The dict is suitable for ``plant_report.json`` which ``grader/post.py``
        reads to inject a partial-credit plant-survival score.
        """
        data = {
            "sols_survived": self.sols_survived,
            "target_sols": float(self.days),
            "terminated_early": self.terminated_early,
            "failure_cause": self.failure_cause,
            "failure_sol": self.failure_sol,
            "plant_health": self.plant_health,
            "failure_report": self.failure_report(),
        }
        if output_path is not None:
            with open(output_path, "w", encoding="utf-8") as fh:
                json.dump(data, fh, indent=2)
        return data

    def summary(self) -> str:
        """Return a human-readable performance summary string."""
        lines = [
            f"{'=' * 60}",
            f"  Martian Greenhouse Simulation — {self.days}-sol run",
            f"  Δt = {self.dt_seconds:.0f} s  |  seed = {self.seed}",
            f"{'=' * 60}",
            f"  Temperature MAE        : {self.mean_temp_error_c:.2f} °C",
            f"  CO₂ in range           : {self.co2_in_range_fraction:.1%}  "
            f"[target {LETTUCE_CO2_LOW_PPM:.0f}–{LETTUCE_CO2_HIGH_PPM:.0f} ppm]",
            f"  RH in range            : {self.rh_in_range_fraction:.1%}  "
            f"[target {LETTUCE_RH_LOW_PCT:.0f}–{LETTUCE_RH_HIGH_PCT:.0f} %]",
        ]
        if self.co2_toxic_event:
            lines.append(
                f"  CO₂ safety             : FAIL — {self.co2_toxic_duration_s:.0f} s "
                f"above {CO2_TOXIC_PPM:.0f} ppm"
            )
        else:
            lines.append("  CO₂ safety             : PASS")
        lines.append("")
        lines.append(self.failure_report())
        lines.append(f"{'=' * 60}")
        return "\n".join(lines)

    def to_csv(self) -> str:
        """
        Serialise per-step records to a CSV string.

        Returns an empty string if ``run_simulation`` was called with
        ``log_records=False`` (the default).
        """
        if not self.records:
            return ""
        buf = io.StringIO()
        fieldnames = list(asdict(self.records[0]).keys())
        writer = csv.DictWriter(buf, fieldnames=fieldnames)
        writer.writeheader()
        for record in self.records:
            writer.writerow(asdict(record))
        return buf.getvalue()


# ---------------------------------------------------------------------------
# Helper
# ---------------------------------------------------------------------------


def _build_setpoints(env: MarsEnvironment) -> Setpoints:
    """Return the current Lettuce setpoints based on the diurnal phase."""
    is_day = env.is_daytime()
    return Setpoints(
        temperature_c=LETTUCE_TEMP_DAY_C if is_day else LETTUCE_TEMP_NIGHT_C,
        co2_ppm=LETTUCE_CO2_SETPOINT_PPM,
        rh_pct=LETTUCE_RH_SETPOINT_PCT,
        soil_vwc=LETTUCE_VWC_SETPOINT,
        is_daytime=is_day,
    )


# ---------------------------------------------------------------------------
# Main simulation loop
# ---------------------------------------------------------------------------


def run_simulation(
    days: int = 30,
    dt_seconds: float = DEFAULT_DT_S,
    seed: int = DEFAULT_SEED,
    controller_cls: Type = StudentPIDController,
    log_records: bool = False,
) -> SimulationResult:
    """
    Run the Martian greenhouse stress-test simulation.

    Stress events
    -------------
    **Global dust storm** — A single dust storm is injected at a random sol
    between 2 and ``days − 5``.  Its duration is 2 – 5 sols and its peak Tau
    is drawn from [5.0, 8.5], reducing solar irradiance by 57 – 97 %.
    Student controllers must ramp up the heater to compensate.

    **K30 CO₂ sensor freeze fault** — During the run the K30 primary CO₂
    sensor occasionally freezes and returns a stuck reading of 400 ppm.
    The SCD41 backup continues to return correct (noisy) readings.  A
    controller that fails to detect and handle this fault will drive CO₂ to
    toxic levels (> 5 000 ppm), triggering an automatic failure flag.

    Parameters
    ----------
    days : int
        Simulation duration in Martian sols (default 30).
    dt_seconds : float
        Time step in seconds (default 60 s).
    seed : int
        RNG seed for reproducible storm scheduling, sensor noise, and fault
        injection (default 42).
    controller_cls : type
        Student controller class.  Must expose an
        ``update(readings, setpoints, dt) -> ActuatorCommands`` method.
    log_records : bool
        If True, populate ``SimulationResult.records`` with a per-step log.
        Useful for plotting and debugging; adds memory overhead for long runs.

    Returns
    -------
    SimulationResult
        Performance summary and optional step-by-step log.
    """
    # Separate seeds so storm schedule and sensor noise are independent
    env_rng = random.Random(seed)
    sensor_rng = random.Random(seed + 1)

    # --- Initialise subsystems ---
    env = MarsEnvironment(rng=env_rng)
    greenhouse = Greenhouse()
    actuators = VirtualActuators()
    sensors = VirtualSensors(greenhouse, rng=sensor_rng)
    controller = controller_cls()

    # --- Schedule one guaranteed global dust storm ---
    total_sim_s = days * SOL_SECONDS
    # Storm starts at a random sol in [2, days-5] (clamped so it fits)
    storm_start_sol = env_rng.uniform(2.0, max(3.0, float(days) - 5.0))
    storm_duration_sol = env_rng.uniform(2.0, 5.0)
    storm = env.schedule_dust_storm(
        start_time_s=storm_start_sol * SOL_SECONDS,
        duration_s=storm_duration_sol * SOL_SECONDS,
    )

    # --- Initialise plant cohort ---
    plants = PlantCohort()

    # --- Evaluation accumulators ---
    total_steps = int(total_sim_s / dt_seconds)
    temp_error_sum = 0.0
    co2_in_range_count = 0
    rh_in_range_count = 0
    co2_toxic_s = 0.0
    records: List[SimulationRecord] = []
    steps_run = 0

    # Snapshot of the last tick's conditions (used in failure report)
    last_snapshot: Dict[str, Any] = {}

    for _step in range(total_steps):
        steps_run += 1
        current_time_s = env.get_time_s()

        # 1. Advance fault state (must happen before reading sensors)
        sensors.tick_faults(current_time_s, dt_seconds)

        # 2. Read sensors
        temp_reading, rh_reading = sensors.read_DHT22()
        co2_k30 = sensors.read_K30()  # primary — may be frozen at 400 ppm
        co2_scd41 = sensors.read_SCD41()  # backup  — always correct
        vwc_reading = sensors.read_TEROS12()
        par_reading = sensors.read_SQ500()

        # 3. Build controller inputs
        readings = SensorReadings(
            temperature_c=temp_reading,
            rh_pct=rh_reading,
            co2_ppm_primary=co2_k30,
            co2_ppm_backup=co2_scd41,
            soil_vwc=vwc_reading,
            par_umol_m2_s=par_reading,
        )
        setpoints = _build_setpoints(env)

        # 4. Student controller step
        commands: ActuatorCommands = controller.update(readings, setpoints, dt_seconds)

        # 5. Apply actuator commands (VirtualActuators clamps to [0, 100])
        actuators.set_heater(commands.heater_pct)
        actuators.set_LED_lights(commands.led_pct)
        actuators.inject_CO2(commands.co2_valve_pct)
        actuators.run_irrigation_pump(commands.pump_pct)

        # 6. Advance physics (environment first, then greenhouse)
        env.update(dt_seconds)
        state = greenhouse.update_state(env, actuators.state, dt_seconds)

        # 7. Score against Lettuce targets
        temp_error_sum += abs(state.temp_c - setpoints.temperature_c)

        if LETTUCE_CO2_LOW_PPM <= state.co2_ppm <= LETTUCE_CO2_HIGH_PPM:
            co2_in_range_count += 1
        if LETTUCE_RH_LOW_PCT <= state.rh_pct <= LETTUCE_RH_HIGH_PCT:
            rh_in_range_count += 1
        if state.co2_ppm > CO2_TOXIC_PPM:
            co2_toxic_s += dt_seconds

        # 8. Update plant cohort
        plants.update(
            temp_c=state.temp_c,
            soil_vwc=state.soil_vwc,
            par_umol=state.par_umol_m2_s,
            dt_seconds=dt_seconds,
            current_time_s=current_time_s,
        )
        last_snapshot = {
            "t_in_c": state.temp_c,
            "soil_vwc": state.soil_vwc,
            "par_umol": state.par_umol_m2_s,
            "heater_pct": commands.heater_pct,
            "led_pct": commands.led_pct,
            "co2_valve_pct": commands.co2_valve_pct,
            "pump_pct": commands.pump_pct,
        }

        # 9. Optional per-step logging (includes the death step when terminated)
        if log_records:
            dust_active = storm.start_time_s <= current_time_s < storm.end_time_s
            records.append(
                SimulationRecord(
                    time_s=current_time_s,
                    sol=env.get_sol(),
                    t_out_c=env.get_temperature_c(),
                    tau=env.get_tau(),
                    t_in_c=state.temp_c,
                    rh_pct=state.rh_pct,
                    co2_ppm=state.co2_ppm,
                    soil_vwc=state.soil_vwc,
                    par_umol=state.par_umol_m2_s,
                    heater_pct=commands.heater_pct,
                    led_pct=commands.led_pct,
                    co2_valve_pct=commands.co2_valve_pct,
                    pump_pct=commands.pump_pct,
                    co2_k30_reading=co2_k30,
                    co2_scd41_reading=co2_scd41,
                    co2_freeze_active=sensors.co2_freeze_active,
                    dust_storm_active=dust_active,
                )
            )

        # 10. Early-stop check (after logging so death step is included)
        if not plants.alive:
            break

    denom = steps_run if steps_run > 0 else 1
    sols_survived = (steps_run * dt_seconds) / SOL_SECONDS

    return SimulationResult(
        days=days,
        dt_seconds=dt_seconds,
        seed=seed,
        total_steps=total_steps,
        steps_run=steps_run,
        mean_temp_error_c=temp_error_sum / denom,
        co2_in_range_fraction=co2_in_range_count / denom,
        rh_in_range_fraction=rh_in_range_count / denom,
        co2_toxic_event=co2_toxic_s >= CO2_TOXIC_DURATION_S,
        co2_toxic_duration_s=co2_toxic_s,
        terminated_early=not plants.alive,
        failure_sol=plants.failure_sol,
        failure_cause=plants.failure_cause,
        failure_snapshot=last_snapshot if not plants.alive else None,
        plant_health=plants.health,
        sols_survived=sols_survived,
        records=records,
    )


# ---------------------------------------------------------------------------
# Student submission loader
# ---------------------------------------------------------------------------


def load_student_controller(search_dirs: Optional[List[str]] = None) -> Type:
    """
    Locate and load the student's controller class from their submission.

    The function searches for either:

    * ``student_controller.py``   — a single-file submission, or
    * ``student_controller/``     — a package directory containing
      ``__init__.py`` (which must re-export ``GreenhouseController``).

    In both cases the module must define a class named
    ``GreenhouseController`` with an ``update(readings, setpoints, dt)``
    method whose signature matches :class:`~.controllers.StudentPIDController`.

    Parameters
    ----------
    search_dirs : list of str, optional
        Directories to search (in order).  The current working directory is
        always appended as a final fallback.

    Returns
    -------
    type
        The ``GreenhouseController`` class found in the student's module.

    Raises
    ------
    FileNotFoundError
        If no submission is found in any of the searched directories.
    AttributeError
        If the located module does not define ``GreenhouseController``.
    """
    dirs_to_try: List[Path] = []
    if search_dirs:
        dirs_to_try.extend(Path(d) for d in search_dirs)
    dirs_to_try.append(Path.cwd())

    for directory in dirs_to_try:
        # Option A: single file
        single_file = directory / "student_controller.py"
        if single_file.is_file():
            spec = importlib.util.spec_from_file_location(  # type: ignore[attr-defined]
                "student_controller", single_file
            )
            if spec and spec.loader:
                module = importlib.util.module_from_spec(spec)  # type: ignore[attr-defined]
                sys.modules["student_controller"] = module
                spec.loader.exec_module(module)
                return getattr(module, "GreenhouseController")

        # Option B: package directory
        pkg_dir = directory / "student_controller"
        if pkg_dir.is_dir() and (pkg_dir / "__init__.py").is_file():
            if str(directory) not in sys.path:
                sys.path.insert(0, str(directory))
            module = importlib.import_module("student_controller")
            return getattr(module, "GreenhouseController")

    searched = ", ".join(str(d) for d in dirs_to_try)
    raise FileNotFoundError(
        "No student_controller.py or student_controller/ package found. "
        f"Searched: {searched}"
    )


if __name__ == "__main__":
    print("Running 30-sol Martian greenhouse stress test (stub controller)…")
    result = run_simulation(days=30, seed=DEFAULT_SEED)
    print(result.summary())
