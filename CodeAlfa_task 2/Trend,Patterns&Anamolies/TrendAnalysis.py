def analyze_trends(self):
    """Identify upward/downward trends in data"""
    
    trends = {}
    
    # Numeric columns trend analysis
    numeric_cols = self.df.select_dtypes(include=[np.number]).columns
    
    for col in numeric_cols:
        # Simple linear trend
        x = np.arange(len(self.df))
        y = self.df[col].values
        
        # Remove NaN for calculation
        mask = ~np.isnan(y)
        if mask.sum() > 1:
            slope, intercept, r_value, p_value, std_err = stats.linregress(x[mask], y[mask])
            
            # Determine trend direction and significance
            if p_value < 0.05:
                if slope > 0:
                    trend = "Significant upward trend"
                elif slope < 0:
                    trend = "Significant downward trend"
                else:
                    trend = "Stable (no significant change)"
            else:
                trend = "No significant trend"
            
            # Calculate moving average for visualization
            window = min(30, len(self.df) // 10)
            if window > 1:
                ma = self.df[col].rolling(window=window, center=True).mean()
            else:
                ma = None
            
            trends[col] = {
                'trend_direction': trend,
                'slope': slope,
                'r_squared': r_value**2,
                'p_value': p_value,
                'magnitude': slope * len(self.df),  # Total change over period
                'moving_average': ma
            }
    
    # Visualize top trends
    self._plot_trends(trends)
    
    self.patterns_found['trends'] = trends
    return trends

def _plot_trends(self, trends):
    """Visualize significant trends"""
    
    # Select top 6 most significant trends
    significant_trends = {k: v for k, v in trends.items() 
                         if v['p_value'] < 0.05 and 'r_squared' in v}
    
    if not significant_trends:
        print("No significant trends found")
        return
    
    # Sort by R-squared
    sorted_trends = sorted(significant_trends.items(), 
                          key=lambda x: x[1]['r_squared'], 
                          reverse=True)[:6]
    
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    axes = axes.flatten()
    
    for idx, (col, trend_info) in enumerate(sorted_trends):
        if idx >= 6:
            break
            
        ax = axes[idx]
        
        # Plot original data
        ax.plot(self.df.index, self.df[col], alpha=0.5, label='Actual')
        
        # Plot trend line
        x = np.arange(len(self.df))
        trend_line = trend_info['slope'] * x + (self.df[col].mean() - trend_info['slope'] * x.mean())
        ax.plot(x, trend_line, 'r--', linewidth=2, label=f'Trend (R²={trend_info["r_squared"]:.2f})')
        
        # Plot moving average if available
        if trend_info['moving_average'] is not None:
            ax.plot(self.df.index, trend_info['moving_average'], 
                   'g-', linewidth=2, label='Moving Average')
        
        ax.set_title(f'{col}\n{trend_info["trend_direction"]}')
        ax.set_xlabel('Time')
        ax.set_ylabel('Value')
        ax.legend()
        ax.grid(True, alpha=0.3)
    
    # Hide unused subplots
    for idx in range(len(sorted_trends), 6):
        axes[idx].set_visible(False)
    
    plt.suptitle(f'Significant Trends in {self.name}', fontsize=16)
    plt.tight_layout()
    plt.show()