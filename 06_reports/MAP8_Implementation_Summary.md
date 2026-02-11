# MAP-8 Pipeline Execution Summary
Date: 2026-02-10

## 1. Data Preparation and EDA
=== IRI Data Preparation Summary ===
Total respondents: 2322
Respondents per year:
year
2023    1110
2024     971
2025     241

Respondents passing QC: 1322
QC failure rate: 43.07%

Descriptive Statistics (Clean Data):
           FS_mean      PT_mean      EC_mean      PD_mean    IRI_total
count  1322.000000  1322.000000  1322.000000  1322.000000  1322.000000
mean      2.563648     2.878971     2.662308     2.353577     2.614626
std       0.701619     0.570145     0.546781     0.640322     0.504105
min       0.571429     0.571429     0.857143     0.571429     0.642857
25%       2.142857     2.571429     2.285714     2.000000     2.285714
50%       2.571429     2.857143     2.714286     2.285714     2.607143
75%       3.000000     3.285714     3.000000     2.714286     2.928571
max       5.000000     5.000000     5.000000     5.000000     5.000000

## 2. Measurement Reliability (Step 4A)
=== Reliability Analysis (Cronbach's Alpha) ===
FS: 0.617
PT: 0.525
EC: 0.372
PD: 0.599

=== Factor Correlations ===
          FS_mean   PT_mean   EC_mean   PD_mean
FS_mean  1.000000  0.516854  0.580853  0.584836
PT_mean  0.516854  1.000000  0.513036  0.484027
EC_mean  0.580853  0.513036  1.000000  0.687894
PD_mean  0.584836  0.484027  0.687894  1.000000

## 3. Empathy Profiles - Clustering (Step 4C)
Optimal number of clusters (max silhouette): 2
Cluster sizes:
cluster
1    662
2    641

Cluster Centroids (Means):
          FS_mean   PT_mean   EC_mean   PD_mean
cluster                                        
1        2.700043  3.345490  3.084592  2.359948
2        3.545799  3.861154  3.867172  2.866280

## 4. fsQCA Calibration (Step 4B)
=== fsQCA Calibration Report ===
Thresholds used (5th, 50th, 95th percentiles):
FS_mean: [1.4285714285714286, 2.571428571428572, 3.7142857142857135]
PT_mean: [2.0, 2.857142857142857, 3.857142857142857]
EC_mean: [1.7142857142857142, 2.7142857142857144, 3.4285714285714284]
PD_mean: [1.4285714285714286, 2.2857142857142856, 3.571428571428572]
IRI_total: [1.8214285714285712, 2.607142857142857, 3.4285714285714284]

Calibration complete. Save to 04_qca/df_qca_calibrated.csv

## 5. Directory Structure Created
```
00_raw/          - Original Excel files
01_harmonized/   - Cleaned and combined CSVs
02_eda/          - Descriptive statistics
03_sem/          - Reliability and correlations
04_qca/          - Fuzzy set calibration
05_clustering/   - Dendrogram, silhouette, cluster centroids
06_reports/      - This summary report
```

*Execution complete according to MAP8_IRI_pipeline.md guidelines.*
