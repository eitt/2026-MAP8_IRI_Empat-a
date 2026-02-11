import pandas as pd
import numpy as np
import os
from scipy.stats import chi2

# Create directories
os.makedirs('01_harmonized', exist_ok=True)
os.makedirs('02_eda', exist_ok=True)

# 1. Load Raw Data
df23_raw = pd.read_excel('00_raw/1_2023_data_IRI.xlsx')
df24_raw = pd.read_excel('00_raw/2_2024_data_IRI.xlsx')
df25_raw = pd.read_excel('00_raw/3_2025_data_IRI.xlsx')

df23_raw['year'] = 2023
df24_raw['year'] = 2024
df25_raw['year'] = 2025

# Item indices
fs_idx = [1, 5, 7, 12, 16, 23, 26]
pt_idx = [3, 8, 11, 15, 21, 25, 28]
ec_idx = [2, 4, 9, 14, 18, 20, 22]
pd_idx = [6, 10, 13, 17, 19, 24, 27]

def get_canonical(idx):
    if idx in fs_idx: return f"FS{idx}"
    if idx in pt_idx: return f"PT{idx}"
    if idx in ec_idx: return f"EC{idx}"
    if idx in pd_idx: return f"PD{idx}"
    return None

all_items = [get_canonical(idx) for idx in range(1, 29)]

# 2. Harmonization Logic
# 2023: 0-4 to 1-5 (+1), already reversed
df23 = df23_raw.copy()
for cid in all_items:
    if cid in df23.columns:
        df23[cid] = df23[cid] + 1

# 2024: 1-5, already reversed
df24 = df24_raw.copy()
mapping24 = {f"E{get_canonical(i)}": get_canonical(i) for i in range(1, 29)}
df24 = df24.rename(columns=mapping24)

# 2025: 1-5, reverse FS7 and PD13 ONLY
df25 = df25_raw.copy()
mapping25 = {f"iri_{get_canonical(i)}": get_canonical(i) for i in range(1, 29)}
df25 = df25.rename(columns=mapping25)
df25['FS7'] = 6 - df25['FS7']
df25['PD13'] = 6 - df25['PD13']

# 3. Concatenate
def get_h(df, year):
    map_cols = {
        'ID': 'respondent_id', 'iri_id': 'respondent_id',
        'age': 'age', 'gender': 'gender',
        'economic_level': 'ses', 'socioeconomic_level': 'ses',
        'AC1': 'AC1', 'iri_commitment': 'AC1',
        'AC2': 'AC2', 'iri_ac1_rta5': 'AC2',
        'AC3': 'AC3', 'iri_ac2_rta1': 'AC3'
    }
    df_h = df.rename(columns=map_cols)
    base = ['respondent_id', 'year', 'age', 'gender', 'ses', 'AC1', 'AC2', 'AC3']
    cols = base + all_items
    for c in cols:
        if c not in df_h.columns: df_h[c] = np.nan
    return df_h[cols]

df_all = pd.concat([get_h(df23, 2023), get_h(df24, 2024), get_h(df25, 2025)], ignore_index=True)

# 4. Computed Scores
df_all['FS_mean'] = df_all[[f"FS{i}" for i in fs_idx]].mean(axis=1)
df_all['PT_mean'] = df_all[[f"PT{i}" for i in pt_idx]].mean(axis=1)
df_all['EC_mean'] = df_all[[f"EC{i}" for i in ec_idx]].mean(axis=1)
df_all['PD_mean'] = df_all[[f"PD{i}" for i in pd_idx]].mean(axis=1)
df_all['IRI_total'] = df_all[['FS_mean', 'PT_mean', 'EC_mean', 'PD_mean']].mean(axis=1)

# 5. Case Cleaning (QC + Outliers)
# QC: Attention checks
def calc_qc(row):
    fails = 0
    if pd.notnull(row['AC2']):
        if row['AC2'] != 5: fails += 1
    if pd.notnull(row['AC3']):
        if row['AC3'] != 1: fails += 1
    return fails

df_all['qc_fail_count'] = df_all.apply(calc_qc, axis=1)
df_clean = df_all[df_all['qc_fail_count'] == 0].copy()

# Multivariate Outliers (Random Answers Check)
def get_md(df_items):
    data = df_items.dropna()
    mu = data.mean()
    cov = data.cov()
    prec = np.linalg.pinv(cov)
    diff = data - mu
    md = diff.apply(lambda x: np.sqrt(np.dot(np.dot(x, prec), x)), axis=1)
    return md

# Use only items for MD
md_items = [c for c in all_items if c in df_clean.columns]
md_scores = get_md(df_clean[md_items])
# Threshold: Chi2 df=28, p < 0.001 (approx MD > 7.5 or D2 > 56)
threshold = np.sqrt(chi2.ppf(1 - 0.001, df=len(md_items)))
df_clean['md_score'] = md_scores
df_clean['is_outlier'] = df_clean['md_score'] > threshold
df_final = df_clean[df_clean['is_outlier'] == False].drop(columns=['md_score', 'is_outlier'])

# 6. Save
df_all.to_csv('01_harmonized/df_iri_all_harmonized.csv', index=False)
df_final.to_csv('01_harmonized/df_iri_clean.csv', index=False)

# EDA Summary
with open('02_eda/eda_cleaning_report.txt', 'w') as f:
    f.write(f"Raw cases: {len(df_all)}\n")
    f.write(f"Cases after QC (AC2/AC3): {len(df_clean)}\n")
    f.write(f"Cases after MD outliers removal: {len(df_final)}\n")
    f.write(f"Dropped as potentially random: {len(df_clean) - len(df_final)}\n")

print(f"Data Prep Complete. Clean N = {len(df_final)}")
