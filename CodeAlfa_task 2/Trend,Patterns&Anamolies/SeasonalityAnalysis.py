def analyze_seasonality(self):
    """Identify seasonal patterns in time-based data"""
    
    seasonality = {}
    
    # Check for datetime index or column
    date_cols = self.df.select_dtypes(include=['datetime64']).columns
    time_index = None
    
    if len(date_cols) > 0:
        time_index = date_cols[0]
        df_time = self.df.copy()
        
        # Extract time components
        df_time['year'] = df_time[time_index].dt.year
        df_time['month'] = df_time[time_index].dt.month
        df_time['quarter'] = df_time[time_index].dt.quarter
        df_time['dayofweek'] = df_time[time_index].dt.dayofweek
        df_time['day'] = df_time[time_index].dt.day
        df_time['hour'] = df_time[time_index].dt.hour if hasattr(df_time[time_index].dt, 'hour') else None
        
        # Analyze numeric columns for seasonality
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        
        for col in numeric_cols[:3]:  # Limit to first 3 for performance
            col_seasonality = {}
            
            # Monthly patterns
            monthly_avg = df_time.groupby('month')[col].mean()
            if len(monthly_avg) >= 12:  # Full year of data
                # Detect seasonal pattern
                from statsmodels.tsa.seasonal import seasonal_decompose
                
                try:
                    # Need at least 2 full cycles
                    if len(df_time[col].dropna()) >= 24:
                        decomposition = seasonal_decompose(df_time[col].dropna().values, 
                                                         model='additive', period=12)
                        col_seasonality['has_seasonality'] = True
                        col_seasonality['seasonal_strength'] = np.std(decomposition.seasonal) / np.std(decomposition.resid + decomposition.seasonal)
                        col_seasonality['peak_month'] = monthly_avg.idxmax()
                        col_seasonality['trough_month'] = monthly_avg.idxmin()
                except:
                    col_seasonality['has_seasonality'] = False
            
            # Weekly patterns
            weekly_avg = df_time.groupby('dayofweek')[col].mean()
            if len(weekly_avg) > 0:
                col_seasonality['weekly_pattern'] = weekly_avg.to_dict()
                col_seasonality['peak_day'] = weekly_avg.idxmax()
                col_seasonality['trough_day'] = weekly_avg.idxmin()
            
            # Quarterly patterns
            quarterly_avg = df_time.groupby('quarter')[col].mean()
            if len(quarterly_avg) > 0:
                col_seasonality['quarterly_pattern'] = quarterly_avg.to_dict()
                col_seasonality['peak_quarter'] = quarterly_avg.idxmax()
            
            seasonality[col] = col_seasonality
        
        # Visualize seasonality
        self._plot_seasonality(seasonality, df_time)
    
    self.patterns_found['seasonality'] = seasonality
    return seasonality

def _plot_seasonality(self, seasonality, df_time):
    """Visualize seasonal patterns"""
    
    if not seasonality:
        print("No seasonal patterns detected")
        return
    
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    
    # 1. Monthly patterns
    ax = axes[0, 0]
    for col, info in list(seasonality.items())[:3]:
        if 'month' in df_time.columns:
            monthly_data = df_time.groupby('month')[col].mean()
            ax.plot(monthly_data.index, monthly_data.values, 'o-', label=col)
    ax.set_title('Monthly Patterns')
    ax.set_xlabel('Month')
    ax.set_ylabel('Average Value')
    ax.set_xticks(range(1, 13))
    ax.set_xticklabels(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                       'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # 2. Weekly patterns
    ax = axes[0, 1]
    for col, info in list(seasonality.items())[:3]:
        if 'weekly_pattern' in info:
            days = list(info['weekly_pattern'].keys())
            values = list(info['weekly_pattern'].values())
            ax.plot(days, values, 'o-', label=col)
    ax.set_title('Weekly Patterns')
    ax.set_xlabel('Day of Week')
    ax.set_ylabel('Average Value')
    ax.set_xticks(range(7))
    ax.set_xticklabels(['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'])
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # 3. Quarterly patterns
    ax = axes[1, 0]
    for col, info in list(seasonality.items())[:3]:
        if 'quarterly_pattern' in info:
            quarters = list(info['quarterly_pattern'].keys())
            values = list(info['quarterly_pattern'].values())
            ax.bar([f'Q{q}' for q in quarters], values, alpha=0.7, label=col)
    ax.set_title('Quarterly Patterns')
    ax.set_xlabel('Quarter')
    ax.set_ylabel('Average Value')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # 4. Seasonality strength
    ax = axes[1, 1]
    seasonal_cols = [col for col, info in seasonality.items() 
                    if info.get('has_seasonality', False)]
    strengths = [info.get('seasonal_strength', 0) for info in seasonality.values()]
    
    if seasonal_cols:
        ax.barh(seasonal_cols, strengths[:len(seasonal_cols)], color='green')
        ax.set_xlabel('Seasonal Strength')
        ax.set_title('Seasonality Strength by Column')
        ax.axvline(0.5, color='red', linestyle='--', label='Strong Seasonality Threshold')
        ax.legend()
    else:
        ax.text(0.5, 0.5, 'No strong seasonality detected', 
               ha='center', va='center', transform=ax.transAxes)
        ax.set_title('Seasonality Strength')
    
    plt.suptitle('Seasonality Analysis', fontsize=16)
    plt.tight_layout()
    plt.show()