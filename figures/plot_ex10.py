"""Exercise 10: worst worker of the median run of commands A, B, C as stacked bars in figures/ex10.png."""
import csv
from pathlib import Path
from statistics import median_low

import matplotlib.pyplot as plt
from matplotlib.patches import Patch

ROOT = Path(__file__).resolve().parent.parent
RESULTS = ROOT / "results"

INK, MUTED, GRID, SURFACE = "#0b0b0b", "#52514e", "#e4e3df", "#ffffff"

# One colour family per command, one shade per purpose
COLORS = {
    "A": {"comm": "#86b6ef", "comp": "#2a78d6", "join": "#104281"},
    "B": {"comm": "#f5ad8c", "comp": "#eb6834", "join": "#9c3a12"},
    "C": {"comm": "#b3abee", "comp": "#6250d6", "join": "#35298a"},
}
PURPOSE_NAMES = {"comm": "worker communication", "comp": "worker computation", "join": "master join"}

COMMANDS = [("A", "ex10_i7"), ("B", "ex10_xs"), ("C", "ex10_mixed")]


def load(name):
    with open(RESULTS / f"{name}.csv") as f:
        return list(csv.DictReader(f))


def median_run(rows):
    """Rows of the run whose master total is the median (the earliest such run on ties)."""
    totals = {r["run"]: float(r["total_time_s"]) for r in rows if r["role"] == "master"}
    target = median_low(totals.values())
    run = min((run for run, total in totals.items() if total == target), key=int)
    return run, [r for r in rows if r["run"] == run]


plt.rcParams.update({"font.size": 8, "font.family": "DejaVu Sans"})
fig, ax = plt.subplots(figsize=(5.6, 2.6))
ticks = []

for x, (label, name) in enumerate(COMMANDS):
    run, rows = median_run(load(name))
    workers = [r for r in rows if r["role"] == "worker"]
    master = next(r for r in rows if r["role"] == "master")

    # Worst worker: largest communication + computation, which the master has to wait for
    worst = max(workers, key=lambda r: float(r["comm_time_s"]) + float(r["comp_time_s"]))
    comm, comp = float(worst["comm_time_s"]), float(worst["comp_time_s"])
    total = float(master["total_time_s"])
    join = max(total - comm - comp, 0.0)

    bottom = 0.0
    for purpose, value in (("comm", comm), ("comp", comp), ("join", join)):
        ax.bar(x, value, 0.6, bottom=bottom, color=COLORS[label][purpose], edgecolor=SURFACE, linewidth=1)
        bottom += value
    ax.text(x, max(total, bottom) + 0.6, f"total {total:.2f} s", ha="center", va="bottom", color=INK, fontsize=7.5)
    ticks.append(f"{label} (run {run}, rank {worst['rank']})")

ax.set_xticks(range(len(COMMANDS)), ticks)
ax.set_ylabel("time (s)", color=MUTED)
ax.set_ylim(0, 48)
for side in ("top", "right"):
    ax.spines[side].set_visible(False)
for side in ("left", "bottom"):
    ax.spines[side].set_color(MUTED)
ax.tick_params(colors=MUTED)
ax.yaxis.grid(True, color=GRID, linewidth=0.6)
ax.set_axisbelow(True)

handles = [Patch(color=COLORS[c][p], label=f"{c} {PURPOSE_NAMES[p]}") for c, _ in COMMANDS for p in PURPOSE_NAMES]
fig.legend(handles=handles, frameon=False, fontsize=7, loc="center left",
           bbox_to_anchor=(0.66, 0.5), labelcolor=INK)

fig.tight_layout(rect=(0, 0, 0.65, 1))
fig.savefig(ROOT / "figures" / "ex10.png", dpi=220)
