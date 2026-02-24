# Create an executive dashboard with key insights
fig = plt.figure(figsize=(18, 12))
fig.patch.set_facecolor('#f0f2f5')

# Define layout
gs = fig.add_gridspec(3, 6, hspace=0.3, wspace=0.3)

# 1. Key Metrics Cards (Top Row)
metric_positions = [(0, i) for i in range(6)]
metrics_data = [
    ('Revenue', '$2.4M', '+15%', '↑', 'green'),
    ('Customers', '1,892', '+8%', '↑', 'green'),
    ('Market Share', '23.5%', '+2.1%', '↑', 'green'),
    ('Satisfaction', '4.2/5', '-0.3', '↓', 'red'),
    ('Profit Margin', '18.4%', '+1.2%', '↑', 'green'),
    ('Cash Flow', '$845K', '-5%', '↓', 'orange')
]

for idx, (metric, value, change, arrow, color) in enumerate(metrics_data):
    ax = fig.add_subplot(gs[0, idx])
    ax.set_facecolor('white')
    ax.axis('off')
    
    # Add a card-like appearance
    rect = Rectangle((0, 0), 1, 1, transform=ax.transAxes, 
                    facecolor='white', edgecolor='lightgray', linewidth=1)
    ax.add_patch(rect)
    
    # Add metric content
    ax.text(0.5, 0.7, metric, ha='center', va='center', fontsize=10, color='gray')
    ax.text(0.5, 0.4, value, ha='center', va='center', fontsize=16, fontweight='bold')
    ax.text(0.5, 0.15, f'{arrow} {change}', ha='center', va='center', 
           fontsize=10, color=color, fontweight='bold')

# 2. Main Performance Story (Middle Row, spanning multiple columns)
ax_main = fig.add_subplot(gs[1, :4])
ax_main.set_facecolor('white')

# Create compelling narrative with annotations
x = np.arange(12)
y1 = 100 + np.cumsum(np.random.normal(2, 5, 12))
y2 = y1 * 0.7 + np.random.normal(0, 10, 12)

ax_main.plot(x, y1, linewidth=3, color='#2E86AB', marker='o', label='Actual Performance')
ax_main.plot(x, y2, linewidth=2, color='#A23B72', linestyle='--', label='Industry Average')
ax_main.fill_between(x, y1, y2, where=(y1>y2), alpha=0.3, color='green', 
                     interpolate=True, label='Outperforming')
ax_main.fill_between(x, y1, y2, where=(y1<=y2), alpha=0.3, color='red', 
                     interpolate=True, label='Underperforming')

# Add key insight annotations
ax_main.annotate('Strategic Initiative Launch\n(Q2 2023)', 
                xy=(3, y1[3]), xytext=(1, y1[3]+30),
                arrowprops=dict(arrowstyle='->', color='green', lw=2),
                bbox=dict(boxstyle='round,pad=0.3', facecolor='lightgreen', alpha=0.7))

ax_main.annotate('Market Challenge\n(Q3 2023)', 
                xy=(6, y1[6]), xytext=(4, y1[6]-40),
                arrowprops=dict(arrowstyle='->', color='red', lw=2),
                bbox=dict(boxstyle='round,pad=0.3', facecolor='#ffcccc', alpha=0.7))

ax_main.axhline(y=y1.mean(), color='gray', linestyle=':', alpha=0.7, label='Target')

ax_main.set_xlabel('Months (2023-2024)', fontsize=11, fontweight='bold')
ax_main.set_ylabel('Performance Index', fontsize=11, fontweight='bold')
ax_main.set_title('Performance Story: How Strategic Actions Drove Results', 
                 fontsize=14, fontweight='bold')
ax_main.legend(loc='upper left')
ax_main.grid(True, alpha=0.3)

# 3. Opportunity Analysis (Middle Row, right side)
ax_opp = fig.add_subplot(gs[1, 4:])
ax_opp.set_facecolor('white')

# Market opportunity matrix
opportunities = ['New Markets', 'Product Lines', 'Partnerships', 'Digital', 'Cost Savings']
current = [40, 60, 30, 50, 70]
potential = [85, 75, 65, 90, 45]

