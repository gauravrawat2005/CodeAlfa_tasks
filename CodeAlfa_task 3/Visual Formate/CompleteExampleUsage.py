# Create sample dataset
np.random.seed(42)
n_samples = 1000

sample_data = pd.DataFrame({
    'date': pd.date_range('2023-01-01', periods=n_samples, freq='D'),
    'sales': np.random.normal(1000, 200, n_samples).cumsum(),
    'customers': np.random.poisson(50, n_samples).cumsum(),
    'revenue': np.random.normal(5000, 1000, n_samples).cumsum(),
    'category': np.random.choice(['Electronics', 'Clothing', 'Food', 'Books'], n_samples),
    'region': np.random.choice(['North', 'South', 'East', 'West'], n_samples),
    'satisfaction': np.random.uniform(1, 5, n_samples),
    'latitude': np.random.uniform(25, 50, n_samples),
    'longitude': np.random.uniform(-120, -70, n_samples)
})

# Initialize visualizer
visualizer = DataVisualizer(sample_data, "Sales Analysis")

# Create various visualizations
visualizer.create_univariate_plots(['sales', 'customers', 'revenue', 'category'])
visualizer.create_bivariate_plots('sales', 'revenue', 'region')
visualizer.create_multivariate_plots()
visualizer.create_time_series_plots('date', ['sales', 'customers', 'revenue'])
visualizer.create_interactive_plots()

# Create geospatial visualization
create_geospatial_visualization(sample_data, 'latitude', 'longitude', 'sales')

# Launch interactive dashboard
dashboard = InteractiveDashboard(sample_data, "Sales Dashboard")
# dashboard.run()  # Uncomment to run dashboard