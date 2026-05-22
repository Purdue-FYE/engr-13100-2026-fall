# Milestone 2 Sandbox — Design Document

| | |
|---|---|
| **Status** | v1 shipped (commit `430651c` on `kpritche`); v2 design open |
| **Owners** | Kory Pritchett · Holly Fortner · ENGR 131 instructional team |
| **Last updated** | 2026-05-22 |
| **Scope** | The interactive sandbox at `source/Part_05_Team_Project/martian_greenhouse_sim/gui.py` and the Milestone 2 student experience that uses it |
| **Related** | [`Design Project Evaluation`](../../../Obsidian%20Vault/Purdue/ENGR%20131/Design%20Project%20Evaluation.md) (Obsidian) · [`plans/martian-greenhouse-simulation-plan.md`](../../plans/martian-greenhouse-simulation-plan.md) (original sim plan) · `martian_greenhouse_sim/0_overview.md` |

> **How to use this document.** Sections 1–4 are *as-built* — read them to understand what shipped and why. Sections 5–8 are *open* — every subsection has explicit `**Decision needed:**` prompts. Fill them in as we converge. Section 9 is the running decision log. When a v2 feature lands in code, move its row out of Section 7 into the relevant `gui.py` docstring and Section 9.

---

## 1. Purpose of the sandbox

The Martian Greenhouse design project asks first-year students to write a PID controller against a simulation whose physics, sensor faults, and plant model they've never seen before. The course's own learning objectives (`source/Part_04_Python/M*/0_overview.md`) carry them through `if/elif`, `for`, functions, `numpy`, `matplotlib`, and linear regression — but never through control theory, sensor redundancy, or coupled-system reasoning. The evaluation document captured this gap.

The sandbox closes the gap experientially. Before students write any controller code, they:

1. **See** the greenhouse with plants inside and a Mars sky overhead.
2. **Drag** actuator sliders by hand to feel how heater/LED/CO₂/pump change the world.
3. **Read** the K30 / SCD41 sensors and watch them disagree when the freeze fault fires.
4. **Configure** if/elif rule tables — the syntactic kin of what they learned in Python M2 — and watch their rules drive the actuators automatically.
5. **Fail** to keep plants alive by hand-tuning rules, and walk into Milestone 3 wanting to write something better.

The "fail" step is intentional. The sandbox is calibrated so that competent rule sets approach but do not perfectly hit the lettuce setpoints — students discover the limits of threshold control without us telling them.

---

## 2. v1 as-built

### 2.1 Files shipped (commit `430651c` on `kpritche`)

| Path | Lines | Role |
|------|------:|------|
| `source/Part_05_Team_Project/martian_greenhouse_sim/gui.py` | 1237 | Single-file tkinter + matplotlib sandbox |
| `source/Part_05_Team_Project/run_sandbox.py` | 27 | `sys.path`-bootstrap launcher students invoke from repo root |

### 2.2 Stack

- **Python 3.13** via `.venv` (`uv` toolchain)
- **tkinter** (standard library) — windowing, widgets
- **matplotlib 3.10** with `FigureCanvasTkAgg` — both the visual greenhouse panel and the rolling chart
- **Zero new dependencies** beyond what the existing simulation already required

### 2.3 Window layout

```
┌──────────────────────────────────────────────────────────────────┐
│ Top bar: Pause/Play  Reset  Speed (1x|10x|60x|600x)  Manual/Auto │
├──────────────────────┬───────────────────┬───────────────────────┤
│ VISUAL GREENHOUSE    │ SENSORS + PLANT   │ ROLLING CHART         │
│ (matplotlib axes)    │ (tk text labels)  │ (4 stacked traces)    │
├──────────────────────┴───────────────────┴───────────────────────┤
│ Tabbed bottom: Actuators (sliders) | Rules (tables) | Faults     │
└──────────────────────────────────────────────────────────────────┘
```

### 2.4 Visual greenhouse — what's on screen

- **Mars sky** — gradient by sol fraction (midnight → twilight → noon → twilight → midnight). Stars fade in at night.
- **Sun** — yellow disc following a diurnal arc across the sky; dims under dust storms (`alpha` decays with `tau`).
- **Mars surface** — rust ground with a darker horizon band.
- **Greenhouse** — translucent cylinder rendered as a rectangle with circular caps. Interior tint shifts blue (cold) → green (in lettuce band) → red (hot) by `gh.state.temp_c`.
- **5 plant sprites** — leafy polygons inside the greenhouse, scale and color tied to `plant.health` and `plant.alive`.
- **Actuator indicators** — heater glow (red, intensity by `heater_pct`), LED bar (warm white across the top, alpha by `led_pct`), CO₂ valve badge, pump droplet (size by `pump_pct`).
- **Dust storm overlay** — semi-transparent orange-brown rectangle covering the scene during a storm, opacity `tau / 8.5`.
- **Title line** — current sol, mode (MANUAL/AUTO), `T_out`, `tau`.

