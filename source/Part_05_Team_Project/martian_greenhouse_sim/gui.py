"""Interactive sandbox GUI for the Martian Greenhouse Simulation.

A Milestone 2 onboarding tool. Students drag actuator sliders or configure
if/elif rule tables, watch sensors respond in real time, see plants live
or die in a visual greenhouse, and discover the K30 freeze fault by
triggering it themselves. Bridges the gap between Python M2 control
structures and writing a real PID controller in Milestone 3.

Run locally (NOT in Codespaces — tkinter needs a real display).

The package lives under `source/Part_05_Team_Project/` so the easiest launch
is the convenience script `run_sandbox.py` at that directory:

    cd ~/Documents/github/13100_content
    .venv/bin/python source/Part_05_Team_Project/run_sandbox.py

Equivalently with PYTHONPATH:

    PYTHONPATH=source/Part_05_Team_Project .venv/bin/python -m martian_greenhouse_sim.gui

Pedagogical sequence the GUI enables:
  1. Pause at t=0. Read every label. Look at the controls.
  2. Play at 60x. Watch what happens with everything at zero — plants freeze.
  3. Manually drive the heater. Notice night needs much more heat than day.
  4. Add LED, notice it adds heat too.
  5. Trigger a K30 freeze. Watch the two CO2 sensors diverge.
  6. Trigger a dust storm during a sunny day. Watch solar collapse.
  7. Flip to Auto mode, add a few if/elif rules, watch them drive the actuators.
  8. Try to keep plants alive for 5 sols by hand-tuning rules. Fail. Realise
     you need a real controller. Walk into Milestone 3.
"""

import math
import random
import sys
import tkinter as tk
from dataclasses import dataclass, field
from tkinter import ttk
from typing import Callable, Dict, List, Optional

import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg  # noqa: E402
from matplotlib.figure import Figure  # noqa: E402
from matplotlib.patches import Circle, Polygon, Rectangle  # noqa: E402

from .actuators import VirtualActuators
from .constants import (
    CO2_TOXIC_PPM,
    LETTUCE_CO2_HIGH_PPM,
    LETTUCE_CO2_LOW_PPM,
    LETTUCE_CO2_SETPOINT_PPM,
    LETTUCE_RH_HIGH_PCT,
    LETTUCE_RH_LOW_PCT,
    LETTUCE_TEMP_DAY_C,
    LETTUCE_TEMP_NIGHT_C,
    LETTUCE_VWC_SETPOINT,
    PLANT_DROUGHT_DURATION_S,
    PLANT_LETHAL_HIGH_DURATION_S,
    PLANT_LETHAL_LOW_DURATION_S,
    PLANT_LOW_LIGHT_DURATION_S,
    PLANT_WATERLOG_DURATION_S,
    SOL_SECONDS,
)
from .environment import MarsEnvironment
from .greenhouse import ActuatorState, Greenhouse
from .plants import (
    CAUSE_DROUGHT,
    CAUSE_LIGHT,
    CAUSE_TEMP_HIGH,
    CAUSE_TEMP_LOW,
    CAUSE_WATERLOG,
    PlantCohort,
)
from .sensors import VirtualSensors

# ---------------------------------------------------------------------------
# GUI configuration
# ---------------------------------------------------------------------------

WINDOW_TITLE = "Martian Greenhouse — Sandbox"
WINDOW_W = 1280
WINDOW_H = 820

# Tick scheduling.
TICK_INTERVAL_MS = 16  # ~60 Hz outer scheduler
RENDER_EVERY_N = 4     # redraw matplotlib every 4 ticks (~15 fps)
CHART_HISTORY_S = 6 * SOL_SECONDS  # rolling 6-sol chart window
SIM_DT_S = 60.0        # each sim step is one sim minute (matches engine default)

# Speed presets: sim-minutes advanced per wall second.
SPEED_PRESETS = [("1x", 1), ("10x", 10), ("60x", 60), ("600x", 600)]
DEFAULT_SPEED = 60

# Color palette. Kept small so the file reads well.
COLOR_SKY_NIGHT = "#0a1633"
COLOR_SKY_TWILIGHT = "#d97742"
COLOR_SKY_DAY = "#7eb6e6"
COLOR_GROUND = "#a0522d"
COLOR_GROUND_DARK = "#603218"
COLOR_GREENHOUSE_FRAME = "#e6e6e6"
COLOR_PLANT_HEALTHY = "#3fa84a"
COLOR_PLANT_STRESSED = "#c7b22b"
COLOR_PLANT_DEAD = "#5a3a1a"
COLOR_HEATER_GLOW = "#ff6a3d"
COLOR_LED = "#fff6b0"
COLOR_PUMP_WATER = "#3a7ec7"
COLOR_DUST = "#b87a45"

# Rule-engine vocabulary.
SENSOR_KEYS = [
    "temperature_c",
    "rh_pct",
    "co2_k30_ppm",
    "co2_scd41_ppm",
    "co2_discrepancy",
    "soil_vwc",
    "par_umol",
    "is_daytime",
]
OPERATORS = ["<", "<=", ">", ">=", "=="]
ACTUATOR_KEYS = ["heater", "led", "co2_valve", "pump"]
ACTUATOR_LABELS = {
    "heater": "Heater",
    "led": "LED",
    "co2_valve": "CO2 valve",
    "pump": "Irrigation pump",
}

# ---------------------------------------------------------------------------
# Rule engine
# ---------------------------------------------------------------------------


@dataclass
class Rule:
    """A single if-then rule: when `sensor op value` is true, output `pct`."""

    sensor: str
    op: str
    value: float
    output_pct: float

    def matches(self, readings: Dict[str, float]) -> bool:
        if self.sensor not in readings:
            return False
        v = float(readings[self.sensor])
        try:
            t = float(self.value)
        except (TypeError, ValueError):
            return False
        if self.op == "<":
            return v < t
        if self.op == "<=":
            return v <= t
        if self.op == ">":
            return v > t
        if self.op == ">=":
            return v >= t
        if self.op == "==":
            return abs(v - t) < 0.5
        return False


