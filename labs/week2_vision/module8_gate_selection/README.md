# Week 2 · Module 8 — Gate Selection

A race course shows several gates at once. Detecting one gate isn't enough — you
have to choose *which* one is next. This module finds every gate in view, then
applies a selection rule to pick a target.

## What you'll learn

- Detecting multiple objects, not just the largest
- Writing a selection rule (a policy) over candidates
- Turning a chosen target into a yaw command

## Key terms

- **Candidate** — any detected gate that could be the next target. `find_gates` returns all of them.
- **Selection rule (policy)** — the logic that picks one candidate. Here: largest apparent area, which (for same-size gates) means closest.
- **Apparent area** — the contour's pixel area; bigger means nearer.
- **Tie-break** — what to do when two candidates score equally (e.g. prefer the one nearer the image center). Worth thinking about even if rare.

## How to run

```bash
drone open_sim                          # launch the sim once
drone sim course/week2_vision/module8_gate_selection/main.py            # all steps, your code
drone sim course/week2_vision/module8_gate_selection/main_solution.py   # reference flight
```

Press **Enter** in the simulator window to start.

`find_gates(image)` is **provided** in each step file — it returns a list of
`(col, area, contour)` for every gate-shaped cyan blob. This module is about what
you do *with* that list, so the detection is done for you.

## Steps

1. **`step1_list_gates.py`** — count and report every gate in view
2. **`step2_pick_next.py`** — pick the closest gate and turn to center it

## What to expect

Step 1 hovers and prints how many gates it sees and each one's column and area.
Step 2 chooses the closest gate, yaws to center it, holds, then lands.

## You're done when

- Step 1 prints a gate count and one line per gate (column and area).
- Step 2 turns toward the largest-area gate and reports a lock once it's centered for `HOLD_TIME`.

## If it doesn't work

| Symptom | Fix |
|---------|-----|
| `find_gates` returns nothing | No cyan gates in view, or `MIN_AREA` too high for distant gates. |
| Picks the wrong gate | Check your selection key — `max(gates, key=lambda g: g[1])` selects by area (index 1). |
| Yaws past center and oscillates | Lower `MAX_YAW`, and reduce yaw as the normalized error shrinks. |
| Never locks | Make sure `_hold` accumulates only while within `CENTER_TOL` and resets otherwise. |

## Going further (optional)

- Change the policy to "nearest the image center" instead of "closest," and describe when each is the better choice on a real course.
- Add a tie-break: among gates of similar area, prefer the one closer to center.
- Track the selected gate across frames (store its column, match with `neo_lab.gate_nearest_to`) so the choice doesn't flicker as areas change — the bridge to the Week 4 gate run.

---

Fill in the blanks in `tasks/`; completed references are in `solutions/` (try it yourself first!).
