import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta

# Set the style
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

# Create sample sales data
np.random.seed(42)
dates = pd.date_range(start='2023-01-01', end='2023-12-31', freq='D')
sales_data = pd.DataFrame({
    'date': dates,
    'sales': np.random.normal(1000, 200, len(dates)) + 
             np.sin(np.arange(len(dates)) * 2 * np.pi / 365) * 300,
    'region': np.random.choice(['North', 'South', 'East', 'West'], len(dates)),
    'product': np.random.choice(['Electronics', 'Clothing', 'Food', 'Books'], len(dates))
})

# Create a multi-panel figure
fig = plt.figure(figsize=(16, 10))

# 1. Time Series with Trend (Top Left)
ax1 = plt.subplot(2, 3, 1)
monthly_sales = sales_data.resample('M', on='date')['sales'].mean()
ax1.plot(monthly_sales.index, monthly_sales.values, 
         marker='o', linewidth=2, markersize=4, color='#2E86AB')
ax1.fill_between(monthly_sales.index, monthly_sales.values, alpha=0.3)
ax1.set_title('Monthly Sales Trend', fontsize=14, fontweight='bold')
ax1.set_xlabel('Month')
ax1.set_ylabel('Average Sales ($)')
ax1.tick_params(axis='x', rotation=45)

# 2. Regional Distribution (Top Middle)
ax2 = plt.subplot(2, 3, 2)
region_sales = sales_data.groupby('region')['sales'].mean().sort_values()
bars = ax2.barh(region_sales.index, region_sales.values, color='#A23B72')
ax2.set_title('Average Sales by Region', fontsize=14, fontweight='bold')
ax2.set_xlabel('Average Sales ($)')
# Add value labels
for i, (bar, val) in enumerate(zip(bars, region_sales.values)):
    ax2.text(val + 10, bar.get_y() + bar.get_height()/2, 
             f'${val:.0f}', va='center')

# 3. Product Performance (Top Right)
ax3 = plt.subplot(2, 3, 3)
product_sales = sales_data.groupby('product')['sales'].agg(['mean', 'std']).round()
product_sales['mean'].plot(kind='bar', ax=ax3, yerr=product_sales['std'], 
                           capsize=5, color=['#F18F01', '#C73E1D', '#2E86AB', '#A23B72'])
ax3.set_title('Product Performance with Variability', fontsize=14, fontweight='bold')
ax3.set_xlabel('Product')
ax3.set_ylabel('Average Sales ($)')
ax3.tick_params(axis='x', rotation=45)

# 4. Sales Distribution (Bottom Left)
ax4 = plt.subplot(2, 3, 4)
sns.histplot(data=sales_data, x='sales', bins=30, kde=True, ax=ax4, color='#2E86AB')
ax4.axvline(sales_data['sales'].mean(), color='red', linestyle='--', 
            label=f"Mean: ${sales_data['sales'].mean():.0f}")
ax4.axvline(sales_data['sales'].median(), color='green', linestyle=':', 
            label=f"Median: ${sales_data['sales'].median():.0f}")
ax4.set_title('Sales Distribution', fontsize=14, fontweight='bold')
ax4.set_xlabel('Sales ($)')
ax4.set_ylabel('Frequency')
ax4.legend()

# 5. Correlation Heatmap (Bottom Middle)
ax5 = plt.subplot(2, 3, 5)
# Create numeric columns for correlation
sales_data_numeric = sales_data.copy()
sales_data_numeric['dayofweek'] = sales_data['date'].dt.dayofweek
sales_data_numeric['month'] = sales_data['date'].dt.month
corr_matrix = sales_data_numeric[['sales', 'dayofweek', 'month']].corr()
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0, ax=ax5,
            square=True, linewidths=1, cbar_kws={"shrink": 0.8})
ax5.set_title('Correlation Analysis', fontsize=14, fontweight='bold')

# 6. Sales by Region and Product (Bottom Right)
ax6 = plt.subplot(2, 3, 6)
pivot_table = sales_data.pivot_table(values='sales', 
                                      index='region', 
                                      columns='product', 
                                      aggfunc='mean')
sns.heatmap(pivot_table, annot=True, fmt='.0f', cmap='YlOrRd', ax=ax6,
            linewidths=1, cbar_kws={"shrink": 0.8})
ax6.set_title('Regional Product Performance', fontsize=14, fontweight='bold')

plt.tight_layout()
plt.suptitle('Sales Performance Dashboard 2023', fontsize=18, fontweight='bold', y=1.02)
plt.show()