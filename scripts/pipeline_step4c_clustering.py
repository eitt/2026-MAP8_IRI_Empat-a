import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from scipy.cluster.hierarchy import dendrogram, linkage, fcluster
import os

os.makedirs('05_clustering', exist_ok=True)

features = ['FS_mean', 'PT_mean', 'EC_mean', 'PD_mean']

def run_clustering(input_file, suffix):
    print(f"Running Clustering for {input_file}...")
    df = pd.read_csv(input_file)
    X = df[features]
    
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # 1. Clustering
    Z = linkage(X_scaled, method='ward')
    k = 2
    df['cluster'] = fcluster(Z, k, criterion='maxclust')
    
    # 2. Profiles
    profiles = df.groupby('cluster')[features].mean()
    profiles.to_csv(f'05_clustering/cluster_profiles{suffix}.csv')
    
    # 3. Visualization
    plt.figure(figsize=(10, 6))
    sns.heatmap(profiles, annot=True, cmap='mako', fmt='.2f')
    plt.title(f'Empathy Cluster Profiles{suffix.replace("_", " ").title()}')
    plt.savefig(f'05_clustering/cluster_profiles{suffix}.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    plt.figure(figsize=(12, 8))
    df_melt = df.melt(id_vars=['cluster'], value_vars=features)
    sns.boxplot(x='variable', y='value', hue='cluster', data=df_melt, palette='mako')
    plt.title(f'Empathy Subscale Distributions by Cluster{suffix.replace("_", " ").title()}')
    plt.savefig(f'05_clustering/cluster_boxplots{suffix}.png', dpi=300, bbox_inches='tight')
    plt.close()

    # Compatibility
    if suffix == "_with_md":
        profiles.to_csv('05_clustering/cluster_profiles.csv')
        # We don't overwrite the main boxplot yet as report expects certain names

# Run three versions
run_clustering('01_harmonized/df_iri_clean_raw.csv', '_raw')
run_clustering('01_harmonized/df_iri_clean_no_md.csv', '_no_md')
run_clustering('01_harmonized/df_iri_clean_with_md.csv', '_with_md')

print("Clustering Complete for all three versions.")