### 2.5 Rule engine

Each of the four actuators owns a `RuleSet` — an ordered list of `Rule(sensor, op, value, output_pct)` entries plus a default `ELSE` percentage. The first matching rule wins; otherwise the default fires.

**Sensors available in conditions:** `temperature_c`, `rh_pct`, `co2_k30_ppm`, `co2_scd41_ppm`, `co2_discrepancy`, `soil_vwc`, `par_umol`, `is_daytime` (last coerced to 0/1).

**Operators:** `<`, `<=`, `>`, `>=`, `==` (the last with float tolerance `< 0.5`).

This vocabulary is deliberately small and maps 1:1 to Python M2 `if/elif/else` syntax. Students who can read

```python
if temperature_c < 18.0: heater = 100
elif temperature_c < 22.0: heater = 60
else: heater = 0
```

can read the rule table, and vice versa.

### 2.6 Time model

- Outer tick scheduler runs every ~16 ms (`tk.after(16, ...)`).
- Simulation steps in chunks of `SIM_DT_S = 60` sim seconds (matches the engine default).
- Speed multiplier = sim minutes advanced per wall second. Steps per tick = `speed × (tick_interval / 1000)`; a fractional accumulator carries remainder across ticks so 1× still advances exactly one step per wall second.
- Matplotlib redraw at `RENDER_EVERY_N = 4` outer ticks (~15 fps), bounded by `draw_idle()` not `draw()`.
- Chart history decimated to one sample per 5 sim minutes, trimmed to `CHART_HISTORY_S = 6 sols`.

### 2.7 Verified at ship

- Headless 400-step run completes without exception (against `DISPLAY=:0`).
- Full render path (`_render_text()` + `_render_full()`) executes cleanly.
- K30 freeze button trips `sensors._co2_freeze_active = True` and the readout flips to red.
- Existing 116-test simulation suite still passes — no regression.
- With all actuators at zero, plants die from `TEMP_LETHAL_LOW` after ~7 sim hours, the intentional "do something!" teaching moment.

---

## 3. Known limitations of v1

| # | Limitation | Why it matters | Source |
|---|---|---|---|
| L1 | **No save/load of rule sets** — every session starts from the built-in starter rules. | Students can't persist a working configuration between sessions, can't share rules with teammates, can't iterate week over week. | gui.py — no `json` serializer wired up |
| L2 | **No CSV export** — chart data lives only in memory and trims to a rolling window. | Students can't take their session data into a Python M4 matplotlib exercise or a written report. | gui.py — `hist_t/temp/...` lists not exposed |
| L3 | **RH control is structurally hard** with no dehumidifier actuator. | The pump-RH coupling is the same problem the autograder hit; rule-based control on RH will always fight itself. | `MEMORY/KNOWLEDGE/Research/engr131-design-project-physics.md` |
| L4 | **No tutorial / guided sequence inside the GUI.** | The pedagogical sequence (pause → manual heater → manual LED → fault injection → rules → fail → next milestone) lives in the module docstring; students have to find it. | gui.py docstring |
| L5 | **Codespaces incompatible** — tkinter needs a real display. | The course's recommended dev environment doesn't run this tool. Local install required. | `tkinter` choice |
| L6 | **No way to compare two runs side by side.** | Students can't directly see "my rules vs the starter rules" without manually switching between configurations. | architectural — single-state runtime |
| L7 | **Rule editor is form-based**, not Python expressions. | Bridge to actual controller code is shorter with expressions; longer with forms. | Decision logged 2026-05-22; deliberate v1 choice |
| L8 | **Faults are manual-only** in v1; the random fault schedule is suppressed. | Students see faults only when they press the button. Mixed-blessing — easier to study, less realistic. | gui.py — sensors instantiated without `freeze_prob_per_step` |
| L9 | **No autograder integration.** | Students can't run the test_config rubric on their rule set without exporting to a Python file first. | gui.py is read-only of the engine |
| L10 | **No accessibility pass.** | Color-coded plant status assumes color vision; no keyboard shortcuts beyond standard tk; no screen reader hooks. | universal — not addressed in v1 |

