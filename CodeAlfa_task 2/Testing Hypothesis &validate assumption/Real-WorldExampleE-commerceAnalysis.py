# Generate realistic e-commerce data
np.random.seed(42)
n_customers = 1000

ecommerce_data = pd.DataFrame({
    'customer_id': range(n_customers),
    'segment': np.random.choice(['New', 'Regular', 'VIP'], n_customers, p=[0.3, 0.5, 0.2]),
    'purchase_amount': np.concatenate([
        np.random.gamma(2, 20, 300),  # New customers
        np.random.gamma(3, 25, 500),  # Regular
        np.random.gamma(5, 30, 200)   # VIP
    ]),
    'time_on_site': np.random.exponential(300, n_customers),
    'pages_visited': np.random.poisson(5, n_customers),
    'returning_customer': np.random.choice([0, 1], n_customers, p=[0.4, 0.6]),
    'satisfaction_score': np.random.uniform(1, 5, n_customers)
})

# Hypothesis 1: VIP customers spend more than Regular customers
print("HYPOTHESIS 1: VIP vs Regular Spending")
print("="*50)

vip_spending = ecommerce_data[ecommerce_data['segment'] == 'VIP']['purchase_amount']
regular_spending = ecommerce_data[ecommerce_data['segment'] == 'Regular']['purchase_amount']

# Visualize
fig, axes = plt.subplots(1, 2, figsize=(12, 5))

axes[0].hist(vip_spending, alpha=0.5, label='VIP', bins=30)
axes[0].hist(regular_spending, alpha=0.5, label='Regular', bins=30)
axes[0].axvline(vip_spending.mean(), color='blue', linestyle='--', label=f'VIP Mean: ${vip_spending.mean():.2f}')
axes[0].axvline(regular_spending.mean(), color='orange', linestyle='--', label=f'Regular Mean: ${regular_spending.mean():.2f}')
axes[0].set_xlabel('Purchase Amount ($)')
axes[0].set_ylabel('Frequency')
axes[0].set_title('Spending Distribution by Segment')
axes[0].legend()

# Statistical test
t_stat, p_value = stats.ttest_ind(vip_spending, regular_spending)
effect_size = (vip_spending.mean() - regular_spending.mean()) / regular_spending.std()

axes[1].axis('off')
results_text = f"""
Statistical Results:
T-statistic: {t_stat:.4f}
P-value: {p_value:.4f}
Effect Size: {effect_size:.4f}

Conclusion:
{'Reject H₀' if p_value < 0.05 else 'Fail to reject H₀'}
VIP customers {'DO' if p_value < 0.05 else 'DO NOT'} spend significantly more
"""
axes[1].text(0.1, 0.5, results_text, fontsize=12, fontfamily='monospace')

plt.tight_layout()
plt.show()

# Hypothesis 2: Satisfaction score correlates with purchase amount
print("\nHYPOTHESIS 2: Satisfaction vs Purchase Amount Correlation")
print("="*50)

correlation, p_corr = stats.pearsonr(
    ecommerce_data['satisfaction_score'],
    ecommerce_data['purchase_amount']
)

plt.figure(figsize=(10, 6))
plt.scatter(ecommerce_data['satisfaction_score'], 
           ecommerce_data['purchase_amount'], 
           alpha=0.5, c='skyblue', edgecolors='darkblue')

# Add regression line
z = np.polyfit(ecommerce_data['satisfaction_score'], 
              ecommerce_data['purchase_amount'], 1)
p = np.poly1d(z)
plt.plot(ecommerce_data['satisfaction_score'].sort_values(),
         p(ecommerce_data['satisfaction_score'].sort_values()),
         'r--', linewidth=2, label=f'R² = {z[0]**2:.3f}')

plt.xlabel('Satisfaction Score (1-5)')
plt.ylabel('Purchase Amount ($)')
plt.title('Satisfaction Score vs Purchase Amount')
plt.grid(True, alpha=0.3)
plt.legend()

plt.figtext(0.15, 0.85, f'Correlation: {correlation:.3f}\nP-value: {p_corr:.4f}',
            bbox=dict(facecolor='white', alpha=0.8))

plt.show()