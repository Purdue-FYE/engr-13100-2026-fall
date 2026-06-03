"""Convenience launcher for the Milestone 2 sandbox GUI.

Adds this directory to sys.path so `martian_greenhouse_sim.gui` resolves,
then calls its main(). Students should just run:

    python source/Part_05_Team_Project/run_sandbox.py

from the repo root (or pass an integer seed as the first arg).
"""

import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))

from martian_greenhouse_sim.gui import main  # noqa: E402

if __name__ == "__main__":
    seed = 42
    if len(sys.argv) > 1:
        try:
            seed = int(sys.argv[1])
        except ValueError:
            pass
    main(seed=seed)
