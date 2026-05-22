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
    SensorReadings,
    Setpoints,
    StudentPIDController,
)
from .environment import MarsEnvironment
from .greenhouse import Greenhouse, GreenhouseState
from .plants import PlantCohort
from .sensors import VirtualSensors
from .simulation import SimulationResult, load_student_controller, run_simulation

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
    "PlantCohort",
    "run_simulation",
    "load_student_controller",
    "SimulationResult",
]
