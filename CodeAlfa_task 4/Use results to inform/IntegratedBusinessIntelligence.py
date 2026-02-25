class IntegratedBusinessIntelligence:
    """
    Unified framework combining marketing, product, and social insights
    """
    
    def __init__(self):
        self.marketing_analyzer = MarketingCampaignAnalyzer()
        self.product_engine = ProductInsightEngine()
        self.social_analyzer = SocialInsightGenerator()
        
    def generate_executive_dashboard(self, all_data):
        """
        Create comprehensive executive dashboard with cross-functional insights
        """
        fig = plt.figure(figsize=(20, 12))
        fig.patch.set_facecolor('#f8f9fa')
        
        # Define grid
        gs = fig.add_gridspec(3, 4, hspace=0.3, wspace=0.3)
        
        # 1. Marketing KPIs
        ax1 = fig.add_subplot(gs[0, 0])
        marketing_kpis = {
            'Brand Sentiment': 0.72,
            'Campaign ROI': '156%',
            'Share of Voice': '34%',
            'NPS': '+42'
        }
        y_pos = np.arange(len(marketing_kpis))
        ax1.barh(y_pos, [0.72, 1.56, 0.34, 0.42], color='#3498db')
        ax1.set_yticks(y_pos)
        ax1.set_yticklabels(marketing_kpis.keys())
        ax1.set_title('Marketing KPIs', fontsize=12, fontweight='bold')
        ax1.set_xlabel('Value')
        
        # 2. Product Health
        ax2 = fig.add_subplot(gs[0, 1])
        product_metrics = ['Usability', 'Performance', 'Features', 'Support']
        scores = [0.85, 0.72, 0.68, 0.91]
        colors2 = ['#2ecc71' if s > 0.8 else '#f39c12' if s > 0.6 else '#e74c3c' for s in scores]
        ax2.bar(product_metrics, scores, color=colors2)
        ax2.set_title('Product Health Metrics', fontsize=12, fontweight='bold')
        ax2.set_ylim(0, 1)
        ax2.set_ylabel('Score')
        
        # 3. Social Trends
        ax3 = fig.add_subplot(gs[0, 2:4])
        topics = ['Mental Health', 'Climate Change', 'Economy', 'Technology']
        sentiment_by_topic = [0.15, -0.25, -0.35, 0.45]
        colors3 = ['#2ecc71' if s > 0.1 else '#e74c3c' if s < -0.1 else '#95a5a6' for s in sentiment_by_topic]
        ax3.barh(topics, sentiment_by_topic, color=colors3)
        ax3.set_title('Social Sentiment by Topic', fontsize=12, fontweight='bold')
        ax3.set_xlabel('Sentiment Score')
        ax3.axvline(x=0, color='black', linestyle='-', alpha=0.3)
        
        # 4. Integrated Insights
        ax4 = fig.add_subplot(gs[1, :])
        ax4.axis('off')
        
        insights_text = """
        🏢 EXECUTIVE SUMMARY: INTEGRATED BUSINESS INTELLIGENCE
        
        MARKETING INSIGHTS:
        • Brand sentiment remains strong (+0.72) despite competitive pressure
        • Campaign ROI exceeded targets (156%), driven by loyal customer segment
        • Opportunity: Expand into adjacent demographics showing positive sentiment
        
        PRODUCT INSIGHTS:
        • Support satisfaction is high (0.91), but performance needs attention (0.72)
        • Top feature requests: collaboration tools, mobile app, API access
        • Critical pain points: export functionality, loading speed
        
        SOCIAL INSIGHTS:
        • Mental health conversations growing (+34% YoY), sentiment neutral-positive
        • Economic anxiety spiking (-0.35), opportunity for financial wellness content
        • Technology optimism high (+0.45), leverage in product positioning
        
        🎯 RECOMMENDED ACTIONS:
        1. Launch performance optimization sprint (Q2 priority)
        2. Create financial wellness content series addressing economic concerns
        3. Develop collaboration features based on user requests
        4. Expand marketing to demographics showing positive tech sentiment
        """
        
        ax4.text(0.5, 0.5, insights_text, fontsize=11, ha='center', va='center',
                bbox=dict(boxstyle='round', facecolor='white', edgecolor='navy', linewidth=2))
        
        # 5. Trend Forecast
        ax5 = fig.add_subplot(gs[2, :2])
        quarters = ['Q1', 'Q2', 'Q3', 'Q4', 'Q1 (Forecast)']
        sentiment_trend = [0.35, 0.42, 0.38, 0.45, 0.52]
        ax5.plot(quarters, sentiment_trend, marker='o', linewidth=2, color='#2E86AB')
        ax5.fill_between(quarters, sentiment_trend, alpha=0.3)
        ax5.set_title('Sentiment Trend Forecast', fontsize=12, fontweight='bold')
        ax5.set_ylabel('Sentiment Score')
        ax5.grid(True, alpha=0.3)
        
        # 6. Action Priority Matrix
        ax6 = fig.add_subplot(gs[2, 2:4])
        actions = {
            'Performance Fix': (0.8, 0.9, '🔴'),
            'Feature Development': (0.6, 0.7, '🟡'),
            'Content Marketing': (0.4, 0.6, '🟢'),
            'Community Engagement': (0.3, 0.4, '🟢'),
            'Research Initiative': (0.2, 0.3, '🔵')
        }
        
        for action, (impact, urgency, color) in actions.items():
            ax6.scatter(impact, urgency, s=500, marker='o', 
                       color=color.replace('🔴', 'red').replace('🟡', 'orange')
                              .replace('🟢', 'green').replace('🔵', 'blue'))
            ax6.annotate(action, (impact, urgency), 
                        xytext=(5, 5), textcoords='offset points', fontsize=8)
        
        ax6.set_xlim(0, 1)
        ax6.set_ylim(0, 1)
        ax6.set_xlabel('Impact')
        ax6.set_ylabel('Urgency')
        ax6.set_title('Action Priority Matrix', fontsize=12, fontweight='bold')
        ax6.grid(True, alpha=0.3)
        
        plt.suptitle('INTEGRATED BUSINESS INTELLIGENCE DASHBOARD', 
                    fontsize=16, fontweight='bold', y=1.02)
        plt.tight_layout()
        plt.show()