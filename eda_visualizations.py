"""
Portfolio-ready churn analysis visualizations.
Findings sourced from SQL exploration of churn.db.
"""

import os
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns

# ── Setup ────────────────────────────────────────────────────────────────────
os.makedirs("outputs", exist_ok=True)

conn = sqlite3.connect("churn.db")
df = pd.read_sql("SELECT * FROM customers", conn)
conn.close()

# Drop identifier columns per CLAUDE.md convention
df.drop(columns=["RowNumber", "CustomerId", "Surname"], inplace=True)

# fmt: off
STAYED_COLOR    = "#2ecc71"
CHURNED_COLOR   = "#e74c3c"
HIGHLIGHT_COLOR = "#e74c3c"
NEUTRAL_COLOR   = "#95a5a6"
# fmt: on

def clean_axes(ax):
    """Remove top and right spines, set white background."""
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.set_facecolor("white")


# ── Finding 1 — NumOfProducts U-Curve ────────────────────────────────────────
products_data = {
    "products": [1, 2, 3, 4],
    "churn_rate": [27.71, 7.58, 82.71, 100.0],
    "n": [5084, 4590, 266, 60],
}
prod_df = pd.DataFrame(products_data)

bar_colors = [CHURNED_COLOR if r >= 50 else (STAYED_COLOR if r < 15 else "#f39c12")
              for r in prod_df["churn_rate"]]

fig, ax = plt.subplots(figsize=(10, 6))
fig.patch.set_facecolor("white")

bars = ax.bar(
    prod_df["products"].astype(str),
    prod_df["churn_rate"],
    color=bar_colors,
    width=0.55,
    edgecolor="white",
    linewidth=1.5,
)

# Annotate each bar with churn rate % and sample size
for bar, rate, n in zip(bars, prod_df["churn_rate"], prod_df["n"]):
    ax.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() + 1.5,
        f"{rate:.1f}%\n(n={n:,})",
        ha="center", va="bottom",
        fontsize=12, fontweight="bold", color="#2c3e50",
    )

ax.set_title(
    "Product Overload Drives Churn: The U-Curve Effect",
    fontsize=15, fontweight="bold", pad=16, color="#2c3e50",
)
ax.text(
    0.5, 1.01,
    "Churn bottoms at 7.6% with 2 products, then explodes to 83% and 100% at 3–4 products",
    transform=ax.transAxes, ha="center", va="bottom",
    fontsize=10, color="#7f8c8d",
)
ax.set_xlabel("Number of Products", fontsize=12, labelpad=8)
ax.set_ylabel("Churn Rate (%)", fontsize=12)
ax.set_ylim(0, 115)
ax.set_yticks(range(0, 101, 20))
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"{int(x)}%"))
clean_axes(ax)
plt.tight_layout()
plt.savefig("outputs/finding1.png", dpi=150, bbox_inches="tight", facecolor="white")
plt.close()
print("Saved: outputs/finding1.png")


# ── Finding 2 — Germany Geographic Anomaly ────────────────────────────────────
geo_data = {
    "Geography": ["Germany", "Spain", "France"],
    "churn_rate": [32.44, 16.67, 16.15],
    "n": [2509, 2477, 5014],
}
geo_df = pd.DataFrame(geo_data)

geo_colors = [HIGHLIGHT_COLOR if g == "Germany" else NEUTRAL_COLOR
              for g in geo_df["Geography"]]

fig, ax = plt.subplots(figsize=(10, 6))
fig.patch.set_facecolor("white")

bars = ax.bar(
    geo_df["Geography"],
    geo_df["churn_rate"],
    color=geo_colors,
    width=0.5,
    edgecolor="white",
    linewidth=1.5,
)

for bar, rate, n in zip(bars, geo_df["churn_rate"], geo_df["n"]):
    ax.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() + 0.5,
        f"{rate:.2f}%\n(n={n:,})",
        ha="center", va="bottom",
        fontsize=12, fontweight="bold", color="#2c3e50",
    )

ax.set_title(
    "Germany Churns at 2x the Rate of France and Spain",
    fontsize=15, fontweight="bold", pad=16, color="#2c3e50",
)
ax.text(
    0.5, 1.01,
    "Germany: 32.4%  |  Spain: 16.7%  |  France: 16.2%  — Germany is the primary geographic risk",
    transform=ax.transAxes, ha="center", va="bottom",
    fontsize=10, color="#7f8c8d",
)
ax.set_xlabel("Geography", fontsize=12, labelpad=8)
ax.set_ylabel("Churn Rate (%)", fontsize=12)
ax.set_ylim(0, 42)
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"{int(x)}%"))

