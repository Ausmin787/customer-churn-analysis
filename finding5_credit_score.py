"""
Finding 5: Credit Score Analysis
Does credit score differentiate churners? Does Germany's anomaly persist among high-credit customers?
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns

os.makedirs("outputs", exist_ok=True)

df = pd.read_csv("churn_data.csv")

# fmt: off
STAYED_COLOR  = "#2ecc71"
CHURNED_COLOR = "#e74c3c"
GERMANY_COLOR = "#e74c3c"
NEUTRAL_COLOR = "#95a5a6"
# fmt: on

churned = df[df["Exited"] == 1]["CreditScore"]
stayed  = df[df["Exited"] == 0]["CreditScore"]

mean_churned = churned.mean()  # ~645.4
mean_stayed  = stayed.mean()   # ~651.9

bins   = [0, 580, 670, 740, 800, 900]
labels = ["Poor\n(<580)", "Fair\n(580-669)", "Good\n(670-739)", "Very Good\n(740-799)", "Exceptional\n(800+)"]
df["cs_band"] = pd.cut(df["CreditScore"], bins=bins, labels=labels)

band_churn = df.groupby("cs_band", observed=True)["Exited"].agg(["mean", "count"]).reset_index()
band_churn["churn_pct"] = band_churn["mean"] * 100

geo_hi = (
    df[df["CreditScore"] >= 700]
    .groupby("Geography")["Exited"]
    .agg(["mean", "count"])
    .reset_index()
)
geo_hi["churn_pct"] = geo_hi["mean"] * 100
geo_hi = geo_hi.sort_values("churn_pct", ascending=False)

fig, axes = plt.subplots(1, 3, figsize=(18, 6))
fig.patch.set_facecolor("white")

for ax in axes:
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.set_facecolor("white")

# Panel 1 — KDE overlay
ax = axes[0]
sns.kdeplot(stayed,  fill=True, color=STAYED_COLOR,  alpha=0.45, linewidth=2, label=f"Stayed (avg {mean_stayed:.0f})",  ax=ax)
sns.kdeplot(churned, fill=True, color=CHURNED_COLOR, alpha=0.45, linewidth=2, label=f"Churned (avg {mean_churned:.0f})", ax=ax)
ax.axvline(mean_stayed,  color=STAYED_COLOR,  linestyle="--", linewidth=1.8)
ax.axvline(mean_churned, color=CHURNED_COLOR, linestyle="--", linewidth=1.8)
ymax = ax.get_ylim()[1]
ax.text(mean_stayed  - 8, ymax * 0.82, f"Stayed\n{mean_stayed:.0f}", ha="right",  fontsize=9.5, color=STAYED_COLOR,  fontweight="bold")
ax.text(mean_churned + 8, ymax * 0.82, f"Churned\n{mean_churned:.0f}", ha="left", fontsize=9.5, color=CHURNED_COLOR, fontweight="bold")
ax.set_title("Credit Score Distribution:\nChurned vs Retained", fontsize=13, fontweight="bold", color="#2c3e50")
ax.set_xlabel("Credit Score", fontsize=11)
ax.set_ylabel("Density", fontsize=11)
ax.legend(fontsize=10, frameon=False)

# Panel 2 — Churn rate by band
ax = axes[1]
bar_colors = ["#e74c3c" if v < 20 else "#e74c3c" for v in band_churn["churn_pct"]]
bar_colors = ["#95a5a6"] * len(band_churn)
bars = ax.bar(band_churn["cs_band"].astype(str), band_churn["churn_pct"], color=bar_colors, width=0.6, edgecolor="white", linewidth=1.5)
for bar, rate, n in zip(bars, band_churn["churn_pct"], band_churn["count"]):
    ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.4,
            f"{rate:.1f}%\n(n={n:,})", ha="center", va="bottom", fontsize=9.5, fontweight="bold", color="#2c3e50")
ax.set_title("Churn Rate by Credit Score Band:\nNo Strong Pattern", fontsize=13, fontweight="bold", color="#2c3e50")
ax.set_xlabel("Credit Score Band", fontsize=11)
ax.set_ylabel("Churn Rate (%)", fontsize=11)
ax.set_ylim(0, 30)
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"{int(x)}%"))

# Panel 3 — Germany anomaly persists at high credit score
ax = axes[2]
geo_colors = [GERMANY_COLOR if g == "Germany" else NEUTRAL_COLOR for g in geo_hi["Geography"]]
bars = ax.bar(geo_hi["Geography"], geo_hi["churn_pct"], color=geo_colors, width=0.5, edgecolor="white", linewidth=1.5)
for bar, rate, n in zip(bars, geo_hi["churn_pct"], geo_hi["count"]):
    ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.4,
            f"{rate:.1f}%\n(n={n:,})", ha="center", va="bottom", fontsize=10, fontweight="bold", color="#2c3e50")
ax.set_title("Germany Churn at High Credit Score (700+):\nAnomaly Persists", fontsize=13, fontweight="bold", color="#2c3e50")
ax.set_xlabel("Geography", fontsize=11)
ax.set_ylabel("Churn Rate (%)", fontsize=11)
ax.set_ylim(0, 42)
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"{int(x)}%"))
ger_patch = mpatches.Patch(color=GERMANY_COLOR, label="Germany (elevated)")
oth_patch  = mpatches.Patch(color=NEUTRAL_COLOR, label="France / Spain")
ax.legend(handles=[ger_patch, oth_patch], fontsize=9.5, frameon=False)

fig.suptitle(
    "Finding 5: Credit Score Doesn't Explain Churn — But Germany's Anomaly Is Credit-Score-Agnostic",
    fontsize=14, fontweight="bold", color="#2c3e50", y=1.02,
)
plt.tight_layout()
plt.savefig("outputs/finding5_credit_score.png", dpi=150, bbox_inches="tight", facecolor="white")
plt.close()
print("Saved: outputs/finding5_credit_score.png")
