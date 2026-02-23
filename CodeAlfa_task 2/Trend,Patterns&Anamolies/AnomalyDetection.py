def detect_anomalies(self):
    """Identify outliers and anomalies in the data"""
    
    anomalies = {}
    
    # Method 1: Statistical Outliers (IQR)
    numeric_cols = self.df.select_dtypes(include=[np.number]).columns
    
    iqr_anomalies = {}
    for col in numeric_cols:
        Q1 = self.df[col].quantile(0.25)
        Q3 = self.df[col].quantile(0.75)
        IQR = Q3 - Q1
        
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        
        outliers = self.df[(self.df[col] < lower_bound) | (self.df[col] > upper_bound)]
        
        if len(outliers) > 0:
            iqr_anomalies[col] = {
                'count': len(outliers),
                'percentage': (len(outliers) / len(self.df)) * 100,
                'indices': outliers.index.tolist()[:10],  # First 10 indices
                'bounds': {'lower': lower_bound, 'upper': upper_bound}
            }
    
    anomalies['statistical_outliers'] = iqr_anomalies
    
    # Method 2: Z-Score Anomalies
    zscore_anomalies = {}
    for col in numeric_cols:
        z_scores = np.abs(stats.zscore(self.df[col].dropna()))
        threshold = 3
        anomaly_indices = np.where(z_scores > threshold)[0]
        
        if len(anomaly_indices) > 0:
            zscore_anomalies[col] = {
                'count': len(anomaly_indices),
                'percentage': (len(anomaly_indices) / len(self.df[col].dropna())) * 100,
                'max_zscore': z_scores.max()
            }
    
    anomalies['zscore_anomalies'] = zscore_anomalies
    
    # Method 3: Isolation Forest (Machine Learning)
    if len(numeric_cols) >= 2 and len(self.df) > 100:
        # Prepare data
        data_for_if = self.df[numeric_cols].dropna()
        
        if len(data_for_if) > 50:
            iso_forest = IsolationForest(contamination=0.1, random_state=42)
            preds = iso_forest.fit_predict(data_for_if)
            
            anomalies['isolation_forest'] = {
                'count': (preds == -1).sum(),
                'percentage': ((preds == -1).sum() / len(preds)) * 100,
                'anomaly_scores': iso_forest.score_samples(data_for_if).tolist()[:10]
            }
    
    # Method 4: Temporal Anomalies (if time series)
    date_cols = self.df.select_dtypes(include=['datetime64']).columns
    if len(date_cols) > 0 and len(numeric_cols) > 0:
        temporal_anomalies = self._detect_temporal_anomalies()
        anomalies['temporal_anomalies'] = temporal_anomalies
    
    # Visualize anomalies
    self._visualize_anomalies(anomalies)
    
    # Print summary
    self._print_anomaly_summary(anomalies)
    
    self.patterns_found['anomalies'] = anomalies
    return anomalies

def _detect_temporal_anomalies(self):
    """Detect anomalies in time series data"""
    
    temporal_anomalies = {}
    numeric_cols = self.df.select_dtypes(include=[np.number]).columns[:3]  # Limit to first 3
    
    for col in numeric_cols:
        # Calculate rolling statistics
        rolling_mean = self.df[col].rolling(window=7, center=True).mean()
        rolling_std = self.df[col].rolling(window=7, center=True).std()
        
        # Points outside 3 sigma
        upper_bound = rolling_mean + 3 * rolling_std
        lower_bound = rolling_mean - 3 * rolling_std
        
        anomalies = self.df[(self.df[col] > upper_bound) | (self.df[col] < lower_bound)]
        
        if len(anomalies) > 0:
            temporal_anomalies[col] = {
                'count': len(anomalies),
                'percentage': (len(anomalies) / len(self.df)) * 100,
                'dates': anomalies.index[:5].tolist() if isinstance(anomalies.index, pd.DatetimeIndex) else []
            }
    
    return temporal_anomalies

