class RealTimeEmotionAnalyzer:
    """Production-ready emotion detection system"""
    
    def __init__(self):
        self.lexicon_detector = LexiconEmotionDetector()
        self.advanced_detector = advanced_detector
        self.emotion_colors = {
            'joy': '#2ecc71',
            'sadness': '#3498db',
            'anger': '#e74c3c',
            'fear': '#f39c12',
            'surprise': '#9b59b6',
            'disgust': '#95a5a6',
            'neutral': '#7f8c8d'
        }
        
    def analyze_text(self, text, detailed=True):
        """Analyze text for emotions with detailed explanation"""
        
        # Get predictions from both methods
        lexicon_result = self.lexicon_detector.detect_emotions(text)
        ml_emotion = self.advanced_detector.predict(text)
        ml_details = self.advanced_detector.predict(text, return_details=True)
        
        # Combine results
        result = {
            'text': text,
            'lexicon_based': lexicon_result['primary_emotion'],
            'ml_based': ml_emotion,
            'lexicon_scores': lexicon_result['all_scores'],
            'ml_scores': ml_details['probabilities'] if detailed else None,
            'intensity': lexicon_result['intensity']
        }
        
        # Determine consensus emotion
        if lexicon_result['primary_emotion'] == ml_emotion:
            result['consensus'] = lexicon_result['primary_emotion']
            result['confidence'] = 'high'
        else:
            # Weighted combination
            combined_scores = {}
            for emotion in self.emotion_colors.keys():
                if emotion in lexicon_result['all_scores']:
                    lexicon_score = lexicon_result['all_scores'][emotion]
                    ml_score = ml_details['probabilities'].get(emotion, 0) if detailed else 0
                    combined_scores[emotion] = (lexicon_score + ml_score) / 2
            
            result['consensus'] = max(combined_scores, key=combined_scores.get)
            result['confidence'] = 'medium'
        
        return result
    
    def visualize_emotion(self, text):
        """Create a visualization of emotion analysis"""
        result = self.analyze_text(text, detailed=True)
        
        fig, axes = plt.subplots(1, 3, figsize=(15, 5))
        
        # 1. Emotion bar chart
        ax1 = axes[0]
        emotions = list(result['lexicon_scores'].keys())
        scores = list(result['lexicon_scores'].values())
        colors = [self.emotion_colors.get(e, '#95a5a6') for e in emotions]
        
        bars = ax1.bar(emotions, scores, color=colors)
        ax1.set_title('Lexicon-Based Scores', fontsize=12, fontweight='bold')
        ax1.set_xlabel('Emotion')
        ax1.set_ylabel('Score')
        ax1.tick_params(axis='x', rotation=45)
        
        # 2. ML probabilities
        ax2 = axes[1]
        if result['ml_scores']:
            emotions_ml = list(result['ml_scores'].keys())
            scores_ml = list(result['ml_scores'].values())
            colors_ml = [self.emotion_colors.get(e, '#95a5a6') for e in emotions_ml]
            
            bars = ax2.bar(emotions_ml, scores_ml, color=colors_ml)
            ax2.set_title('ML-Based Probabilities', fontsize=12, fontweight='bold')
            ax2.set_xlabel('Emotion')
            ax2.set_ylabel('Probability')
            ax2.tick_params(axis='x', rotation=45)
        
        # 3. Radar chart comparison
        ax3 = axes[2], projection='polar'
        from math import pi
        
        categories = emotions
        N = len(categories)
        angles = [n / float(N) * 2 * pi for n in range(N)]
        angles += angles[:1]
        
        # Lexicon values
        lexicon_values = list(result['lexicon_scores'].values())
        lexicon_values += lexicon_values[:1]
        ax3.plot(angles, lexicon_values, 'o-', linewidth=2, label='Lexicon', color='blue')
        ax3.fill(angles, lexicon_values, alpha=0.1, color='blue')
        
        # ML values
        if result['ml_scores']:
            ml_values = list(result['ml_scores'].values())
            ml_values += ml_values[:1]
            ax3.plot(angles, ml_values, 'o-', linewidth=2, label='ML', color='red')
            ax3.fill(angles, ml_values, alpha=0.1, color='red')
        
        ax3.set_xticks(angles[:-1])
        ax3.set_xticklabels(categories)
        ax3.set_ylim(0, 1)
        ax3.set_title('Emotion Profile Comparison', fontsize=12, fontweight='bold', pad=20)
        ax3.legend(loc='upper right', bbox_to_anchor=(1.3, 1.0))
        
        plt.suptitle(f'Emotion Analysis: "{text[:50]}..."\nConsensus: {result["consensus"]} (Confidence: {result["confidence"]})', 
                    fontsize=14, fontweight='bold')
        plt.tight_layout()
        plt.show()
        
        return result

# Initialize real-time analyzer
real_time_analyzer = RealTimeEmotionAnalyzer()

# Test with sample texts
test_texts = [
    "I'm absolutely overjoyed and thrilled with this amazing news!",
    "This is terrifying and I'm so scared about what might happen.",
    "I can't believe it! This is so unexpected and astonishing!",
    "This makes me furious! How could they do this?",
    "I feel so empty and heartbroken, like everything is hopeless."
]

print("\n" + "="*60)
print("REAL-TIME EMOTION ANALYSIS")
print("="*60)

for text in test_texts:
    result = real_time_analyzer.analyze_text(text)
    print(f"\n📝 Text: {text}")
    print(f"🎭 Primary Emotion: {result['consensus']} (Confidence: {result['confidence']})")
    print(f"📊 Lexicon-based: {result['lexicon_based']}")
    print(f"🤖 ML-based: {result['ml_based']}")
    
    # Show top 3 emotions
    if result['ml_scores']:
        sorted_emotions = sorted(result['ml_scores'].items(), key=lambda x: x[1], reverse=True)[:3]
        print("   Top emotions:", ', '.join([f"{e}: {s:.1%}" for e, s in sorted_emotions]))