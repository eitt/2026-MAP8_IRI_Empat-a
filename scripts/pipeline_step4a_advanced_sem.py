import pandas as pd
import numpy as np
from factor_analyzer import calculate_kmo, calculate_bartlett_sphericity
from semopy import Model, calc_stats
import os

os.makedirs('03_sem', exist_ok=True)

df = pd.read_csv('01_harmonized/df_iri_clean.csv')

# Item lists
fs = [f"FS{i}" for i in [1, 5, 7, 12, 16, 23, 26]]
pt = [f"PT{i}" for i in [3, 8, 11, 15, 21, 25, 28]]
ec = [f"EC{i}" for i in [2, 4, 9, 14, 18, 20, 22]]
pd_items = [f"PD{i}" for i in [6, 10, 13, 17, 19, 24, 27]]
all_iri = fs + pt + ec + pd_items

def cronbach_alpha(df_scale):
    item_vars = df_scale.var(axis=0, ddof=1)
    t_var = df_scale.sum(axis=1).var(ddof=1)
    n = df_scale.shape[1]
    return (n / (n - 1)) * (1 - item_vars.sum() / t_var)

# 1. Reliability & Factorability
kmo_all, kmo_model = calculate_kmo(df[all_iri])
chi_square, p_value = calculate_bartlett_sphericity(df[all_iri])

rel_data = []
for name, items in [('FS', fs), ('PT', pt), ('EC', ec), ('PD', pd_items)]:
    alpha = cronbach_alpha(df[items])
    rel_data.append({'Construct': name, 'Alpha': round(alpha, 3), 'Items': len(items)})

# 2. CFA
mod_desc = f"""
FS =~ {" + ".join(fs)}
PT =~ {" + ".join(pt)}
EC =~ {" + ".join(ec)}
PD =~ {" + ".join(pd_items)}
"""
model = Model(mod_desc)
res = model.fit(df)
print(f"SEM Fit results: {res}")

estimates = model.inspect()
stats = calc_stats(model)

# 3. Factor Correlations
latent_vars = ['FS', 'PT', 'EC', 'PD']
corr_matrix = pd.DataFrame(index=latent_vars, columns=latent_vars)

# Standardized estimates fallback
try:
    std_ests = model.inspect(std_est=True) # Newer semopy uses std_est argument
except:
    std_ests = model.inspect(mode='std')

if std_ests is not None:
    latent_std_cov = std_ests[std_ests['op'] == '~~']
    for v1 in latent_vars:
        for v2 in latent_vars:
            if v1 == v2: corr_matrix.loc[v1, v2] = 1.0
            else:
                val = latent_std_cov[((latent_std_cov['lval'] == v1) & (latent_std_cov['rval'] == v2)) |
                                     ((latent_std_cov['lval'] == v2) & (latent_std_cov['rval'] == v1))]
                if not val.empty:
                    corr_matrix.loc[v1, v2] = round(val.iloc[0]['Estimate'], 3)
else:
    print("Warning: Standardized estimates not available.")

# 4. Save Outputs
pd.DataFrame(rel_data).to_csv('03_sem/reliability_stats.csv', index=False)
corr_matrix.to_csv('03_sem/factor_correlations.csv')
estimates.to_csv('03_sem/cfa_estimates.csv', index=False)
stats.to_csv('03_sem/cfa_fit_indices.csv')

with open('03_sem/advanced_sem_detailed_report.txt', 'w') as f:
    f.write(f"Global KMO MSA: {kmo_model:.3f}\n")
    f.write(f"Bartlett Sphericity: Chi2={chi_square:.2f}, p={p_value:.3e}\n\n")
    f.write("--- Scale Reliabilities ---\n")
    for r in rel_data:
        f.write(f"{r['Construct']}: Alpha = {r['Alpha']}\n")
    f.write("\n=== CFA Model Fit ===\n")
    f.write(stats.to_string())
    f.write("\n\n=== Factor Loadings ===\n")
    f.write(estimates[estimates['op'] == '~'].to_string())

print("Advanced SEM Complete.")
