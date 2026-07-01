"""
MIT BWSI Autonomous Drone Racing Course - UAV Neo
GNU General Public License v3.0

Week 4 · Module 3 — Capstone: Gate Run
Fly through a series of gates and time the run. This combines everything: gate
detection (Week 2), distance from apparent size (Module 6), gate selection
(Module 8), and yaw/forward control (Week 3) -- organized as a state machine.

A state machine is a controller with named modes ("states") and rules for moving
between them. Here:

    SEARCH   no gate in view -> spin until one appears
    CENTER   turn to put the chosen gate in the middle of the frame
    APPROACH fly forward (still correcting yaw) until the gate looks big/close
    PASS     fly straight for a moment to go through it, then look for the next
    DONE     all gates passed -> stop and report the time
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
CENTER_TOL = 0.12      # normalized error to switch from CENTER to APPROACH
APPROACH_PITCH = 0.18
PASS_WIDTH = 220       # gate box this wide (px) => close enough to pass
PASS_TIME = 1.5        # seconds to fly straight through the gate
NUM_GATES = 3          # gates to pass before the run is done

# -- Module-level state -----------------------------------------------------
_state = "SEARCH"
_gates_passed = 0
_pass_timer = 0.0
_elapsed = 0.0
_done = False


def find_gates(image, min_area=MIN_AREA):
    """Every square-ish cyan gate in the frame, as a list of (col, area, width)."""
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


def update(drone):
    global _state, _gates_passed, _pass_timer, _elapsed, _done
    if _done:
        return True
    dt = drone.get_delta_time()
    _elapsed += dt
    image = drone.camera.get_color_image()
    gates = find_gates(image)
    ##################################
    #### START PUT CODE HERE #########

    # Implement the state machine described at the top of this file.
    # Tools: gates is a list of (col, area, width); the closest gate is the one with
    # the largest area (max on the area field). The yaw error is
    # (col - COL_CENTER) / COL_CENTER. Use drone.flight.send_pcmd(pitch, roll, yaw, throttle)
    # and uav_utils.clamp(...). Set _state to the next mode when a rule fires.
    #
    # SEARCH:   no gates -> send_pcmd(0, 0, SEARCH_YAW, 0); if gates appear -> "CENTER".
    # CENTER:   pick the closest gate, yaw to center it; when abs(err) < CENTER_TOL -> "APPROACH".
    # APPROACH: keep yaw-centering AND add APPROACH_PITCH; when its width >= PASS_WIDTH -> "PASS"
    #           (reset _pass_timer). If gates vanish in CENTER/APPROACH, go back to "SEARCH".
    # PASS:     fly straight (send_pcmd(APPROACH_PITCH, 0, 0, 0)); after PASS_TIME, count the
    #           gate (_gates_passed += 1). If _gates_passed >= NUM_GATES -> "DONE", else "SEARCH".
    # DONE:     stop, print _elapsed, set _done = True.

    ###### END PUT CODE HERE #########
    ##################################
    return _done


if __name__ == "__main__":
    _drone = drone_core.create_drone()
    _launcher = neo_lab.Launcher(3.0)

    def start():
        _launcher.reset()
        reset()
        print("Capstone: Gate Run")

    def _update():
        if not _launcher.done:        # arm + climb to a safe height first
            _launcher.update(_drone)
            return
        if update(_drone):
            _drone.flight.land()

    _drone.set_start_update(start, _update)
    _drone.go()
