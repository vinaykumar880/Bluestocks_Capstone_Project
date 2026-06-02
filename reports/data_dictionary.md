# Data Dictionary

## dim_fund

| Column | Type | Description |
|----------|----------|----------|
| amfi_code | INTEGER | Unique AMFI scheme code |
| scheme_name | TEXT | Scheme name |
| fund_house | TEXT | AMC name |
| category | TEXT | Equity/Debt |
| sub_category | TEXT | Large Cap, Small Cap etc |
| plan | TEXT | Direct/Regular |
| risk_category | TEXT | Risk classification |

Source:
01_fund_master.csv

---

## fact_nav

| Column | Type | Description |
|----------|----------|----------|
| amfi_code | INTEGER | Fund code |
| date | DATE | NAV date |
| nav | REAL | Daily NAV |

Source:
02_nav_history.csv