"""
Lesson 3 - matplotlib
=====================
matplotlib turns numbers into pictures: the line, bar, histogram, and scatter
charts your paper needs (Fig 1 and Fig 2 in the plan).

Run:  python learn/lesson_03_matplotlib.py

Figures are saved into learn/figures/. Uncomment a plt.show() line to view them
interactively when running locally.
"""

from pathlib import Path

import matplotlib
matplotlib.use("Agg")          # render to files; comment out to use a GUI window
import matplotlib.pyplot as plt
import pandas as pd

FIGDIR = Path("learn/figures")
FIGDIR.mkdir(parents=True, exist_ok=True)

df = pd.read_csv("data/Chicago_Crimes_2019_2024.csv",
                 usecols=["date", "primary_type", "latitude", "longitude"],
                 low_memory=True)
df["date"] = pd.to_datetime(df["date"], errors="coerce")


def section(title: str) -> None:
    print("\n" + "=" * 70)
    print(title)
    print("=" * 70)


# ----------------------------------------------------------------------
section("1. THE MODEL - a Figure contains one or more Axes")
# plt.figure() makes the canvas. An Axes is the actual plotting area.
# Most bugs come from mixing the two APIs. We use the explicit one (fig, ax).
fig, ax = plt.subplots(figsize=(8, 4))
print("fig type ->", type(fig).__name__)
print("ax  type ->", type(ax).__name__)
print("figsize  ->", fig.get_size_inches(), "inches")


# ----------------------------------------------------------------------
section("2. LINE PLOT - monthly incident counts (this is Fig 1)")
monthly = df.set_index("date").resample("ME").size()

fig, ax = plt.subplots(figsize=(10, 4))
ax.plot(monthly.index, monthly.values, color="steelblue", linewidth=1.2)
ax.set_title("Monthly Reported Crimes - Chicago 2019-2024")
ax.set_xlabel("Month")
ax.set_ylabel("Incidents")
ax.grid(True, alpha=0.3)
fig.tight_layout()
out = FIGDIR / "line_monthly.png"
fig.savefig(out, dpi=120)
plt.close(fig)
print("saved ->", out, " (", monthly.min(), "to", monthly.max(), "per month )")


# ----------------------------------------------------------------------
section("3. BAR CHART - top 10 crime categories (this is Fig 2)")
top = df["primary_type"].value_counts().head(10).sort_values()

fig, ax = plt.subplots(figsize=(9, 5))
ax.barh(top.index, top.values, color="indianred")
ax.set_title("Top 10 Crime Categories - Chicago 2019-2024")
ax.set_xlabel("Incidents")
fig.tight_layout()
out = FIGDIR / "bar_categories.png"
fig.savefig(out, dpi=120)
plt.close(fig)
print("saved ->", out)
print(top)


# ----------------------------------------------------------------------
section("4. HISTOGRAM - the distribution of one numeric column")
# A histogram shows how values are spread. Here: incidents per month.
fig, ax = plt.subplots(figsize=(8, 4))
ax.hist(monthly.values, bins=20, color="seagreen", edgecolor="white")
ax.set_title("Distribution of Monthly Incident Counts")
ax.set_xlabel("Incidents per month")
ax.set_ylabel("Number of months")
fig.tight_layout()
out = FIGDIR / "hist_monthly.png"
fig.savefig(out, dpi=120)
plt.close(fig)
print("saved ->", out)


# ----------------------------------------------------------------------
section("5. SCATTER - a quick map view of coordinates")
# Plotting lat vs lon is a cheap way to 'see' spatial structure before maps.
sample = df.dropna(subset=["latitude", "longitude"]).sample(20000, random_state=0)

fig, ax = plt.subplots(figsize=(6, 7))
ax.scatter(sample["longitude"], sample["latitude"],
           s=1, alpha=0.15, color="purple")
ax.set_title("Incident Locations - Chicago (20k sample)")
ax.set_xlabel("Longitude")
ax.set_ylabel("Latitude")
ax.set_aspect("equal")
fig.tight_layout()
out = FIGDIR / "scatter_map.png"
fig.savefig(out, dpi=120)
plt.close(fig)
print("saved ->", out)
print("A real hotspot map (Fig 3) adds colored cluster areas on top of this.")


# ----------------------------------------------------------------------
section("6. MULTIPLE CHARTS IN ONE FIGURE with subplots")
df["year"] = df["date"].dt.year        # derive year from the parsed date
year_counts = df["year"].value_counts().sort_index()

fig, axes = plt.subplots(1, 2, figsize=(12, 4))
axes[0].bar(year_counts.index.astype(str), year_counts.values, color="darkorange")
axes[0].set_title("Incidents per Year")
axes[0].set_ylabel("Incidents")

weekday = df["date"].dt.day_name().value_counts()
order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
weekday = weekday.reindex(order)
axes[1].bar(weekday.index, weekday.values, color="teal")
axes[1].set_title("Incidents by Weekday")
axes[1].tick_params(axis="x", rotation=45)

fig.suptitle("Chicago Crime - Yearly and Weekly Patterns", fontsize=13)
fig.tight_layout()
out = FIGDIR / "subplots_overview.png"
fig.savefig(out, dpi=120)
plt.close(fig)
print("saved ->", out)


# ----------------------------------------------------------------------
section("7. STYLE ESSENTIALS - what every paper figure needs")
print("""
- ax.set_title / set_xlabel / set_ylabel  : always label your axes
- ax.legend()                             : only when >1 series is plotted
- ax.grid(alpha=0.3)                      : subtle guides for reading values
- fig.tight_layout()                      : stops labels overlapping
- fig.savefig(path, dpi=120-300)          : dpi>=300 for print/publication
- plt.close(fig)                          : free memory in long scripts
""")


# ----------------------------------------------------------------------
section("YOUR TURN - try these in the file, then rerun")
print("""
1. Change the line chart color and add markers=('.', markersize=3).
2. Make a histogram of incidents per weekday.
3. Filter df to one year and re-plot the monthly line for that year only.
4. Add a 300-dpi copy of the bar chart for the paper.
""")
print("Lesson 3 complete. Figures are in learn/figures/")
