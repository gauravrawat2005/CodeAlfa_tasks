def data_quality_report(df):
    """Comprehensive data quality assessment"""
    
    quality_issues = []
    
    for column in df.columns:
        col_issues = []
        
        # Check for missing values
        missing_pct = (df[column].isnull().sum() / len(df)) * 100
        if missing_pct > 20:
            col_issues.append(f"High missingness: {missing_pct:.1f}%")
        elif missing_pct > 5:
            col_issues.append(f"Moderate missingness: {missing_pct:.1f}%")
        
        # Check data types
        if pd.api.types.is_numeric_dtype(df[column]):
            # Check for outliers (IQR method)
            Q1 = df[column].quantile(0.25)
            Q3 = df[column].quantile(0.75)
            IQR = Q3 - Q1
            outliers = ((df[column] < (Q1 - 1.5 * IQR)) | (df[column] > (Q3 + 1.5 * IQR))).sum()
            if outliers > 0:
                col_issues.append(f"{outliers} outliers detected")
            
            # Check for zeros where shouldn't be
            if column not in ['count', 'zero_measure']:  # Adjust based on context
                zeros = (df[column] == 0).sum()
                if zeros > len(df) * 0.1:  # More than 10% zeros
                    col_issues.append(f"High zero count: {zeros:,}")
        
        elif pd.api.types.is_object_dtype(df[column]):
            # Check for inconsistent formatting
            if df[column].str.len().std() > 10:  # High variance in string length
                col_issues.append("Inconsistent string lengths")
            
            # Check for mixed case issues
            if df[column].str.islower().mean() < 0.5 and df[column].str.isupper().mean() < 0.5:
                col_issues.append("Mixed case formatting")
        
        if col_issues:
            quality_issues.append({
                'column': column,
                'issues': col_issues
            })
    
    # Summary statistics
    print("\n📊 DATA QUALITY REPORT")
    print("=" * 50)
    print(f"Total columns with issues: {len(quality_issues)}/{len(df.columns)}")
    
    if quality_issues:
        print("\nIssues by column:")
        for issue in quality_issues:
            print(f"\n• {issue['column']}:")
            for i in issue['issues']:
                print(f"  - {i}")
    else:
        print("\n✅ No significant data quality issues detected!")
    
    return quality_issues