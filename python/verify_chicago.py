
import json
import hashlib
from pathlib import Path
from collections import Counter
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent.parent
CSV = ROOT / "data" / "Chicago_Crimes_2019_2024.csv"
OUT_META = ROOT / "data" / "data_meta.json"
OUT_REPORT = ROOT / "verification_report.md"
FIG_MONTHLY = ROOT / "fig_monthly.png"
FIG_CATEGORY = ROOT / "fig_category.png"

SOURCE_URL = "https://data.cityofchicago.org/Public-Safety/Crimes-2001-to-Present/ijzp-q8t2"
LICENCE = "SEE_TERMS_OF_USE (City of Chicago data portal)"
CHUNKSIZE = 200_000
USECOLS = ["id", "case_number", "date", "primary_type", "latitude", "longitude", "year"]

total = 0
missing_rows_total = 0
zero_coord = 0
out_of_bounds = 0
seen_ids = set()
dup_ids = 0
year_counts = Counter()
cat_counts = Counter()
monthly_counts = Counter()
min_date, max_date = None, None

print(f"Reading {CSV} ...", flush=True)
for i, ch in enumerate(pd.read_csv(CSV, usecols=USECOLS, chunksize=CHUNKSIZE, low_memory=True)):
    # normalize
    ch["date"] = pd.to_datetime(ch["date"], errors="coerce")
    lat = pd.to_numeric(ch["latitude"], errors="coerce")
    lon = pd.to_numeric(ch["longitude"], errors="coerce")

    total += len(ch)
    # rows where either lat or lon missing (accumulate across chunks)
    missing_rows = int((lat.isna() | lon.isna()).sum())
    missing_rows_total += missing_rows
    zero_coord += int(((lat == 0) | (lon == 0)).sum())
    valid = lat.notna() & lon.notna()
    oob = int((((lat < 41.6) | (lat > 42.05) | (lon < -88.0) | (lon > -87.5)) & valid).sum())
    out_of_bounds += oob

    for v in ch["id"].astype(str):
        if v in seen_ids:
            dup_ids += 1
        else:
            seen_ids.add(v)

    for y, c in ch["year"].value_counts(dropna=False).items():
        year_counts[str(y)] += int(c)
    for c, n in ch["primary_type"].value_counts(dropna=False).items():
        cat_counts[str(c)] += int(n)
    m = ch["date"].dt.to_period("M").astype(str).value_counts()
    for k, v in m.items():
        monthly_counts[str(k)] += int(v)

    dmin, dmax = ch["date"].min(), ch["date"].max()
    if pd.notna(dmin) and (min_date is None or dmin < min_date):
        min_date = dmin
    if pd.notna(dmax) and (max_date is None or dmax > max_date):
        max_date = dmax
    print(f"  chunk {i}: total={total}", flush=True)

usable_coords = total - missing_rows_total if total else 0
missing_pct = (missing_rows_total / total * 100) if total else 0

# Figures (reuse aggregates only)
months = sorted(monthly_counts)
plt.figure(figsize=(10, 4))
plt.plot(months, [monthly_counts[m] for m in months])
plt.xticks(months[::12], rotation=45, fontsize=7)
plt.title("Chicago crimes — monthly counts (candidate 2019-2024)")
plt.tight_layout()
plt.savefig(FIG_MONTHLY, dpi=150)
plt.close()

top = Counter(cat_counts).most_common(10)
plt.figure(figsize=(8, 4))
plt.barh([t[0] for t in reversed(top)], [t[1] for t in reversed(top)])
plt.title("Top 10 crime categories")
plt.tight_layout()
plt.savefig(FIG_CATEGORY, dpi=150)
plt.close()

meta = {
    "source_url": SOURCE_URL,
    "licence": LICENCE,
    "city_coverage": "Chicago, USA",
    "date_coverage_candidate": "2019-2024",
    "retrieval_note": "Local file data/Chicago_Crimes_2019_2024.csv (pre-downloaded)",
    "row_count": total,
    "year_counts": dict(year_counts),
    "date_min": str(min_date),
    "date_max": str(max_date),
    "missing_latlong_rows": missing_rows_total,
    "missing_latlong_pct": round(missing_pct, 2),
    "duplicate_id_count": dup_ids,
    "out_of_bounds_41.6-42.05_-88.0--87.5": out_of_bounds,
    "preprocessing_version": "v0.1-verify-only",
}
OUT_META.write_text(json.dumps(meta, indent=2), encoding="utf-8")

def verdict(ok):
    return "PASS" if ok else "FAIL"

checks = [
    ("Incident-level rows sufficient (>1M)", total > 1_000_000),
    ("Date range covers 2019-2024", str(min_date)[:4] <= "2019" and str(max_date)[:4] >= "2024"),
    ("Usable lat/long present (>90%)", missing_pct < 10),
    ("Categories present (>=10 types)", len(cat_counts) >= 10),
]
report = ["# Verification Report — Chicago 2019-2024 candidate (Review 2)",
          "",
          f"Source: {SOURCE_URL}",
          f"Licence: {LICENCE}",
          f"File: data/Chicago_Crimes_2019_2024.csv",
          "",
          "## Counts",
          f"- Total rows: {total}",
          f"- Year counts: {dict(sorted(year_counts.items()))}",
          f"- Date min/max: {min_date} / {max_date}",
          f"- Missing lat/long rows: {missing_rows_total} ({missing_pct:.2f}%)",
          f"- Zero coords: {zero_coord}",
          f"- Out-of-bounds (Chicago box): {out_of_bounds}",
          f"- Duplicate id: {dup_ids}",
          f"- Usable coords: {usable_coords}",
          "",
          "## Contract checks (lock gate)",
          *[f"- {name}: {verdict(ok)}" for name, ok in checks],
          "",
          "## Top categories",
          *[f"- {k}: {v}" for k, v in Counter(cat_counts).most_common(10)],
          "",
          "## Figures",
          "- fig_monthly.png — monthly counts 2019-2024",
          "- fig_category.png — top-10 categories",
          "",
          "## Limitations (for paper Sec 9)",
          "- Reported crimes only, 7-day lag/preliminary possible.",
          "- Block-level redaction, not exact address.",
          "- No overtime comparison; single-city case study.",
          "",
          "_Generated by python/verify_chicago.py v0.1-verify-only_",
          ]
OUT_REPORT.write_text("\n".join(report), encoding="utf-8")
print(f"DONE total={total} missing%={missing_pct:.2f} dups={dup_ids}")
print(f"Wrote {OUT_META}, {OUT_REPORT}, {FIG_MONTHLY}, {FIG_CATEGORY}")
