def find_correlation_patterns(self):
    """Identify interesting correlation patterns"""
    
    correlation_patterns = {}
    
    # Get numeric columns
    numeric_cols = self.df.select_dtypes(include=[np.number]).columns
    
    if len(numeric_cols) < 2:
        print("Insufficient numeric columns for correlation analysis")
        return correlation_patterns
    
    # Calculate correlation matrix
    corr_matrix = self.df[numeric_cols].corr()
    
    # 1. Find strongest correlations
    strong_correlations = []
    for i in range(len(corr_matrix.columns)):
        for j in range(i+1, len(corr_matrix.columns)):
            corr_value = corr_matrix.iloc[i, j]
            if abs(corr_value) > 0.7:
                strong_correlations.append({
                    'var1': corr_matrix.columns[i],
                    'var2': corr_matrix.columns[j],
                    'correlation': corr_value,
                    'type': 'positive' if corr_value > 0 else 'negative'
                })
    
    correlation_patterns['strong_correlations'] = sorted(strong_correlations, 
                                                        key=lambda x: abs(x['correlation']), 
                                                        reverse=True)
    
    # 2. Find uncorrelated variables
    uncorrelated = []
    for i in range(len(corr_matrix.columns)):
        for j in range(i+1, len(corr_matrix.columns)):
            corr_value = abs(corr_matrix.iloc[i, j])
            if corr_value < 0.1:
                uncorrelated.append({
                    'var1': corr_matrix.columns[i],
                    'var2': corr_matrix.columns[j],
                    'correlation': corr_matrix.iloc[i, j]
                })
    
    correlation_patterns['uncorrelated'] = uncorrelated[:10]  # Top 10
    
    # 3. Find variables that form clusters
    from scipy.cluster import hierarchy
    from scipy.spatial.distance import squareform
    
    # Convert correlation to distance
    distance_matrix = 1 - abs(corr_matrix)
    condensed_distances = squareform(distance_matrix)
    
    # Hierarchical clustering
    linkage_matrix = hierarchy.linkage(condensed_distances, method='average')
    
    # Find clusters at threshold 0.5 (moderate correlation)
    clusters = hierarchy.fcluster(linkage_matrix, 0.5, criterion='distance')
    
    correlation_patterns['variable_clusters'] = {}
    for i, cluster_id in enumerate(clusters):
        if cluster_id not in correlation_patterns['variable_clusters']:
            correlation_patterns['variable_clusters'][cluster_id] = []
        correlation_patterns['variable_clusters'][cluster_id].append(corr_matrix.columns[i])
    
    # Visualize correlation patterns
    self._plot_correlation_patterns(corr_matrix, correlation_patterns)
    
    self.patterns_found['correlations'] = correlation_patterns
    return correlation_patterns

def _plot_correlation_patterns(self, corr_matrix, patterns):
    """Visualize correlation patterns"""
    
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    
    # 1. Correlation heatmap
    ax = axes[0, 0]
    mask = np.triu(np.ones_like(corr_matrix), k=1)
    sns.heatmap(corr_matrix, mask=mask, annot=True, fmt='.2f', 
                cmap='RdBu_r', center=0, square=True, ax=ax,
                cbar_kws={'label': 'Correlation Coefficient'})
    ax.set_title('Correlation Matrix Heatmap')
    
    # 2. Strong correlations bar chart
    ax = axes[0, 1]
    strong_corrs = patterns['strong_correlations'][:10]  # Top 10
    if strong_corrs:
        labels = [f"{c['var1']} & {c['var2']}" for c in strong_corrs]
        values = [c['correlation'] for c in strong_corrs]
        colors = ['red' if v < 0 else 'green' for v in values]
        bars = ax.barh(range(len(labels)), values, color=colors)
        ax.set_yticks(range(len(labels)))
        ax.set_yticklabels(labels)
        ax.set_xlabel('Correlation Coefficient')
        ax.set_title('Top 10 Strongest Correlations')
        ax.axvline(0, color='black', linestyle='-', linewidth=0.5)
        ax.grid(True, alpha=0.3, axis='x')
    else:
        ax.text(0.5, 0.5, 'No strong correlations found', 
               ha='center', va='center', transform=ax.transAxes)
        ax.set_title('Strong Correlations')
    
    # 3. Correlation distribution
    ax = axes[1, 0]
    # Get upper triangle of correlation matrix
    upper_triangle = corr_matrix.where(np.triu(np.ones(corr_matrix.shape), k=1).astype(bool))
    correlations = upper_triangle.stack().values
    
    ax.hist(correlations, bins=20, edgecolor='black', alpha=0.7)
    ax.axvline(0, color='red', linestyle='--', linewidth=1)
    ax.axvline(0.7, color='green', linestyle='--', linewidth=1, label='Strong positive')
    ax.axvline(-0.7, color='green', linestyle='--', linewidth=1, label='Strong negative')
    ax.set_xlabel('Correlation Coefficient')
    ax.set_ylabel('Frequency')
    ax.set_title('Distribution of Correlations')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # 4. Variable clusters
    ax = axes[1, 1]
    if patterns['variable_clusters']:
        cluster_text = "Variable Clusters:\n\n"
        for cluster_id, variables in patterns['variable_clusters'].items():
            if len(variables) > 1:  # Only show clusters with multiple variables
                cluster_text += f"Cluster {cluster_id}:\n"
                for var in variables:
                    cluster_text += f"  • {var}\n"
                cluster_text += "\n"
        
        ax.text(0.1, 0.5, cluster_text, fontsize=10, 
               va='center', transform=ax.transAxes, fontfamily='monospace')
    else:
        ax.text(0.5, 0.5, 'No clear variable clusters', 
               ha='center', va='center', transform=ax.transAxes)
    ax.set_title('Variable Clusters')
    ax.axis('off')
    
    plt.suptitle('Correlation Pattern Analysis', fontsize=16)
    plt.tight_layout()
    plt.show()