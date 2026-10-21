"""Plot Exercise 10 and 11 timings from results/*.csv into figures/results.png."""
import csv
from pathlib import Path
from statistics import mean

import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent.parent
RESULTS = ROOT / "results"

INK, MUTED, GRID = "#0b0b0b", "#52514e", "#e4e3df"
I7, XS = "#2a78d6", "#eb6834"      # node type (panel a)
COMM, COMP = "#1baf7a", "#6250d6"  # time component (panel b)


def load(name):
    with open(RESULTS / f"{name}.csv") as f:
        return list(csv.DictReader(f))


def worker_mean(rows, col, nodes=None):
    return mean(float(r[col]) for r in rows
                if r["role"] == "worker" and (nodes is None or r["node"] in nodes))


def master_mean(rows):
    return mean(float(r["total_time_s"]) for r in rows if r["role"] == "master")


def style(ax):
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    for side in ("left", "bottom"):
        ax.spines[side].set_color(MUTED)
    ax.tick_params(colors=MUTED, labelsize=7.5)
    ax.yaxis.grid(True, color=GRID, linewidth=0.6)
    ax.set_axisbelow(True)


plt.rcParams.update({"font.size": 8, "font.family": "DejaVu Sans"})
fig, (a, b) = plt.subplots(1, 2, figsize=(7.2, 2.4), gridspec_kw={"width_ratios": [1.7, 1]})

# (a) Exercise 10: mean worker computation time per node type, master total as a bar-group line
i7, xs, mixed = load("ex10_i7"), load("ex10_xs"), load("ex10_mixed")
i7_node = {r["node"] for r in i7}
xs_node = {r["node"] for r in xs}
bars = [
    ("i7-7700", worker_mean(i7, "comp_time_s"), I7),
    ("xs-4114", worker_mean(xs, "comp_time_s"), XS),
    ("i7 workers", worker_mean(mixed, "comp_time_s", i7_node), I7),
    ("xs workers", worker_mean(mixed, "comp_time_s", xs_node), XS),
]
x = [0, 1, 2.4, 3.4]
for xi, (label, val, color) in zip(x, bars):
    a.bar(xi, val, width=0.7, color=color, edgecolor="white", linewidth=1)
    a.text(xi, val / 2, f"{val:.1f}", ha="center", va="center", color="white", fontsize=7.5, weight="bold")
for (lo, hi), total in [((-0.4, 0.4), master_mean(i7)), ((0.6, 1.4), master_mean(xs)),
                        ((2.0, 3.8), master_mean(mixed))]:
    a.hlines(total, lo, hi, color=INK, linewidth=1.5)
    a.text(hi, total + 1, f"total {total:.1f}", ha="right", va="bottom", color=INK, fontsize=7)
a.set_xticks(x, [b_[0] for b_ in bars])
a.text(2.9, -9.5, "mixed (cyclic)", ha="center", color=MUTED, fontsize=7.5)
a.set_ylim(0, 50)
a.set_ylabel("seconds", color=MUTED)
a.set_title("(a) Ex 10: worker computation vs master total (2048)", fontsize=8, color=INK, loc="left")
style(a)

# (b) Exercise 11: mean worker communication vs computation time
n5, n9 = load("ex11_n5"), load("ex11_n9")
labels = ["-n5", "-n9 --overcommit"]
comm = [worker_mean(n5, "comm_time_s"), worker_mean(n9, "comm_time_s")]
comp = [worker_mean(n5, "comp_time_s"), worker_mean(n9, "comp_time_s")]
w = 0.35
for i in range(2):
    b.bar(i - w / 2, comm[i], width=w, color=COMM, edgecolor="white", linewidth=1,
          label="communication" if i == 0 else None)
    b.bar(i + w / 2, comp[i], width=w, color=COMP, edgecolor="white", linewidth=1,
          label="computation" if i == 0 else None)
    b.text(i - w / 2, comm[i] + 0.03, f"{comm[i]:.2f}", ha="center", va="bottom", color=INK, fontsize=7)
    b.text(i + w / 2, comp[i] + 0.03, f"{comp[i]:.2f}", ha="center", va="bottom", color=INK, fontsize=7)
    b.text(i, 1.85, f"total {[master_mean(n5), master_mean(n9)][i]:.2f}", ha="center", color=INK, fontsize=7)
b.set_xticks(range(2), labels)
b.set_ylim(0, 2)
b.legend(frameon=False, fontsize=7, loc="center left", bbox_to_anchor=(0, 0.6), labelcolor=INK)
b.set_title("(b) Ex 11: mean worker time (256)", fontsize=8, color=INK, loc="left")
style(b)

fig.tight_layout()
fig.savefig(ROOT / "figures" / "results.png", dpi=220)
