# Plan: Martian Greenhouse Simulation Generator

**Created:** 2026-05-05
**Status:** Ready for Atlas Execution

## Summary

Implement a self-contained Python simulation of a deployable Martian greenhouse intended to stress-test student-written environmental control (PID) code. The simulation will model Mars external conditions (diurnal temperature + solar + dust storms), greenhouse thermodynamics, simplified internal atmosphere/plant-zone state, virtual sensors with noise and fault injection, virtual actuators with percentage inputs, and a main loop that runs multi-day scenarios and scores controller performance.

Primary outputs will live under `source/Part_05_Team_Project/` in a code-oriented subfolder, mirroring the repo’s existing content organization (code stored inside `source/`). A small pytest suite will validate key physics invariants, deterministic behavior under a seed, and the required failure modes.

## Context & Analysis

**Relevant Files:**
- `source/Part_05_Team_Project/` (currently only contains `Shredded Documents.pdf`): add a new subdirectory for the simulation package and optional markdown overview.
- `pyproject.toml`: Python 3.13, `pytest` available; `ruff` configured for `E/F/I`.

**Patterns & Conventions:**
- Repo stores Python utilities under `source/` (e.g., `source/utils/*`) and uses straightforward, standard-library-first code.
- Keep the simulation deterministic when `seed` is provided (important for grading/reproducible tests).

## Proposed File Layout

Create a new simulation package under the Team Project content tree:

- `source/Part_05_Team_Project/martian_greenhouse_sim/`
  - `__init__.py`
  - `constants.py` (physical constants, geometry, defaults)
  - `environment.py` (class `MarsEnvironment`)
  - `greenhouse.py` (class `Greenhouse`, state dataclasses)
  - `sensors.py` (virtual sensor classes/functions)
  - `actuators.py` (actuator interfaces + clamping)
  - `controllers.py` (placeholder `StudentPIDController`)
  - `simulation.py` (`run_simulation(days=30, ...)`, scoring, logging)
  - `README.md` or `0_overview.md` (short usage + learning objectives; keep minimal)

Add tests:
- `tests/test_martian_greenhouse_sim.py`

If the repository doesn’t currently have a `tests/` folder at the root (it may exist only in the autograder subproject), place tests under `source/Part_05_Team_Project/martian_greenhouse_sim/tests/` and configure discovery accordingly. Prefer root `tests/` if present.

## Component Design (Meets the 5 Required Components)

### 1) `MarsEnvironment` (in `environment.py`)

**Responsibilities:**
- Track simulation time (seconds since start) and provide external Mars conditions at each timestep.
- Provide diurnal temperature cycle and solar radiation that is reduced by dust storms.
- Inject a multi-day global dust storm event during a run.

**Temperature model:**
- Use a sine wave over one sol. For simplicity, use 24h or optionally Mars sol length (24h 39m = 88775 s).
- Target highs ~ -5°C, lows ~ -70°C.
- Suggested formula (in °C):
  - `T_mean = (-5 + -70)/2 = -37.5`
  - `T_amp = (-5 - -70)/2 = 32.5`
  - `T_out(t) = T_mean + T_amp * sin(2π*(t/sol_seconds) - phase)`
  - Choose `phase` so that local noon aligns with maximum.

**Solar model:**
- Base “clear-day” incident solar power uses Mars factor 0.43 of Earth.
- Use a simple diurnal irradiance curve (e.g., half-wave rectified sine) so radiation is zero at night.
  - `I_clear(t) = I_peak_mars * max(0, sin(2π*(t/sol_seconds) - phase_noon))`
  - `I_peak_mars ≈ 0.43 * 1000 W/m²` (simple pedagogical value) or `0.43 * 1361 W/m²` (solar constant); pick one and document.

**Dust storm / Tau model:**
- Maintain `tau` (atmospheric opacity) with baseline 0.5.
- Provide:
  - `maybe_start_dust_storm(rng)` to probabilistically initiate.
  - Or, for stress testing, schedule exactly one storm with random start day and duration (2–6 days) inside `run_simulation`.
- During storm, set `tau` randomly in [5.0, 8.5].
- Radiation reduction: must be “up to 97%”. Implement transmittance mapping clamped so worst-case reduces 97%.
  - Example: `trans = clamp(1 - 0.97 * storm_strength, min=0.03, max=1.0)` where `storm_strength` maps tau from 0.5→0 and 8.5→1.
  - Keep baseline transmittance at 1.0 for tau=0.5.

**API (suggested):**
- `update(dt_seconds: float) -> None`
- `get_temperature_c() -> float`
- `get_solar_irradiance_w_per_m2() -> float`
- `get_tau() -> float`

### 2) `Greenhouse` Physics (in `greenhouse.py`)

