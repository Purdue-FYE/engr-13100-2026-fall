"""
Physical and simulation constants for the Martian Greenhouse Simulation.

All values are documented with source or rationale. Instructors may override
the tunable parameters (marked with a comment) to change simulation behaviour
without touching the physics model code.
"""

import math

# ===========================================================================
# Martian Environment
# ===========================================================================

#: Length of a Martian solar day (sol) in seconds.
SOL_SECONDS: float = 88_775.0

#: Mars receives approximately 43 % of the solar energy that Earth does.
MARS_SOLAR_FACTOR: float = 0.43

#: Simplified Earth peak direct solar irradiance used for pedagogy (W/m²).
#: A more precise value is 1361 W/m² (solar constant), but 1000 W/m² keeps
#: the arithmetic clean for students.
SOLAR_CONSTANT_W_M2: float = 1000.0

#: Peak clear-sky solar irradiance at the Martian surface (W/m²).
I_PEAK_MARS: float = MARS_SOLAR_FACTOR * SOLAR_CONSTANT_W_M2  # ≈ 430 W/m²

# --- Diurnal temperature model (°C) ---
#: Mean of the diurnal temperature cycle.  = (high + low) / 2
T_MEAN_C: float = (-5.0 + -70.0) / 2.0  # -37.5 °C

#: Amplitude of the diurnal temperature cycle.  = (high - low) / 2
T_AMPLITUDE_C: float = (-5.0 - -70.0) / 2.0  # 32.5 °C

#: Phase offset (rad) so that the temperature maximum aligns with local noon
#: (t = SOL_SECONDS / 2).
#:   sin(2π·(sol/2)/sol − π/2) = sin(π − π/2) = sin(π/2) = 1  ✓
T_PHASE: float = math.pi / 2.0

# --- Dust storm / opacity model ---
#: Atmospheric opacity (Tau) on a clear Martian day.
TAU_CLEAR: float = 0.5

#: Minimum storm-level opacity (Tau).
TAU_STORM_MIN: float = 5.0

#: Maximum storm-level opacity (Tau).
TAU_STORM_MAX: float = 8.5

#: Maximum fractional reduction in solar radiation during a global dust storm.
#: At TAU_STORM_MAX the incident solar drops to (1 − 0.97) = 3 % of clear-sky.
TAU_REDUCTION_MAX: float = 0.97

# ===========================================================================
# Greenhouse Geometry & Structural Properties
# ===========================================================================

#: Cylinder length (m).
CYLINDER_LENGTH_M: float = 5.5

#: Cylinder outer diameter (m).
CYLINDER_DIAMETER_M: float = 2.1

#: Cylinder outer radius (m).
CYLINDER_RADIUS_M: float = CYLINDER_DIAMETER_M / 2.0  # 1.05 m

#: Total geometric volume of the cylinder (m³).
TOTAL_VOLUME_M3: float = 21.0

#: Total structural surface area of the greenhouse (m²).
SURFACE_AREA_M2: float = 43.2

#: Active mixing air volume V_T — approx. 65 % of total volume (m³).
ACTIVE_VOLUME_M3: float = 14.0

#: Maintained internal pressure against the near-vacuum of Mars (kPa).
INTERNAL_PRESSURE_KPA: float = 100.0

# ===========================================================================
# Thermodynamic Properties
# ===========================================================================

#: Thermal transmittance of the double-walled insulated glazing (W/(m²·K)).
#: [TUNABLE] A lower U-value reduces heat loss. 0.6 represents a realistic
#: insulated polycarbonate envelope — balances daytime solar gain against a
#: heater that can keep up at the Martian -70 °C night ambient.
U_VALUE_W_M2_K: float = 0.6

#: Internal air density (kg/m³).
RHO_AIR_KG_M3: float = 1.2

#: Specific heat capacity of air (J/(kg·K)).
CP_AIR_J_KG_K: float = 1006.0

#: Effective projected area of the cylinder for solar capture (m²).
#: Uses the circular cross-section perpendicular to solar incidence.
A_PROJ_M2: float = math.pi * CYLINDER_RADIUS_M**2  # ≈ 3.46 m²

#: Fraction of incident solar radiation absorbed by the glazing and air mass.
#: [TUNABLE] At Mars noon (≈ 585 W/m²) with A_PROJ = 3.46 m², 0.20 yields a
#: passive equilibrium near 10 °C — giving the heater real work while keeping
#: midday temperatures inside the crop's lethal-high envelope.
ABSORPTION_EFFICIENCY: float = 0.20

# ===========================================================================
# PAR (Photosynthetically Active Radiation)
# ===========================================================================

#: Maximum PAR at crop level when Mars solar irradiance is at peak (µmol/m²/s).
#: [TUNABLE]
PAR_SOLAR_MAX_UMOL_M2_S: float = 800.0

#: Maximum supplemental PAR delivered by the LED array at 100 % intensity.
#: [TUNABLE]
LED_PAR_MAX_UMOL_M2_S: float = 300.0

# ===========================================================================
# Actuator Physical Limits
# ===========================================================================

#: Maximum ceramic heater output (W).  [TUNABLE]
HEATER_MAX_W: float = 3000.0

#: Fraction of LED electrical power dissipated as heat (waste heat).
LED_HEAT_FRACTION: float = 0.35

#: Maximum LED array electrical power draw (W).  [TUNABLE]
LED_MAX_POWER_W: float = 600.0

#: Maximum CO₂ injection rate at 100 % valve opening (ppm/s in the mixing volume).
#: Equates to ≈ 60 ppm/min.  [TUNABLE]
CO2_MAX_INJECTION_PPM_S: float = 1.0