@dataclass
class RuleSet:
    """Ordered list of rules + a default percentage. First match wins."""

    rules: List[Rule] = field(default_factory=list)
    default_pct: float = 0.0

    def evaluate(self, readings: Dict[str, float]) -> float:
        for r in self.rules:
            if r.matches(readings):
                return float(r.output_pct)
        return float(self.default_pct)


def _starter_rule_sets() -> Dict[str, RuleSet]:
    """Sensible starter rules so Auto mode shows immediate behaviour.

    These are deliberately competent-but-not-perfect — students see what an
    if/elif controller can do and can iterate.
    """
    return {
        "heater": RuleSet(
            rules=[
                Rule("temperature_c", "<", 15.0, 100.0),
                Rule("temperature_c", "<", 20.0, 60.0),
                Rule("temperature_c", "<", 23.0, 30.0),
            ],
            default_pct=0.0,
        ),
        "led": RuleSet(
            rules=[
                Rule("is_daytime", "==", 1.0, 30.0),
            ],
            default_pct=0.0,
        ),
        "co2_valve": RuleSet(
            rules=[
                Rule("co2_scd41_ppm", "<", 800.0, 40.0),
            ],
            default_pct=0.0,
        ),
        "pump": RuleSet(
            rules=[
                Rule("soil_vwc", "<", 0.30, 100.0),
                Rule("soil_vwc", "<", 0.38, 40.0),
            ],
            default_pct=0.0,
        ),
    }


# ---------------------------------------------------------------------------
# Visual greenhouse panel
# ---------------------------------------------------------------------------