**Given geometry & constants (hard requirements):**
- Cylinder: length 5.5 m, diameter 2.1 m, total volume 21 m³.
- Surface area `SA = 43.2 m²`.
- Active mixing volume `V_T = 14 m³` (~65% of total).
- Internal pressure: 100 kPa (store for reference; near-vacuum external).
- Air density `rho = 1.2 kg/m³`.
- Specific heat `Cp = 1006 J/(kg*K)`.

**State variables (minimum):**
- `T_in_c` (internal air temperature)
- `rh_percent` (relative humidity)
- `co2_ppm`
- `soil_vwc` (volumetric water content)
- `par_umol_m2_s` (photosynthetically active radiation)

**Thermal dynamics (hard requirement):**
- Time step: default `dt = 60 s`.
- Heat loss:
  - `HL = SA * U * (T_in - T_out)` in Watts.
  - Choose an insulated U-value; recommend `U = 0.3 W/(m²*K)` (document as “highly insulated double-wall/vacuum”).
- Temperature update:
  - `dT_in/dt = (-HL + Q_heater + S_i) / (rho * V_T * Cp)`
  - `S_i` is solar radiant energy captured in Watts.

**Solar capture to `S_i`:**
- Use an effective projected area `A_proj` rather than full SA to avoid over-heating:
  - Recommend `A_proj = π*(D/2)^2` (cross-sectional area) or `length*diameter` as a simple “side projection”; choose and document.
- `S_i = I_incident * A_proj * transmittance * absorption_efficiency`
  - `absorption_efficiency` default ~0.6–0.8.

**Other internal dynamics (simplified but needed for sensors/actuators):**
- **Humidity:** first-order response to irrigation evaporation + dehumidification via temperature/condensation simplification.
  - Increase RH when irrigation runs; decrease when heater increases temperature (since saturation vapor pressure increases).
  - Keep bounded [0, 100].
- **CO2:** mass-balance in ppm within mixing volume.
  - Increase with injection valve.
  - Decrease with plant uptake during daytime (proportional to PAR) and/or leakage.
  - Keep bounded [0, e.g., 20000] for safety.
- **Soil moisture:** increase with irrigation pump; decrease via evapotranspiration.
  - Keep bounded [0, 1].
- **PAR:** computed from (a) Mars solar PAR fraction + (b) LED supplemental.

**API (suggested):**
- `update_state(env: MarsEnvironment, actuators: ActuatorState, dt_seconds: float) -> None`
- `get_state() -> GreenhouseState` (dataclass snapshot)

### 3) Virtual Sensors (in `sensors.py`)

Implement sensor read methods named exactly as required and with Gaussian noise.

**Noise:**
- Use `random.Random(seed)` or a passed-in RNG.
- Typical noise (tunable constants):
  - Temperature: σ=0.2°C
  - RH: σ=1.0%
  - CO2: σ=20 ppm
  - Soil VWC: σ=0.01
  - PAR: σ=10 µmol/m²/s

**Required sensor functions (hard requirement):**
- `read_DHT22()` → `(temperature_c, relative_humidity_percent)`
- `read_K30()` or `read_SCD41()` → `co2_ppm`
  - Provide both for redundancy; freeze fault will affect one sensor (see Component 5).
- `read_TEROS12()` → `soil_vwc`
- `read_SQ500()` → `par_umol_m2_s`

**Implementation approach:**
- Provide a `VirtualSensors` class bound to a `Greenhouse` instance and internal RNG.
- Methods read true state, add noise, clamp to physical ranges.

### 4) Virtual Actuators (in `actuators.py`)

Provide percentage-based control methods that clamp inputs to [0, 100] and scale to internal “physics units.”

**Required actuator methods (hard requirement):**
- `set_heater(power_percentage)`
- `set_LED_lights(intensity_percentage)`
- `inject_CO2(valve_open_percentage)`
- `run_irrigation_pump(speed_percentage)`

**Suggested scaling:**
- Heater max: 2000–5000 W (choose 3000 W default; document)
- LED max: convert percent → supplemental PAR (e.g., up to 300 µmol/m²/s) and add some waste heat (e.g., 30–50% converted to heat)
- CO2 valve max: ppm/s injection rate derived from mixing volume (e.g., up to +50 ppm/min at 100%)
- Irrigation max: soil VWC increase rate (e.g., +0.02 VWC per hour at 100%)

**Actuator state structure:**
- Keep an `ActuatorState` dataclass with normalized 0–1 values and derived physical outputs (W, µmol, ppm/s, etc.) for the greenhouse update.

### 5) Student Controller + Evaluation Loop (in `controllers.py` and `simulation.py`)

