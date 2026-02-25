def marketing_sentiment_dashboard():
    """
    Create marketing-focused sentiment dashboard
    """
    fig, axes = plt.subplots(2, 3, figsize=(18, 10))
    
    # 1. Campaign sentiment over time
    ax1 = axes[0, 0]
    dates = pd.date_range(start='2024-01-01', periods=90, freq='D')
    campaign_sentiment = 0.3 * np.sin(np.arange(90) * 0.1) + np.random.normal(0, 0.1, 90)
    campaign_sentiment[30:60] += 0.4  # Campaign period
    
    ax1.plot(dates, campaign_sentiment, color='#2E86AB', linewidth=2)
    ax1.axvspan(dates[30], dates[60], alpha=0.2, color='green', label='Campaign Active')
    ax1.axhline(y=0, color='black', linestyle='-', alpha=0.3)
    ax1.set_title('Campaign Sentiment Impact', fontsize=12, fontweight='bold')
    ax1.set_xlabel('Date')
    ax1.set_ylabel('Sentiment Score')
    ax1.legend()
    
    # 2. Segment response comparison
    ax2 = axes[0, 1]
    segments = ['Loyal Customers', 'New Prospects', 'Competitor Followers']
    pre_campaign = [0.2, -0.1, -0.3]
    post_campaign = [0.25, 0.15, -0.2]
    
    x = np.arange(len(segments))
    width = 0.35
    ax2.bar(x - width/2, pre_campaign, width, label='Pre-Campaign', color='#95a5a6')
    ax2.bar(x + width/2, post_campaign, width, label='Post-Campaign', color='#2ecc71')
    ax2.set_title('Segment Response Analysis', fontsize=12, fontweight='bold')
    ax2.set_xlabel('Customer Segment')
    ax2.set_ylabel('Avg Sentiment')
    ax2.set_xticks(x)
    ax2.set_xticklabels(segments, rotation=45)
    ax2.axhline(y=0, color='black', linestyle='-', alpha=0.3)
    ax2.legend()
    
    # 3. Brand health metrics
    ax3 = axes[0, 2]
    metrics = ['Brand Awareness', 'Purchase Intent', 'Brand Loyalty', 'NPS']
    values = [78, 65, 82, 45]
    colors = ['#3498db', '#2ecc71', '#f39c12', '#e74c3c']
    ax3.barh(metrics, values, color=colors)
    ax3.set_title('Brand Health Metrics', fontsize=12, fontweight='bold')
    ax3.set_xlabel('Score')
    
    # 4. Competitor comparison
    ax4 = axes[1, 0]
    competitors = ['Our Brand', 'Competitor A', 'Competitor B', 'Competitor C']
    sentiment_scores = [0.35, 0.28, 0.15, -0.1]
    ax4.bar(competitors, sentiment_scores, color=['#2ecc71', '#3498db', '#f39c12', '#e74c3c'])
    ax4.set_title('Competitive Sentiment Benchmark', fontsize=12, fontweight='bold')
    ax4.set_xlabel('Brand')
    ax4.set_ylabel('Avg Sentiment')
    ax4.axhline(y=0, color='black', linestyle='-', alpha=0.3)
    
    # 5. Emotion drivers
    ax5 = axes[1, 1]
    emotions = ['Trust', 'Joy', 'Anticipation', 'Anger', 'Fear']
    drivers = [0.42, 0.38, 0.25, 0.12, 0.08]
    ax5.pie(drivers, labels=emotions, autopct='%1.1f%%', 
            colors=['#2ecc71', '#f39c12', '#3498db', '#e74c3c', '#95a5a6'])
    ax5.set_title('Emotional Drivers of Brand Perception', fontsize=12, fontweight='bold')
    
    # 6. Actionable insights
    ax6 = axes[1, 2]
    ax6.axis('off')
    insights_text = """
    🎯 MARKETING ACTION ITEMS
    
    Based on sentiment analysis:
    
    1. Leverage loyal customers as brand advocates
       → Sentiment increase of +25% in this segment
    
    2. Address quality concerns in competitor community
       → 15% of negative mentions relate to durability
    
    3. Optimize messaging around trust emotions
       → Trust is strongest predictor of purchase intent
    
    4. Monitor boycott risk in political discussions
       → 3x higher during controversial topics
    """
    ax6.text(0.1, 0.95, insights_text, fontsize=10, va='top', family='monospace',
            bbox=dict(boxstyle='round', facecolor='#f0f2f5', alpha=0.9))
    
    plt.suptitle('MARKETING SENTIMENT DASHBOARD', fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.show()