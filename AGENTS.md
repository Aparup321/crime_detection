# Crime Hotspot Detection in Major Cities

## Current Scope
- This is an MCA final-year project for crime hotspot detection using data analytics and machine learning.
- The project should be planned so that the core work can realistically be completed by 2 core builders (6 on record, 4 support for report/PPT/testing).
- The first goal is historical crime hotspot analysis. ML-based hotspot prediction is a later stage.
- Focus on one city as a case study — Chicago 2019-2024 is the candidate primary dataset, pending final data-quality verification — with incident-level data.
- Do not scaffold or build application code unless the user explicitly requests it; the repository currently contains planning documents only.

## Approved Architecture
- Keep the web product in TypeScript with Next.js.
- Use Python for data analysis, hotspot detection, and ML.
- A separate FastAPI service is optional and should only be added if necessary.
- Use a simple database only if required by the dashboard. Avoid complex storage and authentication systems.

## Data Rules
- Start from one reliable, versioned crime dataset so the academic work is reproducible.
- The preferred dataset should contain crime type, date/time, city/area, and usable latitude/longitude. It must be incident-level with WGS84 lat/long per row.
- Preserve dataset source, collection date, licence, city coverage, field definitions, and preprocessing version.
- Never present hotspot output as a prediction of individual criminality or as a basis for policing people.
- Results must describe aggregated locations and historical periods, including data-coverage limitations.
- Do not use personally identifying information in the analysis dataset.
- Apply safe aggregation and suppress hotspots with fewer than the configured minimum incidents.

## Implementation Priorities
- Resolve the dataset decision before starting major development.
- Build the reproducible ingestion, cleaning, and validation path before ML or UI work.
- Keep city boundaries, coordinates, timestamps, and crime-category mappings explicit and testable.
- Persist important analysis inputs, parameters, dataset version, and generated results so the analysis can be reproduced.
- Avoid unnecessary application architecture that does not directly support the research work.

## Project Priorities
- Data collection and cleaning
- Exploratory data analysis
- HDBSCAN-based hotspot detection
- Simple grid-based baseline comparison
- One ML model for future hotspot prediction
- Research paper, project report, and PPT (highest priority)
- Interactive map and simple dashboard (secondary, minimal)

## Out of Scope
- Multiple cities unless the selected dataset makes it easy
- Real-time crime data
- Live alerts
- Automated government-data scraping
- Complex authentication and role systems
- MinIO/S3 storage
- Complex asynchronous job systems
- Cross-city crime scoring
- Individual-level risk prediction
- Multiple advanced ML models unless extra time is available

## Ethics and Limitations
- Frame the system as an analysis of reported crime data.
- Do not claim that the system predicts individual criminality.
- Clearly explain missing data, reporting bias, geographic coverage, and other dataset limitations.
- Use aggregated hotspot results in the public dashboard.

## Final Principle
Prioritize dataset quality, data analysis, hotspot detection, ML prediction, results, and the research paper. Extra software architecture should not take priority over the core research work.

## First Build Decision
Before scaffolding, verify Chicago 2019-2024 (data.cityofchicago.org Crimes 2001-Present slice) as the candidate primary dataset, pending final data-quality verification, and confirm that it contains usable crime dates, crime categories, and geographic coordinates. Indian aggregates are rejected for the main pipeline — kept only as viva proof.