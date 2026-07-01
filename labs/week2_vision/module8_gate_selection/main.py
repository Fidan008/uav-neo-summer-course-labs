"""
MIT BWSI Autonomous Drone Racing Course - UAV Neo
GNU General Public License v3.0

Week 2 · Module 8 — Gate Selection — Main orchestrator

Runs every step in sequence against the simulator:
    drone sim module8_gate_selection/main.py
Run a single step directly instead:
    drone sim tasks/<step_file>.py
"""

# -- Course setup: makes the shared `neo_lab` helper importable (don't edit). --
import os as _os, sys as _sys
_d = _os.path.dirname(_os.path.realpath(__file__))
while _os.path.basename(_d) != "labs" and _os.path.dirname(_d) != _d:
    _d = _os.path.dirname(_d)
if _d not in _sys.path:
    _sys.path.insert(0, _d)
import neo_lab

import drone_core
from tasks import (
    step1_list_gates,
    step2_pick_next,
)

drone = drone_core.create_drone()
launcher = neo_lab.Launcher(3.0)

_STEPS = [
    ("Step 1: List All Gates", step1_list_gates),
    ("Step 2: Pick the Next Gate", step2_pick_next),
]

_index = 0


def start():
    global _index
    _index = 0
    launcher.reset()
    print("\n" + "=" * 56)
    print("  Week 2 · Module 8 — Gate Selection")
    print("=" * 56 + "\n")


def update():
    global _index
    neo_lab.record(drone)
    if not launcher.done:
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


if __name__ == "__main__":
    drone.set_start_update(start, update)
    drone.go()
