class PublicOpinionCollector:
    """
    Collect public opinion data from multiple sources
    Inspired by research on multi-platform sentiment analysis [citation:9]
    """
    
    def __init__(self):
        self.sources = {
            'social_media': ['X (Twitter)', 'Facebook', 'Reddit'],
            'news': ['BBC', 'CNN', 'Reuters'],
            'reviews': ['Amazon', 'Yelp'],
            'video_comments': ['YouTube']
        }
        
    def generate_sample_data(self, n_samples=1000):
        """
        Generate synthetic public opinion data based on real-world patterns
        """
        np.random.seed(42)
        
        # Create timestamps over 6 months
        end_date = datetime.now()
        start_date = end_date - timedelta(days=180)
        dates = pd.date_range(start=start_date, end=end_date, periods=n_samples)
        
        # Generate topics based on current events
        topics = [
            'climate change', 'economy', 'healthcare', 'technology',
            'politics', 'sports', 'entertainment', 'education'
        ]
        
        # Platform distribution
        platforms = ['X', 'Facebook', 'Reddit', 'YouTube', 'News', 'Amazon']
        
        data = []
        for i in range(n_samples):
            # Simulate sentiment patterns
            # Public sentiment often follows cyclical patterns with event-driven spikes [citation:1]
            base_sentiment = 0.3 * np.sin(i * 0.05) + np.random.normal(0, 0.2)
            
            # Add event-driven spikes (simulating real events)
            if i % 50 == 0:  # Simulated major events
                base_sentiment += 0.5 if np.random.random() > 0.5 else -0.5
            
            # Ensure sentiment is within bounds
            sentiment = np.clip(base_sentiment, -1, 1)
            
            # Generate emotion distribution
            emotions = self._generate_emotions(sentiment)
            
            data.append({
                'timestamp': dates[i],
                'platform': np.random.choice(platforms),
                'topic': np.random.choice(topics),
                'sentiment_score': sentiment,
                'sentiment_label': 'positive' if sentiment > 0.1 else ('negative' if sentiment < -0.1 else 'neutral'),
                'joy': emotions['joy'],
                'anger': emotions['anger'],
                'sadness': emotions['sadness'],
                'fear': emotions['fear'],
                'surprise': emotions['surprise'],
                'engagement': np.random.randint(10, 10000),
                'region': np.random.choice(['North America', 'Europe', 'Asia', 'South America']),
                'text_length': np.random.randint(50, 500)
            })
        
        return pd.DataFrame(data)
    
    def _generate_emotions(self, sentiment):
        """Generate emotion distribution based on sentiment"""
        if sentiment > 0.5:  # Strong positive
            return {'joy': 0.7, 'anger': 0.1, 'sadness': 0.05, 'fear': 0.05, 'surprise': 0.1}
        elif sentiment > 0.1:  # Mild positive
            return {'joy': 0.4, 'anger': 0.1, 'sadness': 0.1, 'fear': 0.1, 'surprise': 0.3}
        elif sentiment < -0.5:  # Strong negative
            return {'joy': 0.05, 'anger': 0.6, 'sadness': 0.2, 'fear': 0.1, 'surprise': 0.05}
        elif sentiment < -0.1:  # Mild negative
            return {'joy': 0.1, 'anger': 0.3, 'sadness': 0.4, 'fear': 0.1, 'surprise': 0.1}
        else:  # Neutral
            return {'joy': 0.2, 'anger': 0.2, 'sadness': 0.2, 'fear': 0.2, 'surprise': 0.2}

# Initialize collector
collector = PublicOpinionCollector()
opinion_data = collector.generate_sample_data(2000)
print(f"Collected {len(opinion_data)} public opinion samples")
print("\nSample distribution by platform:")
print(opinion_data['platform'].value_counts())