class GreenhouseVisual:
    """Renders the Mars landscape, greenhouse, plants, sun, and storm overlay.

    Lives on a single matplotlib Axes. Patches are created once in __init__
    and mutated in update() — no per-frame allocations.
    """

    PLANT_COUNT = 5

    def __init__(self, ax) -> None:
        self.ax = ax
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 7)
        ax.set_aspect("equal")
        ax.set_facecolor(COLOR_SKY_NIGHT)
        ax.set_xticks([])
        ax.set_yticks([])
        for spine in ax.spines.values():
            spine.set_visible(False)

        # Sky as a single rectangle (color updated per frame).
        self.sky = Rectangle((0, 2.0), 10, 5.0, color=COLOR_SKY_NIGHT, zorder=0)
        ax.add_patch(self.sky)

        # Stars (visible at night only).
        rng = random.Random(7)
        self.stars: List[Circle] = []
        for _ in range(35):
            sx = rng.uniform(0.2, 9.8)
            sy = rng.uniform(3.5, 6.8)
            star = Circle((sx, sy), 0.03, color="white", zorder=1, alpha=0.0)
            ax.add_patch(star)
            self.stars.append(star)

        # Ground.
        self.ground = Rectangle((0, 0), 10, 2.0, color=COLOR_GROUND, zorder=2)
        ax.add_patch(self.ground)
        self.ground_shadow = Rectangle(
            (0, 0), 10, 0.4, color=COLOR_GROUND_DARK, zorder=2.1
        )
        ax.add_patch(self.ground_shadow)

        # Sun (position updated per frame).
        self.sun = Circle((1, 1), 0.45, color="#ffe066", zorder=3, alpha=1.0)
        ax.add_patch(self.sun)

        # Greenhouse cylinder (side view as a rounded rectangle).
        gh_x, gh_y, gh_w, gh_h = 3.0, 1.8, 4.0, 2.5
        self.gh_box = (gh_x, gh_y, gh_w, gh_h)
        self.gh_interior = Rectangle(
            (gh_x, gh_y),
            gh_w,
            gh_h,
            color=COLOR_PLANT_HEALTHY,
            alpha=0.18,
            zorder=4,
        )
        ax.add_patch(self.gh_interior)
        self.gh_frame = Rectangle(
            (gh_x, gh_y),
            gh_w,
            gh_h,
            fill=False,
            edgecolor=COLOR_GREENHOUSE_FRAME,
            linewidth=3,
            zorder=5,
        )
        ax.add_patch(self.gh_frame)
        # Rounded ends to suggest the cylinder cross-section.
        self.gh_end_l = Circle(
            (gh_x, gh_y + gh_h / 2),
            gh_h / 2,
            fill=False,
            edgecolor=COLOR_GREENHOUSE_FRAME,
            linewidth=2,
            zorder=5,
        )
        self.gh_end_r = Circle(
            (gh_x + gh_w, gh_y + gh_h / 2),
            gh_h / 2,
            fill=False,
            edgecolor=COLOR_GREENHOUSE_FRAME,
            linewidth=2,
            zorder=5,
        )
        ax.add_patch(self.gh_end_l)
        ax.add_patch(self.gh_end_r)

        # Heater glow inside the greenhouse (intensity = heater_pct).
        self.heater_glow = Circle(
            (gh_x + 0.5, gh_y + 0.3),
            0.35,
            color=COLOR_HEATER_GLOW,
            alpha=0.0,
            zorder=4.5,
        )
        ax.add_patch(self.heater_glow)

        # LED bar across the top of the greenhouse interior.
        self.led_bar = Rectangle(
            (gh_x + 0.2, gh_y + gh_h - 0.25),
            gh_w - 0.4,
            0.12,
            color=COLOR_LED,
            alpha=0.0,
            zorder=4.5,
        )
        ax.add_patch(self.led_bar)

        # CO2 badge (visible when valve is open).
        self.co2_badge = Rectangle(
            (gh_x + gh_w - 0.9, gh_y + 0.2),
            0.6,
            0.35,
            color="#666666",
            alpha=0.0,
            zorder=4.5,
        )
        ax.add_patch(self.co2_badge)
        self.co2_text = ax.text(
            gh_x + gh_w - 0.6,
            gh_y + 0.35,
            "CO2",
            color="white",
            fontsize=8,
            ha="center",
            va="center",
            zorder=4.6,
            alpha=0.0,
        )

        # Pump droplet (size = pump_pct).
        self.pump_drop = Polygon(
            self._droplet_points(gh_x + 0.8, gh_y + 0.2, 0.15),
            color=COLOR_PUMP_WATER,
            alpha=0.0,
            zorder=4.5,
        )
        ax.add_patch(self.pump_drop)

        # Plant sprites — 5 plants in a row across the bottom of the greenhouse.
        self.plants: List[Polygon] = []
        margin = 0.3
        slot_w = (gh_w - 2 * margin) / self.PLANT_COUNT
        for i in range(self.PLANT_COUNT):
            cx = gh_x + margin + slot_w * (i + 0.5)
            cy = gh_y + 0.15
            poly = Polygon(
                self._plant_points(cx, cy, scale=1.0),
                color=COLOR_PLANT_HEALTHY,
                zorder=4.7,
            )
            ax.add_patch(poly)
            self.plants.append(poly)

        # Sensor LEDs near the greenhouse (for visual reinforcement).
        self.sensor_label = ax.text(
            gh_x + gh_w + 0.2,
            gh_y + gh_h - 0.3,
            "",
            fontsize=8,
            color="white",
            va="top",
            ha="left",
            zorder=6,
        )

        # Storm overlay (covers everything when active).
        self.storm = Rectangle(
            (0, 0), 10, 7, color=COLOR_DUST, alpha=0.0, zorder=8
        )
        ax.add_patch(self.storm)

        # Status text (sol number, mode).
        self.title = ax.text(
            5, 6.7, "", fontsize=11, color="white",
            ha="center", va="center", zorder=9,
            family="monospace",
        )

    @staticmethod
    def _plant_points(cx: float, cy: float, scale: float) -> List[tuple]:
        """Build a simple leafy plant polygon centred at (cx, cy)."""
        h = 0.55 * scale
        w = 0.30 * scale
        return [
            (cx, cy),
            (cx - w, cy + h * 0.4),
            (cx - w * 0.6, cy + h * 0.7),
            (cx, cy + h),
            (cx + w * 0.6, cy + h * 0.7),
            (cx + w, cy + h * 0.4),
        ]

    @staticmethod
    def _droplet_points(cx: float, cy: float, r: float) -> List[tuple]:
        return [
            (cx, cy - r),
            (cx - r, cy),
            (cx - r * 0.7, cy + r * 0.7),
            (cx, cy + r * 1.4),
            (cx + r * 0.7, cy + r * 0.7),
            (cx + r, cy),
        ]

    @staticmethod
    def _lerp_color(c0: str, c1: str, t: float) -> str:
        """Linear interpolation between two hex colors in 0-1 RGB."""
        t = max(0.0, min(1.0, t))
        r0, g0, b0 = int(c0[1:3], 16), int(c0[3:5], 16), int(c0[5:7], 16)
        r1, g1, b1 = int(c1[1:3], 16), int(c1[3:5], 16), int(c1[5:7], 16)
        r = round(r0 + (r1 - r0) * t)
        g = round(g0 + (g1 - g0) * t)
        b = round(b0 + (b1 - b0) * t)
        return f"#{r:02x}{g:02x}{b:02x}"

    def update(
        self,
        env: MarsEnvironment,
        gh: Greenhouse,
        sensors: VirtualSensors,
        plants: PlantCohort,
        actuators: ActuatorState,
        time_s: float,
        sol_idx: int,
        mode_label: str,
    ) -> None:
        # --- Sky color by sol fraction (0 = midnight) ---
        sf = (time_s % SOL_SECONDS) / SOL_SECONDS  # 0..1
        # Map: midnight (0.0) → dawn (0.25) → noon (0.5) → dusk (0.75) → midnight (1.0)
        if sf < 0.25:
            sky_color = self._lerp_color(COLOR_SKY_NIGHT, COLOR_SKY_TWILIGHT, sf / 0.25)
        elif sf < 0.5:
            sky_color = self._lerp_color(COLOR_SKY_TWILIGHT, COLOR_SKY_DAY, (sf - 0.25) / 0.25)
        elif sf < 0.75:
            sky_color = self._lerp_color(COLOR_SKY_DAY, COLOR_SKY_TWILIGHT, (sf - 0.5) / 0.25)
        else:
            sky_color = self._lerp_color(COLOR_SKY_TWILIGHT, COLOR_SKY_NIGHT, (sf - 0.75) / 0.25)
        self.sky.set_color(sky_color)
        self.ax.set_facecolor(sky_color)

        # Stars only visible at night.
        star_alpha = max(0.0, min(1.0, 1.0 - 4.0 * abs(sf - 0.0))) if sf < 0.25 else (
            max(0.0, min(1.0, 4.0 * (sf - 0.75))) if sf > 0.75 else 0.0
        )
        for star in self.stars:
            star.set_alpha(star_alpha)

        # --- Sun position (only above horizon when daytime) ---
        is_day = env.is_daytime()
        if is_day:
            # Arc from x=0.5 at dawn to x=9.5 at dusk, peak at sf=0.5.
            sun_x = 0.5 + 9.0 * (sf - 0.25) / 0.5
            sun_y = 2.0 + 4.5 * math.sin(math.pi * (sf - 0.25) / 0.5)
            self.sun.center = (sun_x, sun_y)
            self.sun.set_alpha(max(0.2, 1.0 - env.get_tau() / 10.0))
        else:
            self.sun.set_alpha(0.0)

        # --- Storm overlay (semi-transparent dust) ---
        tau = env.get_tau()
        storm_alpha = max(0.0, min(0.55, (tau - 0.5) / 8.0))
        self.storm.set_alpha(storm_alpha)

        # --- Greenhouse interior tint by temperature ---
        t_in = gh.state.temp_c
        # Map t_in: <5 blue, 18-23 green, >35 red.
        if t_in < 18.0:
            tint = self._lerp_color("#3a7ec7", COLOR_PLANT_HEALTHY, max(0.0, (t_in - 5.0) / 13.0))
        elif t_in < 30.0:
            tint = self._lerp_color(COLOR_PLANT_HEALTHY, "#e6a23a", (t_in - 23.0) / 7.0 if t_in > 23 else 0.0)
        else:
            tint = self._lerp_color("#e6a23a", "#c43d3d", min(1.0, (t_in - 30.0) / 10.0))
        self.gh_interior.set_color(tint)
        self.gh_interior.set_alpha(0.22)

        # --- Actuator indicators ---
        self.heater_glow.set_alpha(min(0.85, actuators.heater_frac * 0.85))
        self.heater_glow.radius = 0.35 + 0.4 * actuators.heater_frac
        self.led_bar.set_alpha(min(0.95, actuators.led_frac * 0.95))
        self.co2_badge.set_alpha(min(0.9, actuators.co2_valve_frac))
        self.co2_text.set_alpha(min(1.0, actuators.co2_valve_frac))
        gx, gy, gw, _gh_h = self.gh_box
        pump_r = 0.10 + 0.20 * actuators.pump_frac
        self.pump_drop.set_xy(self._droplet_points(gx + 0.8, gy + 0.25, pump_r))
        self.pump_drop.set_alpha(min(0.95, actuators.pump_frac))

        # --- Plants: scale + color by health, hide if dead-and-shrivelled ---
        alive = plants.alive
        health = max(0.0, min(1.0, plants.health))
        if alive:
            if health > 0.7:
                pcolor = COLOR_PLANT_HEALTHY
            elif health > 0.3:
                pcolor = self._lerp_color(
                    COLOR_PLANT_STRESSED, COLOR_PLANT_HEALTHY, (health - 0.3) / 0.4
                )
            else:
                pcolor = self._lerp_color(
                    COLOR_PLANT_DEAD, COLOR_PLANT_STRESSED, health / 0.3
                )
            scale = 0.4 + 0.6 * health
        else:
            pcolor = COLOR_PLANT_DEAD
            scale = 0.35

        gh_x, gh_y, gh_w, _gh_h = self.gh_box
        margin = 0.3
        slot_w = (gh_w - 2 * margin) / self.PLANT_COUNT
        for i, poly in enumerate(self.plants):
            cx = gh_x + margin + slot_w * (i + 0.5)
            cy = gh_y + 0.15
            poly.set_xy(self._plant_points(cx, cy, scale=scale))
            poly.set_color(pcolor)

        # --- Title text (sol + mode) ---
        sol_frac = (time_s % SOL_SECONDS) / SOL_SECONDS
        self.title.set_text(
            f"Sol {sol_idx + sol_frac:6.2f}    Mode: {mode_label:>6s}    "
            f"T_out {env.get_temperature_c():+6.1f} C    tau {tau:4.2f}"
        )


