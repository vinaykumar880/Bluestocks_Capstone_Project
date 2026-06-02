import requests
import pandas as pd

RAW_DIR = "data/raw"

SCHEMES = {
    125497: "HDFC_Top100_Direct",
    119551: "SBI_Bluechip",
    120503: "ICICI_Bluechip",
    118632: "Nippon_LargeCap",
    119092: "Axis_Bluechip",
    120841: "Kotak_Bluechip",
}

all_records = []

for code, label in SCHEMES.items():
    url = f"https://api.mfapi.in/mf/{code}"
    print(f"Fetching {label}...")
    try:
        resp = requests.get(url, timeout=15)
        data = resp.json()
        meta = data.get("meta", {})
        nav_data = data.get("data", [])
        df = pd.DataFrame(nav_data)
        df["scheme_code"] = code
        df["scheme_label"] = label
        df["scheme_name"] = meta.get("scheme_name", "")
        out = f"{RAW_DIR}/nav_{label}.csv"
        df.to_csv(out, index=False)
        print(f"Saved: {out}  ({len(df)} rows)")
        all_records.append(df)
    except Exception as e:
        print(f"Error: {e}")

combined = pd.concat(all_records, ignore_index=True)
combined.to_csv(f"{RAW_DIR}/live_nav_all.csv", index=False)
print(f"\nDone! Combined file has {len(combined)} rows")