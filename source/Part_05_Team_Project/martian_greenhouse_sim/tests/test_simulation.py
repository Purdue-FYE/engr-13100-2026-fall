"""
Test suite for the Martian Greenhouse Simulation package.

Covers:
  - Package-level imports
  - MarsEnvironment: diurnal temperature, solar, dust storm tau & reduction
  - Greenhouse: heat-loss sign, thermal ODE direction, actuator coupling
  - Greenhouse: CO₂, RH, and soil moisture bounds
  - VirtualActuators: percentage clamping and physical output scaling
  - VirtualSensors: noise, K30 freeze fault, SCD41 redundancy
  - run_simulation: end-to-end run, schema, storm injection, fault detection
  - PlantCohort: stress accumulators, health, death detection, early stop
  - SimulationResult: plant survival score, failure report, JSON export
  - load_student_controller: dynamic loading of student module
"""

import math
import random
import tempfile
import textwrap
from pathlib import Path

import pytest

# ---------------------------------------------------------------------------
# Imports under test (conftest.py ensures the package is on sys.path)
# ---------------------------------------------------------------------------
from martian_greenhouse_sim.actuators import VirtualActuators, _clamp_pct
from martian_greenhouse_sim.constants import (
    I_PEAK_MARS,
    PLANT_DROUGHT_DURATION_S,
    PLANT_DROUGHT_VWC,
    PLANT_LETHAL_HIGH_DURATION_S,
    PLANT_LETHAL_LOW_C,
    PLANT_LETHAL_LOW_DURATION_S,
    PLANT_LOW_LIGHT_DURATION_S,
    PLANT_RECOVERY_LIGHT_TAU_S,
    PLANT_RECOVERY_SOIL_TAU_S,
    PLANT_RECOVERY_TEMP_TAU_S,
    PLANT_WATERLOG_DURATION_S,
    PLANT_WATERLOG_VWC,
    SCORING_MAX_POINTS,
    SOL_SECONDS,
    TAU_CLEAR,
    TAU_STORM_MAX,
    TAU_STORM_MIN,
)
from martian_greenhouse_sim.controllers import (
    ActuatorCommands,
)
from martian_greenhouse_sim.environment import MarsEnvironment
from martian_greenhouse_sim.greenhouse import ActuatorState, Greenhouse, GreenhouseState
from martian_greenhouse_sim.plants import (
    CAUSE_DROUGHT,
    CAUSE_LIGHT,
    CAUSE_TEMP_HIGH,
    CAUSE_TEMP_LOW,
    CAUSE_WATERLOG,
    PlantCohort,
)
from martian_greenhouse_sim.sensors import VirtualSensors
from martian_greenhouse_sim.simulation import (
    SimulationResult,
    load_student_controller,
    run_simulation,
)

# ===========================================================================
# Phase 1 — package imports
# ===========================================================================


class TestImports:
    def test_package_imports_without_side_effects(self):
        """Importing the top-level package must not raise any exceptions."""
        import martian_greenhouse_sim  # noqa: F401

    def test_public_api_available(self):
        """All documented public symbols must be reachable from the package."""
        from martian_greenhouse_sim import (  # noqa: F401
            Greenhouse,
            MarsEnvironment,
            SimulationResult,
            StudentPIDController,
            VirtualActuators,
            VirtualSensors,
            run_simulation,
        )

    def test_greenhouse_state_is_dataclass(self):
        """GreenhouseState must be a dataclass with the expected fields."""
        state = GreenhouseState()
        assert hasattr(state, "temp_c")
        assert hasattr(state, "rh_pct")
        assert hasattr(state, "co2_ppm")
        assert hasattr(state, "soil_vwc")
        assert hasattr(state, "par_umol_m2_s")

    def test_actuator_state_is_dataclass(self):
        """ActuatorState must be a dataclass with fraction and physical fields."""
        a = ActuatorState()
        assert hasattr(a, "heater_watts")
        assert hasattr(a, "led_par_umol")
        assert hasattr(a, "co2_ppm_s")
        assert hasattr(a, "vwc_s")


# ===========================================================================
# Phase 2 — MarsEnvironment
# ===========================================================================


