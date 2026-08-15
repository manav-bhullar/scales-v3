# Full pipeline A/B — facets vs skip_facets

Run: 2026-07-30T17:50:55.532221+00:00
Pipeline: **locked CERA CQAs** → CGR → CBTE → Aggregator (no teacher review).
n=8 per question · no_nli=False · no_calibrate=True

| Q | MAE facets | MAE skip | ΔMAE | QWK facets | QWK skip | bias facets | bias skip | defers F/S |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| CE04 | 0.5 | 0.25 | -0.250 | 0.346 | 0.562 | -0.438 | -0.188 | 7/7 |
| CE08 | 0.625 | 0.562 | -0.063 | 0.153 | 0.0 | -0.375 | -0.062 | 15/20 |
| CE03 | 0.875 | 0.688 | -0.187 | 0.0 | 0.0 | -0.875 | -0.688 | 2/2 |
| CE07 | 0.344 | 0.25 | -0.094 | 0.8 | 0.848 | -0.344 | -0.250 | 6/7 |
| CE01 | 0.594 | 0.469 | -0.125 | 0.0 | 0.0 | -0.594 | -0.469 | 3/2 |
| CE06 | 0.375 | 0.375 | +0.000 | 0.688 | 0.818 | +0.375 | +0.125 | 2/2 |
| CE10 | 0.672 | 1.047 | +0.375 | 0.567 | 0.412 | -0.247 | -0.622 | 9/8 |

## Pooled (facets, n=56)
- MAE (marks, unnormalized abs err mean): **0.569**
- Mean bias (sys−human marks): **-0.357**
- QWK (normalized 0–1): **0.341**

## Pooled (skip_facets, n=56)
- MAE (marks, unnormalized abs err mean): **0.520**
- Mean bias (sys−human marks): **-0.308**
- QWK (normalized 0–1): **0.485**