**Student controller stub (hard requirement):**
- Class `StudentPIDController` with placeholder methods for students.
- Include the PID formula in docstring and a minimal working example controller that returns 0 outputs (so simulation runs).
- Provide separate PID loops (recommended) for temperature and CO2; optionally humidity/soil.

**Crop setpoints (hard requirement):**
- Lettuce targets:
  - Temperature: 23°C day, 18°C night
  - CO2: 800–1000 ppm (use 900 as midpoint setpoint for PID)
  - RH: 40–60% (use 50 midpoint setpoint)

**Day/night schedule:**
- Use the environment’s diurnal phase:
  - “Day” when solar irradiance > 0 (simplest and robust under storms), else “night”.
  - Note: during dust storms, irradiance is reduced but nonzero; still considered day.

**Dust storm injection (hard requirement):**
- In `run_simulation(days=30)`, schedule at least one storm event:
  - Random start day in [2, days-5]
  - Random duration 2–5 sols
  - Tau range 5.0–8.5

**CO2 sensor freeze failure (hard requirement):**
- Implement a fault in the CO2 virtual sensor such that occasionally it “freezes” at 400 ppm for a period.
- Recommended approach:
  - `VirtualSensors` maintains a fault state: `co2_freeze_active`, `freeze_end_time`, `freeze_value=400`.
  - Trigger randomly (e.g., once every 1–3 days with small probability per minute) and last 30–180 minutes.
  - Apply the freeze to `read_K30()` only; `read_SCD41()` returns the true (noisy) value.
  - This enables the “sensor redundancy logic” requirement without adding new UI/UX.

**Simulation loop (hard requirement):**
- `run_simulation(days=30, dt_seconds=60, seed=..., controller_cls=StudentPIDController)`
- Each tick:
  1. Update `MarsEnvironment` (temp + solar + tau)
  2. Compute “day/night” and setpoints
  3. Read sensors (including noise + faults)
  4. Call student controller update to obtain actuator percentages
  5. Apply actuators (clamp)
  6. Update greenhouse physics/state
  7. Log states, sensor readings, actuator commands, and fault flags

**Scoring / evaluation:**
- Provide a simple performance score and failure detection:
  - Temperature tracking error integrated over time
  - CO2 out-of-range time fraction
  - RH out-of-range time fraction
  - Hard safety guard: CO2 above a “toxic threshold” (e.g., >5000 ppm for >30 min) yields fail.
- Produce a summary dict plus optional CSV log.

## Implementation Phases

### Phase 1: Scaffold package + core dataclasses

**Objective:** Create the directory structure and foundational types for state, settings, and logs.

**Files to Create:**
- `source/Part_05_Team_Project/martian_greenhouse_sim/__init__.py`
- `source/Part_05_Team_Project/martian_greenhouse_sim/constants.py`
- `source/Part_05_Team_Project/martian_greenhouse_sim/greenhouse.py` (state dataclasses only initially)

**Tests to Write:**
- `test_imports`: package imports without side effects.

**Acceptance Criteria:**
- [ ] Package imports cleanly under Python 3.13
- [ ] State dataclasses exist and serialize to dict cleanly

### Phase 2: Implement `MarsEnvironment`

**Objective:** External Mars conditions with diurnal temperature, solar irradiance, and dust storms.

**Files to Modify/Create:**
- `source/Part_05_Team_Project/martian_greenhouse_sim/environment.py`

**Tests to Write:**
- `test_mars_temp_range`: over one sol, min ≈ -70°C and max ≈ -5°C (with tolerance)
- `test_dust_tau_range`: storm tau in [5.0, 8.5], baseline 0.5
- `test_dust_reduces_solar`: storm reduces irradiance by up to ~97%

**Acceptance Criteria:**
- [ ] `MarsEnvironment` provides `temperature_c`, `solar_irradiance`, and `tau`
- [ ] Dust storm scheduling works deterministically with a seed

### Phase 3: Implement greenhouse thermal model

**Objective:** Implement required heat-loss and temperature update equation.

**Files to Modify/Create:**
- `source/Part_05_Team_Project/martian_greenhouse_sim/greenhouse.py`

**Tests to Write:**
- `test_heat_loss_sign`: when `T_in > T_out`, computed HL positive
- `test_temp_moves_toward_outside_without_heat`: with heater off and no solar, temperature decreases toward outside when outside is colder
- `test_heater_increases_temp`: with strong heater, temperature rises

**Acceptance Criteria:**
- [ ] `update_state()` matches required equation structure
- [ ] Uses SA=43.2, V_T=14, rho=1.2, Cp=1006

### Phase 4: Add atmosphere + plant-zone simplified dynamics

**Objective:** Add plausible, bounded dynamics for RH, CO2, soil moisture, and PAR.

