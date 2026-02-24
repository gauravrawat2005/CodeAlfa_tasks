# Create sample dataset with various issues
np.random.seed(42)
n_samples = 1000

problematic_data = pd.DataFrame({
    'id': range(n_samples),
    'age': np.concatenate([np.random.normal(35, 10, 950), [200, 210, 220, -5, -10, 300]]),
    'income': np.concatenate([np.random.normal(50000, 15000, 980), [1000000, 2000000]]),
    'category': np.random.choice(['A', 'B', 'C', ' D ', 'E'], n_samples, p=[0.3, 0.3, 0.2, 0.1, 0.1]),
    'score': np.random.uniform(0, 100, n_samples),
    'date': pd.date_range('2023-01-01', periods=n_samples, freq='H'),
    'text': ['Sample text ' + str(i) for i in range(n_samples)],
    'missing_col': np.where(np.random.random(n_samples) < 0.2, np.nan, np.random.normal(50, 10, n_samples))
})

# Introduce some issues
problematic_data.loc[100:150, 'age'] = np.nan  # Missing values
problematic_data.loc[200:205, 'income'] = np.nan  # Missing values
problematic_data.loc[300:302] = problematic_data.loc[100:102].values  # Duplicates

# Run quality pipeline
pipeline = DataQualityPipeline(problematic_data)
quality_report = pipeline.run_pipeline()