# ---------------------------------------------------------------------------
# Time-series chart
# ---------------------------------------------------------------------------


class TimeSeriesChart:
    """Four stacked traces with target bands shaded."""

    def __init__(self, fig) -> None:
        gs = fig.add_gridspec(4, 1, hspace=0.4)
        self.ax_t = fig.add_subplot(gs[0])
        self.ax_co2 = fig.add_subplot(gs[1], sharex=self.ax_t)
        self.ax_rh = fig.add_subplot(gs[2], sharex=self.ax_t)
        self.ax_soil = fig.add_subplot(gs[3], sharex=self.ax_t)

        for ax in (self.ax_t, self.ax_co2, self.ax_rh, self.ax_soil):
            ax.grid(alpha=0.3)
            ax.tick_params(labelsize=7)

        # Lines (initially empty).
        (self.line_t,) = self.ax_t.plot([], [], color="#c43d3d", lw=1.5)
        (self.line_co2,) = self.ax_co2.plot([], [], color="#3a7ec7", lw=1.5)
        (self.line_rh,) = self.ax_rh.plot([], [], color="#2ca74a", lw=1.5)
        (self.line_soil,) = self.ax_soil.plot([], [], color="#8b4513", lw=1.5)

        # Target bands.
        self.ax_t.axhspan(LETTUCE_TEMP_NIGHT_C, LETTUCE_TEMP_DAY_C, color="green", alpha=0.10)
        self.ax_co2.axhspan(LETTUCE_CO2_LOW_PPM, LETTUCE_CO2_HIGH_PPM, color="green", alpha=0.10)
        self.ax_rh.axhspan(LETTUCE_RH_LOW_PCT, LETTUCE_RH_HIGH_PCT, color="green", alpha=0.10)
        self.ax_soil.axhspan(0.30, 0.50, color="green", alpha=0.10)

        # Toxic CO2 line.
        self.ax_co2.axhline(CO2_TOXIC_PPM, color="red", lw=1, ls="--", alpha=0.5)

        self.ax_t.set_ylabel("T (°C)", fontsize=8)
        self.ax_co2.set_ylabel("CO2 (ppm)", fontsize=8)
        self.ax_rh.set_ylabel("RH (%)", fontsize=8)
        self.ax_soil.set_ylabel("Soil VWC", fontsize=8)
        self.ax_soil.set_xlabel("Sol", fontsize=8)

        self.ax_t.set_ylim(-5, 45)
        self.ax_co2.set_ylim(0, 1600)
        self.ax_rh.set_ylim(0, 100)
        self.ax_soil.set_ylim(0, 1)

    def update(
        self,
        times_s: List[float],
        temps_c: List[float],
        co2_ppm: List[float],
        rh_pct: List[float],
        soil_vwc: List[float],
    ) -> None:
        if not times_s:
            return
        sols = [t / SOL_SECONDS for t in times_s]
        self.line_t.set_data(sols, temps_c)
        self.line_co2.set_data(sols, co2_ppm)
        self.line_rh.set_data(sols, rh_pct)
        self.line_soil.set_data(sols, soil_vwc)
        x_lo = max(0.0, sols[-1] - CHART_HISTORY_S / SOL_SECONDS)
        x_hi = max(sols[-1], x_lo + 0.5)
        for ax in (self.ax_t, self.ax_co2, self.ax_rh, self.ax_soil):
            ax.set_xlim(x_lo, x_hi)


# ---------------------------------------------------------------------------
# Rule editor — one Frame per actuator, dynamically managed rows
# ---------------------------------------------------------------------------


