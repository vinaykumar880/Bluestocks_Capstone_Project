import os
import sys
import glob
import pandas as pd

# Fix for Windows encoding issue
sys.stdout.reconfigure(encoding='utf-8')

RAW_DIR = "data/raw"

# Only load original 10 CSVs, skip live NAV files
CSV_FILES = sorted([
    f for f in glob.glob(os.path.join(RAW_DIR, "*.csv"))
    if not os.path.basename(f).startswith("nav_")
    and os.path.basename(f) != "live_nav_all.csv"
])

dataframes = {}
anomalies = []

# ─────────────────────────────────────────────────────────────
# TASK 3 - Load all 10 CSVs, print shape / dtypes / head
# ─────────────────────────────────────────────────────────────
print("=" * 60)
print("TASK 3 - LOADING ALL CSV DATASETS")
print("=" * 60)

for path in CSV_FILES:
    name = os.path.splitext(os.path.basename(path))[0]
    df = pd.read_csv(path)
    dataframes[name] = df

    print(f"\n{'-' * 60}")
    print(f"FILE  : {name}")
    print(f"Shape : {df.shape}")
    print(f"Dtypes:\n{df.dtypes.to_string()}")
    print(f"Head  :\n{df.head(3).to_string()}")

    # Anomaly checks
    nulls = df.isnull().sum()
    if nulls.any():
        anomalies.append(f"{name}: nulls -> {nulls[nulls > 0].to_dict()}")
    dupes = df.duplicated().sum()
    if dupes:
        anomalies.append(f"{name}: {dupes} duplicate rows")

print("\n\nANOMALY REPORT")
print("-" * 40)
if anomalies:
    for a in anomalies:
        print(f"  WARNING: {a}")
else:
    print("  No anomalies found!")

# ─────────────────────────────────────────────────────────────
# TASK 6 - Explore fund_master
# ─────────────────────────────────────────────────────────────
print(f"\n\n{'=' * 60}")
print("TASK 6 - FUND MASTER EXPLORATION")
print("=" * 60)

# Find the fund_master dataframe
fm_key = next((k for k in dataframes if "fund_master" in k.lower()), None)

if fm_key:
    fm = dataframes[fm_key]
    print(f"\n  Using file: {fm_key}  {fm.shape}")

    # Unique fund houses
    print(f"\n  FUND HOUSES ({fm['fund_house'].nunique()} unique):")
    for fh in sorted(fm['fund_house'].unique()):
        count = len(fm[fm['fund_house'] == fh])
        print(f"    - {fh}  ({count} schemes)")

    # Unique categories
    print(f"\n  CATEGORIES ({fm['category'].nunique()} unique):")
    for cat in sorted(fm['category'].unique()):
        print(f"    - {cat}")

    # Sub-categories
    sub_col = next((c for c in fm.columns if 'sub' in c.lower()), None)
    if sub_col:
        print(f"\n  SUB-CATEGORIES ({fm[sub_col].nunique()} unique):")
        for sub in sorted(fm[sub_col].dropna().unique()):
            print(f"    - {sub}")

    # Risk grades
    risk_col = next((c for c in fm.columns if 'risk' in c.lower()), None)
    if risk_col:
        print(f"\n  RISK GRADES:")
        for grade, count in fm[risk_col].value_counts().items():
            print(f"    - {grade}: {count} schemes")

    # AMFI code structure
    code_col = next((c for c in fm.columns if 'amfi' in c.lower() or 'code' in c.lower()), None)
    if code_col:
        codes = fm[code_col].dropna().astype(int)
        print(f"\n  AMFI CODE STRUCTURE:")
        print(f"    Total  : {len(codes)}")
        print(f"    Range  : {codes.min()} to {codes.max()}")
        print(f"    Sample : {codes.head(5).tolist()}")
        print(f"    Note   : 6-digit numbers assigned by AMFI to each scheme uniquely")
else:
    print("  ERROR: fund_master file not found - check filename in data/raw/")

# ─────────────────────────────────────────────────────────────
# TASK 7 - Validate AMFI codes
# ─────────────────────────────────────────────────────────────
print(f"\n\n{'=' * 60}")
print("TASK 7 - AMFI CODE VALIDATION")
print("=" * 60)

nav_key = next((k for k in dataframes if "nav_history" in k.lower()), None)

if fm_key and nav_key:
    fm  = dataframes[fm_key]
    nav = dataframes[nav_key]

    fm_code_col  = next((c for c in fm.columns  if 'amfi' in c.lower() or 'code' in c.lower()), None)
    nav_code_col = next((c for c in nav.columns if 'amfi' in c.lower() or 'code' in c.lower()), None)

    fm_codes  = set(fm[fm_code_col].dropna().astype(int))
    nav_codes = set(nav[nav_code_col].dropna().astype(int))

    matched = fm_codes & nav_codes
    missing = fm_codes - nav_codes
    extra   = nav_codes - fm_codes

    print(f"\n  fund_master codes        : {len(fm_codes)}")
    print(f"  nav_history unique codes : {len(nav_codes)}")
    print(f"  Matched                  : {len(matched)}")
    print(f"  In master, missing in NAV: {len(missing)}")
    if missing:
        print(f"    Codes: {sorted(missing)}")
    print(f"  In NAV, not in master    : {len(extra)}")

    # Save quality report
    os.makedirs("reports", exist_ok=True)
    with open("reports/data_quality_day1.txt", "w", encoding="utf-8") as f:
        f.write("DATA QUALITY SUMMARY - Day 1\n")
        f.write("=" * 40 + "\n\n")
        f.write(f"CSVs loaded           : {len(dataframes)}\n")
        f.write(f"Total anomalies found : {len(anomalies)}\n")
        for a in anomalies:
            f.write(f"  - {a}\n")
        f.write(f"\nAMFI Code Validation\n")
        f.write(f"  fund_master codes   : {len(fm_codes)}\n")
        f.write(f"  nav_history codes   : {len(nav_codes)}\n")
        f.write(f"  Matched             : {len(matched)}\n")
        f.write(f"  Missing from NAV    : {len(missing)}\n")
        if missing:
            f.write(f"  Missing codes       : {sorted(missing)}\n")
        f.write(f"\nConclusion: ")
        if len(missing) == 0:
            f.write("All AMFI codes in fund_master exist in nav_history. Data is consistent.\n")
        else:
            f.write(f"{len(missing)} codes in fund_master have no NAV history. Investigate before analysis.\n")

    print(f"\n  Report saved -> reports/data_quality_day1.txt")
else:
    print("  ERROR: Could not find fund_master or nav_history - check filenames")

print(f"\n\n{'=' * 60}")
print("Day 1 - data_ingestion.py COMPLETE")
print("=" * 60)