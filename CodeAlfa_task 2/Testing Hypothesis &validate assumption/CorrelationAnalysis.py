def correlation_analysis(df, method='pearson'):
    """
    Comprehensive correlation analysis with visualization
    """
    # Calculate correlation matrix
    if method == 'pearson':
        corr_matrix = df.corr(method='pearson')
        test_name = "Pearson"
    elif method == 'spearman':
        corr_matrix = df.corr(method='spearman')
        test_name = "Spearman"
    elif method == 'kendall':
        corr_matrix = df.corr(method='kendall')
        test_name = "Kendall"
    
    # Visualization
    fig = plt.figure(figsize=(15, 10))
    
    # Correlation heatmap
    ax1 = plt.subplot(2, 2, 1)
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0,
                square=True, linewidths=1, cbar_kws={"shrink": 0.8})
    ax1.set_title(f'{test_name} Correlation Matrix')
    
    # Pairplot for key relationships
    ax2 = plt.subplot(2, 2, 2)
    if len(df.columns) >= 2:
        # Select top 2 variables for scatter plot
        x_var = df.columns[0]
        y_var = df.columns[1]
        
        ax2.scatter(df[x_var], df[y_var], alpha=0.5)
        
        # Add regression line
        z = np.polyfit(df[x_var], df[y_var], 1)
        p = np.poly1d(z)
        ax2.plot(df[x_var].sort_values(), 
                p(df[x_var].sort_values()), 
                "r--", alpha=0.8, label=f'R² = {z[0]**2:.3f}')
        
        ax2.set_xlabel(x_var)
        ax2.set_ylabel(y_var)
        ax2.set_title(f'Scatter Plot: {x_var} vs {y_var}')
        ax2.legend()
    
    # Correlation bar chart
    ax3 = plt.subplot(2, 2, 3)
    if len(df.columns) >= 2:
        correlations = corr_matrix.iloc[0, 1:].sort_values()
        colors = ['red' if x < 0 else 'green' for x in correlations.values]
        correlations.plot(kind='barh', color=colors, ax=ax3)
        ax3.set_title(f'Correlations with {df.columns[0]}')
        ax3.set_xlabel('Correlation Coefficient')
    
    # P-values heatmap (for Pearson)
    ax4 = plt.subplot(2, 2, 4)
    if method == 'pearson':
        p_values = pd.DataFrame(index=df.columns, columns=df.columns)
        for i in df.columns:
            for j in df.columns:
                if i != j:
                    _, p_value = stats.pearsonr(df[i], df[j])
                    p_values.loc[i, j] = p_value
                else:
                    p_values.loc[i, j] = 0
        
        sns.heatmap(p_values.astype(float), annot=True, cmap='Reds_r',
                   square=True, linewidths=1, cbar_kws={"shrink": 0.8})
        ax4.set_title('P-values Matrix')
    
    plt.tight_layout()
    plt.show()
    
    # Statistical significance testing
    print(f"\n{test_name} CORRELATION ANALYSIS")
    print("="*50)
    
    significant_pairs = []
    for i in range(len(df.columns)):
        for j in range(i+1, len(df.columns)):
            if method == 'pearson':
                corr, p_value = stats.pearsonr(df.iloc[:, i], df.iloc[:, j])
            elif method == 'spearman':
                corr, p_value = stats.spearmanr(df.iloc[:, i], df.iloc[:, j])
            else:
                corr, p_value = stats.kendalltau(df.iloc[:, i], df.iloc[:, j])
            
            significance = "***" if p_value < 0.001 else "**" if p_value < 0.01 else "*" if p_value < 0.05 else "ns"
            print(f"{df.columns[i]} vs {df.columns[j]}: r = {corr:.4f}, p = {p_value:.4f} {significance}")
            
            if p_value < 0.05:
                significant_pairs.append((df.columns[i], df.columns[j], corr, p_value))
    
    return corr_matrix, significant_pairs

# Example usage
np.random.seed(42)
df_example = pd.DataFrame({
    'Sales': np.random.normal(1000, 200, 100),
    'Marketing_Spend': np.random.normal(500, 100, 100) + np.random.normal(0, 50, 100),
    'Customer_Satisfaction': np.random.normal(4.5, 0.5, 100),
    'Employee_Count': np.random.normal(50, 10, 100)
})

corr_matrix, sig_pairs = correlation_analysis(df_example, 'pearson')