-- 1
SELECT fund_house,
SUM(aum_crore)
FROM fact_aum
GROUP BY fund_house
ORDER BY SUM(aum_crore) DESC
LIMIT 5;

-- 2
SELECT
strftime('%Y-%m',date),
AVG(nav)
FROM fact_nav
GROUP BY 1;

-- 3
SELECT *
FROM fact_performance
WHERE expense_ratio_pct < 1;

-- 4
SELECT state,
COUNT(*)
FROM fact_transactions
GROUP BY state
ORDER BY COUNT(*) DESC;

-- 5
SELECT transaction_type,
SUM(amount_inr)
FROM fact_transactions
GROUP BY transaction_type;

-- 6
SELECT risk_category,
COUNT(*)
FROM dim_fund
GROUP BY risk_category;

-- 7
SELECT category,
AVG(return_3yr_pct)
FROM fact_performance
GROUP BY category;

-- 8
SELECT fund_house,
AVG(expense_ratio_pct)
FROM fact_performance
GROUP BY fund_house;

-- 9
SELECT plan,
AVG(return_5yr_pct)
FROM fact_performance
GROUP BY plan;

-- 10
SELECT amfi_code,
MAX(nav)
FROM fact_nav
GROUP BY amfi_code;