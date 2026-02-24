def hypothesis_testing_decision_tree(data, group_col=None, target_col=None, test_type='auto'):
    """
    Automated hypothesis testing based on data characteristics
    """
    print("HYPOTHESIS TESTING DECISION TREE")
    print("="*50)
    
    if group_col and target_col:
        # Comparing groups
        groups = data[group_col].unique()
        
        if len(groups) == 2:
            # Two groups - choose appropriate test
            group1 = data[data[group_col] == groups[0]][target_col]
            group2 = data[data[group_col] == groups[1]][target_col]
            
            # Check normality
            _, p1 = stats.shapiro(group1[:5000])
            _, p2 = stats.shapiro(group2[:5000])
            
            if p1 > 0.05 and p2 > 0.05:
                print("✓ Data is normally distributed")
                print("→ Using Independent T-test")
                stat, p_value = stats.ttest_ind(group1, group2)
                test_used = "Independent T-test"
            else:
                print("⚠ Data is not normally distributed")
                print("→ Using Mann-Whitney U test")
                stat, p_value = stats.mannwhitneyu(group1, group2)
                test_used = "Mann-Whitney U"
        
        elif len(groups) > 2:
            # Multiple groups
            print(f"→ Multiple groups detected ({len(groups)})")
            
            # Test homogeneity of variances
            group_data = [data[data[group_col] == g][target_col] for g in groups]
            _, levene_p = stats.levene(*group_data)
            
            if levene_p > 0.05:
                print("✓ Variances are homogeneous")
                print("→ Using ANOVA")
                f_stat, p_value = stats.f_oneway(*group_data)
                test_used = "ANOVA"
            else:
                print("⚠ Variances are not homogeneous")
                print("→ Using Kruskal-Wallis H-test")
                h_stat, p_value = stats.kruskal(*group_data)
                test_used = "Kruskal-Wallis"
    
    elif target_col:
        # Single variable tests
        if test_type == 'mean':
            # One-sample t-test
            print("→ Testing against population mean")
            stat, p_value = stats.ttest_1samp(data[target_col], popmean=0)
            test_used = "One-sample T-test"
        
        elif test_type == 'normality':
            # Normality test
            stat, p_value = stats.shapiro(data[target_col][:5000])
            test_used = "Shapiro-Wilk"
    
    print(f"\nTest used: {test_used}")
    print(f"Test statistic: {stat:.4f}")
    print(f"P-value: {p_value:.4f}")
    
    if p_value < 0.05:
        print("✓ Result: Statistically significant (reject H₀)")
    else:
        print("✗ Result: Not statistically significant (fail to reject H₀)")
    
    return test_used, stat, p_value

# Example usage
np.random.seed(42)
test_data = pd.DataFrame({
    'group': np.repeat(['A', 'B', 'C'], 100),
    'value': np.concatenate([
        np.random.normal(100, 15, 100),
        np.random.normal(110, 15, 100),
        np.random.normal(90, 15, 100)
    ])
})

test_used, stat, p_value = hypothesis_testing_decision_tree(
    test_data, group_col='group', target_col='value'
)