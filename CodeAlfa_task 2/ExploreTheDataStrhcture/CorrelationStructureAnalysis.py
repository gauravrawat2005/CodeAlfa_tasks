def analyze_correlation_structure(df):
    """Analyze relationships between variables"""
    
    # Select only numeric columns
    numeric_df = df.select_dtypes(include=[np.number])
    
    if len(numeric_df.columns) < 2:
        print("Not enough numeric columns for correlation analysis")
        return None
    
    # Correlation matrix
    corr_matrix = numeric_df.corr()
    
    # Find highly correlated pairs
    high_corr = []
    for i in range(len(corr_matrix.columns)):
        for j in range(i+1, len(corr_matrix.columns)):
            if abs(corr_matrix.iloc[i, j]) > 0.7:
                high_corr.append({
                    'var1': corr_matrix.columns[i],
                    'var2': corr_matrix.columns[j],
                    'correlation': corr_matrix.iloc[i, j]
                })
    
    # Multicollinearity check (VIF)
    from statsmodels.stats.outliers_influence import variance_inflation_factor
    
    vif_data = pd.DataFrame()
    vif_data["Variable"] = numeric_df.columns
    vif_data["VIF"] = [variance_inflation_factor(numeric_df.values, i) 
                       for i in range(numeric_df.shape[1])]
    
    # Visualize correlation matrix
    plt.figure(figsize=(12, 8))
    mask = np.triu(np.ones_like(corr_matrix), k=1)
    sns.heatmap(corr_matrix, mask=mask, annot=True, fmt='.2f', 
                cmap='RdBu_r', center=0, square=True)
    plt.title('Correlation Matrix (Numeric Variables)')
    plt.tight_layout()
    plt.show()
    
    return {
        'correlation_matrix': corr_matrix,
        'high_correlations': high_corr,
        'vif': vif_data
    }