class TestMarsEnvironment:
    """Tests for the external Martian environment model."""

    # --- Temperature diurnal cycle ---

    def test_temperature_maximum_near_noon(self):
        """Temperature at local noon (t = SOL/2) should be close to -5 °C."""
        env = MarsEnvironment()
        # Advance to local noon
        env.update(SOL_SECONDS / 2)
        temp = env.get_temperature_c()
        assert -10.0 <= temp <= 0.0, f"Noon temp {temp:.1f} °C not near -5 °C"

    def test_temperature_minimum_near_midnight(self):
        """Temperature at midnight (t = 0 and t = SOL) should be near -70 °C."""
        env = MarsEnvironment()
        temp_midnight = env.get_temperature_c()  # t = 0
        assert -75.0 <= temp_midnight <= -65.0, (
            f"Midnight temp {temp_midnight:.1f} °C not near -70 °C"
        )

    def test_diurnal_range_over_one_sol(self):
        """Over one sol the temperature should span at least 60 °C."""
        env = MarsEnvironment(initial_time_s=0.0)
        steps = 1440  # one sample per minute over one sol
        dt = SOL_SECONDS / steps
        temps = []
        for _ in range(steps):
            env.update(dt)
            temps.append(env.get_temperature_c())
        span = max(temps) - min(temps)
        assert span >= 60.0, f"Diurnal temperature span {span:.1f} °C < 60 °C"
        assert max(temps) >= -10.0, "Peak temperature should be near -5 °C"
        assert min(temps) <= -60.0, "Trough temperature should be near -70 °C"

    # --- Solar irradiance ---

    def test_solar_irradiance_zero_at_midnight(self):
        """Solar irradiance at t = 0 (midnight) must be 0."""
        env = MarsEnvironment(initial_time_s=0.0)
        assert env.get_solar_irradiance_w_per_m2() == pytest.approx(0.0, abs=1e-6)

    def test_solar_irradiance_peak_at_noon(self):
        """Irradiance at local noon must equal I_PEAK_MARS on a clear day."""
        env = MarsEnvironment(initial_time_s=SOL_SECONDS / 2)
        irr = env.get_solar_irradiance_w_per_m2()
        assert irr == pytest.approx(I_PEAK_MARS, rel=1e-3)

    def test_is_daytime_returns_false_at_night(self):
        """is_daytime() must return False at midnight."""
        env = MarsEnvironment(initial_time_s=0.0)
        assert env.is_daytime() is False

    def test_is_daytime_returns_true_at_noon(self):
        """is_daytime() must return True at local noon."""
        env = MarsEnvironment(initial_time_s=SOL_SECONDS / 2)
        assert env.is_daytime() is True

    # --- Dust storm tau ---

    def test_baseline_tau_is_clear(self):
        """With no storm scheduled, tau should equal TAU_CLEAR = 0.5."""
        env = MarsEnvironment()
        env.update(SOL_SECONDS * 5)  # advance well past any ghost state
        assert env.get_tau() == pytest.approx(TAU_CLEAR)

    def test_storm_peak_tau_in_valid_range(self):
        """A scheduled storm with no peak_tau specified should sample in [5.0, 8.5]."""
        rng = random.Random(7)
        env = MarsEnvironment(rng=rng)
        storm = env.schedule_dust_storm(
            start_time_s=1.0 * SOL_SECONDS,
            duration_s=3.0 * SOL_SECONDS,
        )
        assert TAU_STORM_MIN <= storm.peak_tau <= TAU_STORM_MAX

    def test_storm_peak_tau_explicit(self):
        """A storm with an explicit peak_tau must record that exact value."""
        env = MarsEnvironment()
        storm = env.schedule_dust_storm(
            start_time_s=0.5 * SOL_SECONDS,
            duration_s=1.0 * SOL_SECONDS,
            peak_tau=7.0,
        )
        assert storm.peak_tau == pytest.approx(7.0)

    def test_storm_tau_during_event(self):
        """Tau must rise above TAU_CLEAR inside the storm window."""
        env = MarsEnvironment(initial_time_s=0.0)
        start = 1.0 * SOL_SECONDS
        duration = 2.0 * SOL_SECONDS
        env.schedule_dust_storm(start, duration, peak_tau=8.5)

        # Step into the middle of the storm
        dt = 60.0
        while env.get_time_s() < start + duration * 0.5:
            env.update(dt)

        assert env.get_tau() > TAU_CLEAR + 1.0

    def test_storm_tau_after_event(self):
        """Tau must return to TAU_CLEAR after the storm ends."""
        env = MarsEnvironment(initial_time_s=0.0)
        start = 0.1 * SOL_SECONDS
        duration = 0.5 * SOL_SECONDS
        env.schedule_dust_storm(start, duration, peak_tau=6.0)

        end = start + duration + 3600.0  # 1 hour after storm ends
        dt = 600.0
        while env.get_time_s() < end:
            env.update(dt)

        assert env.get_tau() == pytest.approx(TAU_CLEAR, abs=0.01)

    # --- Solar reduction during storm ---

    def test_storm_reduces_solar_by_up_to_97_percent(self):
        """At peak tau (8.5), solar irradiance should be reduced by ~ 97 %."""
        # Step into the flat part of a storm at a midday solar angle
        # by choosing a start time offset such that the storm middle is at noon.
        sol_half = SOL_SECONDS / 2.0  # noon of sol 1
        storm_dur = 3.0 * SOL_SECONDS
        storm_start = sol_half - storm_dur * 0.5  # storm centred on first noon

        env_clear = MarsEnvironment(initial_time_s=sol_half)
        clear_irr = env_clear.get_solar_irradiance_w_per_m2()

        env_storm = MarsEnvironment(initial_time_s=0.0)
        env_storm.schedule_dust_storm(storm_start, storm_dur, peak_tau=TAU_STORM_MAX)

        # Advance to midday through the centre of the storm
        dt = 300.0
        while env_storm.get_time_s() < sol_half:
            env_storm.update(dt)

        storm_irr = env_storm.get_solar_irradiance_w_per_m2()
        if clear_irr > 0:
            reduction_frac = 1.0 - storm_irr / clear_irr
            assert reduction_frac >= 0.90, (
                f"Storm only reduced solar by {reduction_frac:.1%}; expected ≥ 90 %"
            )

    def test_storm_transmittance_not_negative(self):
        """Transmittance must never drop below zero (no negative irradiance)."""
        env = MarsEnvironment(initial_time_s=SOL_SECONDS / 2)
        env.schedule_dust_storm(0.0, 2.0 * SOL_SECONDS, peak_tau=TAU_STORM_MAX)
        for _ in range(100):
            env.update(600.0)
            assert env.get_solar_irradiance_w_per_m2() >= 0.0


# ===========================================================================
# Phase 3 & 4 — Greenhouse physics
# ===========================================================================


