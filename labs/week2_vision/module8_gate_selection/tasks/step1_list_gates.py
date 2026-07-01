"""
MIT BWSI Autonomous Drone Racing Course - UAV Neo
GNU General Public License v3.0

Week 2 · Module 8 — Step 1: List All Gates
A race course has more than one gate in view at once. Before you can pick the
right one to fly through, you have to find them all. `find_gates` (provided) returns
every gate-shaped cyan contour; here you count and report them.
"""

import drone_core
import drone_utils as uav_utils
import cv2
import numpy as np

# -- Course setup: makes the shared `neo_lab` helper importable.
#    You don't need to read or change this block. --
import os as _os, sys as _sys
_d = _os.path.dirname(_os.path.realpath(__file__))
while _os.path.basename(_d) != "labs" and _os.path.dirname(_d) != _d:
    _d = _os.path.dirname(_d)
if _d not in _sys.path:
    _sys.path.insert(0, _d)
import neo_lab

# -- Constants --------------------------------------------------------------
MIN_AREA = 400
MAX_ASPECT = 2.5
HOVER_TIME = 3.0

# -- Module-level state -----------------------------------------------------
_timer = 0.0
_done = False


def find_gates(image, min_area=MIN_AREA):
    """Every square-ish cyan gate in the frame, as a list of (col, area, contour).
    This is the multi-gate version of neo_lab.largest_cyan_gate."""
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, neo_lab.CYAN_LOWER, neo_lab.CYAN_UPPER)
    mask = cv2.dilate(mask, np.ones((5, 5), np.uint8), iterations=2)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    gates = []
    for c in contours:
        area = cv2.contourArea(c)
        if area < min_area:
            continue
        x, y, w, h = cv2.boundingRect(c)
        if w == 0 or h == 0 or max(w, h) / min(w, h) > MAX_ASPECT:
            continue
        gates.append((x + w / 2.0, area, c))
    return gates


def reset():
    global _timer, _done
    _timer = 0.0
    _done = False


def update(drone):
    global _timer, _done
    if _done:
        return True
    drone.flight.stop()   # hover in place
    ##################################
    #### START PUT CODE HERE #########

    # 1. image = drone.camera.get_color_image()
    # 2. gates = find_gates(image)            # list of (col, area, contour)
    # 3. _timer += drone.get_delta_time()
    # 4. When _timer >= HOVER_TIME: print len(gates) and each gate's (col, area),
    #    then set _done = True.

    ###### END PUT CODE HERE #########
    ##################################
    return _done


if __name__ == "__main__":
    _drone = drone_core.create_drone()
    _launcher = neo_lab.Launcher(3.0)

    def start():
        _launcher.reset()
        reset()
        print("Step 1: List All Gates")

    def _update():
        if not _launcher.done:        # arm + climb to a safe height first
            _launcher.update(_drone)
            return
        if update(_drone):
            _drone.flight.land()

    _drone.set_start_update(start, _update)
    _drone.go()
