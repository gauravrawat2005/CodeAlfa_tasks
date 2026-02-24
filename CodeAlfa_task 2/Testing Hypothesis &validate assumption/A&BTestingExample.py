def ab_test_analysis(control_data, treatment_data, alpha=0.05):
    """
    Perform A/B test analysis with visualization
    """
    # Calculate statistics
    control_mean = np.mean(control_data)
    treatment_mean = np.mean(treatment_data)
    
    # T-test
    t_stat, p_value = stats.ttest_ind(control_data, treatment_data)
    
    # Effect size (Cohen's d)
    pooled_std = np.sqrt((np.std(control_data)**2 + np.std(treatment_data)**2) / 2)
    cohens_d = (treatment_mean - control_mean) / pooled_std
    
    # Visualization
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    
    # Distribution plot
    axes[0].hist(control_data, alpha=0.5, label='Control', bins=20)
    axes[0].hist(treatment_data, alpha=0.5, label='Treatment', bins=20)
    axes[0].axvline(control_mean, color='blue', linestyle='--', label=f'Control Mean: {control_mean:.2f}')
    axes[0].axvline(treatment_mean, color='orange', linestyle='--', label=f'Treatment Mean: {treatment_mean:.2f}')
    axes[0].set_xlabel('Value')
    axes[0].set_ylabel('Frequency')
    axes[0].set_title('Distribution Comparison')
    axes[0].legend()
    
    # Box plot
    data_to_plot = [control_data, treatment_data]
    axes[1].boxplot(data_to_plot, labels=['Control', 'Treatment'])
    axes[1].set_ylabel('Value')
    axes[1].set_title('Box Plot Comparison')
    
    # Confidence intervals
    control_ci = stats.t.interval(0.95, len(control_data)-1, 
                                  loc=control_mean, 
                                  scale=stats.sem(control_data))
    treatment_ci = stats.t.interval(0.95, len(treatment_data)-1,
                                    loc=treatment_mean,
                                    scale=stats.sem(treatment_data))
    
    axes[2].errorbar(['Control', 'Treatment'], 
                     [control_mean, treatment_mean],
                     yerr=[[control_mean - control_ci[0], treatment_mean - treatment_ci[0]],
                           [control_ci[1] - control_mean, treatment_ci[1] - treatment_mean]],
                     fmt='o', capsize=5, capthick=2)
    axes[2].set_ylabel('Mean Value')
    axes[2].set_title('95% Confidence Intervals')
    
    plt.tight_layout()
    plt.show()
    
    # Results
    print("="*50)
    print("A/B TEST RESULTS")
    print("="*50)
    print(f"Control Mean: {control_mean:.4f}")
    print(f"Treatment Mean: {treatment_mean:.4f}")
    print(f"Difference: {treatment_mean - control_mean:.4f}")
    print(f"T-statistic: {t_stat:.4f}")
    print(f"P-value: {p_value:.4f}")
    print(f"Cohen's d (Effect Size): {cohens_d:.4f}")
    print(f"Significant at α={alpha}: {'Yes' if p_value < alpha else 'No'}")
    
    return {
        'control_mean': control_mean,
        'treatment_mean': treatment_mean,
        't_stat': t_stat,
        'p_value': p_value,
        'cohens_d': cohens_d,
        'significant': p_value < alpha
    }

# Example data
np.random.seed(42)
control = np.random.normal(100, 15, 1000)  # Control group
treatment = np.random.normal(105, 15, 1000)  # Treatment group

results = ab_test_analysis(control, treatment)