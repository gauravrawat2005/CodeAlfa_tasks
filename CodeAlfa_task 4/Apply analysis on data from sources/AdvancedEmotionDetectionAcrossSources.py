class MultiSourceEmotionAnalyzer:
    """
    Emotion detection across multiple data sources
    """
    
    def __init__(self):
        # Emotion lexicons
        self.emotion_lexicons = {
            'joy': ['happy', 'joy', 'love', 'wonderful', 'amazing', 'great', 'excellent', 'fantastic',
                   'thrilled', 'delighted', 'pleased', 'grateful', 'blessed', 'excited'],
            'sadness': ['sad', 'unhappy', 'depressed', 'heartbroken', 'disappointed', 'sorry',
                       'grief', 'sorrow', 'miserable', 'down', 'upset', 'crying'],
            'anger': ['angry', 'mad', 'furious', 'hate', 'annoyed', 'frustrated', 'outraged',
                     'irritated', 'hostile', 'bitter', 'resentment'],
            'fear': ['afraid', 'scared', 'terrified', 'worried', 'anxious', 'nervous',
                    'panic', 'dread', 'horror', 'fearful'],
            'surprise': ['surprised', 'shocked', 'amazed', 'astonished', 'unexpected',
                        'stunned', 'speechless', 'incredible'],
            'disgust': ['disgusted', 'revolting', 'gross', 'repulsive', 'vile',
                       'nauseating', 'appalled', 'offensive']
        }
        
        self.vader = SentimentIntensityAnalyzer()
        
    def detect_emotions(self, text):
        """
        Detect multiple emotions in text
        """
        text_lower = text.lower()
        tokens = word_tokenize(text_lower)
        
        emotion_scores = {}
        for emotion, words in self.emotion_lexicons.items():
            # Count emotion words
            matches = sum(1 for word in tokens if word in words)
            
            # Calculate intensity based on matches and length
            if len(tokens) > 0:
                intensity = matches / len(tokens) * 10  # Scale to 0-10
            else:
                intensity = 0
            
            emotion_scores[emotion] = {
                'count': matches,
                'intensity': min(intensity, 10),  # Cap at 10
                'words_found': [word for word in tokens if word in words]
            }
        
        # Get primary emotion (highest intensity)
        if any(e['count'] > 0 for e in emotion_scores.values()):
            primary = max(emotion_scores.items(), key=lambda x: x[1]['intensity'])
            primary_emotion = primary[0]
            primary_intensity = primary[1]['intensity']
        else:
            primary_emotion = 'neutral'
            primary_intensity = 0
        
        return {
            'emotions': emotion_scores,
            'primary_emotion': primary_emotion,
            'primary_intensity': primary_intensity,
            'text_sample': text[:100]
        }
    
    def analyze_source(self, df, text_column='content', source_name=''):
        """
        Analyze emotions for an entire source
        """
        results = []
        for _, row in df.iterrows():
            text = row[text_column] if text_column in row else row.get('review_text', row.get('headline', ''))
            emotion_result = self.detect_emotions(str(text))
            
            result_row = {
                'source': source_name,
                'primary_emotion': emotion_result['primary_emotion'],
                'intensity': emotion_result['primary_intensity']
            }
            
            # Add emotion counts
            for emotion, data in emotion_result['emotions'].items():
                result_row[f'{emotion}_count'] = data['count']
                result_row[f'{emotion}_intensity'] = data['intensity']
            
            results.append(result_row)
        
        return pd.DataFrame(results)
    
    def generate_emotion_dashboard(self, amazon_df, social_df, news_df):
        """
        Create emotion comparison dashboard across sources
        """
        # Analyze each source
        amazon_emotions = self.analyze_source(amazon_df, text_column='review_text', source_name='Amazon')
        social_emotions = self.analyze_source(social_df, text_column='content', source_name='Social Media')
        news_emotions = self.analyze_source(news_df, text_column='headline', source_name='News')
        
        # Combine results
        all_emotions = pd.concat([amazon_emotions, social_emotions, news_emotions], ignore_index=True)
        
        # Create visualization
        fig, axes = plt.subplots(2, 3, figsize=(18, 12))
        
        # 1. Primary emotion distribution by source
        ax1 = axes[0, 0]
        emotion_by_source = pd.crosstab(all_emotions['source'], all_emotions['primary_emotion'])
        emotion_by_source.plot(kind='bar', ax=ax1, colormap='Set3', edgecolor='black')
        ax1.set_title('Primary Emotions by Source', fontsize=14, fontweight='bold')
        ax1.set_xlabel('Data Source')
        ax1.set_ylabel('Count')
        ax1.tick_params(axis='x', rotation=45)
        ax1.legend(title='Emotion')
        ax1.grid(True, alpha=0.3, axis='y')
        
        # 2. Average emotion intensity
        ax2 = axes[0, 1]
        emotions = list(self.emotion_lexicons.keys())
        x = np.arange(len(emotions))
        width = 0.25
        
        for i, source in enumerate(all_emotions['source'].unique()):
            source_data = all_emotions[all_emotions['source'] == source]
            intensities = [source_data[f'{e}_intensity'].mean() for e in emotions]
            ax2.bar(x + i*width, intensities, width, label=source, alpha=0.7)
        
        ax2.set_title('Average Emotion Intensity by Source', fontsize=14, fontweight='bold')
        ax2.set_xlabel('Emotion')
        ax2.set_ylabel('Average Intensity')
        ax2.set_xticks(x + width)
        ax2.set_xticklabels(emotions, rotation=45)
        ax2.legend()
        ax2.grid(True, alpha=0.3, axis='y')
        
        # 3. Emotion heatmap by source
        ax3 = axes[0, 2]
        emotion_matrix = []
        for source in all_emotions['source'].unique():
            source_data = all_emotions[all_emotions['source'] == source]
            row = [source_data[f'{e}_count'].mean() for e in emotions]
            emotion_matrix.append(row)
        
        sns.heatmap(emotion_matrix, annot=True, fmt='.2f', 
                   xticklabels=emotions, yticklabels=all_emotions['source'].unique(),
                   cmap='YlOrRd', ax=ax3, cbar_kws={'label': 'Avg Word Count'})
        ax3.set_title('Emotion Word Frequency by Source', fontsize=14, fontweight='bold')
        
        # 4. Amazon: Rating vs Emotion
        ax4 = axes[1, 0]
        if 'rating' in amazon_df.columns:
            amazon_with_emotions = amazon_df.copy()
            amazon_with_emotions['primary_emotion'] = amazon_emotions['primary_emotion']
            
            rating_emotion = pd.crosstab(amazon_with_emotions['rating'], amazon_with_emotions['primary_emotion'], normalize='index') * 100
            rating_emotion.plot(kind='bar', stacked=True, ax=ax4, colormap='Set3')
            ax4.set_title('Amazon: Emotion by Star Rating', fontsize=14, fontweight='bold')
            ax4.set_xlabel('Star Rating')
            ax4.set_ylabel('Percentage')
            ax4.legend(title='Emotion', bbox_to_anchor=(1.05, 1))
            ax4.grid(True, alpha=0.3, axis='y')
        
        # 5. Social Media: Platform Emotions
        ax5 = axes[1, 1]
        if 'platform' in social_df.columns:
            social_with_emotions = social_df.copy()
            social_with_emotions['primary_emotion'] = social_emotions['primary_emotion']
            
            platform_emotion = pd.crosstab(social_with_emotions['platform'], social_with_emotions['primary_emotion'])
            platform_emotion.plot(kind='bar', ax=ax5, colormap='Set3', edgecolor='black')
            ax5.set_title('Social Media: Emotions by Platform', fontsize=14, fontweight='bold')
            ax5.set_xlabel('Platform')
            ax5.set_ylabel('Count')
            ax5.tick_params(axis='x', rotation=45)
            ax5.legend(title='Emotion')
            ax5.grid(True, alpha=0.3, axis='y')
        
        # 6. News: Topic Emotions
        ax6 = axes[1, 2]
        if 'topic' in news_df.columns:
            news_with_emotions = news_df.copy()
            news_with_emotions['primary_emotion'] = news_emotions['primary_emotion']
            
            topic_emotion = pd.crosstab(news_with_emotions['topic'], news_with_emotions['primary_emotion'])
            topic_emotion.plot(kind='barh', ax=ax6, colormap='Set3', edgecolor='black')
            ax6.set_title('News: Emotions by Topic', fontsize=14, fontweight='bold')
            ax6.set_xlabel('Count')
            ax6.set_ylabel('Topic')
            ax6.legend(title='Emotion', bbox_to_anchor=(1.05, 1))
            ax6.grid(True, alpha=0.3, axis='x')
        
        plt.suptitle('EMOTION ANALYSIS ACROSS DATA SOURCES', fontsize=16, fontweight='bold', y=1.02)
        plt.tight_layout()
        plt.show()
        
        return all_emotions

# Run emotion analysis
print("\n" + "="*70)
print("EMOTION DETECTION ACROSS SOURCES")
print("="*70)

emotion_analyzer = MultiSourceEmotionAnalyzer()

# Analyze emotions across all sources
all_emotions = emotion_analyzer.generate_emotion_dashboard(
    amazon_reviews, 
    social_posts, 
    pd.concat([bbc_news, financial_news])
)

# Summary statistics
print("\nEmotion Analysis Summary:")
summary = all_emotions.groupby('source')['primary_emotion'].value_counts(normalize=True).unstack().fillna(0) * 100
print(summary.round(1))