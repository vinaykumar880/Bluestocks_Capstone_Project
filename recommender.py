import pandas as pd

risk=input(
"Enter Risk Level:"
)

df=pd.read_csv(
"fund_scorecard.csv"
)

result=df[
df['risk_grade']==risk
]

result=result.sort_values(
'sharpe_ratio',
ascending=False
).head(3)

print(result)