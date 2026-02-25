class MarketingCampaignAnalyzer:
    """
    Track and optimize marketing campaigns using real-time sentiment
    Inspired by Nike's Kaepernick campaign monitoring [citation:2]
    """
    
    def __init__(self):
        self.sentiment_analyzer = EnsembleSentimentAnalyzer()
        self.emotion_detector = MultiSourceEmotionAnalyzer()
        
    def analyze_campaign_impact(self, campaign_data, baseline_period=30):
        """
        Measure campaign impact by comparing to baseline sentiment
        """
        # Calculate baseline sentiment (pre-campaign)
        baseline = campaign_data[campaign_data['days_since_launch'] < 0]
        baseline_sentiment = baseline['sentiment_score'].mean()
        
        # Track campaign period
        campaign_period = campaign_data[campaign_data['days_since_launch'] >= 0]
        
        # Segment by customer groups
        segments = {
            'loyal_customers': campaign_data[campaign_data['customer_tenure'] > 365],
            'new_prospects': campaign_data[campaign_data['customer_tenure'] <= 365],
            'competitor_followers': campaign_data[campaign_data['follows_competitors'] == True]
        }
        
        insights = {}
        for segment_name, segment_data in segments.items():
            if len(segment_data) > 0:
                avg_sentiment = segment_data['sentiment_score'].mean()
                sentiment_shift = avg_sentiment - baseline_sentiment
                
                # Detect boycott signals
                boycott_mentions = segment_data['text'].str.contains('boycott|#boycott', case=False).sum()
                
                insights[segment_name] = {
                    'avg_sentiment': avg_sentiment,
                    'sentiment_shift': sentiment_shift,
                    'boycott_risk': boycott_mentions / len(segment_data) if len(segment_data) > 0 else 0,
                    'engagement_rate': segment_data['engagement'].mean()
                }
        
        # Nike's key finding: Despite initial negative reaction, purchase intent remained positive [citation:2]
        return {
            'baseline_sentiment': baseline_sentiment,
            'campaign_sentiment': campaign_period['sentiment_score'].mean(),
            'segment_insights': insights,
            'recommendation': self._generate_marketing_recommendation(insights)
        }
    
    def _generate_marketing_recommendation(self, insights):
        """Generate actionable marketing recommendations"""
        recommendations = []
        
        if insights.get('loyal_customers', {}).get('sentiment_shift', 0) < -0.2:
            recommendations.append("🔴 Immediate action: Engage loyal customers with personalized outreach")
        elif insights.get('new_prospects', {}).get('sentiment_shift', 0) > 0.1:
            recommendations.append("🟢 Opportunity: Scale campaign targeting similar prospect segments")
        
        if insights.get('competitor_followers', {}).get('boycott_risk', 0) > 0.1:
            recommendations.append("⚠️ Monitor competitor communities for backlash signals")
        
        return recommendations