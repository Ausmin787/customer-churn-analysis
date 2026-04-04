# Bank Customer Churn Analysis — CLAUDE.md

## Project Overview

Portfolio project targeting **banking and finance analytics roles in India**. The goal is to perform EDA, produce publication-quality visualizations, and surface actionable findings on why customers leave a bank.

- **Dataset**: `Churn_Modelling.csv` — 10,000 rows, 14 columns
- **Database**: `churn.db` — SQLite, single table `customers`
- **Target variable**: `Exited` (1 = churned, 0 = stayed), ~20% churn rate

## Database Schema

Table: `customers`

| Column           | Type    | Notes                          |
|------------------|---------|--------------------------------|
| RowNumber        | INTEGER | Index, drop before analysis    |
| CustomerId       | INTEGER | Drop before analysis           |
| Surname          | TEXT    | Drop before analysis           |
| CreditScore      | INTEGER | 350–850                        |
| Geography        | TEXT    | France, Germany, Spain         |
| Gender           | TEXT    | Female, Male                   |
| Age              | INTEGER | 18–92                          |
| Tenure           | INTEGER | Years as customer, 0–10        |
| Balance          | REAL    | Account balance (EUR)          |
| NumOfProducts    | INTEGER | 1–4                            |
| HasCrCard        | INTEGER | Binary flag (0/1)              |
| IsActiveMember   | INTEGER | Binary flag (0/1)              |
| EstimatedSalary  | REAL    | Annual salary estimate (EUR)   |
| Exited           | INTEGER | Target: 1=churned, 0=stayed    |

## Stack

- **Language**: Python 3
- **Data**: `pandas`, `sqlite3`
- **Visualization**: `matplotlib`, `seaborn`
- **DB access**: also available via MCP `sqlite` server (see below)

## MCP Servers

### `sqlite` — query `churn.db` directly
Use the sqlite MCP tools to run exploratory SQL queries before writing Python code. Useful for quick aggregations, sanity checks, and validating findings.

Available tools:
- `mcp__sqlite__read_query` — run SELECT queries
- `mcp__sqlite__describe_table` — inspect schema
- `mcp__sqlite__list_tables` — list all tables
- `mcp__sqlite__write_query` — run INSERT/UPDATE/CREATE (use sparingly)
- `mcp__sqlite__append_insight` — log a key finding

### `context7` — library documentation
Use `mcp__context7__resolve-library-id` + `mcp__context7__query-docs` when you need accurate API references for pandas, matplotlib, seaborn, or sqlite3. Prefer this over guessing at APIs.

## Workflow Convention

1. **Explore with SQL first** — use sqlite MCP tools to validate aggregations quickly
2. **Then implement in Python** — write clean, reproducible `.py` or `.ipynb` scripts
3. **Save all charts** to an `outputs/` directory (create it if needed)
4. **No model building** — this project is EDA and storytelling only; no ML required

## Key Analysis Areas

Focus findings on these angles, which resonate with banking stakeholders in India:

- **Churn rate by Geography** — Germany has significantly higher churn; frame around market risk
- **Age vs Churn** — older customers (40–60) churn more; segment retention implications
- **Active membership effect** — inactive members churn at ~2x the rate of active members
- **Balance distribution** — zero-balance customers and very high-balance customers both churn more
- **NumOfProducts** — customers with 3–4 products have extremely high churn (retention paradox)
- **Gender gap** — female customers churn at a higher rate than male customers
- **Credit score & tenure** — secondary factors; lower scores and shorter tenure correlate with churn

## Visualization Style

- Use `seaborn` for statistical plots; `matplotlib` for custom layouts
- Color scheme: use `Exited` as hue with consistent palette — e.g., `["#2ecc71", "#e74c3c"]` (stayed=green, churned=red)
- Add percentage labels on bar charts for readability
- All charts must have: title, axis labels, legend, and `plt.tight_layout()`
- Target: clean, minimal, portfolio-ready — avoid chart clutter

## Columns to Drop

Always drop before analysis: `RowNumber`, `CustomerId`, `Surname`

## File Naming

- Analysis scripts: `eda_<topic>.py` (e.g., `eda_demographics.py`)
- Notebooks: `churn_analysis.ipynb`
- Output charts: `outputs/<topic>_<chart_type>.png`
