import pandas as pd
import numpy as np
import os
from factor_analyzer.factor_analyzer import calculate_bartlett_sphericity, calculate_kmo
import semopy
from semopy import Model, calc_stats
from scipy.stats import chi2

# Create directory
os.makedirs('03_sem', exist_ok=True)

# 1. Load Data
df_all = pd.read_csv('01_harmonized/df_iri_harmonized_all.csv')

# Item lists
fs_items = ['FS1', 'FS5', 'FS7_rev', 'FS12_rev', 'FS16', 'FS23', 'FS26']
pt_items = ['PT3_rev', 'PT8', 'PT11', 'PT15_rev', 'PT21', 'PT25', 'PT28']
ec_items = ['EC2', 'EC4_rev', 'EC9', 'EC14_rev', 'EC18_rev', 'EC20', 'EC22']
pd_items = ['PD6', 'PD10', 'PD13_rev', 'PD17', 'PD19_rev', 'PD24', 'PD27']
all_iri_items = fs_items + pt_items + ec_items + pd_items

def cronbach_alpha(df_items):
    k = df_items.shape[1]
    if k <= 1: return 0
    item_vars = df_items.var(ddof=1)
    total_var = df_items.sum(axis=1).var(ddof=1)
    return (k / (k - 1)) * (1 - item_vars.sum() / total_var)

# 2. Case Selection Analysis (Strict vs Lenient QC)
report_lines = []
report_lines.append("=== Case Selection Analysis (Impact of Attention Checks) ===\n")

for qc_name, mask in [
    ("Lenient (Allow 1 fail)", df_all['attention_fail_count'] <= 1),
    ("Strict (0 fails)", df_all['attention_fail_count'] == 0)
]:
    sub_df = df_all[mask]
    alphas = [cronbach_alpha(sub_df[itms]) for itms in [fs_items, pt_items, ec_items, pd_items]]
    report_lines.append(f"{qc_name}: N={len(sub_df)}, Avg Alpha={np.mean(alphas):.3f} (FS:{alphas[0]:.2f}, PT:{alphas[1]:.2f}, EC:{alphas[2]:.2f}, PD:{alphas[3]:.2f})")

# 3. Multivariate Outlier Detection (Mahalanobis Distance)
def get_mahalanobis(df_items):
    df_items = df_items.dropna()
    mean = df_items.mean()
    cov = df_items.corr() # Using corr for stability if scaling differs
    # Actually use proper covariance
    cov = df_items.cov()
    inv_cov = np.linalg.pinv(cov)
    diff = df_items - mean
    md = diff.apply(lambda x: np.dot(np.dot(x, inv_cov), x), axis=1)
    return md

df_clean = df_all[df_all['attention_fail_count'] == 0].copy()
md_scores = get_mahalanobis(df_clean[all_iri_items])
# Threshold: Chi2 with df=28 (number of items), p < 0.001
threshold = chi2.ppf(1 - 0.001, df=len(all_iri_items))
outliers = md_scores[md_scores > threshold]

report_lines.append(f"\nMultivariate Outliers (Mahalanobis D > {threshold:.2f}): {len(outliers)} cases identified.")
report_lines.append(f"Suggestion: Consider dropping these {len(outliers)} respondents to stabilize the CFA model.")

# 4. Item Dropping impact on CFA
report_lines.append("\n=== Item Selection Impact on CFA Model Fit ===")

# Model 1: Initial (All items)
model1_desc = f"""
FS =~ {" + ".join(fs_items)}
PT =~ {" + ".join(pt_items)}
EC =~ {" + ".join(ec_items)}
PD =~ {" + ".join(pd_items)}
"""

# Model 2: Dropping all negatively correlated items (_rev items)
fs_red = [i for i in fs_items if '_rev' not in i]
pt_red = [i for i in pt_items if '_rev' not in i]
ec_red = [i for i in ec_items if '_rev' not in i]
pd_red = [i for i in pd_items if '_rev' not in i]

model2_desc = f"""
FS =~ {" + ".join(fs_red)}
PT =~ {" + ".join(pt_red)}
EC =~ {" + ".join(ec_red)}
PD =~ {" + ".join(pd_red)}
"""

for i, desc in enumerate([model1_desc, model2_desc], 1):
    try:
        mod = Model(desc)
        mod.fit(df_clean)
        stats = semopy.calc_stats(mod)
        cfi = stats.loc['Value', 'CFI']
        rmsea = stats.loc['Value', 'RMSEA']
        tli = stats.loc['Value', 'TLI']
        report_lines.append(f"Model {i} ({'Reduced' if i==2 else 'Full'}): CFI={cfi:.3f}, TLI={tli:.3f}, RMSEA={rmsea:.3f}")
    except Exception as e:
        report_lines.append(f"Model {i} failed: {e}")

# 5. Global KMO/Bartlett for the current cleaned subset
chi2_b, p_b = calculate_bartlett_sphericity(df_clean[all_iri_items])
kmo_all, kmo_m = calculate_kmo(df_clean[all_iri_items])
report_lines.append(f"\nClean Subset KMO: {kmo_m:.3f}, Bartlett p: {p_b:.4f}")

# Save
with open('03_sem/case_and_item_enhancement_advise.txt', 'w') as f:
    f.write("\n".join(report_lines))

print("Case and Item enhancement analysis completed. Results saved to 03_sem/case_and_item_enhancement_advise.txt")
