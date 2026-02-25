class EmotionDetectionAPI:
    """
    Production-ready emotion detection API
    """
    
    def __init__(self):
        self.analyzer = RealTimeEmotionAnalyzer()
        self.pattern_analyzer = EmotionPatternAnalyzer()
        self.version = "1.0.0"
        
    def detect(self, text, include_scores=False, include_explanation=False):
        """
        Main API endpoint for emotion detection
        
        Args:
            text: Input text to analyze
            include_scores: Include all emotion scores
            include_explanation: Include explanation of detection
            
        Returns:
            Dictionary with emotion detection results
        """
        try:
            # Validate input
            if not text or not isinstance(text, str):
                return {'error': 'Invalid input text'}
            
            # Analyze
            result = self.analyzer.analyze_text(text, detailed=include_scores)
            
            # Prepare response
            response = {
                'status': 'success',
                'text': text[:100] + '...' if len(text) > 100 else text,
                'primary_emotion': result['consensus'],
                'confidence': result['confidence'],
                'intensity': result['intensity']
            }
            
            if include_scores:
                response['all_scores'] = {
                    'lexicon': result['lexicon_scores'],
                    'ml': result['ml_scores']
                }
            
            if include_explanation:
                response['explanation'] = self.generate_explanation(result)
            
            return response
            
        except Exception as e:
            return {'error': str(e)}
    
    def detect_batch(self, texts):
        """Batch processing endpoint"""
        results = []
        for text in texts:
            results.append(self.detect(text))
        return results
    
    def generate_explanation(self, result):
        """Generate human-readable explanation"""
        emotion = result['consensus']
        intensity = result['intensity']
        
        explanations = {
            'joy': f"The text expresses {emotion} with {intensity:.1f} intensity. "
                   f"Words like 'happy', 'love', 'wonderful' contribute to this.",
            'sadness': f"The text conveys {emotion} with {intensity:.1f} intensity. "
                      f"Terms expressing loss or disappointment are present.",
            'anger': f"The text shows {emotion} with {intensity:.1f} intensity. "
                    f"Strong negative language indicates frustration.",
            'fear': f"The text reveals {emotion} with {intensity:.1f} intensity. "
                   f"Words suggesting anxiety or threat are detected.",
            'surprise': f"The text displays {emotion} with {intensity:.1f} intensity. "
                       f"Unexpected elements and exclamations are present.",
            'disgust': f"The text indicates {emotion} with {intensity:.1f} intensity. "
                      f"Strong aversive language is detected."
        }
        
        return explanations.get(emotion, f"The primary emotion detected is {emotion}.")
    
    def get_statistics(self):
        """Get API statistics"""
        return {
            'version': self.version,
            'emotions_supported': list(real_time_analyzer.emotion_colors.keys()),
            'methods': ['lexicon', 'machine_learning', 'ensemble']
        }

# Initialize API
emotion_api = EmotionDetectionAPI()

print("\n" + "="*60)
print("EMOTION DETECTION API READY")
print("="=60)
print(f"Version: {emotion_api.version}")
print(f"Supported Emotions: {', '.join(emotion_api.get_statistics()['emotions_supported'])}")
print("\nAPI Methods:")
for method in emotion_api.get_statistics()['methods']:
    print(f"  • {method}")

# Test API
test_text = "I'm absolutely thrilled and overjoyed with this wonderful news!"
print(f"\n📡 API Test:")
print(f"Input: {test_text}")
result = emotion_api.detect(test_text, include_scores=True, include_explanation=True)
print(f"Response: {result}")