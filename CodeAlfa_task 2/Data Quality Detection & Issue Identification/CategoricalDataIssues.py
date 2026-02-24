def detect_categorical_issues(df, cat_cols):
    """Detect issues in categorical data"""
    issues = []
    
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    
    for idx, col in enumerate(cat_cols[:4]):  # Limit to 4 columns
        if idx < 4:
            row = idx // 2
            col_idx = idx % 2
            
            value_counts = df[col].value_counts()
            
            # Check for imbalance
            if len(value_counts) > 1:
                max_pct = value_counts.max() / len(df) * 100
                if max_pct > 90:
                    issues.append(f"Highly imbalanced category in {col}: {max_pct:.1f}% in one class")
                    axes[row, col_idx].set_title(f'{col} - Highly Imbalanced', color='red')
                elif max_pct > 70:
                    issues.append(f"Moderately imbalanced category in {col}: {max_pct:.1f}% in one class")
                    axes[row, col_idx].set_title(f'{col} - Moderately Imbalanced', color='orange')
            
            # Check for rare categories
            rare_cats = value_counts[value_counts < len(df) * 0.01]
            if len(rare_cats) > 0:
                issues.append(f"Found {len(rare_cats)} rare categories in {col}")
            
            # Plot
            value_counts.head(10).plot(kind='barh', ax=axes[row, col_idx])
            axes[row, col_idx].set_xlabel('Count')
            axes[row, col_idx].set_ylabel('Category')
    
    plt.suptitle('Categorical Data Analysis', fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.show()
    
    return issues