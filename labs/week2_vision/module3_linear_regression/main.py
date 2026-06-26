"""
MIT BWSI Autonomous Drone Racing Course - UAV Neo
GNU General Public License v3.0

Week 2 · Module 3 — Linear Regression (Edge Following) — Main orchestrator

Runs every step in sequence against the simulator:
    drone sim module3_linear_regression/main.py
Run a single step directly instead:
    drone sim tasks/<step_file>.py
"""

import os as _os, sys as _sys
_d = _os.path.dirname(_os.path.abspath(__file__))
while _os.path.basename(_d) != "labs" and _os.path.dirname(_d) != _d:
    _d = _os.path.dirname(_d)
if _d not in _sys.path:
    _sys.path.insert(0, _d)
import neo_lab

import drone_core
from tasks import (
    step1_detect_line,
    step2_fit_line,
    step3_follow_line,
)

drone = drone_core.create_drone()
launcher = neo_lab.Launcher(3.0)

_STEPS = [
    ("Step 1: Detect the Bright Edge Pixels", step1_detect_line),
    ("Step 2: Fit a Line (Least Squares)", step2_fit_line),
    ("Step 3: Follow the Edge", step3_follow_line)
]

_index = 0


def start():
    global _index
    _index = 0
    launcher.reset()
    print("\n" + "=" * 56)
    print("  Week 2 · Module 3 — Linear Regression (Edge Following)")
    print("=" * 56 + "\n")


def update():
    global _index
    if not launcher.done:                 # arm + climb before running steps
        if launcher.update(drone):
            _STEPS[0][1].reset()
            print(f"--- {_STEPS[0][0]} ---")
        return

    if _index >= len(_STEPS):
        drone.flight.land()
        return

    name, mod = _STEPS[_index]
    if mod.update(drone):
        _index += 1
        if _index < len(_STEPS):
            _STEPS[_index][1].reset()
            print(f"\n--- {_STEPS[_index][0]} ---")
        else:
            print("\n=== Module complete! Landing... ===")


def update_slow():
    if launcher.done and _index < len(_STEPS):
        print(f"[{_STEPS[_index][0]}] height={neo_lab.height(drone):.2f}m")


if __name__ == "__main__":
    drone.set_start_update(start, update, update_slow)
    drone.go()
