"""
Aggregate plant cohort health model for the Martian greenhouse simulation.

The model tracks three failure modes only (as specified for student grading):

    1. Temperature — lethal cold (< 5 °C) or lethal heat (> 40 °C).
    2. Soil moisture — drought (VWC < 0.10) or waterlogging (VWC > 0.70).
    3. Light — insufficient PAR (< 150 µmol/m²/s).

Stress accumulation and recovery
--------------------------------
Each failure mode has a **stress accumulator** (in seconds).  When conditions
fall into a dangerous band, the accumulator grows by dt each tick.  When
conditions recover to a safe level, the accumulator decays exponentially:

    s(t + dt) = s(t) · exp(−dt / τ)

where τ is the mode-specific recovery time constant (see :mod:`constants`).
This means:

* Plants are not immediately fine after brief relief — they carry memory of
  past stress.
* Stress does eventually clear if conditions are good for long enough.
* Death still requires *sustained* exposure: the accumulator must reach its
  lethal threshold before plants die.

Health
------
``health`` is a float in [0.0, 1.0] derived from the worst normalised stress
accumulator across all active failure modes.  It decreases continuously as
plants accumulate stress and recovers (slowly) when conditions improve.

Early-stop contract
-------------------
The simulation loop must call :meth:`PlantCohort.update` once per tick.
When :attr:`PlantCohort.alive` becomes ``False`` the caller should stop the
loop immediately and record :attr:`PlantCohort.failure_cause` and
:attr:`PlantCohort.failure_sol`.

Failure cause codes
-------------------
``"TEMP_LETHAL_LOW"``
    Internal temperature below 5 °C long enough to exhaust the lethal-cold
    stress accumulator.
``"TEMP_LETHAL_HIGH"``
    Internal temperature above 40 °C long enough to exhaust the lethal-heat
    stress accumulator.
``"SOIL_DROUGHT"``
    Soil VWC below 0.10 long enough to exhaust the drought accumulator.
``"SOIL_WATERLOG"``
    Soil VWC above 0.70 long enough to exhaust the waterlogging accumulator.
``"LIGHT_INSUFFICIENT"``
    PAR below 150 µmol/m²/s long enough to exhaust the low-light accumulator.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Optional

from .constants import (
    PLANT_DROUGHT_DURATION_S,
    PLANT_DROUGHT_VWC,
    PLANT_LETHAL_HIGH_C,
    PLANT_LETHAL_HIGH_DURATION_S,
    PLANT_LETHAL_LOW_C,
    PLANT_LETHAL_LOW_DURATION_S,
    PLANT_LOW_LIGHT_DURATION_S,
    PLANT_LOW_PAR_UMOL,
    PLANT_RECOVERY_LIGHT_TAU_S,
    PLANT_RECOVERY_SOIL_TAU_S,
    PLANT_RECOVERY_TEMP_TAU_S,
    PLANT_WATERLOG_DURATION_S,
    PLANT_WATERLOG_VWC,
    SOL_SECONDS,
)

# ---------------------------------------------------------------------------
# Failure cause constants (importable by tests and grader)
# ---------------------------------------------------------------------------

CAUSE_TEMP_LOW = "TEMP_LETHAL_LOW"
CAUSE_TEMP_HIGH = "TEMP_LETHAL_HIGH"
CAUSE_DROUGHT = "SOIL_DROUGHT"
CAUSE_WATERLOG = "SOIL_WATERLOG"
CAUSE_LIGHT = "LIGHT_INSUFFICIENT"


@dataclass
class PlantCohort:
    """
    Aggregate plant-cohort health model.

    Instantiate once at the start of the simulation.  Call :meth:`update`
    every tick *after* the greenhouse physics have been advanced.

    Attributes
    ----------
    alive : bool
        False when a lethal threshold has been crossed.
    health : float
        Aggregate health in [0.0, 1.0]; 0.0 means dead.
    failure_cause : str or None
        One of the CAUSE_* constants, set at the moment of death.
    failure_sol : float or None
        Fractional Martian sol at which death was declared.
    stress : dict
        Mapping from cause-code → accumulated stress seconds (useful for
        diagnostics and snapshots).
    """

    alive: bool = True
    health: float = 1.0
    failure_cause: Optional[str] = None
    failure_sol: Optional[float] = None

    # Stress accumulators (seconds of equivalent lethal exposure).
    # Each accumulator grows when conditions are in the dangerous band and
    # decays exponentially when conditions recover.
    _temp_low_s: float = field(default=0.0, repr=False)
    _temp_high_s: float = field(default=0.0, repr=False)
    _drought_s: float = field(default=0.0, repr=False)
    _waterlog_s: float = field(default=0.0, repr=False)
    _low_light_s: float = field(default=0.0, repr=False)

    @property
    def stress(self) -> dict:
        """Return a snapshot of all stress accumulators (seconds)."""
        return {
            CAUSE_TEMP_LOW: self._temp_low_s,
            CAUSE_TEMP_HIGH: self._temp_high_s,
            CAUSE_DROUGHT: self._drought_s,
            CAUSE_WATERLOG: self._waterlog_s,
            CAUSE_LIGHT: self._low_light_s,
        }

    def update(
        self,
        temp_c: float,
        soil_vwc: float,
        par_umol: float,
        dt_seconds: float,
        current_time_s: float,
    ) -> None:
        """
        Advance the plant cohort model by one time step.

        Parameters
        ----------
        temp_c : float
            Current internal air temperature (°C).
        soil_vwc : float
            Current volumetric water content of the soil (dimensionless).
        par_umol : float
            Current PAR at crop level (µmol/m²/s).
        dt_seconds : float
            Duration of this tick (seconds).
        current_time_s : float
            Elapsed simulation time at the *start* of this tick (seconds).
        """
        if not self.alive:
            return  # once dead, never update

        # --- Accumulate stress / decay toward zero on recovery ---
        # Each stressor uses the same pattern:
        #   - In the dangerous band: accumulator += dt_seconds
        #   - Outside the band: accumulator *= exp(-dt_seconds / τ)
        # This gives genuine stress memory: a brief period of safe conditions
        # does not instantly erase accumulated damage.

        # Temperature cold
        if temp_c < PLANT_LETHAL_LOW_C:
            self._temp_low_s += dt_seconds
        else:
            self._temp_low_s *= math.exp(-dt_seconds / PLANT_RECOVERY_TEMP_TAU_S)

        # Temperature heat
        if temp_c > PLANT_LETHAL_HIGH_C:
            self._temp_high_s += dt_seconds
        else:
            self._temp_high_s *= math.exp(-dt_seconds / PLANT_RECOVERY_TEMP_TAU_S)

        # Soil drought
        if soil_vwc < PLANT_DROUGHT_VWC:
            self._drought_s += dt_seconds
        else:
            self._drought_s *= math.exp(-dt_seconds / PLANT_RECOVERY_SOIL_TAU_S)

        # Soil waterlogging
        if soil_vwc > PLANT_WATERLOG_VWC:
            self._waterlog_s += dt_seconds
        else:
            self._waterlog_s *= math.exp(-dt_seconds / PLANT_RECOVERY_SOIL_TAU_S)

        # Low light (same exponential decay on recovery; normal nighttime
        # darkness decays during daytime, so it does not accumulate to a
        # lethal level over a normal sol cycle — only sustained storm darkness
        # will push the accumulator past the threshold)
        if par_umol < PLANT_LOW_PAR_UMOL:
            self._low_light_s += dt_seconds
        else:
            self._low_light_s *= math.exp(-dt_seconds / PLANT_RECOVERY_LIGHT_TAU_S)

        # --- Check death thresholds ---
        death_checks = [
            (self._temp_low_s, PLANT_LETHAL_LOW_DURATION_S, CAUSE_TEMP_LOW),
            (self._temp_high_s, PLANT_LETHAL_HIGH_DURATION_S, CAUSE_TEMP_HIGH),
            (self._drought_s, PLANT_DROUGHT_DURATION_S, CAUSE_DROUGHT),
            (self._waterlog_s, PLANT_WATERLOG_DURATION_S, CAUSE_WATERLOG),
            (self._low_light_s, PLANT_LOW_LIGHT_DURATION_S, CAUSE_LIGHT),
        ]
        for acc, threshold, cause in death_checks:
            if acc >= threshold:
                self.alive = False
                self.health = 0.0
                self.failure_cause = cause
                self.failure_sol = current_time_s / SOL_SECONDS
                return

        # --- Compute health as 1 − max normalised stress ---
        worst_fraction = max(
            self._temp_low_s / PLANT_LETHAL_LOW_DURATION_S,
            self._temp_high_s / PLANT_LETHAL_HIGH_DURATION_S,
            self._drought_s / PLANT_DROUGHT_DURATION_S,
            self._waterlog_s / PLANT_WATERLOG_DURATION_S,
            self._low_light_s / PLANT_LOW_LIGHT_DURATION_S,
        )
        self.health = max(0.0, 1.0 - worst_fraction)