#: Maximum irrigation pump rate (VWC/s at 100 % speed).
#: Corresponds to +0.02 VWC per hour at 100 %.  [TUNABLE]
PUMP_MAX_VWC_S: float = 0.02 / 3600.0  # ≈ 5.56 × 10⁻⁶ VWC/s

# ===========================================================================
# Sensor Noise (1-sigma Gaussian)
# ===========================================================================

NOISE_TEMP_C: float = 0.2  # DHT22 temperature noise (°C)
NOISE_RH_PCT: float = 1.0  # DHT22 humidity noise (%)
NOISE_CO2_PPM: float = 20.0  # K30 / SCD41 CO₂ noise (ppm)
NOISE_VWC: float = 0.01  # TEROS 12 soil moisture noise
NOISE_PAR_UMOL: float = 10.0  # SQ-500 PAR noise (µmol/m²/s)

# ===========================================================================
# Simulation Defaults
# ===========================================================================

#: Default simulation time step (seconds).
DEFAULT_DT_S: float = 60.0

#: Default simulation duration (Martian sols).
DEFAULT_DAYS: int = 30

#: Default random seed for reproducible runs.
DEFAULT_SEED: int = 42

# ===========================================================================
# Lettuce (Lactuca sativa) Crop Setpoints
# ===========================================================================

LETTUCE_TEMP_DAY_C: float = 23.0  # Daytime target (°C)
LETTUCE_TEMP_NIGHT_C: float = 18.0  # Nighttime target (°C)

LETTUCE_CO2_LOW_PPM: float = 800.0  # Lower CO₂ bound (ppm)
LETTUCE_CO2_HIGH_PPM: float = 1000.0  # Upper CO₂ bound (ppm)
LETTUCE_CO2_SETPOINT_PPM: float = 900.0  # PID setpoint (midpoint)

LETTUCE_RH_LOW_PCT: float = 40.0  # Lower RH bound (%)
LETTUCE_RH_HIGH_PCT: float = 60.0  # Upper RH bound (%)
LETTUCE_RH_SETPOINT_PCT: float = 50.0  # PID setpoint (midpoint)

LETTUCE_VWC_SETPOINT: float = 0.40  # Target soil moisture (VWC)

# ===========================================================================
# Safety Thresholds
# ===========================================================================

#: CO₂ concentration considered acutely toxic / lethal for plants (ppm).
CO2_TOXIC_PPM: float = 5000.0

#: Sustained duration at or above CO2_TOXIC_PPM that constitutes a failure (s).
CO2_TOXIC_DURATION_S: float = 1800.0  # 30 minutes

#: Hard simulation cap on internal CO₂ concentration (ppm).
CO2_BOUNDS_MAX_PPM: float = 20_000.0

# ===========================================================================
# Plant Cohort Health — Lethal Exposure Thresholds
# ===========================================================================
# Plants die when a stress accumulator exceeds its threshold (seconds of
# sustained exposure).  Only three failure modes are tracked; all other
# variables are assumed controlled adequately by the students.

#: Temperature below which exposure is lethal (°C).
PLANT_LETHAL_LOW_C: float = 5.0

#: Temperature above which exposure is lethal (°C).
PLANT_LETHAL_HIGH_C: float = 40.0

#: Seconds at PLANT_LETHAL_LOW_C before the cohort dies (2 hours).
PLANT_LETHAL_LOW_DURATION_S: float = 7_200.0

#: Seconds at PLANT_LETHAL_HIGH_C before the cohort dies (1 hour).
PLANT_LETHAL_HIGH_DURATION_S: float = 3_600.0

#: Volumetric water content below which soil is drought-stressed.
PLANT_DROUGHT_VWC: float = 0.10

#: Volumetric water content above which soil is waterlogged.
PLANT_WATERLOG_VWC: float = 0.70

#: Seconds at PLANT_DROUGHT_VWC before the cohort dies (1 sol).
PLANT_DROUGHT_DURATION_S: float = SOL_SECONDS

#: Seconds at PLANT_WATERLOG_VWC before the cohort dies (0.5 sol).
PLANT_WATERLOG_DURATION_S: float = SOL_SECONDS * 0.5

#: PAR below which the light level is insufficient for plant survival.
PLANT_LOW_PAR_UMOL: float = 150.0

#: Cumulative seconds at PLANT_LOW_PAR_UMOL before the cohort dies (2 sols).
PLANT_LOW_LIGHT_DURATION_S: float = SOL_SECONDS * 2.0

# --- Stress recovery time constants (exponential decay, τ = 1/e recovery) ---
# When conditions recover from a stressful band, the accumulated stress decays
# as  s(t) = s₀ · exp(−Δt / τ).  A larger τ means slower recovery.
#
# Temperature recovers relatively quickly (0.25 sol ≈ 6 h): membrane and
# enzyme damage is partially reversible once temperature is stabilised.
PLANT_RECOVERY_TEMP_TAU_S: float = SOL_SECONDS * 0.25  # ≈ 22 194 s

# Soil stress (drought or waterlog) recovers over ~0.5 sol (≈ 12 h): root
# tissue and water potential normalise more slowly than air temperature.
PLANT_RECOVERY_SOIL_TAU_S: float = SOL_SECONDS * 0.5  # ≈ 44 388 s

# Photosynthetic capacity after a low-light period recovers over ~0.5 sol;
# chloroplast re-orientation and enzyme re-synthesis are relatively slow.
PLANT_RECOVERY_LIGHT_TAU_S: float = SOL_SECONDS * 0.5  # ≈ 44 388 s

# --- Scoring ---
#: Number of Martian sols considered a full-credit run.
SCORING_TARGET_SOLS: float = 30.0

#: Gradescope maximum points awarded to the plant survival test.
SCORING_MAX_POINTS: float = 100.0
