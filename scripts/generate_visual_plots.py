import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

os.makedirs('06_reports/figures', exist_ok=True)

def generate_comparative_heatmaps():
    versions = [('_raw', 'Raw (Unfiltered)'), ('_no_md', 'QC Only'), ('_with_md', 'Clean (QC + MD)')]
    
    # Selection of professional palette for Social Science
    # 'mako' or 'viridis' is standard
    palette = sns.color_palette("mako", as_cmap=True)

    fig, axes = plt.subplots(1, 3, figsize=(18, 5))
    
    for i, (suffix, title) in enumerate(versions):
        path = f'03_sem/subscale_corr{suffix}.csv'
        if os.path.exists(path):
            df_corr = pd.read_csv(path, index_col=0)
            sns.heatmap(df_corr, annot=True, cmap=palette, fmt='.2f', ax=axes[i], cbar=(i==2), vmin=0, vmax=1)
            axes[i].set_title(title)
    
    plt.suptitle('Sensitivity Analysis: Subscale Inter-correlations across Cleaning Stages')
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.savefig('06_reports/figures/comparative_heatmaps.png', dpi=300)
    plt.close()

    # Comparative Cluster Centers Plot
    fig, axes = plt.subplots(1, 3, figsize=(18, 5))
    for i, (suffix, title) in enumerate(versions):
        path = f'05_clustering/cluster_profiles{suffix}.csv'
        if os.path.exists(path):
            df_p = pd.read_csv(path, index_col=0).T
            df_p.plot(kind='bar', ax=axes[i], color=['#2c7fb8', '#7fcdbb'])
            axes[i].set_title(title)
            axes[i].set_ylim(1, 5)
            axes[i].set_ylabel('Mean Score')
            if i > 0: axes[i].set_ylabel('')
    
    plt.suptitle('Cluster Profile Stability (3-Way Comparison)')
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.savefig('06_reports/figures/comparative_clusters.png', dpi=300)
    plt.close()

if __name__ == "__main__":
    generate_comparative_heatmaps()
    print("Comparative visualizations generated in 06_reports/figures/")
