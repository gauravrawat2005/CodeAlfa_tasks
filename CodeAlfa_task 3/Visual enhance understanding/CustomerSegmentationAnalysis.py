# Customer segmentation visualization
np.random.seed(42)
n_customers = 500

customer_data = pd.DataFrame({
    'customer_id': range(n_customers),
    'age': np.random.normal(40, 15, n_customers).clip(18, 80),
    'annual_income': np.random.normal(60000, 25000, n_customers).clip(20000, 150000),
    'spending_score': np.random.normal(50, 25, n_customers).clip(1, 100),
    'purchase_frequency': np.random.normal(10, 5, n_customers).clip(1, 30),
    'loyalty_years': np.random.exponential(3, n_customers).clip(0, 15)
})

fig, axes = plt.subplots(2, 3, figsize=(18, 10))

# 1. Customer Segmentation Scatter Plot
scatter = axes[0, 0].scatter(customer_data['annual_income'], 
                            customer_data['spending_score'],
                            c=customer_data['age'], 
                            s=customer_data['purchase_frequency']*20,
                            alpha=0.6, cmap='viridis')
axes[0, 0].set_xlabel('Annual Income ($)')
axes[0, 0].set_ylabel('Spending Score')
axes[0, 0].set_title('Customer Segments\n(Size = Purchase Frequency, Color = Age)')
plt.colorbar(scatter, ax=axes[0, 0], label='Age')

# 2. Age Distribution by Segments
axes[0, 1].hist([customer_data[customer_data['spending_score'] > 70]['age'],
                 customer_data[(customer_data['spending_score'] <= 70) & 
                               (customer_data['spending_score'] > 30)]['age'],
                 customer_data[customer_data['spending_score'] <= 30]['age']],
                label=['High Spenders', 'Medium Spenders', 'Low Spenders'],
                bins=15, alpha=0.7, edgecolor='black')
axes[0, 1].set_xlabel('Age')
axes[0, 1].set_ylabel('Frequency')
axes[0, 1].set_title('Age Distribution by Spending Segment')
axes[0, 1].legend()

# 3. Loyalty Analysis
axes[0, 2].scatter(customer_data['loyalty_years'], 
                   customer_data['spending_score'],
                   alpha=0.5, c='darkblue')
z = np.polyfit(customer_data['loyalty_years'], customer_data['spending_score'], 1)
p = np.poly1d(z)
axes[0, 2].plot(customer_data['loyalty_years'].sort_values(), 
                p(customer_data['loyalty_years'].sort_values()), 
                "r--", alpha=0.8, label='Trend')
axes[0, 2].set_xlabel('Loyalty Years')
axes[0, 2].set_ylabel('Spending Score')
axes[0, 2].set_title('Loyalty vs Spending')
axes[0, 2].legend()

# 4. Income Distribution by Segment (Violin Plot)
segments = ['Low Spender', 'Medium Spender', 'High Spender']
customer_data['segment'] = pd.cut(customer_data['spending_score'], 
                                  bins=[0, 30, 70, 100], 
                                  labels=segments)
sns.violinplot(data=customer_data, x='segment', y='annual_income', ax=axes[1, 0])
axes[1, 0].set_title('Income Distribution by Customer Segment')
axes[1, 0].set_xlabel('Customer Segment')
axes[1, 0].set_ylabel('Annual Income ($)')

# 5. Purchase Behavior Heatmap
pivot_behavior = customer_data.pivot_table(
    values='spending_score',
    index=pd.cut(customer_data['age'], bins=[18, 30, 45, 60, 80]),
    columns=pd.cut(customer_data['annual_income'], 
                   bins=[20000, 40000, 60000, 80000, 100000, 150000]),
    aggfunc='mean'
)
sns.heatmap(pivot_behavior, annot=True, fmt='.1f', cmap='YlGnBu', ax=axes[1, 1],
            cbar_kws={'label': 'Average Spending Score'})
axes[1, 1].set_title('Spending Patterns: Age vs Income')
axes[1, 1].set_xlabel('Income Bracket')
axes[1, 1].set_ylabel('Age Group')

# 6. Customer Lifetime Value Components
components = ['Age', 'Income', 'Spending', 'Frequency', 'Loyalty']
values = [customer_data['age'].mean()/80*100,
          customer_data['annual_income'].mean()/150000*100,
          customer_data['spending_score'].mean(),
          customer_data['purchase_frequency'].mean()/30*100,
          customer_data['loyalty_years'].mean()/15*100]
colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFE194']
axes[1, 2].bar(components, values, color=colors, alpha=0.7)
axes[1, 2].set_ylabel('Normalized Score (%)')
axes[1, 2].set_title('Customer Profile Components')
axes[1, 2].set_ylim(0, 100)
# Add value labels
for i, v in enumerate(values):
    axes[1, 2].text(i, v + 2, f'{v:.1f}%', ha='center')

plt.tight_layout()
plt.suptitle('Customer Segmentation Analysis Dashboard', fontsize=16, fontweight='bold', y=1.02)
plt.show()