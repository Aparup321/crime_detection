# Crime Hotspot Detection in Major Cities — Plan

## Objective
Deliver an MCA final-year project, "Crime Hotspot Detection in Major Cities," that analyzes reported crime data using Chicago, USA (2019-2024 slice) as the case study — the candidate primary dataset, pending final data-quality verification — identifies historical crime hotspots, and uses one ML model to predict future hotspot activity. The project will also provide a simple interactive dashboard and support a Chicago-specific research paper.

## Confirmed Decisions
- Web application: TypeScript and Next.js.
- Data analysis and ML: Python.
- Database: optional/simple PostgreSQL with Prisma if persistent data is required.
- Initial analysis: historical spatial hotspots.
- Primary clustering method: HDBSCAN.
- Baseline: simple grid-based hotspot detection.
- ML: one suitable prediction model after the hotspot pipeline is working.
- Initial scope: Chicago 2019-2024 (Crimes 2001-Present slice) as candidate primary dataset, pending final data-quality verification; single-city case study.

## Proposed Architecture
- Next.js is the browser-facing application for the dashboard, filters, and map.
- Python handles data cleaning, EDA, spatial analysis, HDBSCAN, feature preparation, and ML.
- A database may be used if required for storing datasets and analysis results.
- Avoid separate services and complex infrastructure unless they solve a real project requirement.
- MapLibre GL JS or Leaflet can be used for the interactive map.

## Data Contract
Use a normalized incident record with at least:
- Source dataset and source-row identifier.
- City and optional administrative area.
- Incident date or timestamp.
- Latitude and longitude in WGS84.
- Normalized crime category and original source category.
- Data-quality status where applicable.

Every selected dataset should record its source URL, licence, retrieval date, geographic coverage, date coverage, field mapping, row count, and preprocessing version.

## Phase 1: Define the Study
- Verify Chicago 2019-2024 candidate (record URL, licence, retrieval date, row count, hash); complete final data-quality verification before locking.
- Check for incident-level coordinates, date/time, crime categories, and sufficient records.
- Check missing values, duplicates, coordinate quality, date range, and crime-category coverage.
- Define the analysis unit, time window, crime categories, and minimum incident threshold.
- Prepare a data dictionary and limitations statement.
- Complete final data-quality verification and lock the dataset before starting major development.

## Phase 2: Establish the Data Pipeline
- Create a versioned dataset and import specification.
- Validate required fields, coordinates, dates, duplicates, and missing values.
- Normalize dates and crime categories.
- Record rejected rows and reasons.
- Create a clean analysis dataset.
- Add basic tests for important data transformations.

## Phase 3: Hotspot Detection
- Use HDBSCAN as the primary hotspot detection method.
- Transform WGS84 coordinates into an appropriate local projected CRS suitable for accurate distance-based clustering in Chicago; select and verify the final CRS before implementation.
- Apply date and crime-category filters when required.
- Remove very small clusters using the minimum incident threshold (min_incidents=10-15).
- Generate aggregated hotspot areas.
- Implement a simple grid-based method as a baseline.
- Compare HDBSCAN vs grid on: number of hotspots, % incidents in hotspots (coverage), and visual map overlap. No extra metrics.

## Phase 4: ML Prediction
- Target (locked for small scope): weekly crime counts per area. No classification unless time permits.
- Create features from historical crime data, such as previous crime counts, time period, crime category, and area/hotspot information.
- One model only: Random Forest is the candidate model (counts) — train 2019-2022, test 2023-2024; confirm the final choice after EDA and feature analysis.
- Baseline (no extra build): historical-average / persistence forecast on same split.
- Use historical data for training and later time periods for testing.
- Predict future weekly counts for defined areas.
- Metrics: MAE/RMSE only.
- Clearly document limitations and avoid individual-level crime prediction claims.

## Phase 5: Build the Web Application
- Create a simple dashboard using Next.js.
- Add city/area, date range, and crime-category filters.
- Display basic crime statistics.
- Display the interactive hotspot map.
- Display ML prediction results.
- Add basic methodology and limitation information.
- Keep the interface simple and responsive.

