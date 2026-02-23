# Load your data
df = pd.read_csv('your_dataset.csv')

# Create analyzer instance
analyzer = DataPatternAnalyzer(df, "Customer Transaction Data")

# Run complete analysis
results = analyzer.run_complete_analysis(generate_report=True)

# Access specific findings
trends = results['trends']
anomalies = results['anomalies']
patterns = results['patterns']
seasonality = results['seasonality']
correlations = results['correlations']

# Example: Print strongest trends
print("\n🔍 STRONGEST TRENDS:")
for col, info in sorted(trends.items(), 
                       key=lambda x: abs(x[1].get('r_squared', 0)), 
                       reverse=True)[:3]:
    print(f"{col}: {info['trend_direction']} (R²={info.get('r_squared', 0):.3f})")

# Example: Print top anomalies
print("\n🚨 TOP ANOMALIES:")
for col, info in sorted(anomalies.get('statistical_outliers', {}).items(),
                       key=lambda x: x[1]['count'], 
                       reverse=True)[:3]:
    print(f"{col}: {info['count']} anomalies ({info['percentage']:.1f}%)")