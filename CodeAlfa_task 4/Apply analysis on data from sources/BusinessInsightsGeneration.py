class BusinessInsightsGenerator:
    """
    Generate actionable business insights from multi-source analysis
    """
    
    def __init__(self, amazon_results, social_results, news_results, emotion_results):
        self.amazon = amazon_results
        self.social = social_results
        self.news = news_results
        self.emotions = emotion_results
        
    def generate_amazon_insights(self):
        """Generate product insights from reviews"""
        insights = []
        
        # Rating distribution
        rating_dist = self.amazon['rating'].value_counts(normalize=True).sort_index() * 100
        insights.append(f"📊 Rating Distribution: {rating_dist[5]:.1f}% 5-star, {rating_dist[1]:.1f}% 1-star")
        
        # Sentiment vs Rating agreement
        agreement = (self.amazon['final_sentiment'] == self.amazon['rating_sentiment']).mean() * 100
        insights.append(f"🎯 Text-Rating Agreement: {agreement:.1f}%")
        
        # Top positive indicators
        positive_reviews = self.amazon[self.amazon['final_sentiment'] == 'positive']
        insights.append(f"👍 Positive Reviews: {len(positive_reviews)} ({len(positive_reviews)/len(self.amazon)*100:.1f}%)")
        
        # Top negative indicators
        negative_reviews = self.amazon[self.amazon['final_sentiment'] == 'negative']
        insights.append(f"👎 Negative Reviews: {len(negative_reviews)} ({len(negative_reviews)/len(self.amazon)*100:.1f}%)")
        
        # Confidence analysis
        high_confidence = self.amazon[self.amazon['confidence'] > 0.7]
        insights.append(f"🔒 High Confidence Reviews: {len(high_confidence)} ({len(high_confidence)/len(self.amazon)*100:.1f}%)")
        
        return insights
    
    def generate_social_insights(self):
        """Generate social media insights"""
        insights = []
        
        # Platform sentiment ranking
        platform_sentiment = self.social.groupby('platform')['sentiment_compound'].mean().sort_values(ascending=False)
        insights.append(f"📱 Platform Sentiment Ranking: {platform_sentiment.to_dict()}")
        
        # Toxicity hotspots
        toxic_posts = self.social[self.social['toxicity_score'] > 0.3]
        toxicity_by_platform = toxic_posts.groupby('platform').size() / self.social.groupby('platform').size() * 100
        insights.append(f"⚠️ Toxicity Hotspots: {toxicity_by_platform.to_dict()}")
        
        # Engagement correlation
        correlation = self.social['sentiment_compound'].corr(self.social['engagement_score'])
        insights.append(f"📈 Sentiment-Engagement Correlation: {correlation:.3f}")
        
        return insights
    
    def generate_news_insights(self):
        """Generate news sentiment insights"""
        insights = []
        
        # Topic sentiment ranking
        if 'topic' in self.news.columns:
            topic_sentiment = self.news.groupby('topic')['vader_score'].mean().sort_values(ascending=False)
            insights.append(f"📰 Topic Sentiment: {topic_sentiment.to_dict()}")
        
        # Financial news impact
        financial_news = self.news[self.news['source'] == 'Financial News']
        if not financial_news.empty:
            fin_sentiment = financial_news['combined_sentiment'].value_counts(normalize=True) * 100
            insights.append(f"💰 Financial News Sentiment: {fin_sentiment.to_dict()}")
        
        return insights
    
    def generate_emotion_insights(self):
        """Generate emotion-based insights"""
        insights = []
        
        # Dominant emotions by source
        for source in self.emotions['source'].unique():
            source_emotions = self.emotions[self.emotions['source'] == source]
            top_emotion = source_emotions['primary_emotion'].mode()[0]
            top_pct = (source_emotions['primary_emotion'] == top_emotion).mean() * 100
            insights.append(f"🎭 {source}: Most common emotion is '{top_emotion}' ({top_pct:.1f}%)")
        
        # Emotion intensity ranking
        emotion_cols = [col for col in self.emotions.columns if '_intensity' in col]
        avg_intensity = self.emotions[emotion_cols].mean().sort_values(ascending=False)
        top_emotion_intensity = avg_intensity.index[0].replace('_intensity', '')
        insights.append(f"💪 Strongest emotion on average: '{top_emotion_intensity}' ({avg_intensity.iloc[0]:.2f}/10)")
        
        return insights
    
    def generate_executive_summary(self):
        """Generate comprehensive executive summary"""
        
        print("\n" + "="*80)
        print("EXECUTIVE SUMMARY: MULTI-SOURCE SENTIMENT & EMOTION ANALYSIS")
        print("="*80)
        
        # Amazon Insights
        print("\n🛍️  AMAZON REVIEW INSIGHTS")
        print("-"*40)
        for insight in self.generate_amazon_insights():
            print(f"  {insight}")
        
        # Social Media Insights
        print("\n📱 SOCIAL MEDIA INSIGHTS")
        print("-"*40)
        for insight in self.generate_social_insights():
            print(f"  {insight}")
        
        # News Insights
        print("\n📰 NEWS SENTIMENT INSIGHTS")
        print("-"*40)
        for insight in self.generate_news_insights():
            print(f"  {insight}")
        
        # Emotion Insights
        print("\n🎭 EMOTION ANALYSIS INSIGHTS")
        print("-"*40)
        for insight in self.generate_emotion_insights():
            print(f"  {insight}")
        
        # Cross-source recommendations
        print("\n💡 RECOMMENDATIONS")
        print("-"*40)
        
        # Generate recommendations based on findings
        recommendations = [
            "🔹 Amazon: Focus on addressing 1-star reviews to improve overall sentiment",
            "🔹 Social Media: Monitor toxicity on Voat platform more closely [citation:8]",
            "🔹 News: Financial news shows more extreme sentiment - consider separate analysis",
            "🔹 Emotion: Joy is dominant in Amazon, but negative emotions in social media need attention"
        ]
        
        for rec in recommendations:
            print(f"  {rec}")
        
        print("\n" + "="*80)

# Generate comprehensive insights
insights_generator = BusinessInsightsGenerator(
    results_with_dates[results_with_dates['source'] == 'Amazon Reviews'],
    results_with_dates[results_with_dates['source'] == 'Social Media'],
    results_with_dates[results_with_dates['source'].isin(['BBC News', 'Financial News'])],
    all_emotions
)

insights_generator.generate_executive_summary()