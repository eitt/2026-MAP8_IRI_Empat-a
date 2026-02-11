import pandas as pd
import numpy as np
import os
from factor_analyzer import FactorAnalyzer
from factor_analyzer.factor_analyzer import calculate_bartlett_sphericity, calculate_kmo
import semopy
from semopy import Model, calc_stats

# Create directory
os.makedirs('03_sem', exist_ok=True)

# 1. Load Data
df = pd.read_csv('01_harmonized/df_iri_clean.csv')

# Item lists (using canonical names which are now properly oriented)
fs_items = ['FS1', 'FS5', 'FS7', 'FS12', 'FS16', 'FS23', 'FS26']
pt_items = ['PT3', 'PT8', 'PT11', 'PT15', 'PT21', 'PT25', 'PT28']
ec_items = ['EC2', 'EC4', 'EC9', 'EC14', 'EC18', 'EC20', 'EC22']
pd_items = ['PD6', 'PD10', 'PD13', 'PD17', 'PD19', 'PD24', 'PD27']
all_iri_items = fs_items + pt_items + ec_items + pd_items

def cronbach_alpha(df_items):
    k = df_items.shape[1]
    if k <= 1: return 0
    item_vars = df_items.var(ddof=1)
    total_var = df_items.sum(axis=1).var(ddof=1)
    return (k / (k - 1)) * (1 - item_vars.sum() / total_var)

def calculate_reliability_metrics(df_scale):
    base_alpha = cronbach_alpha(df_scale)
    item_stats = []
    for col in df_scale.columns:
        reduced_df = df_scale.drop(columns=[col])
        alpha_deleted = cronbach_alpha(reduced_df)
        scale_without_item = reduced_df.sum(axis=1)
        item_total_corr = df_scale[col].corr(scale_without_item)
        item_stats.append({
            'Item': col,
            'AlphaIfDeleted': alpha_deleted,
            'ItemTotalCorr': item_total_corr
        })
    return base_alpha, pd.DataFrame(item_stats)

# 2. Analysis
report_lines = []
report_lines.append("=== Advanced Reliability and SEM Analysis (Updated Scales) ===\n")

kmo_all, kmo_model = calculate_kmo(df[all_iri_items])
report_lines.append(f"Global KMO MSA: {kmo_model:.3f}\n")

for name, items in [('FS', fs_items), ('PT', pt_items), ('EC', ec_items), ('PD', pd_items)]:
    alpha, items_df = calculate_reliability_metrics(df[items])
    report_lines.append(f"--- Scale: {name} (Cronbach's Alpha: {alpha:.3f}) ---")
    report_lines.append(items_df.to_string(index=False))
    report_lines.append("")

# 3. CFA Model
model_desc = f"""
FS =~ {" + ".join(fs_items)}
PT =~ {" + ".join(pt_items)}
EC =~ {" + ".join(ec_items)}
PD =~ {" + ".join(pd_items)}
"""
try:
    cfa = Model(model_desc)
    cfa.fit(df)
    stats = semopy.calc_stats(cfa)
    report_lines.append("\n=== CFA Model Fit ===\n")
    report_lines.append(stats.to_string())
    
    report_lines.append("\n=== Factor Loadings ===")
    estimates = cfa.inspect()
    loadings = estimates[estimates['op'] == '~']
    report_lines.append(loadings[['lval', 'rval', 'Estimate', 'p-value']].to_string(index=False))
except Exception as e:
    report_lines.append(f"CFA Error: {e}")

# 4. Save
with open('03_sem/advanced_sem_detailed_report.txt', 'w') as f:
    f.write("\n".join(report_lines))

print("Advanced SEM & Reliability Analysis completed.")
