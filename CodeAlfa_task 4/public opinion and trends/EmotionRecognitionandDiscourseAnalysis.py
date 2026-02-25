class EmotionDiscourseAnalyzer:
    """
    Analyze emotional dynamics in public discourse
    Based on studies of emotional responses during political events [citation:3][citation:7]
    """
    
    def __init__(self, data):
        self.data = data
        self.emotions = ['joy', 'anger', 'sadness', 'fear', 'surprise']
        
    def analyze_emotion_timeline(self, event_date=None, window=7):
        """
        Track emotion evolution over time, especially around events
        Used in analyzing public emotional response to news [citation:7]
        """
        daily_emotions = self.data.copy()
        daily_emotions['date'] = daily_emotions['timestamp'].dt.date
        
        # Aggregate emotions by day
        emotion_timeline = daily_emotions.groupby('date')[self.emotions].mean()
        
        if event_date:
            event_date = pd.to_datetime(event_date).date()
            pre_event = emotion_timeline[emotion_timeline.index < event_date].tail(window)
            post_event = emotion_timeline[emotion_timeline.index >= event_date].head(window)
            
            return {
                'timeline': emotion_timeline,
                'pre_event': pre_event.mean(),
                'post_event': post_event.mean(),
                'emotion_shift': (post_event.mean() - pre_event.mean()) if not (pre_event.empty or post_event.empty) else None
            }
        
        return {'timeline': emotion_timeline}
    
    def emotion_correlation_matrix(self):
        """Analyze how emotions correlate in public discourse"""
        emotion_data = self.data[self.emotions]
        corr_matrix = emotion_data.corr()
        
        return corr_matrix
    
    def dominant_emotion_by_topic(self):
        """Find dominant emotions for different topics"""
        topic_emotions = self.data.groupby('topic')[self.emotions].mean()
        topic_emotions['dominant'] = topic_emotions.idxmax(axis=1)
        topic_emotions['dominant_value'] = topic_emotions.max(axis=1)
        
        return topic_emotions.sort_values('dominant_value', ascending=False)
    
    def platform_emotion_profile(self):
        """Characterize emotional profiles of different platforms"""
        platform_emotions = self.data.groupby('platform')[self.emotions].mean()
        
        # Normalize to see relative emphasis
        platform_emotions_normalized = platform_emotions.div(platform_emotions.sum(axis=1), axis=0)
        
        return platform_emotions_normalized

# Initialize emotion analyzer
emotion_analyzer = EmotionDiscourseAnalyzer(opinion_data)

# Analyze emotions by topic
topic_emotions = emotion_analyzer.dominant_emotion_by_topic()
print("Dominant Emotions by Topic:")
print(topic_emotions[['dominant', 'dominant_value']].head(10))

# Analyze platform emotional profiles
platform_profiles = emotion_analyzer.platform_emotion_profile()
print("\nPlatform Emotional Profiles (normalized):")
print(platform_profiles.round(3))