def detect_patterns(self):
    """Identify recurring patterns in the data"""
    
    patterns = {
        'clusters': [],
        'cycles': [],
        'distributions': {},
        'frequent_itemsets': []
    }
    
    # 1. Distribution Patterns
    numeric_cols = self.df.select_dtypes(include=[np.number]).columns
    for col in numeric_cols[:5]:  # Limit to first 5 for performance
        data = self.df[col].dropna()
        
        if len(data) > 10:
            # Test for normality
            statistic, p_value = stats.normaltest(data)
            
            # Check for multimodality
            kde = stats.gaussian_kde(data)
            x_range = np.linspace(data.min(), data.max(), 100)
            density = kde(x_range)
            
            # Find peaks in density (potential modes)
            peaks, properties = find_peaks(density, distance=len(x_range)//10)
            
            patterns['distributions'][col] = {
                'is_normal': p_value > 0.05,
                'normality_p_value': p_value,
                'num_modes': len(peaks),
                'mode_locations': x_range[peaks].tolist() if len(peaks) > 0 else [],
                'skewness': data.skew(),
                'kurtosis': data.kurtosis()
            }
    
    # 2. Cyclic Patterns (if time series)
    date_cols = self.df.select_dtypes(include=['datetime64']).columns
    if len(date_cols) > 0:
        date_col = date_cols[0]
        self.df = self.df.set_index(date_col) if date_col not in self.df.index.name else self.df
        
        # Look for cycles in numeric columns
        for col in numeric_cols[:3]:
            if len(self.df[col].dropna()) > 50:
                # Autocorrelation to find cycles
                from pandas.plotting import autocorrelation_plot
                
                # Simple cycle detection
                series = self.df[col].dropna()
                autocorr = [series.autocorr(lag=i) for i in range(1, min(50, len(series)//2))]
                
                # Find peaks in autocorrelation (potential cycle lengths)
                autocorr = np.array(autocorr)
                peaks, _ = find_peaks(autocorr, height=0.2)
                
                if len(peaks) > 0:
                    patterns['cycles'].append({
                        'column': col,
                        'potential_cycle_lengths': peaks.tolist(),
                        'strength': autocorr[peaks].tolist()
                    })
    
    # 3. Clustering Patterns
    if len(numeric_cols) >= 2:
        from sklearn.cluster import KMeans
        from sklearn.preprocessing import StandardScaler
        
        # Prepare data for clustering
        cluster_data = self.df[numeric_cols[:4]].dropna()
        if len(cluster_data) > 100:
            scaler = StandardScaler()
            scaled_data = scaler.fit_transform(cluster_data)
            
            # Find optimal clusters (simplified)
            inertias = []
            for k in range(1, 8):
                kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
                kmeans.fit(scaled_data)
                inertias.append(kmeans.inertia_)
            
            # Find elbow point
            diffs = np.diff(inertias)
            diffs2 = np.diff(diffs)
            optimal_k = np.argmin(diffs2) + 2 if len(diffs2) > 0 else 2
            
            patterns['clusters'] = {
                'optimal_clusters': optimal_k,
                'inertia_values': inertias
            }
    
    # Visualize patterns
    self._visualize_patterns(patterns)
    
    self.patterns_found['patterns'] = patterns
    return patterns

def _visualize_patterns(self, patterns):
    """Visualize detected patterns"""
    
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    
    # 1. Distribution patterns
    ax = axes[0, 0]
    for col, dist_info in list(patterns['distributions'].items())[:3]:
        data = self.df[col].dropna()
        if len(data) > 10:
            sns.kdeplot(data, label=col, ax=ax, fill=True, alpha=0.3)
    ax.set_title('Distribution Patterns')
    ax.set_xlabel('Value')
    ax.set_ylabel('Density')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # 2. Cyclic patterns
    ax = axes[0, 1]
    if patterns['cycles']:
        for cycle in patterns['cycles'][:2]:
            ax.plot(cycle['potential_cycle_lengths'], cycle['strength'], 
                   'o-', label=f"{cycle['column']}")
        ax.set_title('Cycle Detection')
        ax.set_xlabel('Lag')
        ax.set_ylabel('Autocorrelation')
        ax.legend()
        ax.grid(True, alpha=0.3)
    else:
        ax.text(0.5, 0.5, 'No clear cycles detected', 
               ha='center', va='center', transform=ax.transAxes)
        ax.set_title('Cycle Detection')
    
    # 3. Clustering pattern
    ax = axes[1, 0]
    if patterns['clusters']:
        inertias = patterns['clusters']['inertia_values']
        ax.plot(range(1, len(inertias)+1), inertias, 'bo-')
        ax.axvline(patterns['clusters']['optimal_clusters'], 
                  color='r', linestyle='--', 
                  label=f"Optimal: {patterns['clusters']['optimal_clusters']} clusters")
        ax.set_title('Elbow Curve for Clustering')
        ax.set_xlabel('Number of Clusters')
        ax.set_ylabel('Inertia')
        ax.legend()
        ax.grid(True, alpha=0.3)
    else:
        ax.text(0.5, 0.5, 'Insufficient data for clustering', 
               ha='center', va='center', transform=ax.transAxes)
        ax.set_title('Clustering Analysis')
    
    # 4. Pattern summary
    ax = axes[1, 1]
    pattern_summary = f"Patterns Detected:\n\n"
    pattern_summary += f"• Distributions analyzed: {len(patterns['distributions'])}\n"
    pattern_summary += f"• Normal distributions: {sum(1 for v in patterns['distributions'].values() if v['is_normal'])}\n"
    pattern_summary += f"• Multimodal distributions: {sum(1 for v in patterns['distributions'].values() if v['num_modes'] > 1)}\n"
    pattern_summary += f"• Cycles detected: {len(patterns['cycles'])}\n"
    
    ax.text(0.1, 0.5, pattern_summary, fontsize=12, 
           va='center', transform=ax.transAxes, fontfamily='monospace')
    ax.set_title('Pattern Summary')
    ax.axis('off')
    
    plt.suptitle('Pattern Detection Results', fontsize=16)
    plt.tight_layout()
    plt.show()