y_pos = np.arange(len(opportunities))
ax_opp.barh(y_pos - 0.2, current, 0.4, label='Current', color='#2E86AB', alpha=0.7)
ax_opp.barh(y_pos + 0.2, potential, 0.4, label='Potential', color='#F18F01', alpha=0.7)
ax_opp.set_yticks(y_pos)
ax_opp.set_yticklabels(opportunities)
ax_opp.set_xlabel('Market Penetration %')
ax_opp.set_title('Growth Opportunities Gap Analysis', fontsize=12, fontweight='bold')
ax_opp.legend()
ax_opp.grid(True, alpha=0.3, axis='x')

# Add gap labels
for i, (c, p) in enumerate(zip(current, potential)):
    gap = p - c
    ax_opp.text(max(c, p) + 2, i, f'Gap: {gap}%', va='center', fontsize=8, 
               fontweight='bold', color='darkgreen' if gap > 0 else 'darkred')

# 4. Bottom Row - Detailed Insights
# Risk Matrix
ax_risk = fig.add_subplot(gs[2, :2])
ax_risk.set_facecolor('white')

risks = ['Market Volatility', 'Competition', 'Regulatory', 'Tech Disruption', 'Talent']
impact = [8, 7, 5, 6, 4]
probability = [6, 8, 3, 7, 5]

ax_risk.scatter(probability, impact, s=[i*100 for i in impact], 
               c=range(len(risks)), cmap='RdYlGn_r', alpha=0.7)
for i, risk in enumerate(risks):
    ax_risk.annotate(risk, (probability[i]+0.2, impact[i]-0.1), fontsize=8)
    
ax_risk.set_xlabel('Probability (1-10)', fontsize=10)
ax_risk.set_ylabel('Impact (1-10)', fontsize=10)
ax_risk.set_title('Risk Assessment Matrix', fontsize=11, fontweight='bold')
ax_risk.grid(True, alpha=0.3)
ax_risk.set_xlim(0, 10)
ax_risk.set_ylim(0, 10)

# Customer Insights
ax_cust = fig.add_subplot(gs[2, 2:4])
ax_cust.set_facecolor('white')

segments = ['Enterprise', 'Mid-Market', 'SMB', 'Startup']
values = [45, 30, 15, 10]
explode = (0.05, 0, 0, 0)
colors = ['#2E86AB', '#A23B72', '#F18F01', '#C73E1D']

wedges, texts, autotexts = ax_cust.pie(values, explode=explode, labels=segments, 
                                       colors=colors, autopct='%1.1f%%',
                                       shadow=True, startangle=90)
ax_cust.set_title('Customer Segment Revenue Distribution', fontsize=11, fontweight='bold')

# Action Items
ax_action = fig.add_subplot(gs[2, 4:])
ax_action.axis('off')
ax_action.set_facecolor('#f0f2f5')

action_items = [
    '🔴 URGENT: Address satisfaction decline in Q2',
    '🟡 HIGH: Launch new product line by June',
    '🟢 MEDIUM: Expand into Asian market',
    '🟢 MEDIUM: Optimize cost structure',
    '🔵 LOW: Update employee training program'
]

ax_action.text(0.5, 0.95, 'RECOMMENDED ACTIONS', 
              ha='center', fontsize=12, fontweight='bold', color='navy')

for i, action in enumerate(action_items):
    y_pos = 0.8 - i*0.12
    ax_action.text(0.1, y_pos, action, ha='left', va='center', fontsize=10,
                  bbox=dict(boxstyle='round,pad=0.3', facecolor='white', 
                           edgecolor='lightgray', alpha=0.9))

# Add expected impact
ax_action.text(0.5, 0.15, 'Expected Impact: +15-20% Growth', 
              ha='center', fontsize=11, fontweight='bold', color='green',
              bbox=dict(boxstyle='round,pad=0.5', facecolor='#e6ffe6', 
                       edgecolor='green', alpha=0.9))

plt.suptitle('EXECUTIVE INSIGHTS DASHBOARD: Data-Driven Decision Making\n', 
            fontsize=18, fontweight='bold', y=1.02)
plt.show()