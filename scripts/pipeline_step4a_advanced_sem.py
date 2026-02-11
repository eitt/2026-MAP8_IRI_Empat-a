import pandas as pd
import numpy as np
from factor_analyzer import calculate_kmo, calculate_bartlett_sphericity
from semopy import Model, calc_stats
import os

os.makedirs('03_sem', exist_ok=True)

item_lists = {
    'FS': [f"FS{i}" for i in [1, 5, 7, 12, 16, 23, 26]],
    'PT': [f"PT{i}" for i in [3, 8, 11, 15, 21, 25, 28]],
    'EC': [f"EC{i}" for i in [2, 4, 9, 14, 18, 20, 22]],
    'PD': [f"PD{i}" for i in [6, 10, 13, 17, 19, 24, 27]]
}
all_iri = item_lists['FS'] + item_lists['PT'] + item_lists['EC'] + item_lists['PD']

def cronbach_alpha(df_scale):
    item_vars = df_scale.var(axis=0, ddof=1)
    t_var = df_scale.sum(axis=1).var(ddof=1)
    n = df_scale.shape[1]
    return (n / (n - 1)) * (1 - item_vars.sum() / t_var)

def run_sem_analysis(input_file, suffix):
    print(f"Running SEM for {input_file}...")
    df = pd.read_csv(input_file)
    
    # 1. Reliability & Factorability
    kmo_all, kmo_model = calculate_kmo(df[all_iri])
    chi_square, p_value = calculate_bartlett_sphericity(df[all_iri])
    
    rel_data = []
    for name, items in item_lists.items():
        alpha = cronbach_alpha(df[items])
        rel_data.append({'Construct': name, 'Alpha': round(alpha, 3), 'Items': len(items)})
    
    # 2. CFA
    mod_desc = "\n".join([f"{name} =~ {' + '.join(items)}" for name, items in item_lists.items()])
    model = Model(mod_desc)
    model.fit(df)
    
    estimates = model.inspect()
    stats = calc_stats(model)
    
    # 3. Factor Correlations
    latent_vars = ['FS', 'PT', 'EC', 'PD']
    corr_matrix = pd.DataFrame(index=latent_vars, columns=latent_vars)
    try: std_ests = model.inspect(std_est=True)
    except: std_ests = model.inspect(mode='std')
    
    if std_ests is not None:
        latent_std_cov = std_ests[std_ests['op'] == '~~']
        for v1 in latent_vars:
            for v2 in latent_vars:
                if v1 == v2: corr_matrix.loc[v1, v2] = 1.0
                else:
                    val = latent_std_cov[((latent_std_cov['lval'] == v1) & (latent_std_cov['rval'] == v2)) |
                                         ((latent_std_cov['lval'] == v2) & (latent_std_cov['rval'] == v1))]
                    if not val.empty: corr_matrix.loc[v1, v2] = round(val.iloc[0]['Estimate'], 3)
    
    # 4. Save Outputs
    pd.DataFrame(rel_data).to_csv(f'03_sem/reliability_stats{suffix}.csv', index=False)
    corr_matrix.to_csv(f'03_sem/factor_correlations{suffix}.csv')
    estimates.to_csv(f'03_sem/cfa_estimates{suffix}.csv', index=False)
    stats.to_csv(f'03_sem/cfa_fit_indices{suffix}.csv')
    
    with open(f'03_sem/advanced_sem_detailed_report{suffix}.txt', 'w') as f:
        f.write(f"Global KMO MSA: {kmo_model:.3f}\n")
        f.write(f"Bartlett Sphericity: Chi2={chi_square:.2f}, p={p_value:.3e}\n\n")
        f.write("--- Scale Reliabilities ---\n")
        for r in rel_data: f.write(f"{r['Construct']}: Alpha = {r['Alpha']}\n")
        f.write("\n=== CFA Model Fit ===\n")
        f.write(stats.to_string())
        f.write("\n\n=== Factor Loadings ===\n")
        f.write(estimates[estimates['op'] == '~'].to_string())
    
    # For backward compatibility with report scripts that expect no suffix
    if suffix == "_with_md":
        pd.DataFrame(rel_data).to_csv('03_sem/reliability_stats.csv', index=False)
        corr_matrix.to_csv('03_sem/factor_correlations.csv')
        estimates.to_csv('03_sem/cfa_estimates.csv', index=False)
        stats.to_csv('03_sem/cfa_fit_indices.csv')
        # Rename report as well
        with open('03_sem/advanced_sem_detailed_report.txt', 'w') as f:
            f.write(f"Global KMO MSA: {kmo_model:.3f}\n")
            f.write(f"Bartlett Sphericity: Chi2={chi_square:.2f}, p={p_value:.3e}\n\n")
            f.write("--- Scale Reliabilities ---\n")
            for r in rel_data: f.write(f"{r['Construct']}: Alpha = {r['Alpha']}\n")
            f.write("\n=== CFA Model Fit ===\n")
            f.write(stats.to_string())

# Run three versions for full sensitivity
run_sem_analysis('01_harmonized/df_iri_clean_raw.csv', '_raw')
run_sem_analysis('01_harmonized/df_iri_clean_no_md.csv', '_no_md')
run_sem_analysis('01_harmonized/df_iri_clean_with_md.csv', '_with_md')

# Generate raw item correlation heatmap data for all 3 for report
for s in ['_raw', '_no_md', '_with_md']:
    df_s = pd.read_csv(f'01_harmonized/df_iri_clean{s}.csv')
    subscales = ['FS_mean', 'PT_mean', 'EC_mean', 'PD_mean']
    df_s[subscales].corr().to_csv(f'03_sem/subscale_corr{s}.csv')

print("Advanced SEM Complete for all three versions.")
