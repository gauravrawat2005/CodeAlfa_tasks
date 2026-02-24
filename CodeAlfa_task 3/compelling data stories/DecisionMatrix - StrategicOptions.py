# Create a strategic decision-making visualization
fig, axes = plt.subplots(2, 3, figsize=(18, 10))
fig.patch.set_facecolor('#f8f9fa')

# Sample strategic options data
options = ['Option A: Aggressive Growth', 'Option B: Market Consolidation', 
           'Option C: Innovation Focus', 'Option D: Cost Optimization']
metrics = ['ROI (%)', 'Risk Level', 'Time to Market (months)', 
           'Resource Need', 'Competitive Advantage']

# Create decision matrix data
np.random.seed(123)
decision_data = pd.DataFrame({
    'Option': options,
    'ROI': np.random.uniform(15, 35, 4),
    'Risk': np.random.uniform(20, 70, 4),
    'Time': np.random.uniform(6, 24, 4),
    'Resources': np.random.uniform(40, 90, 4),
    'Advantage': np.random.uniform(30, 95, 4)
})

# 1. Bubble Chart Decision Matrix
ax1 = axes[0, 0]
scatter = ax1.scatter(decision_data['Risk'], decision_data['ROI'], 
                     s=decision_data['Resources']*20, 
                     c=decision_data['Advantage'], 
                     cmap='RdYlGn', alpha=0.7, edgecolors='black', linewidth=1)

# Add labels for each option
for i, option in enumerate(decision_data['Option']):
    ax1.annotate(f'{i+1}', 
                (decision_data.iloc[i]['Risk'], decision_data.iloc[i]['ROI']),
                fontsize=12, fontweight='bold', ha='center', va='center')

ax1.set_xlabel('Risk Level (%)', fontsize=11, fontweight='bold')
ax1.set_ylabel('Expected ROI (%)', fontsize=11, fontweight='bold')
ax1.set_title('Strategic Options Matrix\n(Bubble size = Resource Needs, Color = Competitive Advantage)', 
             fontsize=12, fontweight='bold')
ax1.grid(True, alpha=0.3)
plt.colorbar(scatter, ax=ax1, label='Advantage Score')

# Add quadrant lines
ax1.axhline(y=25, color='gray', linestyle='--', alpha=0.5)
ax1.axvline(x=45, color='gray', linestyle='--', alpha=0.5)

# Add quadrant labels
ax1.text(25, 32, 'SWEET SPOT', fontsize=10, fontweight='bold', ha='center', color='green')
ax1.text(65, 32, 'HIGH RISK/HIGH REWARD', fontsize=9, ha='center', color='orange')
ax1.text(25, 18, 'SAFE BET', fontsize=9, ha='center', color='blue')
ax1.text(65, 18, 'AVOID', fontsize=9, ha='center', color='red')

# 2. Radar Chart for Option Comparison
from math import pi

ax2 = axes[0, 1]
categories = ['ROI', 'Low Risk', 'Speed', 'Efficiency', 'Advantage']
N = len(categories)

# Create angles for radar chart
angles = [n / float(N) * 2 * pi for n in range(N)]
angles += angles[:1]

# Plot each option
for idx, option in enumerate(decision_data['Option']):
    values = [decision_data.iloc[idx]['ROI']/40*100,  # Normalize
              100 - decision_data.iloc[idx]['Risk'],  # Invert risk
              100 - decision_data.iloc[idx]['Time']/24*100,  # Invert time
              100 - decision_data.iloc[idx]['Resources'],  # Invert resources
              decision_data.iloc[idx]['Advantage']]
    values += values[:1]
    
    ax2.plot(angles, values, 'o-', linewidth=2, label=f'Option {idx+1}')
    ax2.fill(angles, values, alpha=0.1)

ax2.set_xticks(angles[:-1])
ax2.set_xticklabels(categories, fontsize=9)
ax2.set_ylim(0, 100)
ax2.set_title('Strategic Option Profiles', fontsize=12, fontweight='bold')
ax2.legend(loc='upper right', bbox_to_anchor=(1.3, 1.0))
ax2.grid(True)

# 3. Decision Tree
ax3 = axes[0, 2]
ax3.axis('off')
ax3.set_title('Decision Framework', fontsize=12, fontweight='bold')

# Draw decision tree
def draw_decision_node(ax, x, y, text, box_style='round'):
    bbox_props = dict(boxstyle=f"{box_style},pad=0.3", facecolor="lightblue", 
                      edgecolor="navy", linewidth=2)
    ax.text(x, y, text, ha='center', va='center', fontsize=9,
           bbox=bbox_props)

