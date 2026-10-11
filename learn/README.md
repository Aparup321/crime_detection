# Learning Path — Python Libraries for This Project

This folder teaches the exact libraries your crime-hotspot project uses, using your
real Chicago dataset. Run each lesson top to bottom; every section prints an
explanation and its output so you learn by seeing real results.

## The stack, and *why* each one exists

| Library | What it's for | Where it appears in the project |
|---|---|---|
| **pandas** | Loading, cleaning, filtering, grouping tabular data | Phase 1 verification, Phase 2 data pipeline, EDA |
| **NumPy** | Fast math on arrays of numbers (pandas is built on it) | Coordinate math, statistics, feature arrays for ML |
| **matplotlib** | Making charts and maps (static figures) | Fig 1 (monthly curve), Fig 2 (categories), Fig 3/4 maps |
| **scikit-learn** | ML models + metrics | Phase 4 Random Forest, MAE/RMSE |
| **hdbscan** | Density-based clustering | Phase 3 hotspot detection |
| **geopandas** *(optional)* | Spatial data + projections | Phase 3 CRS handling, hotspot polygons |

> Rule of thumb: **pandas** answers "what does my data look like?", **NumPy** answers
> "how do I compute with it fast?", **matplotlib** answers "how do I show it?",
> **scikit-learn** answers "how do I predict with it?".

## Lessons

1. `lesson_01_pandas.py` — load, inspect, select, filter, group, dates, resample
2. `lesson_02_numpy.py` — arrays, vectorized math, broadcasting, stats
3. `lesson_03_matplotlib.py` — line/bar/scatter/hist, labels, saving figures

## How to run

```bash
python learn/lesson_01_pandas.py
```

Each lesson ends with small "Your turn" exercises. Try them by editing the file
before moving on — that's where the learning sticks.

## Status

- pandas, NumPy, matplotlib: **installed**
- scikit-learn, hdbscan: **not yet installed** — we add them when we reach Phase 3/4
