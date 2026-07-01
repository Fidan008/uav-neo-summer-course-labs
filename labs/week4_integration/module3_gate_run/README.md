# Week 4 · Module 3 — Capstone: Gate Run

Fly through a series of gates on your own and time the run. This is the course
capstone: it pulls together gate detection (Week 2), distance from apparent size
(Module 6), gate selection (Module 8), and yaw/forward control (Week 3), organized
as a **state machine**.

## What you'll learn

- Designing a state machine for an autonomous task
- Sequencing perception and control into a repeating loop
- Measuring performance (a timed run)

## Key terms

- **State machine** — a controller with named modes (states) and rules for switching between them. Only one state is active at a time, which keeps complex behavior readable.
- **State** — one mode of behavior: `SEARCH`, `CENTER`, `APPROACH`, `PASS`, `DONE`.
- **Transition** — the rule that moves you from one state to the next (e.g. "gate width ≥ `PASS_WIDTH` → start passing").
- **Pass-through** — flying straight for `PASS_TIME` to go *through* a gate, because once you're close the gate fills or leaves the frame and you can't servo on it anymore.
- **Lap time** — the elapsed time to clear all `NUM_GATES`, your performance score.

## How to run

```bash
drone open_sim                          # launch the sim once
drone sim course/week4_integration/module3_gate_run/main.py            # your code
drone sim course/week4_integration/module3_gate_run/main_solution.py   # reference run
```

Press **Enter** in the simulator window to start.

`find_gates(image)` is **provided** (returns `(col, area, width)` per gate). The
capstone is the state machine, not the detection — that part is done for you.

## What to expect

The drone searches for a gate, centers on it, flies toward it, passes through, then
looks for the next one. After `NUM_GATES` it stops, prints the run time, and lands.

## You're done when

The drone passes `NUM_GATES` gates in sequence (you'll see a "passed gate N" message
for each), prints a total run time, and lands. Beating the `main_solution` time is
the stretch goal.

## If it doesn't work

| Symptom | Fix |
|---------|-----|
| Spins forever in SEARCH | No cyan gate in view, or `MIN_AREA` rejects distant gates. Lower it or reposition the start. |
| Never leaves CENTER | `CENTER_TOL` too tight, or yaw sign inverted so it never centers. |
| Stops short of the gate | Raise `PASS_WIDTH` so it gets closer before switching to PASS, or lengthen `PASS_TIME`. |
| Re-locks the same gate after passing | `PASS_TIME`/`APPROACH_PITCH` too small to clear it — fly through longer or faster. |
| Counts gates it didn't pass | Only increment in the `PASS` state after `PASS_TIME`, not on every frame. |

## Going further (optional)

- Add altitude control so the drone passes through the **middle** of each gate, using the gate's vertical position in the frame.
- Replace the fixed `PASS_TIME` with a detection of the gate leaving the frame (a more honest "I went through it").
- Log each gate's pass time and print split times. Then tune `APPROACH_PITCH`, `MAX_YAW`, and `PASS_WIDTH` to cut the total — a real race-tuning loop.
- Make it a true lap: after the last gate, return to the start (Module 1 waypoint) and stop the clock there.

---

Fill in the blanks in `tasks/`; completed references are in `solutions/` (try it yourself first!).
