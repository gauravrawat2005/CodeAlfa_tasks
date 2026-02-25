class LexiconEmotionDetector:
    """Detect emotions using multiple lexicons"""
    
    def __init__(self):
        self.lexicons = emotion_lexicons
        self.intensity_multipliers = {
            '!!!': 1.5, '!!': 1.3, '!': 1.2,
            'very': 1.3, 'so': 1.2, 'really': 1.2,
            'absolutely': 1.4, 'completely': 1.3, 'totally': 1.3
        }
        
    def detect_emotions(self, text, threshold=0.1):
        """Detect emotions in text with intensity"""
        tokens = emotion_preprocessor.preprocess(text)
        text_lower = text.lower()
        
        # Initialize emotion scores
        emotion_scores = {emotion: 0.0 for emotion in self.lexicons.get_all_emotions()}
        
        # Check for intensity multipliers
        intensity = 1.0
        for multiplier, value in self.intensity_multipliers.items():
            if multiplier in text_lower:
                intensity = value
        
        # Score based on lexicon matches
        for emotion in emotion_scores.keys():
            emotion_words = self.lexicons.get_emotion_words(emotion)
            matches = [token for token in tokens if token in emotion_words]
            
            # Base score from word matches
            base_score = len(matches) / max(len(tokens), 1)
            
            # Apply intensity
            emotion_scores[emotion] = base_score * intensity
            
            # Bonus for exact phrase matches
            if emotion in text_lower:
                emotion_scores[emotion] += 0.2
                
        # Normalize scores
        total = sum(emotion_scores.values())
        if total > 0:
            emotion_scores = {k: v/total for k, v in emotion_scores.items()}
        
        # Filter by threshold
        detected = {k: v for k, v in emotion_scores.items() if v >= threshold}
        
        # Get primary emotion
        if detected:
            primary_emotion = max(detected, key=detected.get)
        else:
            primary_emotion = 'neutral'
            
        return {
            'primary_emotion': primary_emotion,
            'all_scores': emotion_scores,
            'detected': detected,
            'intensity': intensity
        }
    
    def analyze_batch(self, texts):
        """Analyze multiple texts"""
        results = []
        for text in texts:
            result = self.detect_emotions(text)
            results.append({
                'text': text,
                'primary_emotion': result['primary_emotion'],
                'confidence': result['all_scores'][result['primary_emotion']] if result['primary_emotion'] != 'neutral' else 0,
                'scores': result['all_scores']
            })
        return pd.DataFrame(results)

# Initialize detector
lexicon_detector = LexiconEmotionDetector()

# Test on sample texts
print("Lexicon-Based Emotion Detection:")
print("="*60)
sample_results = lexicon_detector.analyze_batch(df['text'].head(10).tolist())
for _, row in sample_results.iterrows():
    emotion = row['primary_emotion']
    confidence = row['confidence']
    
    # Color coding
    colors = {'joy': '\033[92m', 'sadness': '\033[94m', 'anger': '\033[91m',
              'fear': '\033[93m', 'surprise': '\033[95m', 'disgust': '\033[90m'}
    color = colors.get(emotion, '\033[0m')
    reset = '\033[0m'
    
    print(f"\nText: {row['text'][:50]}...")
    print(f"Emotion: {color}{emotion}{reset} (Confidence: {confidence:.1%})")