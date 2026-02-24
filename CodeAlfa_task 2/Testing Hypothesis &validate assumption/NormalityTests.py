def check_normality(data, variable_name):
    """
    Comprehensive normality testing
    """
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    
    # Histogram with KDE
    axes[0, 0].hist(data, bins=30, density=True, alpha=0.7, color='skyblue', edgecolor='black')
    sns.kdeplot(data, color='red', ax=axes[0, 0])
    axes[0, 0].set_title('Histogram with KDE')
    axes[0, 0].set_xlabel(variable_name)
    
    # Q-Q plot
    stats.probplot(data, dist="norm", plot=axes[0, 1])
    axes[0, 1].set_title('Q-Q Plot')
    
    # Box plot
    axes[1, 0].boxplot(data, vert=False)
    axes[1, 0].set_title('Box Plot')
    axes[1, 0].set_xlabel(variable_name)
    
    # Statistical tests
    shapiro_stat, shapiro_p = stats.shapiro(data[:5000])  # Shapiro works best with n<5000
    ks_stat, ks_p = stats.kstest(data, 'norm', args=(np.mean(data), np.std(data)))
    anderson_stat = stats.anderson(data, dist='norm')
    
    # Display results
    axes[1, 1].axis('off')
    results_text = f"""
    NORMALITY TEST RESULTS
    {'='*30}
    
    Shapiro-Wilk Test:
    Statistic: {shapiro_stat:.4f}
    P-value: {shapiro_p:.4f}
    {'Normal' if shapiro_p > 0.05 else 'Not Normal'}
    
    Kolmogorov-Smirnov Test:
    Statistic: {ks_stat:.4f}
    P-value: {ks_p:.4f}
    {'Normal' if ks_p > 0.05 else 'Not Normal'}
    
    Anderson-Darling Test:
    Statistic: {anderson_stat.statistic:.4f}
    Critical values: {anderson_stat.critical_values}
    """
    
    axes[1, 1].text(0.1, 0.5, results_text, fontsize=10, 
                    verticalalignment='center', fontfamily='monospace')
    
    plt.tight_layout()
    plt.show()
    
    return {
        'shapiro': {'statistic': shapiro_stat, 'p_value': shapiro_p},
        'ks': {'statistic': ks_stat, 'p_value': ks_p},
        'anderson': {'statistic': anderson_stat.statistic, 
                     'critical_values': anderson_stat.critical_values}
    }

# Test
data = np.random.normal(0, 1, 1000)
normality_results = check_normality(data, 'Normal Distribution')