## Phase 6: Research Paper
Research-paper title (Chicago case study): Density-Based vs Grid-Based Crime Hotspot Detection with Temporal Forecasting: A Reproducible Study on Chicago Open Crime Data (2019–2024).

Research questions (locked, no scope expansion):
- RQ1: How do HDBSCAN hotspots differ from grid-based hotspots for Chicago 2019-2024?
- RQ2: Can historical counts forecast next-week counts per area?
- RQ3: How did hotspots shift from 2019 to 2024?

The research paper should focus on the research problem and findings rather than only the web application.

Suggested structure:
1. Introduction
2. Related Work
3. Research Gap
4. Dataset and Preprocessing
5. Proposed Method
6. Hotspot Detection
7. ML Prediction
8. Results and Discussion
9. Limitations
10. Conclusion and Future Work

Keep the experiments manageable:
- HDBSCAN hotspot detection
- Grid-based baseline comparison
- One ML prediction experiment
- Basic evaluation and discussion

Required figures/tables only (reuse analysis outputs, no extra work):
- Fig1 temporal curve (monthly counts 2019-2024)
- Fig2 crime-category bar chart
- Fig3 HDBSCAN hotspot map
- Fig4 grid-baseline hotspot map
- Table1 ML results (baseline vs Random Forest, MAE/RMSE)
- Table2/Fig5 feature importance (top features only)

Reproducibility log (record once, reuse in paper):
- Dataset URL, licence, retrieval date, row count, hash, preprocessing v0.1
- Final projected CRS, HDBSCAN params, min_incidents value, random seed, library versions

## Phase 7: Verify and Present
- Test the complete flow from dataset to dashboard.
- Check that hotspot results can be reproduced from the same dataset and parameters.
- Verify the ML model using unseen time periods.
- Prepare screenshots and demo data.
- Document methodology, data sources, limitations, ethics, and results.
- Prepare the project report, research paper, PPT, and demo instructions.

## Acceptance Criteria
- Dataset is documented and reproducible.
- Data cleaning produces a usable analysis dataset.
- HDBSCAN produces meaningful aggregated hotspots.
- Grid baseline is implemented for comparison.
- ML model produces evaluated predictions on unseen time periods.
- Dashboard displays the analysis clearly.
- Results and limitations are documented in the research paper.

## Timeline & Milestones (Sept-Dec, 2 builders)
- Sept: Data-quality verification of Chicago 2019-24 candidate, Python cleaning + EDA. Dev1: pipeline, Dev2: train/test split.
- Oct: Hotspot detection and spatial analysis. Dev1: HDBSCAN, Dev2: grid baseline + dashboard skeleton. Start paper Sections 3-4 draft (dataset + method).
- Nov: ML prediction and evaluation + dashboard integration. One model only. Draft Results + Limitations in parallel.
- Dec: Research paper polish, report, PPT, final polishing, demo practice, and submission. No new experiments in Dec.

## Risk Register
- Data availability: selected dataset does not contain usable geographic information → Chicago slice is candidate only; verify lat/long and complete data-quality verification before locking.
- Reviewer why-foreign-data: examiner asks why Chicago not India → cite Indian-gap research note (21 primary sources, no incident lat/long) + viva defence.
- Team capacity: 6 on record, 2 active → Dev1 data+hotspots, Dev2 ML+dashboard; other 4 own report/PPT/testing only, zero code dependency.

## Deferred Work
- Multiple cities unless easily supported by the dataset.
- Real-time ingestion and live alerting.
- Automated government-data scraping.
- Complex authentication.
- Complex cloud/object storage.
- Advanced asynchronous processing.
- Individual-level risk prediction.
- Multiple advanced ML models.
- Cross-city crime scoring.

## Final Scope
Dataset
→ Cleaning
→ EDA
→ HDBSCAN Hotspot Detection
→ Grid Baseline
→ One ML Prediction Model
→ Simple Dashboard
→ Research Paper
→ Project Report + PPT