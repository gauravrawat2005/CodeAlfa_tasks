# Create a compelling turnaround story visualization
fig = plt.figure(figsize=(16, 10))
fig.patch.set_facecolor('#f8f9fa')

# Main plot with story arc
ax1 = plt.subplot(2, 2, (1, 2))

# Plot revenue with story annotations
ax1.plot(business_data['date'], business_data['revenue']/1000, 
         linewidth=3, color='#2E86AB', label='Revenue', marker='o', markersize=4)
ax1.plot(business_data['date'], business_data['costs']/1000, 
         linewidth=2, color='#A23B72', linestyle='--', label='Costs', alpha=0.7)

# Highlight key story moments
# The crisis point
crisis_idx = 10
crisis_date = business_data.iloc[crisis_idx]['date']
crisis_value = business_data.iloc[crisis_idx]['revenue']/1000
ax1.scatter([crisis_date], [crisis_value], s=200, color='red', zorder=5, 
           edgecolor='darkred', linewidth=2)

# The turning point
turn_idx = 14
turn_date = business_data.iloc[turn_idx]['date']
turn_value = business_data.iloc[turn_idx]['revenue']/1000
ax1.scatter([turn_date], [turn_value], s=200, color='green', zorder=5,
           edgecolor='darkgreen', linewidth=2)

# The success point
success_idx = 20
success_date = business_data.iloc[success_idx]['date']
success_value = business_data.iloc[success_idx]['revenue']/1000
ax1.scatter([success_date], [success_value], s=200, color='blue', zorder=5,
           edgecolor='darkblue', linewidth=2)

# Add story annotations with arrows
ax1.annotate('CRISIS: Revenue Drop\nNew competitor enters', 
            xy=(crisis_date, crisis_value), xytext=(crisis_date - pd.Timedelta(days=90), crisis_value - 200),
            arrowprops=dict(arrowstyle='->', color='red', lw=2),
            bbox=dict(boxstyle='round,pad=0.5', facecolor='#ffcccc', alpha=0.9),
            fontsize=10, ha='center')

ax1.annotate('TURNING POINT\nProduct Launch & Strategy Pivot', 
            xy=(turn_date, turn_value), xytext=(turn_date + pd.Timedelta(days=60), turn_value + 150),
            arrowprops=dict(arrowstyle='->', color='green', lw=2),
            bbox=dict(boxstyle='round,pad=0.5', facecolor='#ccffcc', alpha=0.9),
            fontsize=10, ha='center')

ax1.annotate('SUCCESS\nMarket Leadership Achieved', 
            xy=(success_date, success_value), xytext=(success_date - pd.Timedelta(days=120), success_value + 250),
            arrowprops=dict(arrowstyle='->', color='blue', lw=2),
            bbox=dict(boxstyle='round,pad=0.5', facecolor='#cce5ff', alpha=0.9),
            fontsize=10, ha='center')

# Add shaded regions for story acts
ax1.axvspan(business_data['date'].min(), crisis_date, alpha=0.1, color='gray', label='_nolegend_')
ax1.axvspan(crisis_date, turn_date, alpha=0.1, color='red', label='_nolegend_')
ax1.axvspan(turn_date, success_date, alpha=0.1, color='yellow', label='_nolegend_')
ax1.axvspan(success_date, business_data['date'].max(), alpha=0.1, color='green', label='_nolegend_')

# Add act labels
ax1.text(crisis_date - pd.Timedelta(days=180), ax1.get_ylim()[1]*0.9, 'ACT 1: Stability', 
        fontsize=12, fontweight='bold', ha='center', color='gray')
ax1.text(crisis_date + pd.Timedelta(days=60), ax1.get_ylim()[1]*0.9, 'ACT 2: Crisis', 
        fontsize=12, fontweight='bold', ha='center', color='red')
ax1.text(turn_date + pd.Timedelta(days=90), ax1.get_ylim()[1]*0.9, 'ACT 3: Transformation', 
        fontsize=12, fontweight='bold', ha='center', color='orange')
ax1.text(success_date + pd.Timedelta(days=90), ax1.get_ylim()[1]*0.9, 'ACT 4: Growth', 
        fontsize=12, fontweight='bold', ha='center', color='green')

ax1.set_xlabel('Timeline', fontsize=12, fontweight='bold')
ax1.set_ylabel('Revenue / Costs ($K)', fontsize=12, fontweight='bold')
ax1.set_title('The Turnaround Story: How We Overcame Market Disruption', 
             fontsize=16, fontweight='bold', pad=20)
ax1.legend(loc='upper left')
ax1.grid(True, alpha=0.3)

# Supporting metrics - Customer Impact
ax2 = plt.subplot(2, 2, 3)
ax2.fill_between(business_data['date'], business_data['customers']/1000, alpha=0.3, color='#2E86AB')
ax2.plot(business_data['date'], business_data['customers']/1000, 
         linewidth=2, color='#2E86AB', marker='s', markersize=3)
ax2.axvline(x=crisis_date, color='red', linestyle='--', alpha=0.5)
ax2.axvline(x=turn_date, color='green', linestyle='--', alpha=0.5)
ax2.set_xlabel('Timeline', fontsize=10)
ax2.set_ylabel('Customers (K)', fontsize=10)
ax2.set_title('Customer Base Growth', fontsize=12, fontweight='bold')
ax2.grid(True, alpha=0.3)

# Supporting metrics - Quality Impact
ax3 = plt.subplot(2, 2, 4)
ax3.plot(business_data['date'], business_data['satisfaction'], 
         linewidth=2, color='#F18F01', marker='^', markersize=3)
ax3.fill_between(business_data['date'], business_data['satisfaction'], 70, 
                 where=(business_data['satisfaction'] >= 70), alpha=0.3, color='green')
ax3.fill_between(business_data['date'], business_data['satisfaction'], 70, 
                 where=(business_data['satisfaction'] < 70), alpha=0.3, color='red')
ax3.axhline(y=70, color='gray', linestyle=':', alpha=0.7, label='Target')
ax3.axvline(x=crisis_date, color='red', linestyle='--', alpha=0.5)
ax3.axvline(x=turn_date, color='green', linestyle='--', alpha=0.5)
ax3.set_xlabel('Timeline', fontsize=10)
ax3.set_ylabel('Customer Satisfaction', fontsize=10)
ax3.set_title('Quality Metrics', fontsize=12, fontweight='bold')
ax3.legend()
ax3.grid(True, alpha=0.3)

plt.tight_layout()
plt.suptitle('DATA STORY: From Crisis to Market Leadership\n', 
            fontsize=18, fontweight='bold', y=1.02)
plt.show()