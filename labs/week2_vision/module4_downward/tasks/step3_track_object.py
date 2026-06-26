"""
MIT BWSI Autonomous Drone Racing Course - UAV Neo
GNU General Public License v3.0

Week 2/3 Lab — Step 3: Center Over the Gate
Visual-servo the drone to hover directly above the gate frame.
Source: 04_Downward.ipynb applied live (downward camera).
"""

import drone_core
import drone_utils as uav_utils
import cv2
import numpy as np

import os as _os, sys as _sys
_d = _os.path.dirname(_os.path.abspath(__file__))
while _os.path.basename(_d) != "labs" and _os.path.dirname(_d) != _d:
    _d = _os.path.dirname(_d)
if _d not in _sys.path:
    _sys.path.insert(0, _d)
import neo_lab

# -- Constants --------------------------------------------------------------
V_MIN = 200
MIN_AREA = 300
MAX_TILT = 0.18      # pitch/roll authority
CENTER_TOL = 60      # pixels considered 'centered'
HOLD_TIME = 2.0      # seconds to stay centered before done
ROW_CENTER = 240
COL_CENTER = 320

# -- Module-level state -----------------------------------------------------
_hold = 0.0
_done = False

def reset():
    global _hold, _done
    _hold = 0.0
    _done = False


def update(drone):
    global _hold, _done
    if _done:
        return True
    ##################################
    #### START PUT CODE HERE #########

    # 1. best = neo_lab.largest_bright_contour(image, V_MIN, MIN_AREA)
    # 2. If best is None: drone.flight.stop(); _hold = 0.0; return False
    # 3. row, col = uav_utils.get_contour_center(best)
    # 4. err_col = col - COL_CENTER ; err_row = row - ROW_CENTER
    # 5. roll  = clamp(err_col / COL_CENTER * MAX_TILT, -MAX_TILT, MAX_TILT)
    #    pitch = clamp(-err_row / ROW_CENTER * MAX_TILT, -MAX_TILT, MAX_TILT)
    #    (signs may need flipping depending on camera mounting -- experiment!)
    # 6. drone.flight.send_pcmd(pitch, roll, 0, 0)
    # 7. Accumulate _hold while both errors < CENTER_TOL; when _hold >= HOLD_TIME,
    #    stop and set _done = True

    ###### END PUT CODE HERE #########
    ##################################
    return _done


if __name__ == "__main__":
    _drone = drone_core.create_drone()
    _launcher = neo_lab.Launcher(3.0)

    def start():
        _launcher.reset()
        reset()
        print("Step 3: Center Over the Gate")

    def _update():
        if not _launcher.done:        # arm + climb to a safe height first
            _launcher.update(_drone)
            return
        if update(_drone):
            _drone.flight.land()

    _drone.set_start_update(start, _update)
    _drone.go()
