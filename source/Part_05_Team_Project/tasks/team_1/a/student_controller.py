"""Sample reference controller for the Martian greenhouse design project.

Competent (not optimal) PI controller that maintains lettuce setpoints during a
30-sol mission including the guaranteed dust storm and the K30 CO2 sensor
freeze fault. Targets the autograder thresholds with margin.
"""

from martian_greenhouse_sim.controllers import (
    ActuatorCommands,
    SensorReadings,
    Setpoints,
)


def _clamp(value: float, lo: float, hi: float) -> float:
    """Clamp a scalar to the closed interval [lo, hi]."""
    if value < lo:
        return lo
    if value > hi:
        return hi
    return value


class GreenhouseController:
    """PI-based environmental controller for the Lettuce mission.

    Uses a heating-dominant temperature loop (PI with anti-windup), a CO2 loop
    fed by a redundancy-checked sensor reading (K30 vs. SCD41), day/night-gated
    LED supplementation, and a combined RH + soil-moisture pump law.
    """

    # Temperature PI gains (heater fights large losses to -70 C ambient).
    # KP_TEMP kept modest so the proportional term does not saturate during the
    # initial cold-start, which would otherwise overshoot once the integral
    # term catches up. KI_TEMP eliminates the steady-state offset against the
    # constant heat-loss disturbance.
    KP_TEMP: float = 12.0
    KI_TEMP: float = 0.02

    # CO2 P gain. Valve is one-way (no venting), so we never command negative.
    KP_CO2: float = 0.08

    # Pump gains. Combined RH deficit + soil-moisture deficit drive the pump.
    # KP_SOIL is sized so a 0.07 VWC deficit (just below the drought threshold)
    # saturates the pump — soil drying is by far the dominant failure mode.
    KP_RH: float = 1.5
    KP_SOIL: float = 1500.0

    # K30 vs SCD41 disagreement that flags a primary-sensor fault (ppm).
    CO2_REDUNDANCY_PPM: float = 200.0

    # LED setpoints (percent) for day-time supplementation.
    LED_DAY_LOW_PAR_PCT: float = 50.0
    LED_DAY_HIGH_PAR_PCT: float = 20.0
    LED_PAR_THRESHOLD_UMOL: float = 400.0

    # Anti-windup band on the temperature integral as a backstop in case the
    # conditional-integration logic below ever fails to engage.
    TEMP_INTEGRAL_LIMIT: float = 2000.0

    def __init__(self) -> None:
        """Initialise PI state. Integrators start at zero."""
        self._integral_temp: float = 0.0

    def update(
        self,
        readings: SensorReadings,
        setpoints: Setpoints,
        dt_seconds: float,
    ) -> ActuatorCommands:
        """Compute one tick of actuator commands.

        Returns clamped percentages for the heater, LED, CO2 valve, and pump.
        """
        # --- Temperature PI -------------------------------------------------
        e_temp = setpoints.temperature_c - readings.temperature_c
        # Anti-windup via conditional integration: only accumulate the integral
        # when the *previous* command was not saturated and the error is not
        # driving the output further into saturation. This prevents the long
        # cold-start (and any dust-storm period with the heater pinned at 100
        # percent) from accumulating an integral that then overshoots once the
        # greenhouse warms up.
        p_term = self.KP_TEMP * e_temp
        prospective_u = p_term + self.KI_TEMP * self._integral_temp
        if 0.0 < prospective_u < 100.0:
            self._integral_temp += e_temp * dt_seconds
            self._integral_temp = _clamp(
                self._integral_temp,
                -self.TEMP_INTEGRAL_LIMIT,
                self.TEMP_INTEGRAL_LIMIT,
            )
        u_heat = p_term + self.KI_TEMP * self._integral_temp
        heater_pct = _clamp(u_heat, 0.0, 100.0)

        # --- CO2 P with K30 / SCD41 redundancy -----------------------------
        # The K30 primary can freeze at 400 ppm; trusting it during a freeze
        # drives CO2 above the 5000 ppm toxic threshold and fails the run.
        # When the two sensors disagree by more than CO2_REDUNDANCY_PPM, we
        # fall back to the SCD41 backup, which is always reliable.
        if (
            abs(readings.co2_ppm_primary - readings.co2_ppm_backup)
            > self.CO2_REDUNDANCY_PPM
        ):
            co2_actual = readings.co2_ppm_backup
        else:
            co2_actual = readings.co2_ppm_primary

        e_co2 = setpoints.co2_ppm - co2_actual
        u_co2 = self.KP_CO2 * e_co2
        # Valve is one-way: never negative. Clamp before the final [0, 100].
        u_co2 = max(0.0, u_co2)
        co2_valve_pct = _clamp(u_co2, 0.0, 100.0)

        # --- LED supplementation (day-gated, temperature-aware) ------------
        # The LED draws 600 W electrical, 35 percent of which dissipates as
        # waste heat (up to 210 W). We refuse to add that heat when the
        # greenhouse is already running above setpoint -- there is no cooling
        # actuator, so every avoidable watt matters during midday solar peak.
        if setpoints.is_daytime and readings.temperature_c <= setpoints.temperature_c:
            if readings.par_umol_m2_s < self.LED_PAR_THRESHOLD_UMOL:
                led_pct = self.LED_DAY_LOW_PAR_PCT
            else:
                led_pct = self.LED_DAY_HIGH_PAR_PCT
        else:
            led_pct = 0.0

        # --- Pump from soil deficit, RH-aware throttling --------------------
        # Irrigation is the only water input; it raises soil VWC directly and
        # also drives RH up via evaporation. Without a dehumidifier the pump
        # has to balance two coupled goals. The strategy:
        #   * Emergency refill when soil VWC drops near the drought floor.
        #   * Gentle top-up only when RH headroom exists (RH below upper bound).
        #   * Idle when RH is already at or above setpoint, letting soil drift.
        soil_floor = 0.25
        if readings.soil_vwc < soil_floor:
            pump_pct = 100.0
        elif readings.rh_pct < setpoints.rh_pct:
            e_soil = setpoints.soil_vwc - readings.soil_vwc
            e_rh = setpoints.rh_pct - readings.rh_pct
            u_pump = self.KP_SOIL * max(0.0, e_soil) + self.KP_RH * max(0.0, e_rh)
            pump_pct = _clamp(u_pump, 0.0, 100.0)
        else:
            pump_pct = 0.0

        return ActuatorCommands(
            heater_pct=heater_pct,
            led_pct=led_pct,
            co2_valve_pct=co2_valve_pct,
            pump_pct=pump_pct,
        )
