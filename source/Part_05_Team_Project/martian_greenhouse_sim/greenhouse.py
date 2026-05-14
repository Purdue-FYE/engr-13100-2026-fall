"""
Thermodynamic and atmospheric state model for the cylindrical MLGH prototype.

Greenhouse geometry (hard requirements)
---------------------------------------
  Cylinder: 5.5 m long * 2.1 m diameter
  Total volume : 21 m³   Surface area SA : 43.2 m²
  Active mixing volume V_T : 14 m³  (≈ 65 % of total)
  Internal pressure : 100 kPa

Thermal dynamics (required equations)
--------------------------------------
Heat loss:
    HL = SA * U * (T_in − T_out)              [Watts]

Temperature update per time step Δt:
    dT_in/dt = (−HL + Q_heater + S_i) / (ρ * V_T * Cp)
    T_in ← T_in + dT_in/dt * Δt

where:
    U       = thermal transmittance of wall glazing  (W/(m²·K))
    Q_heater= total heat input from actuators         (W)
    S_i     = solar radiant energy captured          (W)
    ρ       = air density  1.2 kg/m³
    Cp      = specific heat of air  1006 J/(kg·K)

Simplified internal atmosphere dynamics
-----------------------------------------
CO₂   : balance of injection, plant uptake (PAR-driven), and leakage.
RH    : increases with irrigation evaporation; decreases via heater drying
        and natural Mars-ambient drift.
Soil  : gains from irrigation pump; loses via evapotranspiration.
PAR   : sum of solar component and supplemental LED contribution.
"""

import copy
from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from .constants import (
    A_PROJ_M2,
    ABSORPTION_EFFICIENCY,
    ACTIVE_VOLUME_M3,
    CO2_BOUNDS_MAX_PPM,
    CP_AIR_J_KG_K,
    DEFAULT_DT_S,
    I_PEAK_MARS,
    LED_PAR_MAX_UMOL_M2_S,
    PAR_SOLAR_MAX_UMOL_M2_S,
    RHO_AIR_KG_M3,
    SURFACE_AREA_M2,
    U_VALUE_W_M2_K,
)

if TYPE_CHECKING:
    from .environment import MarsEnvironment


# ---------------------------------------------------------------------------
# Shared state types
# ---------------------------------------------------------------------------


@dataclass
class ActuatorState:
    """
    Current actuator commands expressed both as 0–1 fractions and as the
    corresponding physical output quantities consumed by the physics model.

    Populated by :class:`VirtualActuators`; consumed by :meth:`Greenhouse.update_state`.
    """

    # Normalised fractions [0, 1]
    heater_frac: float = 0.0
    led_frac: float = 0.0
    co2_valve_frac: float = 0.0
    pump_frac: float = 0.0

    # Derived physical outputs (filled by VirtualActuators)
    heater_watts: float = 0.0        #: Heater output (W)
    led_par_umol: float = 0.0        #: Supplemental LED PAR (µmol/m²/s)
    led_heat_watts: float = 0.0      #: LED waste heat (W)
    co2_ppm_s: float = 0.0           #: CO₂ injection rate (ppm/s)
    vwc_s: float = 0.0               #: Irrigation rate (VWC/s)


@dataclass
class GreenhouseState:
    """
    Snapshot of the greenhouse internal environment at a single time step.

    All fields are SI-compatible; units are annotated in the docstring.
    """

    time_s: float = 0.0                #: Simulation time (s)
    temp_c: float = 22.0               #: Internal air temperature (°C)
    rh_pct: float = 50.0              #: Relative humidity (%)
    co2_ppm: float = 900.0            #: CO₂ concentration (ppm)
    soil_vwc: float = 0.40            #: Soil volumetric water content [0–1]
    par_umol_m2_s: float = 0.0        #: PAR at crop level (µmol/m²/s)

    # Ancillary / diagnostic fields
    solar_irradiance_w_m2: float = 0.0  #: Incident solar irradiance (W/m²)
    t_out_c: float = -37.5              #: External Martian temperature (°C)
    heat_loss_w: float = 0.0           #: Conductive heat loss HL (W)
    solar_gain_w: float = 0.0          #: Solar energy captured S_i (W)


# ---------------------------------------------------------------------------
# Greenhouse physics model
# ---------------------------------------------------------------------------


