"""
Virtual actuators for the Martian greenhouse simulation.

All control inputs are expressed as percentages (0.0 to 100.0).
Inputs outside this range are silently clamped before scaling to physical
output units.  The resulting :class:`ActuatorState` is passed directly to
:meth:`Greenhouse.update_state` each simulation tick.

Actuator summary
----------------
+----------------------+----------+-----------------------------------+
| Method               | Max      | Effect                            |
+======================+==========+===================================+
| set_heater           | 3 000 W  | Raises internal temperature       |
+----------------------+----------+-----------------------------------+
| set_LED_lights       | 300 µmol | Supplemental PAR + 35 % waste     |
|                      | /m²/s   | heat (210 W max)                  |
+----------------------+----------+-----------------------------------+
| inject_CO₂           | 1 ppm/s  | Raises CO₂ (~60 ppm/min at 100 %) |
+----------------------+----------+-----------------------------------+
| run_irrigation_pump  | 5.56e-6  | Raises soil VWC + RH              |
|                      | VWC/s   |                                   |
+----------------------+----------+-----------------------------------+
"""

from .constants import (
    CO2_MAX_INJECTION_PPM_S,
    HEATER_MAX_W,
    LED_HEAT_FRACTION,
    LED_MAX_POWER_W,
    LED_PAR_MAX_UMOL_M2_S,
    PUMP_MAX_VWC_S,
)
from .greenhouse import ActuatorState


def _clamp_pct(value: float) -> float:
    """Clamp *value* to the range [0, 100] inclusive."""
    return max(0.0, min(100.0, value))


class VirtualActuators:
    """
    Provides the four physical control interfaces for the greenhouse.

    Each method accepts a percentage input (0 – 100) and updates the
    internal :class:`ActuatorState` that is passed to the greenhouse
    physics model at the end of each simulation tick.

    Example
    -------
    >>> actuators = VirtualActuators()
    >>> actuators.set_heater(75)          # 75 % of 3 000 W = 2 250 W
    >>> actuators.set_LED_lights(50)      # 50 % LED intensity
    >>> actuators.inject_CO2(20)          # 20 % valve = 0.2 ppm/s
    >>> actuators.run_irrigation_pump(0)  # pump off
    >>> state = actuators.state           # pass to Greenhouse.update_state()
    """

    def __init__(self) -> None:
        self._state = ActuatorState()

    @property
    def state(self) -> ActuatorState:
        """Return the current :class:`ActuatorState` for the physics model."""
        return self._state

    # ------------------------------------------------------------------
    # Required actuator API
    # ------------------------------------------------------------------

    def set_heater(self, power_percentage: float) -> None:
        """
        Set ceramic heater output.

        Parameters
        ----------
        power_percentage : float
            Heater power as a percentage of the 3 000 W maximum (0 – 100).
            Values outside this range are clamped.

        Physical effect
        ---------------
        At 100 %, the heater delivers 3 000 W of thermal energy directly
        into the mixing air volume, raising internal temperature.
        """
        pct = _clamp_pct(power_percentage)
        frac = pct / 100.0
        self._state.heater_frac = frac
        self._state.heater_watts = frac * HEATER_MAX_W

    def set_LED_lights(self, intensity_percentage: float) -> None:
        """
        Set supplemental red/blue LED array intensity.

        Parameters
        ----------
        intensity_percentage : float
            LED intensity as a percentage of maximum (0 – 100).
            Values outside this range are clamped.

        Physical effect
        ---------------
        At 100 %, the LED array delivers up to 300 µmol/m²/s of
        photosynthetically active radiation (PAR) to the crop layer.
        Approximately 35 % of the 600 W electrical draw is dissipated as
        waste heat (210 W max), which contributes to internal temperature.
        """
        pct = _clamp_pct(intensity_percentage)
        frac = pct / 100.0
        self._state.led_frac = frac
        self._state.led_par_umol = frac * LED_PAR_MAX_UMOL_M2_S
        self._state.led_heat_watts = frac * LED_MAX_POWER_W * LED_HEAT_FRACTION

    def inject_CO2(self, valve_open_percentage: float) -> None:
        """
        Open the CO₂ solenoid valve to release gas from pressurised tanks.

        Parameters
        ----------
        valve_open_percentage : float
            Valve opening as a percentage of maximum (0 – 100).
            Values outside this range are clamped.

        Physical effect
        ---------------
        At 100 %, CO₂ is injected at 1.0 ppm/s (≈ 60 ppm/min) into the
        14 m³ mixing volume.  At 20 % valve opening, the rate is 0.2 ppm/s
        (≈ 12 ppm/min).

        Warning
        -------
        Never call this method based solely on the K30 primary CO₂ sensor
        reading without first checking the SCD41 backup.  A frozen K30
        (stuck at 400 ppm) will cause runaway CO₂ injection.
        """
        pct = _clamp_pct(valve_open_percentage)
        frac = pct / 100.0
        self._state.co2_valve_frac = frac
        self._state.co2_ppm_s = frac * CO2_MAX_INJECTION_PPM_S

    def run_irrigation_pump(self, speed_percentage: float) -> None:
        """
        Run the peristaltic pump to deliver nutrient solution to the roots.

        Parameters
        ----------
        speed_percentage : float
            Pump speed as a percentage of maximum (0 – 100).
            Values outside this range are clamped.

        Physical effect
        ---------------
        At 100 %, the pump delivers nutrient solution at a rate that
        increases soil volumetric water content (VWC) by approximately
        +0.02 per hour.  Irrigation also increases relative humidity
        through evaporation from the root zone and plant transpiration.
        """
        pct = _clamp_pct(speed_percentage)
        frac = pct / 100.0
        self._state.pump_frac = frac
        self._state.vwc_s = frac * PUMP_MAX_VWC_S
