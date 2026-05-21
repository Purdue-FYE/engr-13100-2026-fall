"""Autograder config for the Martian Greenhouse Simulation design project.

Grades a student `student_controller.py` against the simulation framework
across the following weighted criteria (total = 100 points):

  test_00 (5 pts) — file presence: student_controller.py exists
  test_10 (5 pts) — module loads without raising
  test_20 (10 pts) — simulation runs to completion without exception
  test_30 (15 pts) — no CO2 toxic event (verifies K30 redundancy logic)
  test_40 (25 pts) — plants survive at least 28 of 30 sols
  test_50 (15 pts) — mean temperature error below 3.0 °C
  test_60 (15 pts) — CO2 inside [800, 1000] ppm at least 65 % of ticks
  test_70 (5 pts)  — RH inside [40, 60] %% at least 1 % of ticks (see note)
  test_80 (5 pts)  — deterministic: same seed yields same result

Notes
-----

* **RH (test_70):** the current simulation has no dehumidifier actuator,
  so any irrigation pulse drives RH to 100 %% until evaporation balances.
  A 1 %% in-range floor verifies the controller does not entirely abandon
  RH. Tighten this threshold once either a dehumidifier is added to the
  simulation or the rubric explicitly de-prioritises RH.

* **File presence (test_00):** we use a path-based check instead of
  `generic_grader.file.file_presence` because the latter enforces a Purdue
  ``<filename>_<login>.py`` convention but `load_student_controller` in the
  simulation package hardcodes the filename ``student_controller.py``. For
  production, the autograder runtime should rename the submitted
  ``student_controller_<login>.py`` to ``student_controller.py`` before
  invoking pytest, or the loader should be taught to glob.

Run locally with:

    uv run pytest source/Part_05_Team_Project/tasks/team_1/a/test_config.py -q
"""

import sys
import unittest
from pathlib import Path

from generic_grader.utils.options import Options
from gradescope_utils.autograder_utils.decorators import number, visibility, weight

# The simulation package lives one directory above this assignment in the
# repo tree. We add it to sys.path so the student's submission can `import
# martian_greenhouse_sim` regardless of where pytest is invoked from.
_ASSIGNMENT_DIR = Path(__file__).resolve().parent
_PART_05_DIR = _ASSIGNMENT_DIR.parents[2]  # source/Part_05_Team_Project/
for _p in (str(_PART_05_DIR), str(_ASSIGNMENT_DIR)):
    if _p not in sys.path:
        sys.path.insert(0, _p)

from martian_greenhouse_sim.simulation import (  # noqa: E402
    SimulationResult,
    load_student_controller,
    run_simulation,
)

DUE_DATE = None  # Filled in when the assignment is scheduled.

SUB_MODULE = "student_controller"
REQUIRED_FILES = (SUB_MODULE + ".py",)

file_set_up_options = Options(required_files=REQUIRED_FILES)


# ---------------------------------------------------------------------------
# File presence — path-based (see module docstring for why)
# ---------------------------------------------------------------------------


class TestFilePresence(unittest.TestCase):
    """Verify the student submission file is on disk."""

    @weight(5)
    @number("0.0")
    def test_00_student_controller_present(self):
        """student_controller.py (or student_controller/) must exist."""
        single_file = _ASSIGNMENT_DIR / "student_controller.py"
        package_dir = _ASSIGNMENT_DIR / "student_controller"
        package_init = package_dir / "__init__.py"
        found = single_file.is_file() or (package_dir.is_dir() and package_init.is_file())
        self.assertTrue(
            found,
            "No submission found. Expected either "
            f"'{single_file.name}' or '{package_dir.name}/__init__.py' "
            f"in {_ASSIGNMENT_DIR}.",
        )


# ---------------------------------------------------------------------------
# Shared simulation fixture
# ---------------------------------------------------------------------------

# Fixed seed makes grading deterministic. A different seed should be used for
# the hidden test set when this assignment ships.
SEED = 42
DAYS = 30


def _load_controller():
    """Locate the student submission via load_student_controller."""
    return load_student_controller(search_dirs=[str(_ASSIGNMENT_DIR)])


def _run_with_student() -> SimulationResult:
    """Run the canonical 30-sol seed=42 simulation with the student controller."""
    controller_cls = _load_controller()
    return run_simulation(
        days=DAYS,
        seed=SEED,
        controller_cls=controller_cls,
    )


# ---------------------------------------------------------------------------
# Performance tests
# ---------------------------------------------------------------------------


