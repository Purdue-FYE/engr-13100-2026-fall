# Martian Greenhouse Simulation

## Overview

This module contains a physics-based simulation of a deployable **Mars-Lunar Greenhouse (MLGH)** cylindrical prototype. It is used as the stress-test harness for the **ENGR 13100 Team Project** — students implement a PID environmental controller and the simulation evaluates it over a 30-sol Martian mission.

## Learning Objectives

By completing this project, students will:

1. Apply PID control theory to a multi-variable physical system.
2. Implement sensor redundancy logic to handle hardware fault modes.
3. Reason about thermal dynamics, atmospheric composition, and plant physiology simultaneously.
4. Experience realistic engineering constraints: limited actuator power, Mars environment extremes, and stochastic disturbances.

## Package Structure

```
martian_greenhouse_sim/
├── constants.py      Physical and simulation constants (geometry, materials, crop targets)
├── environment.py    MarsEnvironment — diurnal temperature, solar irradiance, dust storms
├── greenhouse.py     Greenhouse — thermal ODE, CO₂/RH/soil dynamics, state dataclasses
├── actuators.py      VirtualActuators — heater, LED, CO₂ valve, irrigation pump
├── sensors.py        VirtualSensors — DHT22, K30, SCD41, TEROS12, SQ-500 with noise + faults
├── controllers.py    StudentPIDController stub — students implement this
├── simulation.py     run_simulation() — 30-sol stress test loop + scoring
└── tests/            Pytest suite covering all components
```

## Quick Start

```python
from martian_greenhouse_sim.simulation import run_simulation
from martian_greenhouse_sim.controllers import StudentPIDController

result = run_simulation(days=30, seed=42, controller_cls=StudentPIDController)
print(result.summary())
```

Run from the repository root:

```sh
python -m pytest source/Part_05_Team_Project/martian_greenhouse_sim/tests/ -v
```

## Greenhouse Specifications

| Parameter | Value |
|---|---|
| Cylinder dimensions | 5.5 m × 2.1 m diameter |
| Surface area (SA) | 43.2 m² |
| Active mixing volume (V_T) | 14 m³ |
| Internal pressure | 100 kPa |
| Air density (ρ) | 1.2 kg/m³ |
| Specific heat (C_p) | 1006 J/(kg·K) |
| Wall U-value | 0.3 W/(m²·K) |

## Thermal Dynamics

$$HL = SA \times U \times (T_{in} - T_{out})$$

$$\frac{dT_{in}}{dt} = \frac{-HL + Q_{heater} + S_i}{\rho \times V_T \times C_p}$$

## Lettuce (*Lactuca sativa*) Targets

| Variable | Target |
|---|---|
| Temperature (day) | 23 °C |
| Temperature (night) | 18 °C |
| CO₂ | 800 – 1 000 ppm |
| Relative humidity | 40 – 60 % |

## Stress Events

**Global dust storm** — automatically injected at a random sol.  Atmospheric opacity (τ) rises to 5.0–8.5, reducing solar irradiance by up to 97%.

**K30 CO₂ sensor freeze** — the primary CO₂ sensor occasionally freezes at 400 ppm.  Students must validate readings against the backup SCD41 sensor to prevent runaway CO₂ injection.