class TestGreenhousePhysics:
    """Tests for the thermal ODE and atmospheric state dynamics."""

    def _make_env(self, t_out_c: float, irradiance: float = 0.0):
        """Build a MarsEnvironment stub using a real env at a fixed time."""
        # Start at midnight (no solar) and override with a known time
        env = MarsEnvironment(initial_time_s=0.0)  # midnight → no solar, T_out ≈ -70
        return env

    # --- Heat-loss equation ---

    def test_heat_loss_positive_when_inside_warmer(self):
        """HL = SA × U × (T_in − T_out) must be positive when T_in > T_out."""
        gh = Greenhouse(initial_temp_c=22.0)
        env = MarsEnvironment(initial_time_s=0.0)  # midnight → T_out ≈ -70 °C
        state = gh.update_state(env, ActuatorState(), dt_seconds=60.0)
        assert state.heat_loss_w > 0.0, (
            "Heat loss must be positive when inside is warmer"
        )

    def test_heat_loss_negative_when_outside_warmer(self):
        """HL must be negative (heat flows in) when T_out > T_in."""
        gh = Greenhouse(initial_temp_c=-80.0)  # colder than any Mars ambient
        env = MarsEnvironment(initial_time_s=0.0)  # T_out ≈ -70 °C > -80 °C
        state = gh.update_state(env, ActuatorState(), dt_seconds=60.0)
        assert state.heat_loss_w < 0.0

    # --- Temperature ODE direction ---

    def test_temp_decreases_without_heater_at_night(self):
        """Without heater or solar, inside temp should fall toward outside."""
        gh = Greenhouse(initial_temp_c=22.0)
        env = MarsEnvironment(initial_time_s=0.0)  # midnight → T_out ≈ -70, no solar
        t_before = gh.state.temp_c
        gh.update_state(env, ActuatorState(), dt_seconds=60.0)
        assert gh.state.temp_c < t_before, "Temperature should drop without heating"

    def test_heater_increases_temperature(self):
        """A fully-on heater should raise internal temperature each step."""
        gh = Greenhouse(initial_temp_c=-60.0)  # near Mars ambient at night
        env = MarsEnvironment(initial_time_s=0.0)

        actuators = ActuatorState(
            heater_frac=1.0,
            heater_watts=3000.0,  # maximum heater
        )
        t_before = gh.state.temp_c
        gh.update_state(env, actuators, dt_seconds=60.0)
        assert gh.state.temp_c > t_before, "Heater at 100 % should raise temperature"

    def test_solar_gain_stored_in_state(self):
        """solar_gain_w must be positive at noon (non-zero irradiance)."""
        gh = Greenhouse()
        env = MarsEnvironment(initial_time_s=SOL_SECONDS / 2)  # noon
        state = gh.update_state(env, ActuatorState(), dt_seconds=60.0)
        assert state.solar_gain_w > 0.0

    # --- CO₂ dynamics ---

    def test_co2_increases_with_injection(self):
        """Open CO₂ valve should raise internal CO₂ on each step."""
        gh = Greenhouse(initial_co2_ppm=400.0)
        env = MarsEnvironment(initial_time_s=0.0)  # night → zero PAR → no uptake
        act = ActuatorState(co2_valve_frac=1.0, co2_ppm_s=1.0)
        co2_before = gh.state.co2_ppm
        gh.update_state(env, act, dt_seconds=60.0)
        assert gh.state.co2_ppm > co2_before

    def test_co2_bounded_from_below(self):
        """CO₂ should never drop below 200 ppm (bounded)."""
        gh = Greenhouse(initial_co2_ppm=200.5)
        env = MarsEnvironment(initial_time_s=SOL_SECONDS / 2)  # noon → plant uptake
        # Add PAR so plant uptake occurs
        gh.state.par_umol_m2_s = 800.0
        for _ in range(200):
            gh.update_state(env, ActuatorState(), dt_seconds=60.0)
            assert gh.state.co2_ppm >= 200.0

    def test_co2_bounded_from_above(self):
        """CO₂ must be capped at CO2_BOUNDS_MAX_PPM."""
        from martian_greenhouse_sim.constants import CO2_BOUNDS_MAX_PPM

        gh = Greenhouse(initial_co2_ppm=CO2_BOUNDS_MAX_PPM - 10)
        env = MarsEnvironment(initial_time_s=0.0)
        act = ActuatorState(co2_valve_frac=1.0, co2_ppm_s=1.0)
        for _ in range(50):
            gh.update_state(env, act, dt_seconds=60.0)
            assert gh.state.co2_ppm <= CO2_BOUNDS_MAX_PPM

    # --- RH dynamics ---

    def test_rh_bounded(self):
        """Relative humidity must stay within [0, 100] under any actuator setting."""
        gh = Greenhouse(initial_rh_pct=50.0)
        env = MarsEnvironment(initial_time_s=0.0)
        act_max = ActuatorState(
            pump_frac=1.0,
            vwc_s=5.56e-6,
            heater_frac=1.0,
            heater_watts=3000.0,
        )
        for _ in range(300):
            gh.update_state(env, act_max, dt_seconds=60.0)
            assert 0.0 <= gh.state.rh_pct <= 100.0

    def test_irrigation_increases_rh(self):
        """Running the pump at 100 % should eventually increase RH."""
        gh = Greenhouse(initial_rh_pct=20.0)
        env = MarsEnvironment(initial_time_s=0.0)
        act = ActuatorState(pump_frac=1.0, vwc_s=5.56e-6)
        rh_start = gh.state.rh_pct
        for _ in range(10):
            gh.update_state(env, act, dt_seconds=60.0)
        assert gh.state.rh_pct > rh_start

    # --- Soil moisture dynamics ---

    def test_soil_bounded(self):
        """Soil VWC must stay within [0, 1]."""
        gh = Greenhouse(initial_soil_vwc=0.50)
        env = MarsEnvironment(initial_time_s=0.0)
        act_max = ActuatorState(pump_frac=1.0, vwc_s=5.56e-6)
        for _ in range(500):
            gh.update_state(env, act_max, dt_seconds=60.0)
            assert 0.0 <= gh.state.soil_vwc <= 1.0

    def test_irrigation_increases_soil_vwc(self):
        """Irrigation pump at 100 % should raise soil moisture."""
        gh = Greenhouse(initial_soil_vwc=0.10)
        env = MarsEnvironment(initial_time_s=0.0)
        act = ActuatorState(pump_frac=1.0, vwc_s=5.56e-6)
        vwc_start = gh.state.soil_vwc
        for _ in range(20):
            gh.update_state(env, act, dt_seconds=60.0)
        assert gh.state.soil_vwc > vwc_start

    def test_get_state_returns_copy(self):
        """get_state() must return a copy, not a live reference."""
        gh = Greenhouse()
        snap = gh.get_state()
        snap.temp_c = 999.0
        assert gh.state.temp_c != 999.0


# ===========================================================================
# Phase 5 — Virtual actuators
# ===========================================================================


class TestVirtualActuators:
    """Tests for percentage clamping and physical output scaling."""

    def test_clamp_pct_below_zero(self):
        assert _clamp_pct(-10.0) == 0.0

    def test_clamp_pct_above_hundred(self):
        assert _clamp_pct(150.0) == 100.0

    def test_clamp_pct_at_boundary(self):
        assert _clamp_pct(0.0) == 0.0
        assert _clamp_pct(100.0) == 100.0

    def test_heater_zero_at_zero_percent(self):
        act = VirtualActuators()
        act.set_heater(0.0)
        assert act.state.heater_watts == 0.0

    def test_heater_max_at_hundred_percent(self):
        from martian_greenhouse_sim.constants import HEATER_MAX_W

        act = VirtualActuators()
        act.set_heater(100.0)
        assert act.state.heater_watts == pytest.approx(HEATER_MAX_W)

    def test_heater_clamped_above_hundred(self):
        from martian_greenhouse_sim.constants import HEATER_MAX_W

        act = VirtualActuators()
        act.set_heater(200.0)
        assert act.state.heater_watts == pytest.approx(HEATER_MAX_W)

    def test_led_zero_at_zero_percent(self):
        act = VirtualActuators()
        act.set_LED_lights(0.0)
        assert act.state.led_par_umol == 0.0
        assert act.state.led_heat_watts == 0.0

    def test_led_max_par_at_hundred_percent(self):
        from martian_greenhouse_sim.constants import LED_PAR_MAX_UMOL_M2_S

        act = VirtualActuators()
        act.set_LED_lights(100.0)
        assert act.state.led_par_umol == pytest.approx(LED_PAR_MAX_UMOL_M2_S)

    def test_co2_valve_zero_at_zero_percent(self):
        act = VirtualActuators()
        act.inject_CO2(0.0)
        assert act.state.co2_ppm_s == 0.0

    def test_co2_valve_max_at_hundred_percent(self):
        from martian_greenhouse_sim.constants import CO2_MAX_INJECTION_PPM_S

        act = VirtualActuators()
        act.inject_CO2(100.0)
        assert act.state.co2_ppm_s == pytest.approx(CO2_MAX_INJECTION_PPM_S)

    def test_pump_zero_at_zero_percent(self):
        act = VirtualActuators()
        act.run_irrigation_pump(0.0)
        assert act.state.vwc_s == 0.0

    def test_pump_max_at_hundred_percent(self):
        from martian_greenhouse_sim.constants import PUMP_MAX_VWC_S

        act = VirtualActuators()
        act.run_irrigation_pump(100.0)
        assert act.state.vwc_s == pytest.approx(PUMP_MAX_VWC_S, rel=1e-6)

    def test_pump_scaling_linear(self):
        """50 % pump should produce exactly half of the maximum VWC rate."""
        from martian_greenhouse_sim.constants import PUMP_MAX_VWC_S

        act = VirtualActuators()
        act.run_irrigation_pump(50.0)
        assert act.state.vwc_s == pytest.approx(PUMP_MAX_VWC_S * 0.5, rel=1e-6)


