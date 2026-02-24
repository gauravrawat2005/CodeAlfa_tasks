def detect_time_series_issues(df, date_col, value_col):
    """Detect issues specific to time series data"""
    issues = []
    
    # Convert to datetime
    df[date_col] = pd.to_datetime(df[date_col])
    df = df.sort_values(date_col)
    
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    
    # 1. Check for missing dates
    date_range = pd.date_range(start=df[date_col].min(), 
                              end=df[date_col].max(), 
                              freq='D')
    missing_dates = set(date_range) - set(df[date_col])
    if missing_dates:
        issues.append(f"Missing {len(missing_dates)} dates in series")
        axes[0, 0].plot(date_range, [1]*len(date_range), 'g.', label='Expected')
        axes[0, 0].plot(list(missing_dates), [1]*len(missing_dates), 'r.', label='Missing')
        axes[0, 0].set_title('Missing Dates')
        axes[0, 0].legend()
    
    # 2. Check for duplicates
    duplicates = df[date_col].duplicated().sum()
    if duplicates > 0:
        issues.append(f"Found {duplicates} duplicate timestamps")
    
    # 3. Check for irregular intervals
    intervals = df[date_col].diff().dt.total_seconds() / 3600  # hours
    expected_interval = intervals.median()
    irregular = intervals[abs(intervals - expected_interval) > 1]
    if len(irregular) > 0:
        issues.append(f"Found {len(irregular)} irregular intervals")
        axes[0, 1].hist(intervals.dropna(), bins=50)
        axes[0, 1].axvline(expected_interval, color='r', linestyle='--', 
                          label=f'Expected: {expected_interval:.1f}h')
        axes[0, 1].set_title('Interval Distribution')
        axes[0, 1].legend()
    
    # 4. Check for outliers in values
    values = df[value_col]
    z_scores = np.abs(stats.zscore(values.dropna()))
    outliers = values[z_scores > 3]
    if len(outliers) > 0:
        issues.append(f"Found {len(outliers)} value outliers")
        axes[0, 2].plot(df[date_col], values, 'b-', alpha=0.7)
        axes[0, 2].plot(outliers.index, outliers, 'ro', label='Outliers')
        axes[0, 2].set_title('Time Series with Outliers')
        axes[0, 2].legend()
    
    # 5. Check for trends and seasonality
    from scipy import signal
    if len(values) > 30:
        # Detrend
        detrended = signal.detrend(values.dropna())
        axes[1, 0].plot(df[date_col][:len(detrended)], detrended)
        axes[1, 0].axhline(y=0, color='r', linestyle='--')
        axes[1, 0].set_title('Detrended Series')
        
        # Check for seasonality
        autocorrelation = pd.Series(values).autocorr()
        axes[1, 1].text(0.5, 0.5, f'Autocorrelation:\n{autocorrelation:.3f}', 
                       ha='center', va='center', fontsize=12)
        axes[1, 1].axis('off')
        axes[1, 1].set_title('Autocorrelation')
    
    # 6. Summary
    axes[1, 2].axis('off')
    summary_text = "TIME SERIES ISSUES SUMMARY\n"
    summary_text += "="*30 + "\n\n"
    for i, issue in enumerate(issues, 1):
        summary_text += f"{i}. {issue}\n"
    axes[1, 2].text(0.1, 0.9, summary_text, fontsize=10, 
                   verticalalignment='top', fontfamily='monospace')
    
    plt.suptitle('Time Series Data Quality Analysis', fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.show()
    
    return issues