class SocialInsightGenerator:
    """
    Generate social insights from public discourse analysis
    Based on Clinical Partners' approach to mental health monitoring [citation:4]
    """
    
    def __init__(self):
        self.emotion_lexicons = {
            'anxiety': ['worried', 'anxious', 'stressed', 'overwhelmed', 'panic'],
            'depression': ['sad', 'hopeless', 'empty', 'depressed', 'miserable'],
            'adhd': ['focus', 'distracted', 'hyperactive', 'attention', 'impulsive'],
            'autism': ['sensory', 'meltdown', 'stim', 'social', 'communication']
        }
        
    def analyze_social_discourse(self, social_data, topic):
        """
        Analyze public conversation around specific topics
        """
        # Filter by topic
        topic_data = social_data[social_data['text'].str.contains(topic, case=False, na=False)]
        
        if len(topic_data) == 0:
            return {"error": "Insufficient data"}
        
        # Emotion distribution
        emotions = {}
        for emotion, keywords in self.emotion_lexicons.items():
            matches = topic_data['text'].str.contains('|'.join(keywords), case=False, na=False)
            emotions[emotion] = matches.mean()  # % of posts containing emotion keywords
        
        # Information needs (questions people are asking)
        questions = topic_data[topic_data['text'].str.contains('\?', na=False)]
        question_topics = self._extract_question_topics(questions['text'].tolist())
        
        # Sentiment over time
        topic_data['date'] = pd.to_datetime(topic_data['timestamp']).dt.date
        daily_sentiment = topic_data.groupby('date')['sentiment_score'].agg(['mean', 'count'])
        
        return {
            'topic': topic,
            'volume': len(topic_data),
            'emotion_profile': emotions,
            'avg_sentiment': topic_data['sentiment_score'].mean(),
            'sentiment_trend': daily_sentiment,
            'information_needs': question_topics[:10],  # Top questions
            'engagement_rate': topic_data['engagement'].mean() if 'engagement' in topic_data.columns else 0
        }
    
    def _extract_question_topics(self, questions):
        """Extract common themes from user questions"""
        # Simplified extraction - in practice, use NLP topic modeling
        common_questions = [
            "What are the symptoms?",
            "How to get diagnosed?",
            "Is this normal?",
            "Treatment options?",
            "Support groups near me?"
        ]
        return common_questions
    
    def generate_social_insights_report(self, analysis_results):
        """
        Create actionable social insights report
        """
        report = f"""
        📱 SOCIAL INSIGHTS REPORT: {analysis_results['topic'].upper()}
        
        Conversation Volume: {analysis_results['volume']:,} mentions
        Average Sentiment: {analysis_results['avg_sentiment']:.2f}
        Engagement Rate: {analysis_results['engagement_rate']:.1f}
        
        Emotional Profile:
        """
        
        for emotion, percentage in analysis_results['emotion_profile'].items():
            report += f"\n  • {emotion.title()}: {percentage:.1%}"
        
        report += "\n\n🎯 Information Needs:\n"
        for i, question in enumerate(analysis_results['information_needs'][:5], 1):
            report += f"\n  {i}. {question}"
        
        report += """
        
        💡 Recommendations:
        1. Create content addressing top questions
        2. Monitor anxiety spikes for crisis response
        3. Engage with high-sentiment discussions
        4. Partner with community leaders
        """
        
        return report

# Example usage
social_analyzer = SocialInsightGenerator()
mental_health_insights = social_analyzer.analyze_social_discourse(
    opinion_data, topic="mental health"
)
print(social_analyzer.generate_social_insights_report(mental_health_insights))