# ===========================================================================
# Phase 6 — Virtual sensors + CO₂ freeze fault
# ===========================================================================


class TestVirtualSensors:
    """Tests for sensor noise and the K30 freeze fault mechanism."""

    def _make_sensors(self, freeze_prob=0.0):
        gh = Greenhouse(
            initial_temp_c=23.0,
            initial_co2_ppm=900.0,
            initial_rh_pct=50.0,
            initial_soil_vwc=0.40,
        )
        gh.state.par_umol_m2_s = 400.0
        rng = random.Random(0)
        return VirtualSensors(gh, rng=rng, freeze_prob_per_step=freeze_prob)

    def test_dht22_returns_two_floats(self):
        s = self._make_sensors()
        result = s.read_DHT22()
        assert len(result) == 2
        assert all(isinstance(v, float) for v in result)

    def test_dht22_temperature_near_true_value(self):
        s = self._make_sensors()
        # Average 1000 readings; mean must be close to true 23.0 °C
        temps = [s.read_DHT22()[0] for _ in range(1000)]
        mean_temp = sum(temps) / len(temps)
        assert abs(mean_temp - 23.0) < 0.05, (
            f"DHT22 mean temp {mean_temp:.2f} too far from 23.0"
        )

    def test_dht22_rh_near_true_value(self):
        s = self._make_sensors()
        rhs = [s.read_DHT22()[1] for _ in range(1000)]
        mean_rh = sum(rhs) / len(rhs)
        assert abs(mean_rh - 50.0) < 0.15

    def test_k30_returns_float(self):
        s = self._make_sensors()
        assert isinstance(s.read_K30(), float)

    def test_scd41_returns_float(self):
        s = self._make_sensors()
        assert isinstance(s.read_SCD41(), float)

    def test_teros12_within_bounds(self):
        s = self._make_sensors()
        for _ in range(100):
            assert 0.0 <= s.read_TEROS12() <= 1.0

    def test_sq500_non_negative(self):
        s = self._make_sensors()
        for _ in range(100):
            assert s.read_SQ500() >= 0.0

    def test_noise_is_deterministic_with_seed(self):
        """Two sensors with identical seeds must produce identical sequences."""
        gh = Greenhouse()
        rng1 = random.Random(42)
        rng2 = random.Random(42)
        s1 = VirtualSensors(gh, rng=rng1)
        s2 = VirtualSensors(gh, rng=rng2)
        readings1 = [s1.read_DHT22() for _ in range(20)]
        readings2 = [s2.read_DHT22() for _ in range(20)]
        assert readings1 == readings2

    def test_k30_freeze_fault_returns_400(self):
        """When freeze_prob=1.0, K30 must return 400 ppm on the first tick."""
        s = self._make_sensors(freeze_prob=1.0)
        s.tick_faults(current_time_s=0.0, dt_seconds=60.0)
        assert s.co2_freeze_active is True
        assert s.read_K30() == VirtualSensors.CO2_FREEZE_VALUE_PPM

    def test_scd41_unaffected_by_k30_freeze(self):
        """SCD41 must return the real (noisy) value even when K30 is frozen."""
        s = self._make_sensors(freeze_prob=1.0)
        s.tick_faults(current_time_s=0.0, dt_seconds=60.0)
        assert s.co2_freeze_active is True
        # True CO₂ is 900 ppm; SCD41 must not return the frozen 400 value
        scd41_readings = [s.read_SCD41() for _ in range(50)]
        # All readings should be near 900, not 400
        assert all(r > 600.0 for r in scd41_readings), (
            "SCD41 returned values near 400 ppm — it must not share the K30 fault"
        )

    def test_k30_unfreezes_after_duration(self):
        """K30 freeze must clear after the configured duration elapses."""
        gh = Greenhouse()
        rng = random.Random(0)
        s = VirtualSensors(
            gh,
            rng=rng,
            freeze_prob_per_step=1.0,
            freeze_duration_range_s=(60.0, 60.0),  # exactly 60 s
        )
        s.tick_faults(current_time_s=0.0, dt_seconds=60.0)
        assert s.co2_freeze_active is True

        # Advance past the 60 s freeze duration
        s.tick_faults(current_time_s=60.1, dt_seconds=60.0)
        assert s.co2_freeze_active is False

    def test_co2_freeze_enables_redundancy_detection(self):
        """
        When K30 is frozen at 400 and SCD41 reads 900, the discrepancy
        must exceed 200 ppm so that redundancy logic can detect the fault.
        """
        s = self._make_sensors(freeze_prob=1.0)
        s.tick_faults(0.0, 60.0)
        primary = s.read_K30()  # 400 ppm (frozen)
        backup = s.read_SCD41()  # ≈ 900 ppm (correct)
        discrepancy = abs(primary - backup)
        assert discrepancy > 200.0, (
            f"Discrepancy {discrepancy:.0f} ppm — redundancy logic cannot detect fault"
        )


# ===========================================================================
# Phase 7 — run_simulation + evaluation loop
# ===========================================================================


