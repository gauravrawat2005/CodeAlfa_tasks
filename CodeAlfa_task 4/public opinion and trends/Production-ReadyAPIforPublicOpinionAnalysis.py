class PublicOpinionAPI:
    """
    Production-ready API for public opinion analysis
    """
    
    def __init__(self):
        self.analyzer = EnsembleSentimentAnalyzer()
        self.version = "2.0.0"
        
    def analyze_text(self, text, include_emotions=True, include_trends=True):
        """
        Main API endpoint for public opinion analysis
        
        Args:
            text: Text to analyze
            include_emotions: Include detailed emotion analysis
            include_trends: Include trend predictions
            
        Returns:
            Comprehensive opinion analysis
        """
        try:
            # Sentiment analysis
            sentiment = self.analyzer.ensemble_analysis(text)
            
            # Emotion detection (simplified)
            emotions = self._detect_emotions(text) if include_emotions else None
            
            # Trend context (would connect to database in production)
            trend_context = self._get_trend_context() if include_trends else None
            
            return {
                'status': 'success',
                'text': text[:200] + '...' if len(text) > 200 else text,
                'sentiment': {
                    'score': sentiment['ensemble_score'],
                    'label': sentiment['ensemble_sentiment'],
                    'confidence': sentiment['confidence'],
                    'components': {
                        'vader': sentiment['vader_score'],
                        'transformer': sentiment['transformer_score']
                    }
                },
                'emotions': emotions,
                'trend_context': trend_context,
                'version': self.version,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            return {'status': 'error', 'message': str(e)}
    
    def _detect_emotions(self, text):
        """Detect emotions in text"""
        # Simplified emotion detection
        emotion_keywords = {
            'joy': ['happy', 'great', 'excellent', 'love', 'wonderful'],
            'anger': ['angry', 'hate', 'terrible', 'awful', 'furious'],
            'sadness': ['sad', 'disappointed', 'sorry', 'grief'],
            'fear': ['afraid', 'scared', 'worried', 'anxious'],
            'surprise': ['shocked', 'amazed', 'unexpected', 'wow']
        }
        
        text_lower = text.lower()
        emotions = {}
        
        for emotion, keywords in emotion_keywords.items():
            count = sum(1 for kw in keywords if kw in text_lower)
            emotions[emotion] = min(count * 0.2, 1.0)  # Normalize
        
        return emotions
    
    def _get_trend_context(self):
        """Get current trend context (simulated)"""
        return {
            'current_trend': np.random.choice(['rising', 'stable', 'falling']),
            'anomaly_detected': np.random.random() > 0.9,
            'similar_mentions': np.random.randint(100, 10000),
            'expected_trend': np.random.choice(['positive', 'neutral', 'negative'])
        }
    
    def batch_analyze(self, texts):
        """Analyze multiple texts"""
        results = []
        for text in texts:
            results.append(self.analyze_text(text))
        return results

# Initialize API
opinion_api = PublicOpinionAPI()

print("\n" + "="*60)
print("PUBLIC OPINION ANALYSIS API READY")
print("="=60)
print(f"Version: {opinion_api.version}")

# Test API
test_text = "The new environmental policy is a game-changer! This will transform our future."
print(f"\n📡 API Test:")
result = opinion_api.analyze_text(test_text)
print(f"Sentiment: {result['sentiment']['label']} (score: {result['sentiment']['score']:.3f})")
print(f"Confidence: {result['sentiment']['confidence']:.1%}")