class TestDesignProject(unittest.TestCase):
    """Performance criteria for the Martian Greenhouse controller."""

    # Caches the simulation result across tests in the same class so we only
    # pay the ~1-second cost once even though many tests inspect it.
    _result: SimulationResult | None = None

    @classmethod
    def _result_cached(cls) -> SimulationResult:
        if cls._result is None:
            cls._result = _run_with_student()
        return cls._result

    @weight(5)
    @number("1.0")
    def test_10_loads_controller(self):
        """student_controller.GreenhouseController must load without raising."""
        cls = _load_controller()
        self.assertTrue(
            callable(cls),
            "load_student_controller returned a non-callable object",
        )
        instance = cls()
        self.assertTrue(
            hasattr(instance, "update"),
            "GreenhouseController must define an update() method",
        )

    @weight(10)
    @number("2.0")
    def test_20_simulation_completes(self):
        """The 30-sol simulation must run end-to-end without exception."""
        result = self._result_cached()
        self.assertIsInstance(result, SimulationResult)
        self.assertGreater(
            result.total_steps,
            0,
            "Simulation reported zero total steps",
        )

    @weight(15)
    @number("3.0")
    def test_30_no_toxic_co2_event(self):
        """The controller must NOT trigger a CO2 toxic event.

        This verifies the K30 / SCD41 sensor-redundancy pattern is in place.
        A controller that blindly trusts the frozen K30 reading injects CO2
        continuously and crosses the 5000 ppm toxic threshold.
        """
        result = self._result_cached()
        self.assertFalse(
            result.co2_toxic_event,
            "CO2 toxic event detected — sensor redundancy logic is missing or "
            f"incorrect. toxic_duration_s={result.co2_toxic_duration_s:.0f}",
        )

    @weight(25)
    @number("4.0")
    def test_40_sols_survived(self):
        """Plants must survive at least 28 of 30 sols.

        Failure here usually means temperature, drought, waterlogging, or
        low-light stress accumulated past the lethal threshold. See the
        failure_report() for the specific cause.
        """
        result = self._result_cached()
        report = result.failure_report() if result.terminated_early else "(no failure)"
        self.assertGreaterEqual(
            result.sols_survived,
            28.0,
            f"Plants died too early — sols_survived={result.sols_survived:.2f}. {report}",
        )

    @weight(15)
    @number("5.0")
    def test_50_temp_control(self):
        """Mean absolute temperature error must be below 3.0 °C.

        Computed across all ticks against the active setpoint (23 °C day,
        18 °C night).
        """
        result = self._result_cached()
        self.assertLess(
            result.mean_temp_error_c,
            3.0,
            f"Mean temperature error too high: {result.mean_temp_error_c:.2f} °C >= 3.0",
        )

    @weight(15)
    @number("6.0")
    def test_60_co2_in_range(self):
        """CO2 must be in [800, 1000] ppm at least 65 % of the time."""
        result = self._result_cached()
        self.assertGreaterEqual(
            result.co2_in_range_fraction,
            0.65,
            f"CO2 in range only {result.co2_in_range_fraction:.1%} (need >= 65 %)",
        )

    @weight(5)
    @number("7.0")
    @visibility("after_published")
    def test_70_rh_in_range(self):
        """RH must be inside [40, 60] %% on at least 1 % of ticks.

        See module docstring — this is a placeholder threshold until either
        a dehumidifier is added to the simulation or the rubric explicitly
        scopes RH out. It exists to catch controllers that abandon RH
        entirely (those would score 0); any real attempt clears 1 %.
        """
        result = self._result_cached()
        self.assertGreaterEqual(
            result.rh_in_range_fraction,
            0.01,
            f"RH in range only {result.rh_in_range_fraction:.2%} — the controller "
            "appears to ignore humidity entirely",
        )

    @weight(5)
    @number("8.0")
    def test_80_deterministic(self):
        """Same seed must yield byte-identical headline metrics."""
        first = self._result_cached()
        second = _run_with_student()
        self.assertAlmostEqual(
            first.mean_temp_error_c,
            second.mean_temp_error_c,
            places=6,
            msg="Repeated runs with seed=42 produced different mean_temp_error_c",
        )
        self.assertAlmostEqual(
            first.sols_survived,
            second.sols_survived,
            places=6,
            msg="Repeated runs with seed=42 produced different sols_survived",
        )
        self.assertEqual(
            first.co2_toxic_event,
            second.co2_toxic_event,
            msg="Repeated runs with seed=42 disagreed on co2_toxic_event",
        )
