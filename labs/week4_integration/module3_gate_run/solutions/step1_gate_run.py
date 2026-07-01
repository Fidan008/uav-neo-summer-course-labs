"""
MIT BWSI Autonomous Drone Racing Course - UAV Neo
GNU General Public License v3.0

Week 4 · Module 3 — Capstone: Gate Run  (SOLUTION)
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
SEARCH_YAW = 0.25
MAX_YAW = 0.25
CENTER_TOL = 0.12
APPROACH_PITCH = 0.18
PASS_WIDTH = 220
PASS_TIME = 1.5
NUM_GATES = 3

# -- Module-level state -----------------------------------------------------
_state = "SEARCH"
_gates_passed = 0
_pass_timer = 0.0
_elapsed = 0.0
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
        gates.append((x + w / 2.0, area, w))
    return gates


def reset():
    global _state, _gates_passed, _pass_timer, _elapsed, _done
    _state = "SEARCH"
    _gates_passed = 0
    _pass_timer = 0.0
    _elapsed = 0.0
    _done = False


def _yaw_to(col):
    err = (col - COL_CENTER) / COL_CENTER
    return err, uav_utils.clamp(err * MAX_YAW, -MAX_YAW, MAX_YAW)


def update(drone):
    global _state, _gates_passed, _pass_timer, _elapsed, _done
    if _done:
        return True
    dt = drone.get_delta_time()
    _elapsed += dt
    image = drone.camera.get_color_image()
    gates = find_gates(image)

    if _state == "SEARCH":
        if gates:
            _state = "CENTER"
        else:
            drone.flight.send_pcmd(0, 0, SEARCH_YAW, 0)

    elif _state == "CENTER":
        if not gates:
            _state = "SEARCH"
        else:
            col, area, w = max(gates, key=lambda g: g[1])
            err, yaw = _yaw_to(col)
            drone.flight.send_pcmd(0, 0, yaw, 0)
            if abs(err) < CENTER_TOL:
                _state = "APPROACH"

    elif _state == "APPROACH":
        if not gates:
            _state = "SEARCH"
        else:
            col, area, w = max(gates, key=lambda g: g[1])
            err, yaw = _yaw_to(col)
            drone.flight.send_pcmd(APPROACH_PITCH, 0, yaw, 0)
            if w >= PASS_WIDTH:
                _pass_timer = 0.0
                _state = "PASS"

    elif _state == "PASS":
        drone.flight.send_pcmd(APPROACH_PITCH, 0, 0, 0)
        _pass_timer += dt
        if _pass_timer >= PASS_TIME:
            _gates_passed += 1
            print(f"[Capstone] passed gate {_gates_passed} at t={_elapsed:.1f}s")
            _state = "DONE" if _gates_passed >= NUM_GATES else "SEARCH"

    elif _state == "DONE":
        drone.flight.stop()
        print(f"[Capstone] Run complete: {_gates_passed} gates in {_elapsed:.1f}s")
        _done = True

    return _done


if __name__ == "__main__":
    _drone = drone_core.create_drone()
    _launcher = neo_lab.Launcher(3.0)

    def start():
        _launcher.reset()
        reset()
        print("Capstone: Gate Run")

    def _update():
        if not _launcher.done:
            _launcher.update(_drone)
            return
        if update(_drone):
            _drone.flight.land()

    _drone.set_start_update(start, _update)
    _drone.go()
