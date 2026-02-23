def visualize_data_structure(df):
    """Create visual representations of data structure"""
    
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    
    # 1. Data Types Distribution
    type_counts = df.dtypes.value_counts()
    axes[0, 0].pie(type_counts.values, labels=type_counts.index, autopct='%1.1f%%')
    axes[0, 0].set_title('Data Types Distribution')
    
    # 2. Missing Values Heatmap
    missing_df = df.isnull()
    sns.heatmap(missing_df.T, cmap='Reds', cbar_kws={'label': 'Missing'}, ax=axes[0, 1])
    axes[0, 1].set_title('Missing Values Pattern')
    axes[0, 1].set_xlabel('Rows')
    axes[0, 1].set_ylabel('Columns')
    
    # 3. Column Memory Usage
    memory_usage = df.memory_usage(deep=True)[1:].sort_values(ascending=False).head(15)
    axes[1, 0].barh(range(len(memory_usage)), memory_usage.values / 1024)  # Convert to KB
    axes[1, 0].set_yticks(range(len(memory_usage)))
    axes[1, 0].set_yticklabels(memory_usage.index)
    axes[1, 0].set_xlabel('Memory Usage (KB)')
    axes[1, 0].set_title('Top 15 Columns by Memory Usage')
    
    # 4. Unique Values Distribution
    unique_counts = df.nunique().sort_values(ascending=False).head(15)
    axes[1, 1].bar(range(len(unique_counts)), unique_counts.values)
    axes[1, 1].set_xticks(range(len(unique_counts)))
    axes[1, 1].set_xticklabels(unique_counts.index, rotation=45, ha='right')
    axes[1, 1].set_ylabel('Number of Unique Values')
    axes[1, 1].set_title('Columns with Most Unique Values')
    
    plt.tight_layout()
    plt.show()
    
    return fig