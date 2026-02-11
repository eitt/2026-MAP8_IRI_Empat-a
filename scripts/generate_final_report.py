import os

# Define paths
eda_path = '02_eda/eda_cleaning_report.txt'
sem_path = '03_sem/advanced_sem_detailed_report.txt'
qca_path = '04_qca/qca_report_r.txt'
cluster_path = '05_clustering/cluster_profiles.csv'
output_report = '06_reports/MAP8_Implementation_Summary.md'

def read_file_safe(path):
    if os.path.exists(path):
        with open(path, 'r') as f:
            return f.read()
    return f"File {path} not found."

# Load summaries
eda_sum = read_file_safe(eda_path)
sem_sum = read_file_safe(sem_path)
qca_sum = read_file_safe(qca_path)
cluster_sum = read_file_safe(cluster_path)

# Build Markdown Report
report = f"""# MAP-8 Pipeline Execution Summary
Date: 2026-02-10

## 1. Data Preparation and EDA
{eda_sum}

## 2. Measurement Reliability (Step 4A)
{sem_sum}

## 3. Empathy Profiles - Clustering (Step 4C)
{cluster_sum}

## 4. fsQCA Calibration (Step 4B)
{qca_sum}

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
"""

with open(output_report, 'w') as f:
    f.write(report)

print("Final summary report generated in 06_reports/.")