---

## 4. Pedagogical alignment as-built

| Project skill (from `0_overview.md`) | Sandbox v1 does for it |
|---|---|
| Apply PID control theory | **Indirect.** Sandbox does not teach PID; it teaches the *problem* PID solves by letting students try threshold control and feel its limits. |
| Implement sensor redundancy logic | **Direct.** The K30 freeze fault button + the `co2_discrepancy` sensor variable + the explicit display of `|K30 − SCD41|` make the redundancy lesson concrete. |
| Reason about thermal dynamics + atmospheric composition + plant physiology simultaneously | **Direct.** All four state variables are visible at once on the chart, the visual panel, and the plant cohort panel. |
| Engineering constraints (limited power, extremes, stochastic disturbances) | **Direct.** Heater max, LED max, dust storm trigger, no-cooling reality all become tangible. |
| Define a Python class with a method signature | **Bridges from.** Rule tables are not classes, but the conceptual leap "sensor → decision → actuator output" prepares the Milestone 3 controller class. |
| Tune empirical parameters | **Direct.** Adjusting thresholds is parameter tuning. |
| Diagnose failure modes | **Direct.** The plant cohort panel shows *which* stress is killing the plants, not just *that* they died. |

The evaluation document's headline finding — "PID control theory is the largest curriculum GAP" — remains true. The sandbox does not fill that GAP. It makes the GAP visible and motivates filling it.

---

## 5. Open design questions for v2

> Each subsection has a `**Decision needed:**` prompt. Fill in with the answer when we converge.

### 5.1 Persistence

Should student rule configurations persist between sessions?

- Option A — JSON file (`student_rules.json` next to the launcher), auto-save on change, auto-load on start
- Option B — explicit "Save preset" / "Load preset" buttons with multiple named slots
- Option C — no persistence; force students to rebuild every session (current behavior)

**Decision needed:** _(unanswered)_

### 5.2 CSV export

Students need data to write Python M4 plots against. Where does the export live in the UI?

- Option A — single "Export last session as CSV" button in the Faults / utility tab
- Option B — auto-write to `~/Downloads/sandbox_<timestamp>.csv` every time the user hits Pause
- Option C — keep the GUI in-memory only; document a `from martian_greenhouse_sim.gui import GreenhouseSandbox; ...` API for programmatic data extraction

**Decision needed:** _(unanswered)_

### 5.3 Rule editor — should we add a Python-expression mode toggle?

Per the original v1 design conversation, we deliberately chose tables over Python expressions for first-year safety. v2 could add an opt-in toggle that lets students write `100 if temperature_c < 18 else 60 if temperature_c < 22 else 0` and have it parsed (safely — `ast.literal_eval` + restricted operators).

- Option A — defer expression mode to v3 once students have written one controller
- Option B — add expression mode as an instructor-only feature (off by default, configurable)
- Option C — never; tables forever — keep the bridge to PID via the controller class, not via richer rules

**Decision needed:** _(unanswered)_

### 5.4 Two-run comparison

How should "my rules vs. baseline" comparison work?

- Option A — split-pane: left side runs starter rules at the same seed, right side runs the student's
- Option B — overlay: same chart, two trace styles (solid for student, dashed for baseline)
- Option C — defer; comparison is the autograder's job

**Decision needed:** _(unanswered)_

### 5.5 In-GUI tutorial

How prescriptive should the onboarding be?

- Option A — first-launch banner with a 7-step walkthrough that highlights widgets in sequence
- Option B — a checklist sidebar that students can opt into; ticks off as they explore
- Option C — leave the docstring as-is; let the instructor's class plan drive sequence

**Decision needed:** _(unanswered)_

### 5.6 Autograder integration

Should the sandbox have a "Run autograder against my rules" button that emits a synthetic `student_controller.py` and pipes it through `test_config.py`?

- Option A — yes, button in Faults/utility tab, opens a results popup
- Option B — yes, but only as a CLI flag (`python run_sandbox.py --grade`); UI stays focused on play
- Option C — no — the autograder is for Milestone 3 submissions, not M2 exploration

**Decision needed:** _(unanswered)_

### 5.7 Codespaces story

Local-only was a deliberate v1 choice. Does v2 need a Codespaces-compatible variant?

- Option A — keep local-only; document clearly in the README and the syllabus
- Option B — add a web variant (Bokeh / Streamlit) for Codespaces, share the same `gui_state` module
- Option C — add a CLI-only "headless tutorial mode" (no GUI, just printed sensor/plant state per tick) for Codespaces

