"""
Churn Prediction Model: Logistic Regression
Encodes categorical features, trains on 80% holdout, outputs ROC curve + feature coefficients.
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    roc_auc_score,
    roc_curve,
    confusion_matrix,
    ConfusionMatrixDisplay,
)

os.makedirs("outputs", exist_ok=True)

df = pd.read_csv("churn_data.csv")
df.drop(columns=["RowNumber", "CustomerId", "Surname"], inplace=True)

geo_dummies = pd.get_dummies(df["Geography"], prefix="Geo", drop_first=True)
df["Gender_bin"] = (df["Gender"] == "Male").astype(int)
df = pd.concat([df, geo_dummies], axis=1)
df.drop(columns=["Geography", "Gender"], inplace=True)

X = df.drop(columns=["Exited"])
y = df["Exited"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

scaler = StandardScaler()
X_train_sc = scaler.fit_transform(X_train)
X_test_sc  = scaler.transform(X_test)

model = LogisticRegression(class_weight="balanced", max_iter=1000, random_state=42)
model.fit(X_train_sc, y_train)

y_pred      = model.predict(X_test_sc)
y_prob      = model.predict_proba(X_test_sc)[:, 1]
accuracy    = accuracy_score(y_test, y_pred)
precision   = precision_score(y_test, y_pred)
recall      = recall_score(y_test, y_pred)
roc_auc     = roc_auc_score(y_test, y_prob)
fpr, tpr, _ = roc_curve(y_test, y_prob)

print(f"Accuracy:  {accuracy:.3f}")
print(f"Precision: {precision:.3f}")
print(f"Recall:    {recall:.3f}")
print(f"ROC-AUC:   {roc_auc:.3f}")

coef_df = pd.DataFrame({"Feature": X.columns, "Coefficient": model.coef_[0]})
coef_df = coef_df.reindex(coef_df["Coefficient"].abs().sort_values(ascending=True).index)

# fmt: off
POSITIVE_COLOR = "#e74c3c"
NEGATIVE_COLOR = "#2ecc71"
ROC_COLOR      = "#3498db"
# fmt: on

fig, axes = plt.subplots(1, 2, figsize=(16, 7))
fig.patch.set_facecolor("white")

for ax in axes:
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.set_facecolor("white")

# Panel 1 — Feature Coefficients
ax = axes[0]
colors = [POSITIVE_COLOR if c > 0 else NEGATIVE_COLOR for c in coef_df["Coefficient"]]
ax.barh(coef_df["Feature"], coef_df["Coefficient"], color=colors, edgecolor="white", linewidth=1.2)
ax.axvline(0, color="#2c3e50", linewidth=0.9, linestyle="--")
ax.set_title("Logistic Regression — Feature Coefficients\n(Standardized)", fontsize=13, fontweight="bold", color="#2c3e50")
ax.set_xlabel("Coefficient (standardized scale)", fontsize=11)
pos_patch = mpatches.Patch(color=POSITIVE_COLOR, label="Increases churn risk")
neg_patch = mpatches.Patch(color=NEGATIVE_COLOR, label="Reduces churn risk")
ax.legend(handles=[pos_patch, neg_patch], fontsize=10, frameon=False, loc="lower right")

# Panel 2 — ROC Curve
ax = axes[1]
ax.plot(fpr, tpr, color=ROC_COLOR, linewidth=2.5, label=f"ROC-AUC = {roc_auc:.3f}")
ax.plot([0, 1], [0, 1], color="#bdc3c7", linewidth=1.5, linestyle="--", label="Random baseline")
ax.fill_between(fpr, tpr, alpha=0.08, color=ROC_COLOR)
ax.set_title(
    f"ROC Curve — Logistic Regression\nAccuracy: {accuracy:.1%}  |  Recall: {recall:.1%}  |  Precision: {precision:.1%}",
    fontsize=13, fontweight="bold", color="#2c3e50",
)
ax.set_xlabel("False Positive Rate", fontsize=11)
ax.set_ylabel("True Positive Rate", fontsize=11)
ax.set_xlim(0, 1)
ax.set_ylim(0, 1.02)
ax.legend(fontsize=11, frameon=False, loc="lower right")

plt.tight_layout()
plt.savefig("outputs/roc_curve.png", dpi=150, bbox_inches="tight", facecolor="white")
plt.close()
print("Saved: outputs/roc_curve.png")

# Confusion matrix
fig, ax = plt.subplots(figsize=(6, 5))
fig.patch.set_facecolor("white")
ax.set_facecolor("white")
cm = confusion_matrix(y_test, y_pred)
disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=["Stayed", "Churned"])
disp.plot(ax=ax, colorbar=False, cmap="Blues")
ax.set_title("Confusion Matrix", fontsize=13, fontweight="bold", color="#2c3e50")
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
plt.tight_layout()
plt.savefig("outputs/confusion_matrix.png", dpi=150, bbox_inches="tight", facecolor="white")
plt.close()
print("Saved: outputs/confusion_matrix.png")