class TestRunSimulation:
    """End-to-end tests for the simulation loop."""

    def test_run_simulation_completes_without_error(self):
        """run_simulation must finish a 3-sol run without raising."""
        result = run_simulation(days=3, seed=42)
        assert isinstance(result, SimulationResult)

    def test_result_has_required_fields(self):
        """SimulationResult must expose all required performance fields."""
        result = run_simulation(days=2, seed=0)
        assert hasattr(result, "mean_temp_error_c")
        assert hasattr(result, "co2_in_range_fraction")
        assert hasattr(result, "rh_in_range_fraction")
        assert hasattr(result, "co2_toxic_event")
        assert hasattr(result, "co2_toxic_duration_s")

    def test_total_steps_matches_expected(self):
        """total_steps must equal floor(days × SOL_SECONDS / dt)."""
        days = 5
        dt = 60.0
        result = run_simulation(days=days, dt_seconds=dt, seed=1)
        expected = int(days * SOL_SECONDS / dt)
        assert result.total_steps == expected

    def test_stub_controller_co2_in_range_fraction_between_0_and_1(self):
        """co2_in_range_fraction must be a valid probability in [0, 1]."""
        result = run_simulation(days=2, seed=42)
        assert 0.0 <= result.co2_in_range_fraction <= 1.0

    def test_stub_controller_rh_in_range_fraction_between_0_and_1(self):
        result = run_simulation(days=2, seed=42)
        assert 0.0 <= result.rh_in_range_fraction <= 1.0

    def test_dust_storm_is_scheduled(self):
        """The environment's dust storm descriptor must be populated after run."""
        # Create env the same way run_simulation does to check storm was scheduled
        env = MarsEnvironment(rng=random.Random(42))
        storm = env.schedule_dust_storm(
            start_time_s=2.0 * SOL_SECONDS,
            duration_s=3.0 * SOL_SECONDS,
        )
        assert storm is not None
        assert storm.start_time_s < storm.end_time_s
        assert TAU_STORM_MIN <= storm.peak_tau <= TAU_STORM_MAX

    def test_log_records_populated_when_requested(self):
        """log_records=True must produce one record per simulation step run."""
        result = run_simulation(days=1, seed=0, log_records=True)
        # steps_run may be < total_steps when plants die early
        assert len(result.records) == result.steps_run

    def test_log_records_empty_by_default(self):
        """log_records=False (default) must produce an empty records list."""
        result = run_simulation(days=1, seed=0, log_records=False)
        assert result.records == []

    def test_to_csv_requires_log_records(self):
        """to_csv() must return empty string when no records were collected."""
        result = run_simulation(days=1, seed=0, log_records=False)
        assert result.to_csv() == ""

    def test_to_csv_returns_string_with_records(self):
        """to_csv() must return a non-empty CSV string when records are present."""
        result = run_simulation(days=1, seed=0, log_records=True)
        csv_str = result.to_csv()
        assert len(csv_str) > 0
        # Should have a header row plus at least one data row
        lines = [ln for ln in csv_str.splitlines() if ln.strip()]
        assert len(lines) >= 2

    def test_summary_returns_string(self):
        """summary() must return a non-empty string."""
        result = run_simulation(days=1, seed=0)
        summary = result.summary()
        assert isinstance(summary, str)
        assert len(summary) > 0

    def test_deterministic_with_same_seed(self):
        """Two runs with the same seed must produce identical results."""
        r1 = run_simulation(days=3, seed=77)
        r2 = run_simulation(days=3, seed=77)
        assert r1.mean_temp_error_c == pytest.approx(r2.mean_temp_error_c)
        assert r1.co2_in_range_fraction == pytest.approx(r2.co2_in_range_fraction)
        assert r1.rh_in_range_fraction == pytest.approx(r2.rh_in_range_fraction)
        assert r1.co2_toxic_event == r2.co2_toxic_event

    def test_different_seeds_produce_different_results(self):
        """Different seeds must produce different sensor noise."""
        r1 = run_simulation(days=1, seed=1, log_records=True)
        r2 = run_simulation(days=1, seed=999, log_records=True)
        # The CO2 K30 reading at step 0 depends on seeded Gaussian noise
        # and will almost certainly differ between any two distinct seeds.
        assert r1.records[0].co2_k30_reading != r2.records[0].co2_k30_reading

    def test_stub_controller_no_co2_toxic_event(self):
        """
        With the stub controller (no CO₂ injection), CO₂ should drift down,
        not up — so no toxic event should occur.
        """
        result = run_simulation(days=5, seed=42)
        # Starting at 900 ppm with no injection, CO₂ slowly drops via uptake.
        # A toxic event (>5000 ppm for 30 min) is only possible with runaway injection.
        assert result.co2_toxic_event is False

    def test_student_pid_controller_is_replaceable(self):
        """run_simulation must accept any class with the required update() method."""

        class MinimalController:
            def update(self, readings, setpoints, dt):
                return ActuatorCommands(heater_pct=50.0)

        result = run_simulation(days=1, seed=0, controller_cls=MinimalController)
        assert isinstance(result, SimulationResult)

    def test_required_sensor_names_exist(self):
        """All four required sensor methods must be present on VirtualSensors."""
        gh = Greenhouse()
        sensors = VirtualSensors(gh)
        assert callable(getattr(sensors, "read_DHT22", None))
        assert callable(getattr(sensors, "read_K30", None))
        assert callable(getattr(sensors, "read_SCD41", None))
        assert callable(getattr(sensors, "read_TEROS12", None))
        assert callable(getattr(sensors, "read_SQ500", None))

    def test_required_actuator_methods_exist(self):
        """All four required actuator methods must be present on VirtualActuators."""
        act = VirtualActuators()
        assert callable(getattr(act, "set_heater", None))
        assert callable(getattr(act, "set_LED_lights", None))
        assert callable(getattr(act, "inject_CO2", None))
        assert callable(getattr(act, "run_irrigation_pump", None))


# ===========================================================================
# Phase 8 — PlantCohort health model
# ===========================================================================