class RuleRow:
    """One editable row in a rule table: sensor / op / value / output / delete."""

    def __init__(
        self,
        parent: tk.Widget,
        rule: Rule,
        on_change: Callable[[], None],
        on_delete: Callable[["RuleRow"], None],
    ) -> None:
        self.frame = tk.Frame(parent)
        self.rule = rule
        self.on_change = on_change
        self.on_delete = on_delete

        self.sensor_var = tk.StringVar(value=rule.sensor)
        self.op_var = tk.StringVar(value=rule.op)
        self.value_var = tk.StringVar(value=f"{rule.value:g}")
        self.output_var = tk.StringVar(value=f"{rule.output_pct:g}")

        tk.Label(self.frame, text="IF").pack(side="left", padx=2)
        ttk.Combobox(
            self.frame,
            textvariable=self.sensor_var,
            values=SENSOR_KEYS,
            width=18,
            state="readonly",
        ).pack(side="left", padx=2)
        ttk.Combobox(
            self.frame,
            textvariable=self.op_var,
            values=OPERATORS,
            width=4,
            state="readonly",
        ).pack(side="left", padx=2)
        tk.Entry(self.frame, textvariable=self.value_var, width=8).pack(side="left", padx=2)
        tk.Label(self.frame, text="  THEN  output =").pack(side="left", padx=2)
        tk.Entry(self.frame, textvariable=self.output_var, width=6).pack(side="left", padx=2)
        tk.Label(self.frame, text="%").pack(side="left")
        tk.Button(self.frame, text="X", width=2, command=self._delete).pack(
            side="left", padx=6
        )

        for var in (self.sensor_var, self.op_var, self.value_var, self.output_var):
            var.trace_add("write", lambda *_: self._sync())

    def _sync(self) -> None:
        self.rule.sensor = self.sensor_var.get()
        self.rule.op = self.op_var.get()
        try:
            self.rule.value = float(self.value_var.get())
        except ValueError:
            pass
        try:
            self.rule.output_pct = float(self.output_var.get())
        except ValueError:
            pass
        self.on_change()

    def _delete(self) -> None:
        self.on_delete(self)


class ActuatorRulePanel:
    """The rules table for a single actuator."""

    def __init__(
        self,
        parent: tk.Widget,
        actuator_key: str,
        rule_set: RuleSet,
    ) -> None:
        self.actuator_key = actuator_key
        self.rule_set = rule_set
        self.rows: List[RuleRow] = []

        outer = tk.LabelFrame(
            parent, text=f"{ACTUATOR_LABELS[actuator_key]} rules", padx=6, pady=4
        )
        outer.pack(fill="x", padx=6, pady=4)
        self.outer = outer

        self.rows_frame = tk.Frame(outer)
        self.rows_frame.pack(fill="x")

        # Footer: default + add.
        footer = tk.Frame(outer)
        footer.pack(fill="x", pady=2)
        tk.Label(footer, text="ELSE output =").pack(side="left")
        self.default_var = tk.StringVar(value=f"{rule_set.default_pct:g}")
        tk.Entry(footer, textvariable=self.default_var, width=6).pack(side="left", padx=2)
        tk.Label(footer, text="%").pack(side="left")
        tk.Button(footer, text="+ Add rule", command=self._add_rule).pack(
            side="right", padx=4
        )
        self.default_var.trace_add("write", lambda *_: self._sync_default())

        for r in rule_set.rules:
            self._add_row_widget(r)

    def _add_row_widget(self, rule: Rule) -> None:
        row = RuleRow(self.rows_frame, rule, on_change=self._noop, on_delete=self._delete_row)
        row.frame.pack(fill="x", pady=1)
        self.rows.append(row)

    def _add_rule(self) -> None:
        new = Rule(sensor="temperature_c", op="<", value=20.0, output_pct=50.0)
        self.rule_set.rules.append(new)
        self._add_row_widget(new)

    def _delete_row(self, row: RuleRow) -> None:
        if row in self.rows:
            self.rows.remove(row)
            try:
                self.rule_set.rules.remove(row.rule)
            except ValueError:
                pass
            row.frame.destroy()

    def _sync_default(self) -> None:
        try:
            self.rule_set.default_pct = float(self.default_var.get())
        except ValueError:
            pass

    def _noop(self) -> None:
        pass


# ---------------------------------------------------------------------------
# Main sandbox application
# ---------------------------------------------------------------------------


