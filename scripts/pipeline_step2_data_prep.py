import pandas as pd
import numpy as np
import os

# Create directories if they don't exist
os.makedirs('01_harmonized', exist_ok=True)
os.makedirs('02_eda', exist_ok=True)

# 1. Load Raw Data
df23_raw = pd.read_excel('00_raw/1_2023_data_IRI.xlsx')
df24_raw = pd.read_excel('00_raw/2_2024_data_IRI.xlsx')
df25_raw = pd.read_excel('00_raw/3_2025_data_IRI.xlsx')

# 2. Year tags
df23_raw['year'] = 2023
df24_raw['year'] = 2024
df25_raw['year'] = 2025

# 3. Item List Definition (Canonical IDs)
fs_items_idx = [1, 5, 7, 12, 16, 23, 26]
pt_items_idx = [3, 8, 11, 15, 21, 25, 28]
ec_items_idx = [2, 4, 9, 14, 18, 20, 22]
pd_items_idx = [6, 10, 13, 17, 19, 24, 27]

def get_canonical(idx):
    if idx in fs_items_idx: return f"FS{idx}"
    if idx in pt_items_idx: return f"PT{idx}"
    if idx in ec_items_idx: return f"EC{idx}"
    if idx in pd_items_idx: return f"PD{idx}"
    return None

all_canonical_items = [get_canonical(i) for i in range(1, 29)]

# 4. Dataset-Specific Processing
# 2023: Scale 0-4, items already reversed. Action: Add 1 to unify to 1-5.
df23 = df23_raw.copy()
for cid in all_canonical_items:
    if cid in df23.columns:
        df23[cid] = df23[cid] + 1

# 2024: Scale 1-5, items already reversed. Action: Rename.
df24 = df24_raw.copy()
mapping24 = {f"E{get_canonical(i)}": get_canonical(i) for i in range(1, 29)}
df24 = df24.rename(columns=mapping24)

# 2025: Scale 1-5. Only FS7 and PD13 need reverse. Action: Reverse iri_FS7, iri_PD13.
df25 = df25_raw.copy()
mapping25 = {f"iri_{get_canonical(i)}": get_canonical(i) for i in range(1, 29)}
df25 = df25.rename(columns=mapping25)
df25['FS7'] = 6 - df25['FS7']
df25['PD13'] = 6 - df25['PD13']

# 5. Harmonize Columns for Merge
def get_harmonized_subset(df, year):
    mapping = {
        'ID': 'respondent_id',
        'iri_id': 'respondent_id',
        'age': 'age',
        'gender': 'gender',
        'economic_level': 'ses',
        'socioeconomic_level': 'ses',
        'AC1': 'AC1_commitment',
        'iri_commitment': 'AC1_commitment',
        'AC1_commitment': 'AC1_commitment',
        'AC2': 'AC2_check_expected5',
        'iri_ac1_rta5': 'AC2_check_expected5',
        'AC3': 'AC3_check_expected1',
        'iri_ac2_rta1': 'AC3_check_expected1'
    }
    df_h = df.rename(columns=mapping)
    
    # Selective columns
    base_cols = ['respondent_id', 'year', 'age', 'gender', 'ses', 'AC1_commitment', 'AC2_check_expected5', 'AC3_check_expected1']
    cols = base_cols + all_canonical_items
    
    # Ensure all items exist as NaN if missing
    for c in cols:
        if c not in df_h.columns:
            df_h[c] = np.nan
            
    return df_h[cols]

df23_h = get_harmonized_subset(df23, 2023)
df24_h = get_harmonized_subset(df24, 2024)
df25_h = get_harmonized_subset(df25, 2025)

df_all = pd.concat([df23_h, df24_h, df25_h], ignore_index=True)

# 6. Compute Subscales (as means of unified 1-5 scale)
def get_scale_items(prefix):
    indices = fs_items_idx if prefix=='FS' else pt_items_idx if prefix=='PT' else ec_items_idx if prefix=='EC' else pd_items_idx
    return [f"{prefix}{idx}" for idx in indices]

df_all['FS_mean'] = df_all[get_scale_items('FS')].mean(axis=1)
df_all['PT_mean'] = df_all[get_scale_items('PT')].mean(axis=1)
df_all['EC_mean'] = df_all[get_scale_items('EC')].mean(axis=1)
df_all['PD_mean'] = df_all[get_scale_items('PD')].mean(axis=1)
df_all['IRI_total'] = df_all[['FS_mean', 'PT_mean', 'EC_mean', 'PD_mean']].mean(axis=1)

# 7. QC Logic
# For 2023, AC columns are NaN. Logic: NaN doesn't count as failure.
def check_qc(row):
    fails = 0
    if pd.notnull(row['AC2_check_expected5']):
        if row['AC2_check_expected5'] != 5: fails += 1
    if pd.notnull(row['AC3_check_expected1']):
        if row['AC3_check_expected1'] != 1: fails += 1
    return fails

df_all['attention_fail_count'] = df_all.apply(check_qc, axis=1)
df_all['included_after_qc'] = df_all['attention_fail_count'] == 0

# 8. Filter for QCA readiness (Drop ALL rows with ANY NaN in analysis variables)
qca_vars = ['age', 'ses', 'FS_mean', 'PT_mean', 'EC_mean', 'PD_mean', 'IRI_total']
# Also drop any 2023 rows if you specifically need the attention check columns to be non-null for R,
# but usually QCA only needs the conditions and outcome.
# The error reported columns age, ses, AC1_commitment, AC2_check_expected5, etc.
# If the R script includes them in 'conditions', they must be non-null.

df_all.to_csv('01_harmonized/df_iri_harmonized_all.csv', index=False)

# Clean set: passed QC AND no missing data in core QCA variables
df_clean = df_all[df_all['included_after_qc']].dropna(subset=qca_vars)
df_clean.to_csv('01_harmonized/df_iri_clean.csv', index=False)

print(f"Data Prep Updated. Sample size after QC and dropping NAs for QCA: {len(df_clean)}")