**Decision needed:** _(unanswered)_

### 5.8 RH dehumidifier

Per the evaluation doc, the simulation has no cooling/dehumidifier. We tuned `ABSORPTION_EFFICIENCY` and `U_VALUE_W_M2_K` to make temperature solvable, but RH remains coupled to the pump. Should v2 add a dehumidifier actuator?

- Option A — yes, extend `VirtualActuators` with `set_dehumidifier(pct)`, update the student controller interface, retune
- Option B — no, drop RH from the scored autograder rubric (already done as a placeholder in v1 of test_config)
- Option C — yes, but only in a "stretch difficulty" mode that students can opt into

**Decision needed:** _(unanswered)_

### 5.9 Time controls — more speeds?

v1 speed presets: `1× / 10× / 60× / 600×`. Are any missing?

- Option A — add `100×` and `1000×` to round out the range
- Option B — replace radio buttons with a continuous log-scale slider
- Option C — keep current set

**Decision needed:** _(unanswered)_

### 5.10 Accessibility

What's the minimum accessibility bar v2 should meet?

- Option A — color-blind safe palette + keyboard navigation for all controls + screen-reader labels
- Option B — color-blind safe palette only
- Option C — defer

**Decision needed:** _(unanswered)_

---

## 6. v2 candidate features — prioritized

Pulled from §5 plus other ideas surfaced in conversation. Each row carries a rough effort sizing (S = afternoon, M = day, L = multi-day) and a pedagogical-value note.

| Priority | Feature | Effort | Closes | Pedagogical value |
|----------|---------|--------|--------|-------------------|
| **P0** | JSON save / load of rule sets | S | L1 | Lets teams share configurations; the act of saving is a Python M4-adjacent skill |
| **P0** | CSV export of session data | S | L2 | Bridges directly into Python M4 matplotlib coursework |
| **P0** | First-launch tutorial overlay | S | L4 | Without this, half of students will miss the sequence |
| **P1** | "Run autograder against current rules" button | M | L9 | Closes the loop on Milestone 2 → Milestone 3 |
| **P1** | Two-run comparison overlay on the chart | M | L6 | Powerful "see your improvement" moment |
| **P1** | Dehumidifier actuator (stretch mode opt-in) | M | L3 | Solves RH coupling; expands student design space |
| **P2** | Python expression mode toggle for rules | M | L7 | Bridges form-based rules to code; defer to v3? |
| **P2** | Color-blind safe palette + keyboard nav | M | L10 | Required for any broad rollout |
| **P2** | Continuous speed slider | S | n/a | Polish |
| **P3** | Codespaces / web variant | L | L5 | Big lift; needs separate design |
| **P3** | Fault-schedule toggle (manual vs auto) | S | L8 | Lets advanced students see realistic stochastic faults |

> **Decision needed:** which P0 + P1 items are in v2 scope? Suggested cut line: all P0 plus first two P1 items. Total effort ~ 2 days.

---

## 7. Integration with the course

### 7.1 Milestone 2 session plan (proposed)

| Session | Activity |
|---|---|
| 1 | Instructor demos the sandbox in MANUAL mode. Students follow along, drag sliders, watch plants. |
| 2 | Students paired into teams, work through the in-GUI tutorial. Goal: keep plants alive for 1 sol by hand. |
| 3 | Introduce the rule editor. Students convert their hand-flying knowledge into if/elif rules. |
| 4 | Inject K30 freeze + dust storm. Discover the redundancy requirement and the dust-storm survival problem. |
| 5 | "Tournament" — teams run their rules at the same seed for 10 sols, leaderboard by `sols_survived`. Hand-off to Milestone 3. |

**Decision needed:** which sessions are sync (in-class) vs async (pre-class)?

### 7.2 Cross-references

- The control-systems primer recommended in [the evaluation document](../../../Obsidian%20Vault/Purdue/ENGR%20131/Design%20Project%20Evaluation.md) should land *before* Milestone 2 session 3 (introduction to the rule editor).
- The autograder `test_config.py` at `tasks/team_1/a/test_config.py` is the rubric students will be graded against in Milestone 3 — the sandbox should feel like the prep arena for it.

---

## 8. Implementation notes — for future contributors

### 8.1 Where to extend