def draw_decision_branch(ax, x1, y1, x2, y2, text='', pos=0.5):
    ax.plot([x1, x2], [y1, y2], 'k-', linewidth=1.5, alpha=0.7)
    if text:
        mx, my = x1 + (x2-x1)*pos, y1 + (y2-y1)*pos
        ax.text(mx, my+0.05, text, ha='center', va='bottom', fontsize=8,
               bbox=dict(boxstyle="round,pad=0.2", facecolor="white", alpha=0.7))

# Build decision tree
draw_decision_node(ax3, 0.5, 0.9, 'Strategic Decision\n2024')
draw_decision_node(ax3, 0.3, 0.7, 'Grow Market?')
draw_decision_node(ax3, 0.7, 0.7, 'Optimize?')

draw_decision_branch(ax3, 0.5, 0.86, 0.3, 0.73, 'Yes')
draw_decision_branch(ax3, 0.5, 0.86, 0.7, 0.73, 'No')

draw_decision_node(ax3, 0.15, 0.5, 'Option A\nAggressive')
draw_decision_node(ax3, 0.45, 0.5, 'Option C\nInnovation')
draw_decision_node(ax3, 0.55, 0.5, 'Option B\nConsolidate')
draw_decision_node(ax3, 0.85, 0.5, 'Option D\nCost Cut')

# 4. Risk-Reward Waterfall
ax4 = axes[1, 0]
options_short = ['A', 'B', 'C', 'D']
rewards = decision_data['ROI']
risks = decision_data['Risk']

x_pos = np.arange(len(options_short))
width = 0.35

ax4.bar(x_pos - width/2, rewards, width, label='Reward (ROI)', color='green', alpha=0.7)
ax4.bar(x_pos + width/2, risks, width, label='Risk Level', color='red', alpha=0.5)

ax4.set_xlabel('Strategic Options', fontsize=11, fontweight='bold')
ax4.set_ylabel('Score (%)', fontsize=11, fontweight='bold')
ax4.set_title('Risk vs Reward Analysis', fontsize=12, fontweight='bold')
ax4.set_xticks(x_pos)
ax4.set_xticklabels([f'Option {opt}' for opt in options_short])
ax4.legend()
ax4.grid(True, alpha=0.3, axis='y')

# Add risk-reward ratio labels
for i in range(len(options_short)):
    ratio = rewards[i] / risks[i] * 10
    ax4.text(i, max(rewards[i], risks[i]) + 2, f'R/R: {ratio:.1f}', 
            ha='center', fontsize=8, fontweight='bold')

# 5. Resource Allocation
ax5 = axes[1, 1]
resources = decision_data['Resources']
colors = ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99']
explode = (0.1, 0, 0, 0)  # Highlight Option A

ax5.pie(resources, explode=explode, labels=[f'Option {i+1}' for i in range(4)], 
        colors=colors, autopct='%1.1f%%', startangle=90, shadow=True)
ax5.axis('equal')
ax5.set_title('Resource Allocation Impact', fontsize=12, fontweight='bold')

# 6. Timeline and Milestones
ax6 = axes[1, 2]
timeline_data = {
    'Option A': {'Q1': 30, 'Q2': 40, 'Q3': 20, 'Q4': 10},
    'Option B': {'Q1': 10, 'Q2': 30, 'Q3': 40, 'Q4': 20},
    'Option C': {'Q1': 20, 'Q2': 20, 'Q3': 30, 'Q4': 30},
    'Option D': {'Q1': 40, 'Q2': 30, 'Q3': 20, 'Q4': 10}
}

quarters = ['Q1', 'Q2', 'Q3', 'Q4']
bottom = np.zeros(len(quarters))

for option, values in timeline_data.items():
    quarter_values = [values[q] for q in quarters]
    ax6.bar(quarters, quarter_values, bottom=bottom, label=option, alpha=0.7)
    bottom += quarter_values

ax6.set_xlabel('Quarter', fontsize=11, fontweight='bold')
ax6.set_ylabel('Resource Allocation %', fontsize=11, fontweight='bold')
ax6.set_title('Implementation Timeline', fontsize=12, fontweight='bold')
ax6.legend(loc='upper left', fontsize=8)
ax6.grid(True, alpha=0.3, axis='y')

plt.tight_layout()
plt.suptitle('STRATEGIC DECISION MATRIX: Choosing the Optimal Path Forward\n', 
            fontsize=18, fontweight='bold', y=1.02)
plt.show()