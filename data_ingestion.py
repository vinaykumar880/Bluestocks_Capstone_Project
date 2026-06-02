import os
import glob
import pandas as pd

RAW_DIR = "data/raw"
CSV_FILES = glob.glob(os.path.join(RAW_DIR, "*.csv"))

dataframes = {}
anomalies = []

for path in CSV_FILES:
    name = os.path.splitext(os.path.basename(path))[0]
    df = pd.read_csv(path)
    dataframes[name] = df

    print(f"\n{'='*60}")
    print(f"FILE: {name}")
    print(f"Shape: {df.shape}")
    print(f"Dtypes:\n{df.dtypes}")
    print(f"Head:\n{df.head()}")

    nulls = df.isnull().sum()
    if nulls.any():
        anomalies.append(f"{name}: nulls found -> {nulls[nulls>0].to_dict()}")
    dupes = df.duplicated().sum()
    if dupes:
        anomalies.append(f"{name}: {dupes} duplicate rows")

print("\n\nANOMALY REPORT")
if anomalies:
    for a in anomalies:
        print("WARNING:", a)
else:
    print("No anomalies found!")