**Files to Modify/Create:**
- `greenhouse.py` (extend `update_state`)

**Tests to Write:**
- `test_bounds`: RH in [0,100], soil in [0,1], CO2 >= 0
- `test_irrigation_increases_soil`: soil moisture increases when pump on
- `test_co2_injection_increases_ppm`: CO2 increases when valve open

**Acceptance Criteria:**
- [ ] State variables update smoothly and remain bounded

### Phase 5: Virtual actuators

**Objective:** Implement required actuator APIs and scaling to physical outputs.

**Files to Create:**
- `source/Part_05_Team_Project/martian_greenhouse_sim/actuators.py`

**Tests to Write:**
- `test_clamp_percent`: inputs below 0 → 0, above 100 → 100
- `test_scaling_outputs`: 0% yields 0 output; 100% yields max output

**Acceptance Criteria:**
- [ ] Required actuator methods exist with 0–100% inputs

### Phase 6: Virtual sensors + noise + CO2 freeze fault

**Objective:** Implement required sensor names, noise, and the CO2 freeze failure mode.

**Files to Create:**
- `source/Part_05_Team_Project/martian_greenhouse_sim/sensors.py`

**Tests to Write:**
- `test_noise_deterministic_with_seed`
- `test_co2_freeze_fault_only_primary_sensor`: `read_K30()` can freeze at 400 while `read_SCD41()` tracks true

**Acceptance Criteria:**
- [ ] Sensor methods match required names and return values
- [ ] CO2 freeze fault triggers and can be detected via redundancy

### Phase 7: Student PID stub + main simulation loop

**Objective:** Provide `StudentPIDController` stub and implement `run_simulation(days=30)` with dust storm and faults.

**Files to Create/Modify:**
- `source/Part_05_Team_Project/martian_greenhouse_sim/controllers.py`
- `source/Part_05_Team_Project/martian_greenhouse_sim/simulation.py`

**Tests to Write:**
- `test_run_simulation_completes`: runs for short duration without errors
- `test_storm_injected`: run includes a storm interval
- `test_outputs_schema`: returned summary contains expected fields

**Acceptance Criteria:**
- [ ] `run_simulation(days=30)` exists and runs end-to-end
- [ ] Uses lettuce day/night setpoints and CO2/RH target ranges
- [ ] Includes multi-day dust storm and CO2 sensor freeze failure mode

## Open Questions

1. **Where should tests live?**
   - **Option A:** Root `tests/` (standard pytest discovery)
   - **Option B:** Under `source/Part_05_Team_Project/martian_greenhouse_sim/tests/`
   - **Recommendation:** Use root `tests/` if it already exists or is acceptable to add; otherwise colocate inside the simulation folder and document how to run.

2. **Solar constant choice for pedagogy vs realism**
   - **Option A:** Use 1000 W/m² baseline * 0.43 (simple)
   - **Option B:** Use 1361 W/m² * 0.43 (more “physical”)
   - **Recommendation:** Option A for simplicity; the simulation is for control behavior rather than perfect Mars modeling.

3. **U-value selection**
   - **Option A:** Fixed `U=0.3` (high insulation)
   - **Option B:** Configurable with default `0.3`
   - **Recommendation:** Make configurable but default to 0.3.

## Risks & Mitigation

- **Risk:** Overly aggressive solar capture overheats greenhouse unrealistically.
  - **Mitigation:** Use an effective projected area and absorption efficiency; validate temperature remains within plausible bounds under no control.
- **Risk:** Non-determinism makes grading flaky.
  - **Mitigation:** Centralize RNG; thread `seed` through environment, sensors, and storm/fault scheduling.
- **Risk:** Student controller API ambiguity.
  - **Mitigation:** Provide a minimal, clear `update(readings, setpoints, dt)` interface and keep actuator methods percentage-based.

## Success Criteria

- [ ] `MarsEnvironment` implements diurnal temperature and dust storm Tau behavior
- [ ] `Greenhouse.update_state()` implements required heat-loss and temperature ODE step
- [ ] Virtual sensors (`read_DHT22`, `read_K30`/`read_SCD41`, `read_TEROS12`, `read_SQ500`) add Gaussian noise
- [ ] Actuators accept 0–100% and scale to physics inputs
- [ ] `run_simulation(days=30)` injects a multi-day dust storm and CO2 sensor freeze fault
- [ ] Tests validate invariants and deterministic behavior under a seed

## Notes for Atlas

- Keep everything standard-library-only (no numpy) unless the repo already prefers otherwise.
- Make the simulation runnable as a script: `python -m ...simulation` or a simple `if __name__ == '__main__':` in `simulation.py`.
- Don’t add extra UX/pages; keep to the requested simulation architecture and file placement under `source/Part_05_Team_Project/`.
