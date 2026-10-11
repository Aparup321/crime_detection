"""
Lesson 1 — pandas
=================
pandas is the workhorse for tabular data. A "DataFrame" is basically a spreadsheet
in code: rows + named columns, with powerful filtering and grouping.

Run:  python learn/lesson_01_pandas.py
"""

import pandas as pd

CSV = "data/Chicago_Crimes_2019_2024.csv"


def section(title: str) -> None:
    """Pretty-print a section header so the output is easy to follow."""
    print("\n" + "=" * 70)
    print(title)
    print("=" * 70)


# ----------------------------------------------------------------------
section("1. LOADING - pandas.read_csv turns a text file into a DataFrame")
# The file is ~1.45M rows; a full read takes only ~3 seconds, so we read it all.
#  - usecols: load ONLY the columns we need (saves time + memory)
#  - for truly huge files, add `chunksize=N` to read in pieces
cols = ["id", "date", "primary_type", "arrest", "district",
        "latitude", "longitude", "year"]
df = pd.read_csv(CSV, usecols=cols, low_memory=True)

print("type(df)      ->", type(df).__name__)
print("df.shape      ->", df.shape, "  (rows, columns)")
print("\nFirst 5 rows (df.head()):")
print(df.head())


# ----------------------------------------------------------------------
section("2. INSPECTING - know your data before you touch it")
print("Column names:  df.columns.tolist()")
print(df.columns.tolist())

print("\nData types:  df.dtypes  <- strings (object) vs numbers (int64/float64)")
print(df.dtypes)

print("\nMissing values per column:  df.isna().sum()")
print(df.isna().sum())

print("\nSummary stats for numeric columns:  df.describe()")
print(df.describe())


# ----------------------------------------------------------------------
section("3. SELECTING - grabbing columns and rows")
# One column -> a Series; two or more -> a DataFrame
print("One column (a Series):  df['primary_type'].head()")
print(df["primary_type"].head().to_string())

print("\nSeveral columns:  df[['primary_type', 'year']].head()")
print(df[["primary_type", "year"]].head().to_string())

# .iloc = by position, .loc = by label
print("\nBy position:  df.iloc[0]  (first row)")
print(df.iloc[0].to_string())
print("\nBy label:  df.loc[0, 'primary_type']  ->", df.loc[0, "primary_type"])


# ----------------------------------------------------------------------
section("4. FILTERING - the single most useful pandas skill")
# A condition on a column returns a True/False ("boolean mask") Series.
mask = df["primary_type"] == "THEFT"
print("mask.head()  ->", mask.head().tolist())
print("thefts in our slice:", mask.sum())

thefts = df[mask]
print("\nTheft rows, first 3:")
print(thefts.head(3).to_string())

# Combine conditions with & (and), | (or). Each needs its own parentheses!
robbery_or_battery = df[(df["primary_type"] == "ROBBERY") |
                        (df["primary_type"] == "BATTERY")]
print("\nROBBERY or BATTERY rows:", len(robbery_or_battery))

# Numeric + string conditions together
arrested_thefts_2023 = df[(df["primary_type"] == "THEFT") &
                          (df["arrest"] == True) &
                          (df["year"] == 2023)]
print("Thefts in 2023 with an arrest:", len(arrested_thefts_2023))

# .isin() is cleaner for "in a list of values"
top3 = df[df["primary_type"].isin(["THEFT", "BATTERY", "ASSAULT"])]
print("Rows in THEFT/BATTERY/ASSAULT:", len(top3))


# ----------------------------------------------------------------------
section("5. value_counts - counting categories (your EDA bread & butter)")
print("Crime category counts:")
print(df["primary_type"].value_counts())

print("\nAs percentages (normalize=True):")
print(df["primary_type"].value_counts(normalize=True).round(4).head())


# ----------------------------------------------------------------------
section("6. GROUPING - split data by a key, compute per group")
# groupby is how you answer "counts per year", "average per district", etc.
print("Incidents per year:  df.groupby('year').size()")
print(df.groupby("year").size())

print("\nMultiple stats at once with .agg():")
by_year = df.groupby("year").agg(
    incidents=("id", "size"),          # count rows
    arrests=("arrest", "sum"),         # sum the True values
)
by_year["arrest_rate"] = (by_year["arrests"] / by_year["incidents"]).round(4)
print(by_year)

print("\nTop crimes per year (group by two keys, then count):")
print(df.groupby(["year", "primary_type"]).size().head(8))


# ----------------------------------------------------------------------
section("7. DATES - turn text into real timestamps, then extract parts")
# The 'date' column is text. pd.to_datetime converts it into datetime objects.
df["date"] = pd.to_datetime(df["date"], errors="coerce")
print("dtype after conversion:", df["date"].dtype)
print("Date range:", df["date"].min(), "to", df["date"].max())

# The .dt accessor pulls out components
print("\nMonth numbers from the first 5 rows:", df["date"].dt.month.head().tolist())
print("Weekdays from the first 5 rows:     ", df["date"].dt.day_name().head().tolist())

# resample = group by time period. 'ME' = month-end.
monthly = df.set_index("date").resample("ME").size()
print("\nMonthly incident counts (first 6 months):")
print(monthly.head(6))
print("\nThat Series is exactly what Fig 1 (the monthly curve) is drawn from.")


# ----------------------------------------------------------------------
section("8. ADDING COLUMNS + SORTING")
# New column from existing data
df["is_violent"] = df["primary_type"].isin(["HOMICIDE", "ROBBERY", "BATTERY", "ASSAULT"])
print("Violent share:", round(df["is_violent"].mean(), 4))

# Sort: nlargest is a shortcut for "top N"
print("\nTop 5 districts by incident count:")
print(df["district"].value_counts().head(5))


# ----------------------------------------------------------------------
section("YOUR TURN - try these in the file, then rerun")
print("""
1. How many rows have a missing latitude?          (hint: df['latitude'].isna().sum())
2. Which district has the highest arrest rate?      (hint: groupby('district')['arrest'].mean())
3. Show only rows where primary_type == 'HOMICIDE'  (hint: boolean mask)
4. Count incidents per weekday name.                (hint: df['date'].dt.day_name().value_counts())
""")
print("Lesson 1 complete.")