class TestPlantCohort:
    """Unit tests for the plant cohort health and stress model."""

    def _fresh(self) -> PlantCohort:
        return PlantCohort()

    # --- initial state ---

    def test_initially_alive(self):
        p = self._fresh()
        assert p.alive is True

    def test_initial_health_is_one(self):
        p = self._fresh()
        assert p.health == pytest.approx(1.0)

    def test_initial_failure_cause_none(self):
        p = self._fresh()
        assert p.failure_cause is None

    def test_initial_failure_sol_none(self):
        p = self._fresh()
        assert p.failure_sol is None

    # --- nominal tick (safe conditions) ---

    def test_nominal_tick_stays_alive(self):
        """Tick inside safe band must keep plant alive."""
        p = self._fresh()
        p.update(
            temp_c=22.0,
            soil_vwc=0.40,
            par_umol=300.0,
            dt_seconds=60.0,
            current_time_s=0.0,
        )
        assert p.alive is True
        assert p.health == pytest.approx(1.0)

    # --- temperature lethal low ---

    def test_cold_stress_accumulates(self):
        """Exposure below lethal-low temperature accumulates stress."""
        p = self._fresh()
        p.update(
            temp_c=PLANT_LETHAL_LOW_C - 1,
            soil_vwc=0.40,
            par_umol=300.0,
            dt_seconds=60.0,
            current_time_s=0.0,
        )
        assert p._temp_low_s == pytest.approx(60.0)

    def test_cold_recovery_decays_accumulator(self):
        """Recovery above lethal-low temperature must decay (not zero) the accumulator."""
        p = self._fresh()
        p.update(
            temp_c=PLANT_LETHAL_LOW_C - 1,
            soil_vwc=0.40,
            par_umol=300.0,
            dt_seconds=60.0,
            current_time_s=0.0,
        )
        stress_before = p._temp_low_s
        p.update(
            temp_c=20.0,
            soil_vwc=0.40,
            par_umol=300.0,
            dt_seconds=60.0,
            current_time_s=60.0,
        )
        # Must be strictly less than before recovery, but not yet zero
        assert 0.0 < p._temp_low_s < stress_before

    def test_lethal_cold_kills_after_threshold(self):
        """Sustained cold beyond threshold must set alive=False and correct cause."""
        p = self._fresh()
        steps = int(PLANT_LETHAL_LOW_DURATION_S / 60.0) + 1
        for i in range(steps):
            p.update(
                temp_c=0.0,
                soil_vwc=0.40,
                par_umol=300.0,
                dt_seconds=60.0,
                current_time_s=float(i * 60),
            )
        assert p.alive is False
        assert p.failure_cause == CAUSE_TEMP_LOW
        assert p.health == pytest.approx(0.0)
        assert p.failure_sol is not None

    def test_lethal_cold_records_failure_sol(self):
        """failure_sol must be set when death occurs from cold."""
        p = self._fresh()
        steps = int(PLANT_LETHAL_LOW_DURATION_S / 60.0) + 1
        for i in range(steps):
            p.update(
                temp_c=0.0,
                soil_vwc=0.40,
                par_umol=300.0,
                dt_seconds=60.0,
                current_time_s=float(i * 60),
            )
        assert p.failure_sol is not None
        assert p.failure_sol >= 0.0

    # --- temperature lethal high ---

    def test_lethal_heat_kills_after_threshold(self):
        """Sustained heat beyond threshold must kill with correct cause."""
        p = self._fresh()
        steps = int(PLANT_LETHAL_HIGH_DURATION_S / 60.0) + 1
        for i in range(steps):
            p.update(
                temp_c=50.0,
                soil_vwc=0.40,
                par_umol=300.0,
                dt_seconds=60.0,
                current_time_s=float(i * 60),
            )
        assert p.alive is False
        assert p.failure_cause == CAUSE_TEMP_HIGH

    # --- drought ---

    def test_drought_stress_accumulates(self):
        p = self._fresh()
        p.update(
            temp_c=22.0,
            soil_vwc=PLANT_DROUGHT_VWC - 0.01,
            par_umol=300.0,
            dt_seconds=60.0,
            current_time_s=0.0,
        )
        assert p._drought_s == pytest.approx(60.0)

    def test_drought_recovery_decays_accumulator(self):
        p = self._fresh()
        p.update(
            temp_c=22.0,
            soil_vwc=0.05,
            par_umol=300.0,
            dt_seconds=60.0,
            current_time_s=0.0,
        )
        stress_before = p._drought_s
        p.update(
            temp_c=22.0,
            soil_vwc=0.40,
            par_umol=300.0,
            dt_seconds=60.0,
            current_time_s=60.0,
        )
        assert 0.0 < p._drought_s < stress_before

    def test_lethal_drought_kills_after_threshold(self):
        p = self._fresh()
        steps = int(PLANT_DROUGHT_DURATION_S / 60.0) + 1
        for i in range(steps):
            p.update(
                temp_c=22.0,
                soil_vwc=0.05,
                par_umol=300.0,
                dt_seconds=60.0,
                current_time_s=float(i * 60),
            )
        assert p.alive is False
        assert p.failure_cause == CAUSE_DROUGHT

    # --- waterlogging ---

    def test_waterlog_stress_accumulates(self):
        p = self._fresh()
        p.update(
            temp_c=22.0,
            soil_vwc=PLANT_WATERLOG_VWC + 0.01,
            par_umol=300.0,
            dt_seconds=60.0,
            current_time_s=0.0,
        )
        assert p._waterlog_s == pytest.approx(60.0)

    def test_lethal_waterlog_kills_after_threshold(self):
        p = self._fresh()
        steps = int(PLANT_WATERLOG_DURATION_S / 60.0) + 1
        for i in range(steps):
            p.update(
                temp_c=22.0,
                soil_vwc=0.80,
                par_umol=300.0,
                dt_seconds=60.0,
                current_time_s=float(i * 60),
            )
        assert p.alive is False
        assert p.failure_cause == CAUSE_WATERLOG

    # --- low light (exponential decay on recovery) ---

    def test_low_light_accumulates_during_darkness(self):
        """Low-light stress accumulates when PAR is below threshold."""
        p = self._fresh()
        p.update(
            temp_c=22.0,
            soil_vwc=0.40,
            par_umol=50.0,
            dt_seconds=60.0,
            current_time_s=0.0,
        )
        assert p._low_light_s == pytest.approx(60.0)

    def test_low_light_decays_during_bright_conditions(self):
        """Low-light stress must decay (not hold) when PAR recovers."""
        p = self._fresh()
        p.update(
            temp_c=22.0,
            soil_vwc=0.40,
            par_umol=50.0,
            dt_seconds=60.0,
            current_time_s=0.0,
        )
        stress_before = p._low_light_s
        p.update(
            temp_c=22.0,
            soil_vwc=0.40,
            par_umol=600.0,
            dt_seconds=60.0,
            current_time_s=60.0,
        )
        assert 0.0 < p._low_light_s < stress_before

    def test_lethal_low_light_kills_after_threshold(self):
        p = self._fresh()
        steps = int(PLANT_LOW_LIGHT_DURATION_S / 60.0) + 1
        for i in range(steps):
            p.update(
                temp_c=22.0,
                soil_vwc=0.40,
                par_umol=10.0,
                dt_seconds=60.0,
                current_time_s=float(i * 60),
            )
        assert p.alive is False
        assert p.failure_cause == CAUSE_LIGHT

    # --- health degradation ---

    def test_health_degrades_as_stress_grows(self):
        """Health must decrease monotonically as cold stress accumulates."""
        p = self._fresh()
        prev_health = 1.0
        for i in range(10):
            p.update(
                temp_c=0.0,
                soil_vwc=0.40,
                par_umol=300.0,
                dt_seconds=600.0,
                current_time_s=float(i * 600),
            )
            if p.alive:
                assert p.health <= prev_health
                prev_health = p.health

    def test_dead_plant_does_not_update(self):
        """After death, further update() calls must not change state."""
        p = self._fresh()
        steps = int(PLANT_LETHAL_LOW_DURATION_S / 60.0) + 1
        for i in range(steps):
            p.update(
                temp_c=0.0,
                soil_vwc=0.40,
                par_umol=300.0,
                dt_seconds=60.0,
                current_time_s=float(i * 60),
            )
        cause_at_death = p.failure_cause
        sol_at_death = p.failure_sol
        # Extra ticks should not change anything
        p.update(
            temp_c=22.0,
            soil_vwc=0.40,
            par_umol=300.0,
            dt_seconds=60.0,
            current_time_s=float((steps + 1) * 60),
        )
        assert p.failure_cause == cause_at_death
        assert p.failure_sol == sol_at_death

    # --- stress property ---

    def test_stress_property_returns_dict_with_all_keys(self):
        p = self._fresh()
        s = p.stress
        assert set(s.keys()) == {
            CAUSE_TEMP_LOW,
            CAUSE_TEMP_HIGH,
            CAUSE_DROUGHT,
            CAUSE_WATERLOG,
            CAUSE_LIGHT,
        }

    # --- exponential decay rate ---

    def test_cold_stress_decay_rate_matches_tau(self):
        """One recovery tick must decay stress by exp(-dt/tau)."""
        p = self._fresh()
        dt = 600.0  # 10 minutes
        # Seed stress with one bad tick
        p.update(
            temp_c=0.0, soil_vwc=0.40, par_umol=300.0, dt_seconds=dt, current_time_s=0.0
        )
        stress_after_bad = p._temp_low_s  # == dt
        # One recovery tick
        p.update(
            temp_c=20.0, soil_vwc=0.40, par_umol=300.0, dt_seconds=dt, current_time_s=dt
        )
        expected = stress_after_bad * math.exp(-dt / PLANT_RECOVERY_TEMP_TAU_S)
        assert p._temp_low_s == pytest.approx(expected, rel=1e-6)

    def test_soil_stress_decay_rate_matches_tau(self):
        """Soil drought decay for one recovery tick must equal exp(-dt/tau)."""
        p = self._fresh()
        dt = 600.0
        p.update(
            temp_c=22.0,
            soil_vwc=0.05,
            par_umol=300.0,
            dt_seconds=dt,
            current_time_s=0.0,
        )
        stress_after_bad = p._drought_s
        p.update(
            temp_c=22.0, soil_vwc=0.40, par_umol=300.0, dt_seconds=dt, current_time_s=dt
        )
        expected = stress_after_bad * math.exp(-dt / PLANT_RECOVERY_SOIL_TAU_S)
        assert p._drought_s == pytest.approx(expected, rel=1e-6)

    def test_light_stress_decay_rate_matches_tau(self):
        """Light stress decay for one recovery tick must equal exp(-dt/tau)."""
        p = self._fresh()
        dt = 600.0
        p.update(
            temp_c=22.0, soil_vwc=0.40, par_umol=50.0, dt_seconds=dt, current_time_s=0.0
        )
        stress_after_bad = p._low_light_s
        p.update(
            temp_c=22.0, soil_vwc=0.40, par_umol=600.0, dt_seconds=dt, current_time_s=dt
        )
        expected = stress_after_bad * math.exp(-dt / PLANT_RECOVERY_LIGHT_TAU_S)
        assert p._low_light_s == pytest.approx(expected, rel=1e-6)

    def test_stress_approaches_zero_after_long_recovery(self):
        """After many recovery ticks (>> tau), stress should be near zero."""
        p = self._fresh()
        dt = 60.0
        # Build up cold stress for 1 hour (short of the lethal threshold)
        for i in range(60):
            p.update(
                temp_c=0.0,
                soil_vwc=0.40,
                par_umol=300.0,
                dt_seconds=dt,
                current_time_s=float(i * dt),
            )
        # Recover for 3× the temperature tau
        recovery_steps = int(3 * PLANT_RECOVERY_TEMP_TAU_S / dt)
        for i in range(recovery_steps):
            p.update(
                temp_c=20.0,
                soil_vwc=0.40,
                par_umol=300.0,
                dt_seconds=dt,
                current_time_s=float((60 + i) * dt),
            )
        # After 3 tau, stress should be < 5% of peak
        assert p._temp_low_s < 0.05 * PLANT_LETHAL_LOW_DURATION_S

    def test_health_recovers_as_stress_decays(self):
        """Health must increase back toward 1.0 during a recovery period."""
        p = self._fresh()
        dt = 60.0
        # Build up some cold stress (one hour, well below lethal threshold)
        for i in range(60):
            p.update(
                temp_c=0.0,
                soil_vwc=0.40,
                par_umol=300.0,
                dt_seconds=dt,
                current_time_s=float(i * dt),
            )
        health_at_peak_stress = p.health
        # Recover for 2× tau
        recovery_steps = int(2 * PLANT_RECOVERY_TEMP_TAU_S / dt)
        for i in range(recovery_steps):
            p.update(
                temp_c=20.0,
                soil_vwc=0.40,
                par_umol=300.0,
                dt_seconds=dt,
                current_time_s=float((60 + i) * dt),
            )
        assert p.health > health_at_peak_stress