| Want to add | Edit |
|---|---|
| A new actuator | `martian_greenhouse_sim/actuators.py` (engine) + `ACTUATOR_KEYS` / `ACTUATOR_LABELS` constants in `gui.py` + a new slider in `_build_actuator_tab` + a new `RuleSet` entry |
| A new sensor variable in rules | Add to `SENSOR_KEYS` in `gui.py` + populate in `_readings_for_rules` |
| A new operator | Add string to `OPERATORS` + handle in `Rule.matches` |
| A new visual element | Patch on the `GreenhouseVisual` axes in `__init__`, mutate in `update` |
| A new bottom tab | `self.tabs.add(<frame>, text=...)` in `_build_ui` |

### 8.2 Anti-patterns to avoid

- **Don't allocate matplotlib patches in `update()`.** All patches are created once in `__init__` and only their attributes (`set_alpha`, `set_xy`, `set_color`) mutate per frame.
- **Don't bypass the engine.** All physics goes through `Greenhouse.update_state`. No "shortcut" temperature calculations in the GUI.
- **Don't write to private attributes** unless there's no public setter. The K30 freeze injection writes to `_co2_freeze_active` and `_freeze_end_time_s` because the public surface is read-only — flag this for a future public setter (`sensors.force_freeze(duration_s)`).

### 8.3 Testing

The smoke test pattern used during v1 verification:

```python
import sys
sys.path.insert(0, "source/Part_05_Team_Project")
from martian_greenhouse_sim.gui import GreenhouseSandbox
import tkinter as tk
root = tk.Tk(); root.withdraw()
app = GreenhouseSandbox(root)
for _ in range(400):
    app._step_one()
app._render_text(); app._render_full()
root.destroy()
```

This runs against any `DISPLAY` (real or `xvfb-run`-supplied). A CI smoke test would wrap this and assert no exceptions.

---

## 9. Decision log

| Date | Topic | Decision | Rationale |
|------|-------|----------|-----------|
| 2026-05-22 | GUI framework | tkinter + matplotlib | Stdlib + already-required dep; zero install cost for students |
| 2026-05-22 | Single file vs modules | Single `gui.py` | First-year students can read it end-to-end if curious |
| 2026-05-22 | Rule UX | Form tables, not Python expressions | Safer; maps 1:1 to Python M2 syntax |
| 2026-05-22 | Mode model | Manual / Auto toggle, non-modal | Onboarding feel; switch mid-run is fine |
| 2026-05-22 | Layout | One window with tabbed bottom (Actuators / Rules / Faults) | Keeps visual + sensors + chart always visible |
| 2026-05-22 | Sim integration | Reuse engine via `_step_one()` mirror of `run_simulation` loop body | Single source of truth for physics |
| 2026-05-22 | K30 freeze access | Write through to `_co2_freeze_active` directly | Public setter does not exist yet; flagged for v2 |
| _(open)_ | Persistence | _(see §5.1)_ | _(unanswered)_ |
| _(open)_ | CSV export | _(see §5.2)_ | _(unanswered)_ |
| _(open)_ | Expression mode | _(see §5.3)_ | _(unanswered)_ |
| _(open)_ | Two-run comparison | _(see §5.4)_ | _(unanswered)_ |
| _(open)_ | Tutorial style | _(see §5.5)_ | _(unanswered)_ |
| _(open)_ | Autograder integration | _(see §5.6)_ | _(unanswered)_ |
| _(open)_ | Codespaces story | _(see §5.7)_ | _(unanswered)_ |
| _(open)_ | Dehumidifier actuator | _(see §5.8)_ | _(unanswered)_ |
| _(open)_ | Speed controls | _(see §5.9)_ | _(unanswered)_ |
| _(open)_ | Accessibility bar | _(see §5.10)_ | _(unanswered)_ |
| _(open)_ | M2 session sequence | _(see §7.1)_ | _(unanswered)_ |

---

## 10. References

- v1 ship commit: `430651c` on `kpritche`
- Simulation tuning commit: `1f06e53` on `kpritche` (the `ABSORPTION_EFFICIENCY` / `U_VALUE_W_M2_K` change that made the physics solvable)
- Autograder + sample submission: `source/Part_05_Team_Project/tasks/team_1/a/`
- Original simulation plan: `plans/martian-greenhouse-simulation-plan.md` (git-ignored — local-only)
- Project evaluation: `~/Documents/Obsidian Vault/Purdue/ENGR 131/Design Project Evaluation.md`
- Audit ISA: `~/.claude/PAI/MEMORY/WORK/20260518_engr131-audit/ISA.md`

---
