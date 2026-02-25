class EmotionPatternAnalyzer:
    """Analyze emotion patterns and generate insights"""
    
    def __init__(self):
        self.analyzer = real_time_analyzer
        
    def analyze_corpus(self, texts):
        """Analyze emotion patterns in a corpus of texts"""
        results = []
        for text in texts:
            result = self.analyzer.analyze_text(text, detailed=False)
            results.append({
                'text': text,
                'emotion': result['consensus'],
                'intensity': result['intensity'],
                'lexicon_scores': result['lexicon_scores']
            })
        
        df_results = pd.DataFrame(results)
        
        # Generate insights
        insights = {
            'total_texts': len(df_results),
            'emotion_distribution': df_results['emotion'].value_counts().to_dict(),
            'average_intensity': df_results['intensity'].mean(),
            'most_common_emotion': df_results['emotion'].mode()[0],
            'emotion_cooccurrence': self.calculate_cooccurrence(df_results)
        }
        
        return df_results, insights
    
    def calculate_cooccurrence(self, df_results):
        """Calculate emotion co-occurrence patterns"""
        cooccurrence = defaultdict(lambda: defaultdict(int))
        
        for _, row in df_results.iterrows():
            main_emotion = row['emotion']
            # Find secondary emotions from lexicon scores
            scores = row['lexicon_scores']
            for emotion, score in scores.items():
                if emotion != main_emotion and score > 0.2:  # Threshold for co-occurrence
                    cooccurrence[main_emotion][emotion] += 1
        
        return cooccurrence
    
    def generate_report(self, df_results, insights):
        """Generate comprehensive emotion analysis report"""
        
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        
        # 1. Emotion distribution
        ax1 = axes[0, 0]
        emotion_counts = df_results['emotion'].value_counts()
        colors = [real_time_analyzer.emotion_colors.get(e, '#95a5a6') for e in emotion_counts.index]
        emotion_counts.plot(kind='bar', ax=ax1, color=colors)
        ax1.set_title('Emotion Distribution in Corpus', fontsize=12, fontweight='bold')
        ax1.set_xlabel('Emotion')
        ax1.set_ylabel('Count')
        ax1.tick_params(axis='x', rotation=45)
        
        # 2. Intensity distribution
        ax2 = axes[0, 1]
        df_results['intensity'].hist(bins=20, ax=ax2, color='#3498db', edgecolor='black', alpha=0.7)
        ax2.axvline(df_results['intensity'].mean(), color='red', linestyle='--', 
                   label=f"Mean: {df_results['intensity'].mean():.2f}")
        ax2.set_title('Emotion Intensity Distribution', fontsize=12, fontweight='bold')
        ax2.set_xlabel('Intensity')
        ax2.set_ylabel('Frequency')
        ax2.legend()
        
        # 3. Co-occurrence heatmap
        ax3 = axes[1, 0]
        emotions = list(real_time_analyzer.emotion_colors.keys())
        co_matrix = np.zeros((len(emotions), len(emotions)))
        
        for i, e1 in enumerate(emotions):
            for j, e2 in enumerate(emotions):
                co_matrix[i, j] = insights['emotion_cooccurrence'].get(e1, {}).get(e2, 0)
        
        sns.heatmap(co_matrix, annot=True, fmt='g', 
                   xticklabels=emotions, yticklabels=emotions,
                   cmap='YlOrRd', ax=ax3)
        ax3.set_title('Emotion Co-occurrence Matrix', fontsize=12, fontweight='bold')
        
        # 4. Key insights text
        ax4 = axes[1, 1]
        ax4.axis('off')
        
        insight_text = f"""
        📊 EMOTION ANALYSIS INSIGHTS
        
        Total Texts Analyzed: {insights['total_texts']}
        
        🎭 Most Common Emotion: {insights['most_common_emotion']}
        
        📈 Average Intensity: {insights['average_intensity']:.2f}
        
        Distribution:
        """
        
        for emotion, count in insights['emotion_distribution'].items():
            percentage = count/insights['total_texts']*100
            insight_text += f"\n   {emotion}: {count} ({percentage:.1f}%)"
        
        insight_text += f"""
        
        Key Patterns:
        • {insights['most_common_emotion']} tends to co-occur with 
          {list(insights['emotion_cooccurrence'].get(insights['most_common_emotion'], {}).keys())[:2]}
        • Highest intensity found in {df_results.loc[df_results['intensity'].idxmax(), 'emotion']} texts
        """
        
        ax4.text(0.1, 0.9, insight_text, fontsize=10, va='top',
                bbox=dict(boxstyle='round', facecolor='#f0f2f5', alpha=0.9))
        
        plt.tight_layout()
        plt.show()

# Analyze emotion patterns
print("\n" + "="*60)
print("EMOTION PATTERN ANALYSIS")
print("="*60)

pattern_analyzer = EmotionPatternAnalyzer()
df_results, insights = pattern_analyzer.analyze_corpus(df['text'].tolist())

print(f"\nAnalysis Complete!")
print(f"Total texts analyzed: {insights['total_texts']}")
print(f"\nEmotion Distribution:")
for emotion, count in insights['emotion_distribution'].items():
    print(f"  {emotion}: {count} ({count/insights['total_texts']*100:.1f}%)")

# Generate visualization report
pattern_analyzer.generate_report(df_results, insights)