# ===========================================================================
# Phase 9 — SimulationResult plant fields + early termination
# ===========================================================================


class TestSimulationResultPlantFields:
    """Tests for new plant-related fields on SimulationResult."""

    def test_result_has_plant_fields(self):
        result = run_simulation(days=2, seed=0)
        assert hasattr(result, "terminated_early")
        assert hasattr(result, "failure_sol")
        assert hasattr(result, "failure_cause")
        assert hasattr(result, "failure_snapshot")
        assert hasattr(result, "plant_health")
        assert hasattr(result, "sols_survived")
        assert hasattr(result, "steps_run")

    def test_stub_controller_does_not_terminate_early_in_short_run(self):
        """
        The stub controller should not kill plants within 3 sols under
        mild conditions (the greenhouse starts at a reasonable temperature).
        """
        result = run_simulation(days=3, seed=42)
        # If it terminated early, the failure report should be informative
        if result.terminated_early:
            assert result.failure_cause is not None
            assert result.failure_sol is not None

    def test_sols_survived_positive(self):
        result = run_simulation(days=3, seed=42)
        assert result.sols_survived > 0.0

    def test_sols_survived_le_days(self):
        result = run_simulation(days=3, seed=42)
        assert result.sols_survived <= 3.0 + 1e-6  # allow floating point slop

    def test_plant_survival_score_max_when_full_run(self):
        """Full-run result must yield max points."""
        result = run_simulation(days=30, seed=42)
        if not result.terminated_early:
            assert result.plant_survival_score() == pytest.approx(SCORING_MAX_POINTS)

    def test_plant_survival_score_partial_when_early_termination(self):
        """
        Force an immediate low-temperature kill and check that the score
        is strictly less than max.
        """

        class IceController:
            """Sets heater to 0% to let temperature plummet."""

            def update(self, readings, setpoints, dt):
                return ActuatorCommands(heater_pct=0.0)

        result = run_simulation(days=30, seed=42, controller_cls=IceController)
        if result.terminated_early:
            assert result.plant_survival_score() < SCORING_MAX_POINTS
            assert result.plant_survival_score() >= 0.0

    def test_failure_report_mentions_sols(self):
        result = run_simulation(days=3, seed=42)
        report = result.failure_report()
        assert "sol" in report.lower()

    def test_failure_report_mentions_cause_when_terminated(self):
        class IceController:
            def update(self, readings, setpoints, dt):
                return ActuatorCommands(heater_pct=0.0)

        result = run_simulation(days=30, seed=42, controller_cls=IceController)
        if result.terminated_early:
            report = result.failure_report()
            assert result.failure_cause in report

    def test_to_gradescope_json_returns_dict(self):
        result = run_simulation(days=2, seed=0)
        data = result.to_gradescope_json()
        assert isinstance(data, dict)
        assert "sols_survived" in data
        assert "failure_cause" in data
        assert "failure_report" in data
        assert "terminated_early" in data

    def test_to_gradescope_json_writes_file(self):
        result = run_simulation(days=2, seed=0)
        with tempfile.TemporaryDirectory() as tmpdir:
            out = str(Path(tmpdir) / "plant_report.json")
            result.to_gradescope_json(output_path=out)
            import json

            with open(out) as fh:
                data = json.load(fh)
            assert "sols_survived" in data

    def test_early_termination_failure_snapshot_set(self):
        """When terminated early the snapshot dict must be populated."""

        class IceController:
            def update(self, readings, setpoints, dt):
                return ActuatorCommands(heater_pct=0.0)

        result = run_simulation(days=30, seed=42, controller_cls=IceController)
        if result.terminated_early:
            snap = result.failure_snapshot
            assert snap is not None
            assert "t_in_c" in snap
            assert "soil_vwc" in snap
            assert "par_umol" in snap
            assert "heater_pct" in snap

    def test_no_early_termination_snapshot_is_none(self):
        """When the run completes normally the snapshot should be None."""
        result = run_simulation(days=3, seed=42)
        if not result.terminated_early:
            assert result.failure_snapshot is None


