![CI](https://github.com/Ausmin787/customer-churn-analysis/actions/workflows/ci.yml/badge.svg)

# Bank Customer Churn Analysis

Exploratory data analysis on 10,000 bank customers to identify why customers leave — and what the data says about retention priorities.

---

## Business Context

Customer churn is one of the most direct revenue leaks a retail bank faces. Acquiring a new customer costs 5–7x more than retaining an existing one. For a bank with millions of customers, even a 2–3 percentage point reduction in churn translates to significant bottom-line impact. This project treats churn not as a modeling exercise but as a business problem — the goal is to surface actionable patterns that a product, marketing, or retention team can act on.

---

## Dataset

| Property | Detail |
|---|---|
| Source | [Churn Modelling Dataset](https://www.kaggle.com/datasets/shrutimechlearn/churn-modelling) |
| Rows | 10,000 customers |
| Features | 14 columns (credit score, geography, age, balance, products, activity status, etc.) |
| Target | `Exited` — 1 = churned, 0 = stayed |
| Churn rate | **20.37%** (~1 in 5 customers) |
| Geographies | France, Germany, Spain |

---

## Key Findings

**1. Product overload is a churn accelerant**
Customers with 2 products churn at just 7.6% — the sweet spot. At 3 products, churn jumps to 82.7%. Every single customer with 4 products churned (100%). This points to mis-selling or forced bundling as a retention risk, not a loyalty driver.

**2. Germany is a geographic outlier**
German customers churn at 32.4%, more than double the rate in France (16.2%) and Spain (16.7%). Germany accounts for 25% of the customer base but a disproportionate share of churn. This warrants market-specific investigation — pricing, service quality, or competitive pressure.

**3. Older customers are at higher risk**
Churned customers average 44.8 years old vs. 37.4 years for those who stayed — a 7.4-year gap. The 40–60 age cohort is the highest-risk segment. Retention programs targeting this group (relationship managers, loyalty tiers, proactive outreach) would have outsized impact.

**4. High-balance customers are leaving**
Churned customers hold an average balance of €91,109 vs. €72,745 for retained customers — a €18,364 difference. This is the retention paradox: the bank's most financially valuable customers are also the most likely to leave. The driver isn't financial distress; it's likely service or product dissatisfaction.

---

## Interactive Dashboard

**Live:** https://customer-churn-dashboard-delta.vercel.app

Built with Next.js + Recharts + shadcn/ui. Wired to real customer-level data (10,000 rows, papaparse CSV parsing).

---

## Visualizations

All charts saved to `outputs/`:

| File | Chart |
|---|---|
| `finding1.png` | Churn rate by number of products (U-curve) |
| `finding2.png` | Churn rate by geography — Germany highlighted |
| `finding3.png` | Age distribution KDE — churned vs. stayed |
| `finding4.png` | Average balance — churned vs. stayed |

---

## Tools

| Layer | Tool |
|---|---|
| Language | Python 3 |
| Data manipulation | pandas, sqlite3 |
| Visualization | matplotlib, seaborn |
| Database | SQLite (`churn.db`) |
| AI-assisted analysis | Claude Code with MCP sqlite server |

SQL exploration was done directly via the MCP sqlite server before writing any Python — queries first, code second.

---

## How to Run

**1. Clone the repo and install dependencies**
```bash
git clone <repo-url>
cd customer-churn-analysis
pip install pandas matplotlib seaborn
```

**2. Confirm the database exists**
```bash
ls churn.db   # SQLite database with customers table
```

If missing, recreate it from the CSV:
```python
import pandas as pd, sqlite3
df = pd.read_csv("Churn_Modelling.csv")
df.to_sql("customers", sqlite3.connect("churn.db"), if_exists="replace", index=False)
```

**3. Generate all visualizations**
```bash
python eda_visualizations.py
# Charts saved to outputs/
```

---

## About This Project

Built as a portfolio project for **banking and finance analytics roles in India**. The focus is on translating raw data into business narratives — the kind of analysis a data analyst would present to a retention team, product manager, or C-suite stakeholder. No machine learning; pure EDA and storytelling.

Skills demonstrated: SQL-first exploration, stakeholder-facing visualization, business framing of analytical findings.
