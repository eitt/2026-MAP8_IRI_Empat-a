import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from scipy.cluster.hierarchy import dendrogram, linkage, fcluster
from sklearn.metrics import silhouette_score
import os

# Create directory
os.makedirs('05_clustering', exist_ok=True)

# 1. Load Data
df = pd.read_csv('01_harmonized/df_iri_clean.csv')

# 2. Prepare Features
features = ['FS_mean', 'PT_mean', 'EC_mean', 'PD_mean']
X = df[features]

# Standardize
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# 3. Hierarchical Clustering (Ward's method)
Z = linkage(X_scaled, method='ward')

# 4. Dendrogram
plt.figure(figsize=(12, 8))
dendrogram(Z, truncate_mode='lastp', p=30)
plt.title('Hierarchical Clustering Dendrogram (Truncated)')
plt.xlabel('Cluster size')
plt.ylabel('Distance')
plt.savefig('05_clustering/dendrogram.png')
plt.close()

# 5. Determine number of clusters (Silhouette Score)
sil_scores = []
range_n = range(2, 7)
for n in range_n:
    labels = fcluster(Z, n, criterion='maxclust')
    score = silhouette_score(X_scaled, labels)
    sil_scores.append(score)

plt.figure(figsize=(8, 5))
plt.plot(range_n, sil_scores, marker='o')
plt.title('Silhouette Score for different number of clusters')
plt.xlabel('Number of clusters')
plt.ylabel('Silhouette Score')
plt.savefig('05_clustering/silhouette_analysis.png')
plt.close()

# 6. Final Cluster Assignment (e.g., 3 or 4 clusters based on silhouette or theory)
# I'll pick the one with max silhouette score or a reasonable default like 3.
optimal_n = range_n[np.argmax(sil_scores)]
df['cluster'] = fcluster(Z, optimal_n, criterion='maxclust')

# 7. Analyze Clusters
cluster_summary = df.groupby('cluster')[features].mean()
cluster_counts = df['cluster'].value_counts().sort_index()

# Save results
cluster_summary.to_csv('05_clustering/cluster_centroids.csv')
df.to_csv('05_clustering/df_with_clusters.csv', index=False)

# Plot Profile
cluster_summary_melted = cluster_summary.reset_index().melt(id_vars='cluster', var_name='subscale', value_name='mean_score')
plt.figure(figsize=(10, 6))
sns.lineplot(data=cluster_summary_melted, x='subscale', y='mean_score', hue='cluster', marker='o')
plt.title(f'Empathy Profiles (n_clusters={optimal_n})')
plt.savefig('05_clustering/cluster_profiles.png')
plt.close()

with open('05_clustering/clustering_report.txt', 'w') as f:
    f.write(f"Optimal number of clusters (max silhouette): {optimal_n}\n")
    f.write(f"Cluster sizes:\n{cluster_counts.to_string()}\n\n")
    f.write("Cluster Centroids (Means):\n")
    f.write(cluster_summary.to_string())

print(f"Clustering completed. Optimal clusters: {optimal_n}. Results saved to 05_clustering/.")
