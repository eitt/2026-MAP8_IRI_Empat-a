import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

os.makedirs('06_reports/figures', exist_ok=True)

def generate_comparative_heatmaps():
    versions = [('_raw', 'Raw (Unfiltered)'), ('_no_md', 'QC Only'), ('_with_md', 'Clean (QC + MD)')]
    palette = sns.color_palette("mako", as_cmap=True)

    for suffix, title in versions:
        # Individual Heatmap for Correlation
        path_corr = f'03_sem/subscale_corr{suffix}.csv'
        if os.path.exists(path_corr):
            df_corr = pd.read_csv(path_corr, index_col=0)
            plt.figure(figsize=(8.5, 7))
            sns.heatmap(df_corr, annot=True, cmap=palette, fmt='.2f', vmin=0, vmax=1, annot_kws={"size": 12})
            plt.title(f'Inter-correlations: {title}', fontsize=14)
            plt.savefig(f'06_reports/figures/correlation_heatmap{suffix}.jpg', dpi=300, bbox_inches='tight')
            plt.close()

        # Individual Bar Chart for Cluster Profiles
        path_clus = f'05_clustering/cluster_profiles{suffix}.csv'
        if os.path.exists(path_clus):
            df_p = pd.read_csv(path_clus, index_col=0).T
            plt.figure(figsize=(8.5, 6))
            df_p.plot(kind='bar', color=['#2c7fb8', '#7fcdbb'], width=0.8)
            plt.title(f'Cluster Centroids: {title}', fontsize=14)
            plt.ylim(1, 5)
            plt.ylabel('Mean Score (1-5)', fontsize=12)
            plt.grid(axis='y', linestyle='--', alpha=0.7)
            plt.legend(title='Profile Cluster', loc='lower right')
            plt.savefig(f'06_reports/figures/cluster_profiles_bar{suffix}.jpg', dpi=300, bbox_inches='tight')
            plt.close()

if __name__ == "__main__":
    generate_comparative_heatmaps()
    print("Comparative visualizations generated in 06_reports/figures/")
