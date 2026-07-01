"""
MIT BWSI Autonomous Drone Racing Course - UAV Neo
GNU General Public License v3.0

Week 2 · Module 8 — Step 2: Pick the Next Gate  (SOLUTION)
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
COL_CENTER = 320
MAX_YAW = 0.25
SEARCH_YAW = 0.2
CENTER_TOL = 0.1
HOLD_TIME = 1.0

# -- Module-level state -----------------------------------------------------
_hold = 0.0
_done = False


def find_gates(image, min_area=MIN_AREA):
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
    global _hold, _done
    _hold = 0.0
    _done = False


def update(drone):
    global _hold, _done
    if _done:
        return True
    image = drone.camera.get_color_image()
    gates = find_gates(image)
    if not gates:
        drone.flight.send_pcmd(0, 0, SEARCH_YAW, 0)
        _hold = 0.0
        return False
    col, area, _c = max(gates, key=lambda g: g[1])   # largest area = closest
    err = (col - COL_CENTER) / COL_CENTER
    yaw = uav_utils.clamp(err * MAX_YAW, -MAX_YAW, MAX_YAW)
    drone.flight.send_pcmd(0, 0, yaw, 0)
    if abs(err) < CENTER_TOL:
        _hold += drone.get_delta_time()
    else:
        _hold = 0.0
    if _hold >= HOLD_TIME:
        drone.flight.stop()
        print(f"[Step 2] Locked on the closest gate (area={area:.0f})")
        _done = True
    return _done


if __name__ == "__main__":
    _drone = drone_core.create_drone()
    _launcher = neo_lab.Launcher(3.0)

    def start():
        _launcher.reset()
        reset()
        print("Step 2: Pick the Next Gate")

    def _update():
        if not _launcher.done:
            _launcher.update(_drone)
            return
        if update(_drone):
            _drone.flight.land()

    _drone.set_start_update(start, _update)
    _drone.go()
