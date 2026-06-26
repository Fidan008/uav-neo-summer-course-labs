"""
MIT BWSI Autonomous Drone Racing Course - UAV Neo
GNU General Public License v3.0

Week 2/3 Lab — Step 2: Fit a Line (Least Squares)
Fit y = m*x + b to the bright edge pixels with linear regression.
Source: 03_LinearRegression.ipynb (calculate_regression).
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
V_MIN      = 200
MIN_PIXELS = 200
HOVER_TIME = 3.0

# -- Module-level state -----------------------------------------------------
_timer = 0.0
_done  = False

def fit_line(points):
    """Least-squares fit of y = m*x + b. points is the (row, col) array from
    np.argwhere, so column = x and row = y."""
    ##################################
    #### START PUT CODE HERE #########
    # 1. points = points.astype(np.float64)   # int -> float so the fit is exact
    # 2. xs = points[:, 1]   (columns are x)
    #    ys = points[:, 0]   (rows are y)
    # 3. m, b = np.polyfit(xs, ys, 1)
    m, b = 0.0, 0.0  # YOUR CODE HERE
    ###### END PUT CODE HERE #########
    ##################################
    return m, b

def reset():
    global _timer, _done
    _timer = 0.0
    _done  = False


def update(drone):
    global _timer, _done
    if _done:
        return True
    drone.flight.stop()   # hover in place
    ##################################
    #### START PUT CODE HERE #########

    # 1. Build the bright-edge mask like Step 1: neo_lab.bright_mask(image, V_MIN) > 0
    # 2. points = np.argwhere(mask)          # (row, col) coordinates of bright pixels
    # 3. if len(points) < MIN_PIXELS: return False
    # 4. m, b = fit_line(points)             # <-- implement fit_line above
    # 5. When _timer >= HOVER_TIME: print m and b, then set _done = True

    ###### END PUT CODE HERE #########
    ##################################
    return _done


if __name__ == "__main__":
    _drone = drone_core.create_drone()
    _launcher = neo_lab.Launcher(3.0)

    def start():
        _launcher.reset()
        reset()
        print("Step 2: Fit a Line (Least Squares)")

    def _update():
        if not _launcher.done:        # arm + climb to a safe height first
            _launcher.update(_drone)
            return
        if update(_drone):
            _drone.flight.land()

    _drone.set_start_update(start, _update)
    _drone.go()
