"""
Lesson 2 - NumPy
================
NumPy gives you the "ndarray": a fast, typed array of numbers. pandas DataFrames
are built on top of it, and every ML library speaks NumPy. If pandas is the
spreadsheet, NumPy is the calculator underneath.

Run:  python learn/lesson_02_numpy.py
"""

import numpy as np
import pandas as pd


def section(title: str) -> None:
    print("\n" + "=" * 70)
    print(title)
    print("=" * 70)


# ----------------------------------------------------------------------
section("1. WHY NUMPY - the speed difference")
# A Python list must loop element by element. A NumPy array does the math in
# compiled C, all at once. Compare:
n = 1_000_000
py_list = list(range(n))
np_array = np.arange(n)

import time
t = time.perf_counter()
py_result = [x * 2 for x in py_list]
py_time = time.perf_counter() - t

t = time.perf_counter()
np_result = np_array * 2            # no loop - vectorized
np_time = time.perf_counter() - t

print(f"Python list  : {py_time:.4f} s")
print(f"NumPy array  : {np_time:.4f} s")
print(f"NumPy is about {py_time / np_time:.0f}x faster here.")


# ----------------------------------------------------------------------
section("2. CREATING ARRAYS")
print("From a list:      np.array([1, 2, 3])     ->", np.array([1, 2, 3]))
print("Range:            np.arange(0, 10, 2)     ->", np.arange(0, 10, 2))
print("Evenly spaced:    np.linspace(0, 1, 5)    ->", np.linspace(0, 1, 5))
print("Zeros/ones:       np.zeros(3), np.ones(3) ->", np.zeros(3), np.ones(3))
print("Random:           np.random.default_rng(0).normal(size=3)")

print("\nKey attributes of an array `a`:")
a = np.array([[1, 2, 3], [4, 5, 6]])
print("a            ->\n", a)
print("a.shape      ->", a.shape, "  (2 rows, 3 cols)")
print("a.ndim       ->", a.ndim)
print("a.dtype      ->", a.dtype, " (all elements share one type)")
print("a.size       ->", a.size, " (total elements)")


# ----------------------------------------------------------------------
section("3. VECTORIZED MATH + BROADCASTING")
x = np.array([1, 2, 3, 4])
print("x           ->", x)
print("x + 10      ->", x + 10)
print("x * x       ->", x * x)
print("x ** 2      ->", x ** 2)
print("np.sqrt(x)  ->", np.sqrt(x))

# Broadcasting: a smaller array is "stretched" to fit a larger one.
grid = np.array([[1, 2, 3], [4, 5, 6]])
row = np.array([10, 20, 30])
print("\ngrid + row (row broadcasts across each grid row):")
print(grid + row)


# ----------------------------------------------------------------------
section("4. INDEXING, SLICING, AND MASKS")
y = np.array([5, 10, 15, 20, 25, 30])
print("y[0]        ->", y[0], "  (first; 0-based)")
print("y[-1]       ->", y[-1], " (last)")
print("y[1:4]      ->", y[1:4], " (slicing, end exclusive)")

# Boolean mask: the NumPy version of pandas filtering
mask = y > 15
print("mask        ->", mask)
print("y[mask]     ->", y[mask], " (only the True positions)")
print("y[y % 20 == 0] ->", y[y % 20 == 0])

# Fancy indexing: pick arbitrary positions
print("y[[0, 2, 4]] ->", y[[0, 2, 4]])


# ----------------------------------------------------------------------
section("5. AGGREGATIONS AND THE axis ARGUMENT")
m = np.array([[1, 2, 3], [4, 5, 6]])
print("m ->\n", m)
print("m.sum()            ->", m.sum(), " (everything)")
print("m.sum(axis=0)      ->", m.sum(axis=0), " (down the columns)")
print("m.sum(axis=1)      ->", m.sum(axis=1), " (across the rows)")
print("m.mean(), m.std()  ->", round(m.mean(), 3), round(m.std(), 3))
print("m.min(), m.max()   ->", m.min(), m.max())
print("np.median(m)       ->", np.median(m))


# ----------------------------------------------------------------------
section("6. NUMPY + PANDAS - they work together")
# A pandas Series IS a NumPy array plus an index. You can pull out the raw array:
df = pd.read_csv("data/Chicago_Crimes_2019_2024.csv",
                 usecols=["latitude", "longitude", "year"], low_memory=True)
lat = df["latitude"].to_numpy()          # Series -> ndarray
print("type(df['latitude'])      ->", type(df["latitude"]).__name__)
print("type(df['latitude'].to_numpy()) ->", type(lat).__name__)
print("lat.shape                 ->", lat.shape)

# Drop missing coordinates the NumPy way (no NaNs in coordinate math)
valid = ~np.isnan(lat)          # boolean mask: True where latitude exists
lat_clean = lat[valid]
lon_clean = df["longitude"].to_numpy()[valid]   # keep the same rows
print("Valid latitudes:          ->", lat_clean.size)
print("Mean latitude:            ->", round(lat_clean.mean(), 4))
print("Std dev of latitude:      ->", round(lat_clean.std(), 4))

print("\nRecords per year using numpy.unique (with counts):")
years = df["year"].to_numpy()
values, counts = np.unique(years, return_counts=True)
for v, c in zip(values, counts):
    print(f"  {v}: {c}")


# ----------------------------------------------------------------------
section("7. PRACTICAL EXAMPLE - distance between two points")
# The Haversine formula gives the great-circle distance (km) between two
# lat/long points. You'll reuse this idea when working with spatial data.
def haversine(lat1, lon1, lat2, lon2):
    R = 6371.0  # Earth radius in km
    lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    h = np.sin(dlat / 2) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2) ** 2
    return 2 * R * np.arcsin(np.sqrt(h))

# Distance from downtown Chicago (the Loop) to every record, then average.
loop_lat, loop_lon = 41.8837, -87.6324
distances = haversine(lat_clean, lon_clean, loop_lat, loop_lon)
print("Average distance of incidents from the Loop:",
      round(distances.mean(), 2), "km")
print("Median distance:", round(np.median(distances), 2), "km")


# ----------------------------------------------------------------------
section("YOUR TURN - try these in the file, then rerun")
print("""
1. Create np.arange(1, 21) and select only the even numbers.
2. Print the mean longitude, ignoring missing values.
3. Use np.where to label each incident as 'far' (>15 km from the Loop)
   or 'near', then count how many are near.   (hint: np.where(distances > 15, ...))
4. Reshape np.arange(12) into a 3x4 array and sum each row.
""")
print("Lesson 2 complete.")
