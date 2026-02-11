import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from scipy.cluster.hierarchy import dendrogram, linkage, fcluster
import os

os.makedirs('05_clustering', exist_ok=True)

df = pd.read_csv('01_harmonized/df_iri_clean.csv')
features = ['FS_mean', 'PT_mean', 'EC_mean', 'PD_mean']
X = df[features]

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# 1. Clustering
Z = linkage(X_scaled, method='ward')

# Determine clusters (e.g., 2 as previously found)
k = 2
df['cluster'] = fcluster(Z, k, criterion='maxclust')

# 2. Profiles
profiles = df.groupby('cluster')[features].mean()
profiles.to_csv('05_clustering/cluster_profiles.csv')

# 3. Visualization
plt.figure(figsize=(10, 6))
sns.heatmap(profiles, annot=True, cmap='YlGnBu', fmt='.2f')
plt.title('Empathy Cluster Profiles (Subscale Means)')
plt.savefig('05_clustering/cluster_profiles.png', dpi=300, bbox_inches='tight')
plt.close()

# Subscale Distributions by Cluster
plt.figure(figsize=(12, 8))
df_melt = df.melt(id_vars=['cluster'], value_vars=features)
sns.boxplot(x='variable', y='value', hue='cluster', data=df_melt)
plt.title('Empathy Subscale Distributions by Cluster')
plt.savefig('05_clustering/cluster_boxplots.png', dpi=300, bbox_inches='tight')
plt.close()

print(f"Clustering Complete. K={k}")
