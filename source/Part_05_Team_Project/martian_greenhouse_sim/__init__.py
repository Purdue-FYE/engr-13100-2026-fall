"""
Martian Greenhouse Simulation
==============================
A physics-based simulation of a deployable Mars-Lunar Greenhouse (MLGH)
for stress-testing student-written PID environmental control code.

Public API
----------
from martian_greenhouse_sim import (
    MarsEnvironment,
    Greenhouse,
    VirtualActuators,
    VirtualSensors,
    StudentPIDController,
    run_simulation,
)
"""

from .actuators import VirtualActuators
from .controllers import (
    ActuatorCommands,
    Setpoints,
    SensorReadings,
    StudentPIDController,
)
from .environment import MarsEnvironment
from .greenhouse import Greenhouse, GreenhouseState
from .sensors import VirtualSensors
from .simulation import SimulationResult, run_simulation

__all__ = [
    "MarsEnvironment",
    "Greenhouse",
    "GreenhouseState",
    "VirtualActuators",
    "VirtualSensors",
    "StudentPIDController",
    "SensorReadings",
    "Setpoints",
    "ActuatorCommands",
    "run_simulation",
    "SimulationResult",
]