def _visualize_anomalies(self, anomalies):
    """Visualize detected anomalies"""
    
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    
    # 1. Statistical Outliers
    ax = axes[0, 0]
    outlier_counts = [v['count'] for v in anomalies['statistical_outliers'].values()]
    outlier_cols = list(anomalies['statistical_outliers'].keys())
    
    if outlier_counts:
        ax.bar(range(len(outlier_cols)), outlier_counts)
        ax.set_xticks(range(len(outlier_cols)))
        ax.set_xticklabels(outlier_cols, rotation=45, ha='right')
        ax.set_ylabel('Number of Outliers')
        ax.set_title('Statistical Outliers (IQR Method)')
        ax.grid(True, alpha=0.3)
    else:
        ax.text(0.5, 0.5, 'No statistical outliers detected', 
               ha='center', va='center', transform=ax.transAxes)
        ax.set_title('Statistical Outliers')
    
    # 2. Z-Score Anomalies
    ax = axes[0, 1]
    zscore_counts = [v['count'] for v in anomalies['zscore_anomalies'].values()]
    zscore_cols = list(anomalies['zscore_anomalies'].keys())
    
    if zscore_counts:
        ax.bar(range(len(zscore_cols)), zscore_counts, color='orange')
        ax.set_xticks(range(len(zscore_cols)))
        ax.set_xticklabels(zscore_cols, rotation=45, ha='right')
        ax.set_ylabel('Number of Anomalies')
        ax.set_title('Z-Score Anomalies (|z|>3)')
        ax.grid(True, alpha=0.3)
    else:
        ax.text(0.5, 0.5, 'No Z-score anomalies detected', 
               ha='center', va='center', transform=ax.transAxes)
        ax.set_title('Z-Score Anomalies')
    
    # 3. Isolation Forest Results
    ax = axes[1, 0]
    if 'isolation_forest' in anomalies:
        if_data = anomalies['isolation_forest']
        sizes = [len(self.df) - if_data['count'], if_data['count']]
        labels = ['Normal', 'Anomaly']
        colors = ['green', 'red']
        ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
        ax.set_title('Isolation Forest Anomaly Detection')
    else:
        ax.text(0.5, 0.5, 'Insufficient data for Isolation Forest', 
               ha='center', va='center', transform=ax.transAxes)
        ax.set_title('Isolation Forest')
    
    # 4. Temporal Anomalies
    ax = axes[1, 1]
    if 'temporal_anomalies' in anomalies and anomalies['temporal_anomalies']:
        temp_data = anomalies['temporal_anomalies']
        temp_counts = [v['count'] for v in temp_data.values()]
        temp_cols = list(temp_data.keys())
        
        ax.bar(range(len(temp_cols)), temp_counts, color='purple')
        ax.set_xticks(range(len(temp_cols)))
        ax.set_xticklabels(temp_cols, rotation=45, ha='right')
        ax.set_ylabel('Number of Temporal Anomalies')
        ax.set_title('Time Series Anomalies')
        ax.grid(True, alpha=0.3)
    else:
        ax.text(0.5, 0.5, 'No temporal anomalies detected', 
               ha='center', va='center', transform=ax.transAxes)
        ax.set_title('Temporal Anomalies')
    
    plt.suptitle('Anomaly Detection Results', fontsize=16)
    plt.tight_layout()
    plt.show()

def _print_anomaly_summary(self, anomalies):
    """Print summary of detected anomalies"""
    
    print("\n📊 ANOMALY DETECTION SUMMARY")
    print("=" * 50)
    
    total_anomalies = 0
    for method, data in anomalies.items():
        if isinstance(data, dict):
            count = sum(v.get('count', 0) for v in data.values()) if method not in ['isolation_forest'] else data.get('count', 0)
            total_anomalies += count
            print(f"\n{method.replace('_', ' ').title()}:")
            print(f"  • Total anomalies: {count}")
            
            if method == 'statistical_outliers' and data:
                print("  • Top anomalous columns:")
                sorted_cols = sorted(data.items(), key=lambda x: x[1]['count'], reverse=True)[:3]
                for col, info in sorted_cols:
                    print(f"    - {col}: {info['count']} anomalies ({info['percentage']:.1f}%)")
    
    print(f"\n{'='*50}")
    print(f"TOTAL ANOMALIES DETECTED: {total_anomalies}")
    print(f"PERCENTAGE OF DATA: {(total_anomalies/len(self.df)*100):.1f}%")