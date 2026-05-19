"""
Pytest configuration for the Martian greenhouse simulation tests.

Adds the ``source/Part_05_Team_Project/`` directory to sys.path so that
``import martian_greenhouse_sim`` resolves correctly when pytest is run
from the repository root.
"""

import sys
from pathlib import Path

# Resolve: .../source/Part_05_Team_Project/martian_greenhouse_sim/tests/conftest.py
# parents[2] = .../source/Part_05_Team_Project/
_pkg_root = Path(__file__).resolve().parents[2]
if str(_pkg_root) not in sys.path:
    sys.path.insert(0, str(_pkg_root))