# ===========================================================================
# Phase 10 — load_student_controller
# ===========================================================================


class TestLoadStudentController:
    """Tests for the dynamic student submission loader."""

    MINIMAL_CONTROLLER_SRC = textwrap.dedent("""\
        from martian_greenhouse_sim.controllers import ActuatorCommands

        class GreenhouseController:
            def update(self, readings, setpoints, dt_seconds):
                return ActuatorCommands(heater_pct=50.0)
    """)

    def test_loads_single_file_submission(self):
        """load_student_controller must find and load student_controller.py."""
        with tempfile.TemporaryDirectory() as tmpdir:
            sc_file = Path(tmpdir) / "student_controller.py"
            sc_file.write_text(self.MINIMAL_CONTROLLER_SRC)
            cls = load_student_controller(search_dirs=[tmpdir])
            assert cls.__name__ == "GreenhouseController"

    def test_single_file_controller_is_callable(self):
        """The loaded class must be callable and return ActuatorCommands."""
        with tempfile.TemporaryDirectory() as tmpdir:
            (Path(tmpdir) / "student_controller.py").write_text(
                self.MINIMAL_CONTROLLER_SRC
            )
            cls = load_student_controller(search_dirs=[tmpdir])
            instance = cls()
            # Build a minimal readings object
            from martian_greenhouse_sim.controllers import (
                ActuatorCommands,
                SensorReadings,
                Setpoints,
            )

            readings = SensorReadings(
                temperature_c=22.0,
                rh_pct=50.0,
                co2_ppm_primary=900.0,
                co2_ppm_backup=900.0,
                soil_vwc=0.40,
                par_umol_m2_s=300.0,
            )
            setpoints = Setpoints(
                temperature_c=23.0,
                co2_ppm=900.0,
                rh_pct=50.0,
                soil_vwc=0.40,
                is_daytime=True,
            )
            result = instance.update(readings, setpoints, 60.0)
            assert isinstance(result, ActuatorCommands)

    def test_loads_package_submission(self):
        """load_student_controller must find and load a student_controller/ package."""
        with tempfile.TemporaryDirectory() as tmpdir:
            pkg = Path(tmpdir) / "student_controller"
            pkg.mkdir()
            (pkg / "__init__.py").write_text(self.MINIMAL_CONTROLLER_SRC)
            # Remove single-file if present (shouldn't be, but just in case)
            cls = load_student_controller(search_dirs=[tmpdir])
            assert cls.__name__ == "GreenhouseController"

    def test_raises_when_no_submission_found(self):
        """load_student_controller must raise FileNotFoundError for empty dirs."""
        with tempfile.TemporaryDirectory() as tmpdir:
            with pytest.raises(FileNotFoundError):
                load_student_controller(search_dirs=[tmpdir])

    def test_raises_when_class_missing_from_module(self):
        """load_student_controller must raise AttributeError if class is absent."""
        with tempfile.TemporaryDirectory() as tmpdir:
            (Path(tmpdir) / "student_controller.py").write_text(
                "# deliberately empty\n"
            )
            with pytest.raises(AttributeError):
                load_student_controller(search_dirs=[tmpdir])
