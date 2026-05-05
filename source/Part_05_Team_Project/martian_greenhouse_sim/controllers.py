"""
Student PID controller interface for the Martian greenhouse simulation.

Students implement their environmental control algorithm inside the
:class:`StudentPIDController` class below.  The :meth:`update` method is
called once per simulation tick (default Δt = 60 s) and must return
:class:`ActuatorCommands` with all percentages clamped to [0, 100].

PID control law
---------------
For each controlled variable, the control signal u(t) is:

    u(t) = Kp · e(t)  +  Ki · ∫e(t) dt  +  Kd · de(t)/dt

where:

    e(t)       = setpoint − measured_value          (current error)
    ∫e(t) dt   = accumulated over time               (eliminates offset)
    de(t)/dt   ≈ (e(t) − e(t−1)) / Δt              (rate of change)

Lettuce (*Lactuca sativa*) growth targets
-----------------------------------------
+-----------------------+----------------------------------+
| Variable              | Target                           |
+=======================+==================================+
| Temperature (day)     | 23 °C                            |
+-----------------------+----------------------------------+
| Temperature (night)   | 18 °C                            |
+-----------------------+----------------------------------+
| CO₂                   | 800 – 1 000 ppm  (set 900)       |
+-----------------------+----------------------------------+
| Relative humidity     | 40 – 60 %        (set 50 %)      |
+-----------------------+----------------------------------+

CO₂ sensor fault — CRITICAL
-----------------------------
The primary CO₂ sensor (``co2_ppm_primary`` / ``read_K30``) can freeze and
return a stuck value of 400 ppm.  A controller that blindly uses this value
when it is frozen will continuously inject CO₂, potentially raising the
internal level above 5 000 ppm — toxic to both humans and plants.

**Required redundancy pattern:**

    discrepancy = abs(readings.co2_ppm_primary - readings.co2_ppm_backup)
    if discrepancy > 200:
        co2_actual = readings.co2_ppm_backup   # use the backup sensor
    else:
        co2_actual = readings.co2_ppm_primary
"""

from dataclasses import dataclass


@dataclass
class SensorReadings:
    """Bundle of all virtual sensor readings for one simulation tick."""

    temperature_c: float       #: DHT22 temperature reading (°C)
    rh_pct: float              #: DHT22 relative humidity reading (%)
    co2_ppm_primary: float     #: K30  CO₂ reading — MAY BE FROZEN AT 400 ppm
    co2_ppm_backup: float      #: SCD41 CO₂ reading — always reliable
    soil_vwc: float            #: TEROS12 volumetric water content [0–1]
    par_umol_m2_s: float       #: SQ-500 PAR reading (µmol/m²/s)


@dataclass
class Setpoints:
    """Target operating conditions for the current time step."""

    temperature_c: float       #: Target temperature (23 °C day / 18 °C night)
    co2_ppm: float             #: Target CO₂ concentration (ppm)
    rh_pct: float              #: Target relative humidity (%)
    soil_vwc: float            #: Target soil moisture (VWC)
    is_daytime: bool           #: True when the sun is above the horizon


@dataclass
class ActuatorCommands:
    """Control outputs from the student controller (percentages 0 – 100)."""

    heater_pct: float = 0.0      #: Heater power %
    led_pct: float = 0.0         #: LED intensity %
    co2_valve_pct: float = 0.0   #: CO₂ valve opening %
    pump_pct: float = 0.0        #: Irrigation pump speed %


class StudentPIDController:
    """
    ============================================================
    STUDENT IMPLEMENTATION REQUIRED
    ============================================================
    Replace the body of ``update()`` with your PID control logic.

    Your controller is called once per simulation tick (Δt = 60 s).
    It receives sensor readings (with noise and possible faults) and
    the current setpoints, and must return actuator commands as
    percentages in [0, 100].

    Starter pseudocode (temperature loop)::

        e_temp   = setpoints.temperature_c - readings.temperature_c
        integral += e_temp * dt_seconds
        deriv    = (e_temp - prev_error) / dt_seconds
        u_heat   = Kp_temp * e_temp + Ki_temp * integral + Kd_temp * deriv
        prev_error = e_temp
        return ActuatorCommands(heater_pct=max(0, min(100, u_heat)))

    Tune the gains (Kp, Ki, Kd) so the controller:
      1. Maintains temperature within ±2 °C of setpoint.
      2. Keeps CO₂ in [800, 1 000] ppm.
      3. Maintains relative humidity in [40, 60] %.
      4. Handles the K30 CO₂ sensor freeze fault safely.

    See module docstring for the sensor redundancy pattern.
    ============================================================
    """

    def __init__(self) -> None:
        # ---- Tune these PID gains ------------------------------------
        self.Kp_temp: float = 0.0
        self.Ki_temp: float = 0.0
        self.Kd_temp: float = 0.0

        self.Kp_co2: float = 0.0
        self.Ki_co2: float = 0.0
        self.Kd_co2: float = 0.0
        # ---------------------------------------------------------------

        # Internal PID state — add more variables as needed
        self._integral_temp: float = 0.0
        self._prev_error_temp: float = 0.0

        self._integral_co2: float = 0.0
        self._prev_error_co2: float = 0.0

    def update(
        self,
        readings: SensorReadings,
        setpoints: Setpoints,
        dt_seconds: float,
    ) -> ActuatorCommands:
        """
        Compute actuator commands from sensor readings and setpoints.

        Called once per simulation tick.

        Parameters
        ----------
        readings : SensorReadings
            Current sensor values (with noise and possible faults).
        setpoints : Setpoints
            Current target operating conditions for the active crop phase.
        dt_seconds : float
            Time step duration in seconds (typically 60.0).

        Returns
        -------
        ActuatorCommands
            Desired actuator outputs as percentages (0 – 100).

        Notes
        -----
        **CO₂ Sensor Fault Handling (required):**

        The K30 primary sensor (``readings.co2_ppm_primary``) can freeze at
        400 ppm.  If your controller injects CO₂ based on a frozen K30
        reading, the internal CO₂ level will exceed the 5 000 ppm toxic
        threshold and your controller will receive a FAIL grade.

        Implement redundancy logic before computing the CO₂ control signal::

            discrepancy = abs(readings.co2_ppm_primary - readings.co2_ppm_backup)
            co2_actual = (
                readings.co2_ppm_backup if discrepancy > 200
                else readings.co2_ppm_primary
            )
        """
        # ================================================================
        # TODO: Replace this stub with your PID implementation.
        #
        # The stub returns zero commands (no control action) so that the
        # simulation framework can be run before any student code is written.
        # Running the simulation with this stub will result in a FAIL score
        # because the greenhouse temperature will drop to Mars ambient.
        # ================================================================
        return ActuatorCommands(
            heater_pct=0.0,
            led_pct=0.0,
            co2_valve_pct=0.0,
            pump_pct=0.0,
        )