class Greenhouse:
    """
    Thermodynamic and atmospheric model of the cylindrical MLGH prototype.

    The class tracks the internal state of the greenhouse and advances it
    one time step at a time via :meth:`update_state`.

    Parameters
    ----------
    initial_temp_c : float
        Initial internal air temperature (°C).
    initial_co2_ppm : float
        Initial CO₂ concentration (ppm).
    initial_rh_pct : float
        Initial relative humidity (%).
    initial_soil_vwc : float
        Initial soil volumetric water content [0 to 1].
    u_value : float
        Thermal transmittance of the wall (W/(m²·K)).  Lower values give
        better insulation.  Default 0.3 represents high-performance double-
        wall glazing with an insulating gas vacuum.
    """

    def __init__(
        self,
        initial_temp_c: float = 22.0,
        initial_co2_ppm: float = 900.0,
        initial_rh_pct: float = 50.0,
        initial_soil_vwc: float = 0.40,
        u_value: float = U_VALUE_W_M2_K,
    ) -> None:
        self._u = u_value
        self.state = GreenhouseState(
            temp_c=initial_temp_c,
            rh_pct=initial_rh_pct,
            co2_ppm=initial_co2_ppm,
            soil_vwc=initial_soil_vwc,
        )

    # ------------------------------------------------------------------
    # Public interface
    # ------------------------------------------------------------------

    def update_state(
        self,
        env: "MarsEnvironment",
        actuators: ActuatorState,
        dt_seconds: float = DEFAULT_DT_S,
    ) -> GreenhouseState:
        """
        Advance the greenhouse state by one time step *dt_seconds*.

        Implements the required heat-loss and temperature ODE equations:

            HL = SA * U * (T_in − T_out)
            dT_in/dt = (−HL + Q_heater + S_i) / (ρ * V_T * Cp)

        Also updates CO₂, relative humidity, soil moisture, and PAR.

        Parameters
        ----------
        env : MarsEnvironment
            Current Mars external conditions.
        actuators : ActuatorState
            Current actuator command state.
        dt_seconds : float
            Time step duration (s).

        Returns
        -------
        GreenhouseState
            The updated internal state (also stored in ``self.state``).
        """
        t_out = env.get_temperature_c()
        t_in = self.state.temp_c
        I = env.get_solar_irradiance_w_per_m2()

        # --- Thermal dynamics ---
        # Heat loss through the structure walls (W) — positive when T_in > T_out
        HL = SURFACE_AREA_M2 * self._u * (t_in - t_out)

        # Solar energy captured by the greenhouse glazing (W)
        S_i = I * A_PROJ_M2 * ABSORPTION_EFFICIENCY

        # Total heat input from electrical actuators (W)
        Q_heater = actuators.heater_watts + actuators.led_heat_watts

        # Temperature ODE step (required equation)
        dT_dt = (-HL + Q_heater + S_i) / (RHO_AIR_KG_M3 * ACTIVE_VOLUME_M3 * CP_AIR_J_KG_K)
        new_temp = t_in + dT_dt * dt_seconds

        # --- CO₂ dynamics ---
        # Plant photosynthetic uptake (PAR-driven, active during daylight)
        co2_uptake = 1.5e-4 * self.state.par_umol_m2_s * dt_seconds   # ppm

        # Background soil / plant respiration (slight CO₂ source at night too)
        co2_resp = 0.0015 * dt_seconds                                 # ppm

        # Actuator injection
        co2_in = actuators.co2_ppm_s * dt_seconds                     # ppm

        new_co2 = self.state.co2_ppm + co2_in - co2_uptake + co2_resp
        new_co2 = max(200.0, min(CO2_BOUNDS_MAX_PPM, new_co2))

        # --- Relative humidity dynamics ---
        # Evaporation from irrigation raises RH; heater raises temperature
        # which effectively lowers RH (constant absolute humidity / rising
        # saturation point); natural drift toward near-zero Mars ambient.
        rh_gain = actuators.pump_frac * 1.5 / 60.0 * dt_seconds       # %
        rh_heat_drying = (Q_heater / HEATER_MAX_REF_W) * 0.3 / 60.0 * dt_seconds  # %
        rh_ambient_loss = self.state.rh_pct * 5e-6 * dt_seconds       # %

        new_rh = self.state.rh_pct + rh_gain - rh_heat_drying - rh_ambient_loss
        new_rh = max(0.0, min(100.0, new_rh))

        # --- Soil moisture dynamics ---
        vwc_gain = actuators.vwc_s * dt_seconds
        # Evapotranspiration: baseline + PAR-driven transpiration
        et_rate = 5.0e-8 + 1.5e-8 * self.state.par_umol_m2_s         # VWC/s
        vwc_loss = et_rate * dt_seconds

        new_vwc = self.state.soil_vwc + vwc_gain - vwc_loss
        new_vwc = max(0.0, min(1.0, new_vwc))

        # --- PAR at crop level ---
        par_solar = (I / I_PEAK_MARS) * PAR_SOLAR_MAX_UMOL_M2_S if I_PEAK_MARS > 0.0 else 0.0
        par_solar = max(0.0, par_solar)
        new_par = par_solar + actuators.led_par_umol

        # --- Commit updated state ---
        self.state.time_s = env.get_time_s()
        self.state.temp_c = new_temp
        self.state.rh_pct = new_rh
        self.state.co2_ppm = new_co2
        self.state.soil_vwc = new_vwc
        self.state.par_umol_m2_s = new_par
        self.state.solar_irradiance_w_m2 = I
        self.state.t_out_c = t_out
        self.state.heat_loss_w = HL
        self.state.solar_gain_w = S_i

        return self.state

    def get_state(self) -> GreenhouseState:
        """Return a shallow copy of the current state snapshot."""
        return copy.copy(self.state)


# ---------------------------------------------------------------------------
# Internal reference constant for RH drying calculation
# (avoids circular import with constants.py)
# ---------------------------------------------------------------------------
HEATER_MAX_REF_W: float = 3000.0
