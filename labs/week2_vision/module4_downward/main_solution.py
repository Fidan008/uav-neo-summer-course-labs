"""
MIT BWSI Autonomous Drone Racing Course - UAV Neo
GNU General Public License v3.0

Week 2 · Module 4 — Downward Camera (Gate Detection) — SOLUTION orchestrator

Runs every step in sequence against the simulator:
    drone sim module4_downward/main_solution.py
Run a single step directly instead:
    drone sim solutions/<step_file>.py
"""

import os as _os, sys as _sys
_d = _os.path.dirname(_os.path.abspath(__file__))
while _os.path.basename(_d) != "labs" and _os.path.dirname(_d) != _d:
    _d = _os.path.dirname(_d)
if _d not in _sys.path:
    _sys.path.insert(0, _d)
import neo_lab

import drone_core
from solutions import (
    step1_find_contours,
    step2_largest_object,
    step3_track_object,
)

drone = drone_core.create_drone()
launcher = neo_lab.Launcher(3.0)

_STEPS = [
    ("Step 1: Find Gate Contours", step1_find_contours),
    ("Step 2: Largest Gate", step2_largest_object),
    ("Step 3: Center Over the Gate", step3_track_object)
]

_index = 0


def start():
    global _index
    _index = 0
    launcher.reset()
    print("\n" + "=" * 56)
    print("  Week 2 · Module 4 — Downward Camera (Gate Detection)")
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
