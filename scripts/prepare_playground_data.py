import pandas as pd
import numpy as np
import os

# Create directory
os.makedirs('01_harmonized', exist_ok=True)

print("[*] Harmonizing all three datasets (2023, 2024, 2025) for Playground...")

# 1. Load 2023
df23_raw = pd.read_excel('00_raw/1_2023_data_IRI.xlsx')
df23_raw['year'] = 2023

# 2. Load 2024
df24_raw = pd.read_excel('00_raw/2_2024_data_IRI.xlsx')
df24_raw['year'] = 2024

# 3. Load 2025
df25_raw = pd.read_excel('00_raw/3_2025_data_IRI.xlsx')
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

# --- Harmonization of 2023 ---
df23 = df23_raw.copy()
# 2023 scale is 0-4, standard is 1-5
for cid in all_items:
    if cid in df23.columns:
        df23[cid] = df23[cid] + 1

# --- Harmonization of 2024 ---
df24 = df24_raw.copy()
mapping24 = {f"E{get_canonical(i)}": get_canonical(i) for i in range(1, 29)}
df24 = df24.rename(columns=mapping24)

# --- Harmonization of 2025 ---
df25 = df25_raw.copy()
# Prefix is 'iri_'
mapping25 = {f"iri_{get_canonical(i)}": get_canonical(i) for i in range(1, 29)}
df25 = df25.rename(columns=mapping25)

# Mapping generic columns
map_cols = {
    'ID': 'respondent_id', 'iri_id': 'respondent_id',
    'age': 'age', 'gender': 'gender',
    'economic_level': 'ses', 'socioeconomic_level': 'ses',
    'AC1': 'AC1', 'iri_commitment': 'AC1',
    'AC2': 'AC2', 'iri_ac1_rta5': 'AC2',
    'AC3': 'AC3', 'iri_ac2_rta1': 'AC3'
}

def get_h(df, year):
    df_h = df.rename(columns=map_cols)
    base = ['respondent_id', 'year', 'age', 'gender', 'ses', 'AC1', 'AC2', 'AC3']
    cols = base + all_items
    for c in cols:
        if c not in df_h.columns: df_h[c] = np.nan
    return df_h[cols]

# Combine all
df_total = pd.concat([
    get_h(df23, 2023), 
    get_h(df24, 2024), 
    get_h(df25, 2025)
], ignore_index=True)

# Basic Cleaning for sociodemographics
def harmonize_gender(val):
    v = str(val).lower().strip()
    if v in ['hombre', '1', '1.0', 'masculino']: return 1
    if v in ['mujer', '2', '2.0', 'femenino']: return 2
    return np.nan

df_total['gender'] = df_total['gender'].apply(harmonize_gender)

# Define qc_fail_count (Used by Playground)
def calc_qc(row):
    fails = 0
    if pd.notnull(row['AC2']):
        # Standard check: AC2 should be 5
        if row['AC2'] != 5: fails += 1
    if pd.notnull(row['AC3']):
        # Standard check: AC3 should be 1
        if row['AC3'] != 1: fails += 1
    return fails

df_total['qc_fail_count'] = df_total.apply(calc_qc, axis=1)

# Save the special playground file
output_path = '01_harmonized/df_iri_playground.csv'
df_total.to_csv(output_path, index=False)

print(f"[SUCCESS] Playground data saved to {output_path} (N={len(df_total)})")