# Legend
germany_patch = mpatches.Patch(color=HIGHLIGHT_COLOR, label="Germany (elevated risk)")
other_patch   = mpatches.Patch(color=NEUTRAL_COLOR,   label="Spain / France (baseline)")
ax.legend(handles=[germany_patch, other_patch], fontsize=10, frameon=False, loc="upper right")

clean_axes(ax)
plt.tight_layout()
plt.savefig("outputs/finding2.png", dpi=150, bbox_inches="tight", facecolor="white")
plt.close()
print("Saved: outputs/finding2.png")


# ── Finding 3 — Age Distribution KDE ─────────────────────────────────────────
churned = df[df["Exited"] == 1]["Age"]
stayed  = df[df["Exited"] == 0]["Age"]

mean_churned = churned.mean()   # 44.84
mean_stayed  = stayed.mean()    # 37.41

fig, ax = plt.subplots(figsize=(10, 6))
fig.patch.set_facecolor("white")

sns.kdeplot(stayed,  fill=True, color=STAYED_COLOR,  alpha=0.45,
            linewidth=2, label="Stayed (avg 37.4 yrs)", ax=ax)
sns.kdeplot(churned, fill=True, color=CHURNED_COLOR, alpha=0.45,
            linewidth=2, label="Churned (avg 44.8 yrs)", ax=ax)

# Mean vertical lines
ax.axvline(mean_stayed,  color=STAYED_COLOR,  linestyle="--", linewidth=1.8)
ax.axvline(mean_churned, color=CHURNED_COLOR, linestyle="--", linewidth=1.8)

# Mean labels
ymax = ax.get_ylim()[1]
ax.text(mean_stayed  - 1.2, ymax * 0.82, f"Stayed\nmean: {mean_stayed:.1f}",
        ha="right", fontsize=10, color=STAYED_COLOR, fontweight="bold")
ax.text(mean_churned + 1.2, ymax * 0.82, f"Churned\nmean: {mean_churned:.1f}",
        ha="left",  fontsize=10, color=CHURNED_COLOR, fontweight="bold")

ax.set_title(
    "Churned Customers Are Significantly Older (44.8 vs 37.4 Years)",
    fontsize=15, fontweight="bold", pad=16, color="#2c3e50",
)
ax.text(
    0.5, 1.01,
    "Age gap of 7.4 years — the 40–60 cohort represents the highest churn risk segment",
    transform=ax.transAxes, ha="center", va="bottom",
    fontsize=10, color="#7f8c8d",
)
ax.set_xlabel("Age (years)", fontsize=12, labelpad=8)
ax.set_ylabel("Density", fontsize=12)
ax.legend(fontsize=11, frameon=False, loc="upper right")
clean_axes(ax)
plt.tight_layout()
plt.savefig("outputs/finding3.png", dpi=150, bbox_inches="tight", facecolor="white")
plt.close()
print("Saved: outputs/finding3.png")


# ── Finding 4 — Balance Paradox Grouped Bar ───────────────────────────────────
balance_data = {
    "Group":   ["Stayed", "Churned"],
    "Balance": [72745.30, 91108.54],
    "Color":   [STAYED_COLOR, CHURNED_COLOR],
}
bal_df = pd.DataFrame(balance_data)

fig, ax = plt.subplots(figsize=(10, 6))
fig.patch.set_facecolor("white")

bars = ax.bar(
    bal_df["Group"],
    bal_df["Balance"],
    color=bal_df["Color"],
    width=0.4,
    edgecolor="white",
    linewidth=1.5,
)

for bar, val in zip(bars, bal_df["Balance"]):
    ax.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() + 600,
        f"€{val:,.0f}",
        ha="center", va="bottom",
        fontsize=13, fontweight="bold", color="#2c3e50",
    )

ax.set_title(
    "Higher-Balance Customers Are Leaving: The Retention Paradox",
    fontsize=15, fontweight="bold", pad=16, color="#2c3e50",
)
ax.text(
    0.5, 1.01,
    "Churned customers hold €18,363 more on average — churn is not driven by low balances",
    transform=ax.transAxes, ha="center", va="bottom",
    fontsize=10, color="#7f8c8d",
)
ax.set_xlabel("Customer Status", fontsize=12, labelpad=8)
ax.set_ylabel("Average Account Balance (€)", fontsize=12)
ax.set_ylim(0, 110000)
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"€{int(x):,}"))
clean_axes(ax)
plt.tight_layout()
plt.savefig("outputs/finding4.png", dpi=150, bbox_inches="tight", facecolor="white")
plt.close()
print("Saved: outputs/finding4.png")

print("\nAll 4 charts saved to outputs/")
