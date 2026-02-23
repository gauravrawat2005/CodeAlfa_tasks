def analyze_variables(df):
    """Deep dive into each variable's structure"""
    
    analysis = {}
    
    for column in df.columns:
        col_info = {
            'data_type': df[column].dtype,
            'null_count': df[column].isnull().sum(),
            'null_percentage': (df[column].isnull().sum() / len(df)) * 100,
            'unique_values': df[column].nunique(),
            'sample_values': df[column].dropna().sample(min(5, len(df))).tolist()
        }
        
        # Numeric column statistics
        if pd.api.types.is_numeric_dtype(df[column]):
            col_info.update({
                'min': df[column].min(),
                'max': df[column].max(),
                'mean': df[column].mean(),
                'median': df[column].median(),
                'std': df[column].std(),
                'skewness': df[column].skew(),
                'kurtosis': df[column].kurtosis(),
                'zeros': (df[column] == 0).sum(),
                'negatives': (df[column] < 0).sum() if df[column].min() < 0 else 0
            })
        
        # Categorical column statistics
        elif pd.api.types.is_object_dtype(df[column]) or pd.api.types.is_categorical_dtype(df[column]):
            value_counts = df[column].value_counts()
            col_info.update({
                'top_value': value_counts.index[0] if len(value_counts) > 0 else None,
                'top_frequency': value_counts.iloc[0] if len(value_counts) > 0 else 0,
                'value_distribution': value_counts.head(10).to_dict()
            })
        
        # DateTime column statistics
        elif pd.api.types.is_datetime64_any_dtype(df[column]):
            col_info.update({
                'min_date': df[column].min(),
                'max_date': df[column].max(),
                'date_range_days': (df[column].max() - df[column].min()).days,
                'most_common_year': df[column].dt.year.mode()[0] if len(df[column].dt.year.mode()) > 0 else None
            })
        
        analysis[column] = col_info
    
    return analysis

# Display analysis in readable format
def display_variable_analysis(analysis):
    """Format and display variable analysis"""
    
    for col, info in analysis.items():
        print(f"\n{'─'*50}")
        print(f"🔍 Column: {col}")
        print(f"{'─'*50}")
        
        # Basic info
        print(f"Type: {info['data_type']}")
        print(f"Missing: {info['null_count']:,} ({info['null_percentage']:.1f}%)")
        print(f"Unique Values: {info['unique_values']:,}")
        
        # Type-specific info
        if 'mean' in info:  # Numeric
            print(f"\n📊 Numeric Statistics:")
            print(f"  Min: {info['min']:.2f}")
            print(f"  Max: {info['max']:.2f}")
            print(f"  Mean: {info['mean']:.2f}")
            print(f"  Median: {info['median']:.2f}")
            print(f"  Std Dev: {info['std']:.2f}")
            print(f"  Skewness: {info['skewness']:.2f}")
            print(f"  Zeros: {info['zeros']:,}")
            
        elif 'top_value' in info:  # Categorical
            print(f"\n📑 Top Categories:")
            for val, count in list(info['value_distribution'].items())[:5]:
                print(f"  • {val}: {count:,} ({count/sum(info['value_distribution'].values())*100:.1f}%)")
                
        elif 'min_date' in info:  # DateTime
            print(f"\n📅 Date Range:")
            print(f"  From: {info['min_date']}")
            print(f"  To: {info['max_date']}")
            print(f"  Span: {info['date_range_days']} days")
        
        print(f"\nSample values: {info['sample_values']}")