class GreenhouseSandbox:
    """Top-level tkinter window holding all panels and the simulation loop."""

    def __init__(self, root: tk.Tk, seed: int = 42) -> None:
        self.root = root
        self.seed = seed
        root.title(WINDOW_TITLE)
        root.geometry(f"{WINDOW_W}x{WINDOW_H}")

        # Simulation state.
        self.rng = random.Random(seed)
        self.env: MarsEnvironment
        self.gh: Greenhouse
        self.sensors: VirtualSensors
        self.actuators: VirtualActuators
        self.plants: PlantCohort
        self.time_s: float
        self.sol_idx: int
        self.actuator_state: ActuatorState  # last applied
        self._init_simulation()

        # UI state.
        self.paused = tk.BooleanVar(value=True)
        self.mode_auto = tk.BooleanVar(value=False)
        self.speed = DEFAULT_SPEED
        self.rule_sets: Dict[str, RuleSet] = _starter_rule_sets()

        # Manual slider values (one DoubleVar per actuator).
        self.manual_vars: Dict[str, tk.DoubleVar] = {
            k: tk.DoubleVar(value=0.0) for k in ACTUATOR_KEYS
        }

        # Chart history.
        self.hist_t: List[float] = []
        self.hist_temp: List[float] = []
        self.hist_co2: List[float] = []
        self.hist_rh: List[float] = []
        self.hist_soil: List[float] = []

        # Render counter.
        self._render_counter = 0
        self._step_accumulator = 0.0  # carries fractional steps between ticks

        # Build the UI.
        self._build_ui()

        # Start the tick loop.
        self.root.after(TICK_INTERVAL_MS, self._tick)

    # ------------------------------------------------------------------ init

    def _init_simulation(self) -> None:
        """(Re)create the simulation state at t=0."""
        self.rng = random.Random(self.seed)
        self.env = MarsEnvironment(initial_time_s=0.0, rng=self.rng)
        # Schedule the canonical dust storm so students can encounter it on long runs.
        self.env.schedule_dust_storm(
            start_time_s=2.0 * SOL_SECONDS,
            duration_s=3.0 * SOL_SECONDS,
        )
        self.gh = Greenhouse(
            initial_temp_c=15.0,
            initial_co2_ppm=900.0,
            initial_rh_pct=50.0,
            initial_soil_vwc=0.40,
        )
        self.sensors = VirtualSensors(self.gh, rng=self.rng)
        self.actuators = VirtualActuators()
        self.plants = PlantCohort()
        self.time_s = 0.0
        self.sol_idx = 0
        self.actuator_state = ActuatorState()
        self.hist_t = []
        self.hist_temp = []
        self.hist_co2 = []
        self.hist_rh = []
        self.hist_soil = []

    # -------------------------------------------------------------------- UI

    def _build_ui(self) -> None:
        # --- Top control bar -------------------------------------------------
        top = tk.Frame(self.root, padx=6, pady=4)
        top.pack(side="top", fill="x")

        tk.Button(top, text="Pause / Play", width=12, command=self._toggle_pause).pack(
            side="left", padx=2
        )
        tk.Button(top, text="Reset", width=8, command=self._reset).pack(side="left", padx=2)

        tk.Label(top, text="   Speed: ").pack(side="left")
        self.speed_var = tk.IntVar(value=DEFAULT_SPEED)
        for label, val in SPEED_PRESETS:
            tk.Radiobutton(
                top, text=label, variable=self.speed_var, value=val, command=self._set_speed
            ).pack(side="left")

        tk.Label(top, text="   Mode: ").pack(side="left")
        tk.Checkbutton(
            top, text="Auto (rules drive actuators)", variable=self.mode_auto
        ).pack(side="left", padx=4)

        self.status_label = tk.Label(top, text="(paused — press Play)", fg="#666")
        self.status_label.pack(side="right", padx=8)

        # --- Middle row: visual | sensors+plants | chart ---------------------
        middle = tk.Frame(self.root)
        middle.pack(side="top", fill="both", expand=True)

        # Visual greenhouse on the left.
        self.fig_vis = Figure(figsize=(5.5, 4.0), dpi=90)
        self.ax_vis = self.fig_vis.add_subplot(111)
        self.fig_vis.subplots_adjust(left=0, right=1, top=1, bottom=0)
        self.visual = GreenhouseVisual(self.ax_vis)
        self.canvas_vis = FigureCanvasTkAgg(self.fig_vis, master=middle)
        self.canvas_vis.draw()
        self.canvas_vis.get_tk_widget().pack(side="left", padx=6, pady=4)

        # Sensor + plant text panel in the middle.
        info = tk.Frame(middle, padx=8, pady=4)
        info.pack(side="left", fill="y")
        self._build_info_panel(info)

        # Chart on the right.
        self.fig_chart = Figure(figsize=(5.0, 4.0), dpi=90)
        self.chart = TimeSeriesChart(self.fig_chart)
        self.canvas_chart = FigureCanvasTkAgg(self.fig_chart, master=middle)
        self.canvas_chart.draw()
        self.canvas_chart.get_tk_widget().pack(side="left", fill="both", expand=True, padx=6, pady=4)

        # --- Bottom tabs: Actuators / Rules / Faults -------------------------
        self.tabs = ttk.Notebook(self.root)
        self.tabs.pack(side="bottom", fill="x", padx=6, pady=4)

        actuator_tab = tk.Frame(self.tabs)
        rules_tab = tk.Frame(self.tabs)
        faults_tab = tk.Frame(self.tabs)
        self.tabs.add(actuator_tab, text="Actuators (Manual)")
        self.tabs.add(rules_tab, text="Rules (Auto)")
        self.tabs.add(faults_tab, text="Faults")

        self._build_actuator_tab(actuator_tab)
        self._build_rules_tab(rules_tab)
        self._build_faults_tab(faults_tab)

    def _build_info_panel(self, parent: tk.Widget) -> None:
        # Sensors block.
        sensors_box = tk.LabelFrame(parent, text="Sensors", padx=6, pady=4)
        sensors_box.pack(fill="x", pady=2)
        self.lbl_dht_t = tk.Label(sensors_box, text="DHT22 T  : --.- °C", anchor="w", width=24, font=("TkFixedFont",))
        self.lbl_dht_rh = tk.Label(sensors_box, text="DHT22 RH : --.- %",  anchor="w", width=24, font=("TkFixedFont",))
        self.lbl_k30 = tk.Label(sensors_box,    text="K30 CO2  : ---- ppm", anchor="w", width=24, font=("TkFixedFont",))
        self.lbl_scd41 = tk.Label(sensors_box,  text="SCD41    : ---- ppm", anchor="w", width=24, font=("TkFixedFont",))
        self.lbl_dco2 = tk.Label(sensors_box,   text="| K30 - SCD41 | = -- ppm", anchor="w", width=24, font=("TkFixedFont",))
        self.lbl_teros = tk.Label(sensors_box,  text="TEROS12  : 0.-- VWC", anchor="w", width=24, font=("TkFixedFont",))
        self.lbl_sq500 = tk.Label(sensors_box,  text="SQ500    : --- umol", anchor="w", width=24, font=("TkFixedFont",))
        for lbl in (
            self.lbl_dht_t, self.lbl_dht_rh, self.lbl_k30, self.lbl_scd41,
            self.lbl_dco2, self.lbl_teros, self.lbl_sq500,
        ):
            lbl.pack(anchor="w")

        # Plant cohort block.
        plant_box = tk.LabelFrame(parent, text="Plant cohort", padx=6, pady=4)
        plant_box.pack(fill="x", pady=4)
        self.lbl_alive = tk.Label(plant_box, text="Status : ALIVE",  anchor="w", font=("TkFixedFont",))
        self.lbl_health = tk.Label(plant_box, text="Health : 1.00",  anchor="w", font=("TkFixedFont",))
        self.lbl_stress_tlow = tk.Label(plant_box, text="cold     :   0 %", anchor="w", font=("TkFixedFont",))
        self.lbl_stress_thigh = tk.Label(plant_box, text="heat     :   0 %", anchor="w", font=("TkFixedFont",))
        self.lbl_stress_drought = tk.Label(plant_box, text="drought  :   0 %", anchor="w", font=("TkFixedFont",))
        self.lbl_stress_water = tk.Label(plant_box, text="waterlog :   0 %", anchor="w", font=("TkFixedFont",))
        self.lbl_stress_light = tk.Label(plant_box, text="low_light:   0 %", anchor="w", font=("TkFixedFont",))
        for lbl in (
            self.lbl_alive, self.lbl_health, self.lbl_stress_tlow, self.lbl_stress_thigh,
            self.lbl_stress_drought, self.lbl_stress_water, self.lbl_stress_light,
        ):
            lbl.pack(anchor="w")

    def _build_actuator_tab(self, parent: tk.Widget) -> None:
        tk.Label(
            parent,
            text="In MANUAL mode, drag the sliders. In AUTO mode, sliders show what the rules are commanding.",
            anchor="w", justify="left",
        ).pack(fill="x", padx=8, pady=4)

        grid = tk.Frame(parent)
        grid.pack(fill="x", padx=10, pady=4)

        self.slider_widgets: Dict[str, tk.Scale] = {}
        for row, key in enumerate(ACTUATOR_KEYS):
            tk.Label(grid, text=ACTUATOR_LABELS[key], width=15, anchor="w").grid(
                row=row, column=0, sticky="w", padx=4, pady=2
            )
            s = tk.Scale(
                grid,
                from_=0,
                to=100,
                orient="horizontal",
                length=420,
                resolution=1,
                variable=self.manual_vars[key],
            )
            s.grid(row=row, column=1, sticky="w")
            self.slider_widgets[key] = s

    def _build_rules_tab(self, parent: tk.Widget) -> None:
        tk.Label(
            parent,
            text="Configure rules per actuator. In AUTO mode, the first matching rule wins; otherwise ELSE fires.",
            anchor="w", justify="left",
        ).pack(fill="x", padx=8, pady=4)

        canvas = tk.Canvas(parent, height=240)
        scrollbar = tk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        scroll_frame = tk.Frame(canvas)
        scroll_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all")),
        )
        canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True, padx=8)
        scrollbar.pack(side="right", fill="y")

        self.rule_panels: Dict[str, ActuatorRulePanel] = {}
        for key in ACTUATOR_KEYS:
            self.rule_panels[key] = ActuatorRulePanel(scroll_frame, key, self.rule_sets[key])

    def _build_faults_tab(self, parent: tk.Widget) -> None:
        tk.Label(
            parent,
            text="Deliberately inject faults to study controller responses without waiting for the schedule.",
            anchor="w", justify="left",
        ).pack(fill="x", padx=8, pady=6)

        btns = tk.Frame(parent)
        btns.pack(fill="x", padx=10, pady=4)
        tk.Button(
            btns,
            text="Inject K30 freeze (5 sim min)",
            width=32,
            command=self._inject_k30_freeze,
        ).pack(side="left", padx=4)
        tk.Button(
            btns,
            text="Trigger dust storm now",
            width=24,
            command=self._trigger_dust_storm,
        ).pack(side="left", padx=4)

        self.fault_status = tk.Label(parent, text="", anchor="w", fg="#666")
        self.fault_status.pack(fill="x", padx=10, pady=4)

    # ------------------------------------------------------------- callbacks

    def _toggle_pause(self) -> None:
        self.paused.set(not self.paused.get())
        self.status_label.config(
            text=("(paused — press Play)" if self.paused.get() else "(running)"),
            fg=("#666" if self.paused.get() else "#2ca74a"),
        )

    def _reset(self) -> None:
        self._init_simulation()
        self.paused.set(True)
        self.status_label.config(text="(reset — press Play)", fg="#666")
        # Force a draw so the visual resets too.
        self._render_full()

    def _set_speed(self) -> None:
        self.speed = self.speed_var.get()

    def _inject_k30_freeze(self) -> None:
        # The freeze state lives on private attributes; the public surface
        # reads them via @property. We write through to the underscore names.
        self.sensors._co2_freeze_active = True
        self.sensors._freeze_end_time_s = self.time_s + 5 * 60.0
        self.fault_status.config(text="K30 freeze active for ~5 sim minutes.")

    def _trigger_dust_storm(self) -> None:
        storm = self.env.schedule_dust_storm(
            start_time_s=self.time_s + 0.05 * SOL_SECONDS,
            duration_s=2.0 * SOL_SECONDS,
            peak_tau=7.0,
        )
        self.fault_status.config(
            text=f"Dust storm scheduled: start sol {storm.start_time_s / SOL_SECONDS:.2f}, "
            f"duration {storm.duration_s / SOL_SECONDS:.1f} sols, tau {storm.peak_tau:.1f}"
        )

    # ----------------------------------------------------------- simulation

    def _readings_for_rules(self) -> Dict[str, float]:
        """Pull current sensor readings into the rule-eval dict."""
        t, rh = self.sensors.read_DHT22()
        k30 = self.sensors.read_K30()
        scd41 = self.sensors.read_SCD41()
        return {
            "temperature_c": t,
            "rh_pct": rh,
            "co2_k30_ppm": k30,
            "co2_scd41_ppm": scd41,
            "co2_discrepancy": abs(k30 - scd41),
            "soil_vwc": self.sensors.read_TEROS12(),
            "par_umol": self.sensors.read_SQ500(),
            "is_daytime": 1.0 if self.env.is_daytime() else 0.0,
        }

    def _commands_from_rules(self, readings: Dict[str, float]) -> Dict[str, float]:
        return {key: self.rule_sets[key].evaluate(readings) for key in ACTUATOR_KEYS}

    def _commands_from_sliders(self) -> Dict[str, float]:
        return {key: float(self.manual_vars[key].get()) for key in ACTUATOR_KEYS}

    def _apply_commands(self, cmds: Dict[str, float]) -> ActuatorState:
        self.actuators.set_heater(cmds["heater"])
        self.actuators.set_LED_lights(cmds["led"])
        self.actuators.inject_CO2(cmds["co2_valve"])
        self.actuators.run_irrigation_pump(cmds["pump"])
        return self.actuators.state

    def _step_one(self) -> None:
        """Advance the simulation by one SIM_DT_S step."""
        # 1. Environment.
        self.env.update(SIM_DT_S)

        # 2. Sensor faults (K30 freeze schedule).
        self.sensors.tick_faults(self.time_s, SIM_DT_S)

        # 3. Compute commands either from rules (Auto) or sliders (Manual).
        readings = self._readings_for_rules()
        if self.mode_auto.get():
            cmds = self._commands_from_rules(readings)
            # Mirror computed values into the slider variables so the user sees them.
            for k, v in cmds.items():
                self.manual_vars[k].set(round(v))
        else:
            cmds = self._commands_from_sliders()

        # 4. Apply commands.
        self.actuator_state = self._apply_commands(cmds)

        # 5. Greenhouse physics.
        self.gh.update_state(self.env, self.actuator_state, SIM_DT_S)

        # 6. Plant update.
        self.plants.update(
            temp_c=self.gh.state.temp_c,
            soil_vwc=self.gh.state.soil_vwc,
            par_umol=self.gh.state.par_umol_m2_s,
            dt_seconds=SIM_DT_S,
            current_time_s=self.time_s + SIM_DT_S,
        )

        # 7. Advance clock + log.
        self.time_s += SIM_DT_S
        if self.time_s >= (self.sol_idx + 1) * SOL_SECONDS:
            self.sol_idx = int(self.time_s // SOL_SECONDS)

        # 8. Append history (decimate so the chart doesn't carry every minute forever).
        if not self.hist_t or self.time_s - self.hist_t[-1] >= 5 * 60.0:
            self.hist_t.append(self.time_s)
            self.hist_temp.append(self.gh.state.temp_c)
            self.hist_co2.append(self.gh.state.co2_ppm)
            self.hist_rh.append(self.gh.state.rh_pct)
            self.hist_soil.append(self.gh.state.soil_vwc)
            # Trim to the rolling window.
            cutoff = self.time_s - CHART_HISTORY_S
            while self.hist_t and self.hist_t[0] < cutoff:
                self.hist_t.pop(0)
                self.hist_temp.pop(0)
                self.hist_co2.pop(0)
                self.hist_rh.pop(0)
                self.hist_soil.pop(0)

    def _tick(self) -> None:
        """Outer scheduler — called every TICK_INTERVAL_MS."""
        try:
            if not self.paused.get():
                # Steps per tick = speed (sim min/wall sec) * (tick interval in sec)
                # = speed * (TICK_INTERVAL_MS / 1000)
                steps_per_tick = self.speed * (TICK_INTERVAL_MS / 1000.0)
                self._step_accumulator += steps_per_tick
                while self._step_accumulator >= 1.0:
                    self._step_one()
                    self._step_accumulator -= 1.0

            # Update the text panel every tick (cheap).
            self._render_text()

            # Update the visual + chart every Nth tick.
            self._render_counter += 1
            if self._render_counter >= RENDER_EVERY_N:
                self._render_counter = 0
                self._render_full()
        finally:
            self.root.after(TICK_INTERVAL_MS, self._tick)

    # ---------------------------------------------------------------- render

    def _render_text(self) -> None:
        t, rh = self.sensors.read_DHT22()
        k30 = self.sensors.read_K30()
        scd41 = self.sensors.read_SCD41()
        teros = self.sensors.read_TEROS12()
        sq500 = self.sensors.read_SQ500()

        self.lbl_dht_t.config(text=f"DHT22 T  : {t:5.1f} C")
        self.lbl_dht_rh.config(text=f"DHT22 RH : {rh:5.1f} %")
        frozen = bool(self.sensors.co2_freeze_active)
        self.lbl_k30.config(
            text=f"K30 CO2  : {k30:6.0f} ppm" + ("  [FROZEN]" if frozen else ""),
            fg=("#c43d3d" if frozen else "black"),
        )
        self.lbl_scd41.config(text=f"SCD41    : {scd41:6.0f} ppm")
        self.lbl_dco2.config(text=f"|K30-SCD41| = {abs(k30 - scd41):4.0f} ppm")
        self.lbl_teros.config(text=f"TEROS12  : {teros:5.2f} VWC")
        self.lbl_sq500.config(text=f"SQ500    : {sq500:5.0f} umol")

        # Plant labels.
        if self.plants.alive:
            color = "#2ca74a" if self.plants.health > 0.7 else "#c7b22b" if self.plants.health > 0.3 else "#c43d3d"
            self.lbl_alive.config(text="Status : ALIVE", fg=color)
        else:
            self.lbl_alive.config(
                text=f"Status : DEAD  ({self.plants.failure_cause})",
                fg="#c43d3d",
            )
        self.lbl_health.config(text=f"Health : {self.plants.health:.2f}")

        # Stress accumulators as % of lethal duration.
        def pct(acc: float, lim: float) -> float:
            return 100.0 * acc / lim if lim > 0 else 0.0

        self.lbl_stress_tlow.config(
            text=f"cold     : {pct(self.plants._temp_low_s, PLANT_LETHAL_LOW_DURATION_S):3.0f} %"
        )
        self.lbl_stress_thigh.config(
            text=f"heat     : {pct(self.plants._temp_high_s, PLANT_LETHAL_HIGH_DURATION_S):3.0f} %"
        )
        self.lbl_stress_drought.config(
            text=f"drought  : {pct(self.plants._drought_s, PLANT_DROUGHT_DURATION_S):3.0f} %"
        )
        self.lbl_stress_water.config(
            text=f"waterlog : {pct(self.plants._waterlog_s, PLANT_WATERLOG_DURATION_S):3.0f} %"
        )
        self.lbl_stress_light.config(
            text=f"low_light: {pct(self.plants._low_light_s, PLANT_LOW_LIGHT_DURATION_S):3.0f} %"
        )

    def _render_full(self) -> None:
        mode_label = "AUTO" if self.mode_auto.get() else "MANUAL"
        self.visual.update(
            env=self.env,
            gh=self.gh,
            sensors=self.sensors,
            plants=self.plants,
            actuators=self.actuator_state,
            time_s=self.time_s,
            sol_idx=self.sol_idx,
            mode_label=mode_label,
        )
        self.canvas_vis.draw_idle()

        self.chart.update(
            self.hist_t, self.hist_temp, self.hist_co2, self.hist_rh, self.hist_soil
        )
        self.canvas_chart.draw_idle()


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------


def main(seed: int = 42) -> None:
    root = tk.Tk()
    GreenhouseSandbox(root, seed=seed)
    root.mainloop()


if __name__ == "__main__":
    seed_arg = 42
    if len(sys.argv) > 1:
        try:
            seed_arg = int(sys.argv[1])
        except ValueError:
            pass
    main(seed=seed_arg)
