"""
Finding 6: Active Member vs Inactive Member Churn
Inactive members churn at nearly 2x the rate — and Germany's problem is amplified by inactivity.
"""

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

os.makedirs("outputs", exist_ok=True)

df = pd.read_csv("churn_data.csv")

# fmt: off
ACTIVE_COLOR   = "#2ecc71"
INACTIVE_COLOR = "#e74c3c"
NEUTRAL_COLOR  = "#95a5a6"
# fmt: on

# Overall churn by active status
overall = df.groupby("IsActiveMember")["Exited"].agg(["mean", "count"]).reset_index()
overall["churn_pct"] = overall["mean"] * 100
inactive_rate = overall.loc[overall["IsActiveMember"] == 0, "churn_pct"].values[0]  # ~26.9
active_rate   = overall.loc[overall["IsActiveMember"] == 1, "churn_pct"].values[0]  # ~14.3

# Churn by active status × geography
geo_act = (
    df.groupby(["Geography", "IsActiveMember"])["Exited"]
    .mean()
    .mul(100)
    .reset_index()
)
geo_act.columns = ["Geography", "IsActiveMember", "churn_pct"]

# Balance groups × active status
df["bal_group"] = pd.cut(
    df["Balance"],
    bins=[-1, 0, 75000, 130000, 300000],
    labels=["Zero\nBalance", "Low\n(0-75k)", "Mid\n(75k-130k)", "High\n(130k+)"],
)
bal_act = (
    df.groupby(["bal_group", "IsActiveMember"], observed=True)["Exited"]
    .mean()
    .mul(100)
    .reset_index()
)
bal_act.columns = ["bal_group", "IsActiveMember", "churn_pct"]

fig, axes = plt.subplots(1, 3, figsize=(18, 6))
fig.patch.set_facecolor("white")

for ax in axes:
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.set_facecolor("white")

# Panel 1 — Overall active vs inactive
ax = axes[0]
labels = ["Inactive", "Active"]
values = [inactive_rate, active_rate]
colors = [INACTIVE_COLOR, ACTIVE_COLOR]
bars = ax.bar(labels, values, color=colors, width=0.45, edgecolor="white", linewidth=1.5)
for bar, val in zip(bars, values):
    ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.5,
            f"{val:.1f}%", ha="center", va="bottom", fontsize=13, fontweight="bold", color="#2c3e50")
ax.set_title("Inactive Members Churn\nAt Nearly 2× the Rate", fontsize=13, fontweight="bold", color="#2c3e50")
ax.set_xlabel("Member Activity Status", fontsize=11)
ax.set_ylabel("Churn Rate (%)", fontsize=11)
ax.set_ylim(0, 35)
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"{int(x)}%"))

# Panel 2 — Active status × geography grouped bar
ax = axes[1]
geos = ["France", "Germany", "Spain"]
x = np.arange(len(geos))
width = 0.35
for i, (status, color, label) in enumerate([(0, INACTIVE_COLOR, "Inactive"), (1, ACTIVE_COLOR, "Active")]):
    rates = [
        geo_act.loc[(geo_act["Geography"] == g) & (geo_act["IsActiveMember"] == status), "churn_pct"].values[0]
        for g in geos
    ]
    bars = ax.bar(x + (i - 0.5) * width, rates, width, color=color, edgecolor="white", linewidth=1.5, label=label)
    for bar, val in zip(bars, rates):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.5,
                f"{val:.0f}%", ha="center", va="bottom", fontsize=9, fontweight="bold", color="#2c3e50")
ax.set_title("Germany Inactive Churn (41%)\nIs the Highest Risk Segment", fontsize=13, fontweight="bold", color="#2c3e50")
ax.set_xlabel("Geography", fontsize=11)
ax.set_ylabel("Churn Rate (%)", fontsize=11)
ax.set_xticks(x)
ax.set_xticklabels(geos, fontsize=11)
ax.set_ylim(0, 52)
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"{int(x)}%"))
ax.legend(fontsize=10, frameon=False)

# Panel 3 — Active status × balance group
ax = axes[2]
groups = ["Zero\nBalance", "Low\n(0-75k)", "Mid\n(75k-130k)", "High\n(130k+)"]
x = np.arange(len(groups))
for i, (status, color, label) in enumerate([(0, INACTIVE_COLOR, "Inactive"), (1, ACTIVE_COLOR, "Active")]):
    rates = [
        bal_act.loc[(bal_act["bal_group"] == g) & (bal_act["IsActiveMember"] == status), "churn_pct"].values[0]
        for g in groups
    ]
    bars = ax.bar(x + (i - 0.5) * width, rates, width, color=color, edgecolor="white", linewidth=1.5, label=label)
    for bar, val in zip(bars, rates):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.5,
                f"{val:.0f}%", ha="center", va="bottom", fontsize=9, fontweight="bold", color="#2c3e50")
ax.set_title("Inactivity Drives Churn Regardless\nof Account Balance", fontsize=13, fontweight="bold", color="#2c3e50")
ax.set_xlabel("Account Balance Group", fontsize=11)
ax.set_ylabel("Churn Rate (%)", fontsize=11)
ax.set_xticks(x)
ax.set_xticklabels(groups, fontsize=10)
ax.set_ylim(0, 42)
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"{int(x)}%"))
ax.legend(fontsize=10, frameon=False)

fig.suptitle(
    "Finding 6: Inactivity Is a Universal Churn Signal — Active Members Are Protected Even at High Balances",
    fontsize=14, fontweight="bold", color="#2c3e50", y=1.02,
)
plt.tight_layout()
plt.savefig("outputs/finding6_active_member.png", dpi=150, bbox_inches="tight", facecolor="white")
plt.close()
print("Saved: outputs/finding6_active_member.png")
