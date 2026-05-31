"""
Finding 7: Germany Deep Dive — Age + Product Segments
Germany's churn is elevated across all segments, but the 40-59 cohort and 3+ product holders are extreme outliers.
"""

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

os.makedirs("outputs", exist_ok=True)

df = pd.read_csv("churn_data.csv")

# fmt: off
GERMANY_COLOR = "#e74c3c"
OTHER_COLOR   = "#95a5a6"
# fmt: on

df["age_group"] = pd.cut(
    df["Age"],
    bins=[0, 30, 40, 50, 60, 100],
    labels=["<30", "30-39", "40-49", "50-59", "60+"],
)

ger   = df[df["Geography"] == "Germany"]
other = df[df["Geography"].isin(["France", "Spain"])]

age_ger   = ger.groupby("age_group",   observed=True)["Exited"].mean().mul(100).reset_index()
age_other = other.groupby("age_group", observed=True)["Exited"].mean().mul(100).reset_index()

prod_ger   = ger.groupby("NumOfProducts")["Exited"].agg(["mean", "count"]).reset_index()
prod_other = other.groupby("NumOfProducts")["Exited"].agg(["mean", "count"]).reset_index()
prod_ger["churn_pct"]   = prod_ger["mean"]   * 100
prod_other["churn_pct"] = prod_other["mean"] * 100

active_rates = df.groupby("Geography")["IsActiveMember"].mean().mul(100)

fig, axes = plt.subplots(1, 3, figsize=(18, 6))
fig.patch.set_facecolor("white")

for ax in axes:
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.set_facecolor("white")

# Panel 1 — Churn by age group: Germany vs France+Spain
ax = axes[0]
age_groups = ["<30", "30-39", "40-49", "50-59", "60+"]
x = np.arange(len(age_groups))
width = 0.35

rates_ger   = [age_ger.loc[age_ger["age_group"] == g, "Exited"].values[0] for g in age_groups]
rates_other = [age_other.loc[age_other["age_group"] == g, "Exited"].values[0] for g in age_groups]

bars_ger   = ax.bar(x - width / 2, rates_ger,   width, color=GERMANY_COLOR, edgecolor="white", linewidth=1.5, label="Germany")
bars_other = ax.bar(x + width / 2, rates_other, width, color=OTHER_COLOR,   edgecolor="white", linewidth=1.5, label="France + Spain")

for bar, val in zip(bars_ger, rates_ger):
    ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.8,
            f"{val:.0f}%", ha="center", va="bottom", fontsize=9, fontweight="bold", color="#2c3e50")
for bar, val in zip(bars_other, rates_other):
    ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.8,
            f"{val:.0f}%", ha="center", va="bottom", fontsize=9, fontweight="bold", color="#2c3e50")

ax.set_title("Germany Churn by Age Group:\n40-59 Cohort Most Extreme", fontsize=13, fontweight="bold", color="#2c3e50")
ax.set_xlabel("Age Group", fontsize=11)
ax.set_ylabel("Churn Rate (%)", fontsize=11)
ax.set_xticks(x)
ax.set_xticklabels(age_groups, fontsize=11)
ax.set_ylim(0, 80)
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"{int(x)}%"))
ax.legend(fontsize=10, frameon=False)

# Panel 2 — Churn by product count: Germany vs France+Spain
ax = axes[1]
products = [1, 2, 3, 4]
x = np.arange(len(products))

rates_ger_p = [
    prod_ger.loc[prod_ger["NumOfProducts"] == p, "churn_pct"].values[0] if p in prod_ger["NumOfProducts"].values else 0
    for p in products
]
rates_other_p = [
    prod_other.loc[prod_other["NumOfProducts"] == p, "churn_pct"].values[0] if p in prod_other["NumOfProducts"].values else 0
    for p in products
]

bars_ger_p   = ax.bar(x - width / 2, rates_ger_p,   width, color=GERMANY_COLOR, edgecolor="white", linewidth=1.5, label="Germany")
bars_other_p = ax.bar(x + width / 2, rates_other_p, width, color=OTHER_COLOR,   edgecolor="white", linewidth=1.5, label="France + Spain")

for bar, val in zip(bars_ger_p, rates_ger_p):
    ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.8,
            f"{val:.0f}%", ha="center", va="bottom", fontsize=9, fontweight="bold", color="#2c3e50")
for bar, val in zip(bars_other_p, rates_other_p):
    ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.8,
            f"{val:.0f}%", ha="center", va="bottom", fontsize=9, fontweight="bold", color="#2c3e50")

ax.set_title("Germany Product Churn:\n1-Product Gap Is the Key Differentiator", fontsize=13, fontweight="bold", color="#2c3e50")
ax.set_xlabel("Number of Products", fontsize=11)
ax.set_ylabel("Churn Rate (%)", fontsize=11)
ax.set_xticks(x)
ax.set_xticklabels([str(p) for p in products], fontsize=11)
ax.set_ylim(0, 115)
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"{int(x)}%"))
ax.legend(fontsize=10, frameon=False)

# Panel 3 — Active rate by geography
ax = axes[2]
geos   = ["Germany", "France", "Spain"]
rates  = [active_rates[g] for g in geos]
colors = [GERMANY_COLOR if g == "Germany" else OTHER_COLOR for g in geos]

bars = ax.bar(geos, rates, color=colors, width=0.5, edgecolor="white", linewidth=1.5)
for bar, val in zip(bars, rates):
    ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.4,
            f"{val:.1f}%", ha="center", va="bottom", fontsize=12, fontweight="bold", color="#2c3e50")

ax.set_title("Active Member Rate by Geography:\nGermany Not Less Engaged Overall", fontsize=13, fontweight="bold", color="#2c3e50")
ax.set_xlabel("Geography", fontsize=11)
ax.set_ylabel("Active Member Rate (%)", fontsize=11)
ax.set_ylim(0, 65)
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"{int(x)}%"))

fig.suptitle(
    "Finding 7: Germany's Churn Is Structural — Elevated Across All Segments, Worst in the 40–59 Age Cohort",
    fontsize=14, fontweight="bold", color="#2c3e50", y=1.02,
)
plt.tight_layout()
plt.savefig("outputs/finding7_germany_deepdive.png", dpi=150, bbox_inches="tight", facecolor="white")
plt.close()
print("Saved: outputs/finding7_germany_deepdive.png")
