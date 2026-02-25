class AmazonReviewAnalyzer:
    """
    Sentiment and emotion analyzer for Amazon product reviews
    Based on the Amazon Book Reviews dataset [citation:7]
    """
    
    def __init__(self):
        self.vader = SentimentIntensityAnalyzer()
        self.stop_words = set(stopwords.words('english'))
        
    def load_sample_data(self):
        """
        Load sample Amazon review data (in practice, you'd load the full dataset from Kaggle)
        The full dataset contains 3M reviews across 212K books [citation:7]
        """
        # Sample data structure based on Amazon review format [citation:7]
        sample_reviews = pd.DataFrame({
            'review_id': range(1, 101),
            'user_id': [f'user_{i}' for i in np.random.randint(1, 50, 100)],
            'product_id': [f'book_{i}' for i in np.random.randint(1, 30, 100)],
            'rating': np.random.choice([1, 2, 3, 4, 5], 100, p=[0.05, 0.1, 0.15, 0.3, 0.4]),
            'review_text': [
                "This book is absolutely amazing! I couldn't put it down. The characters are so well developed.",
                "Terrible waste of money. The plot makes no sense and the writing is poor.",
                "It's an okay book. Nothing special but passes the time.",
                "Life-changing read! Highly recommend to everyone interested in the topic.",
                "The author's best work yet. Beautiful prose and compelling story.",
                "Disappointing compared to their previous books. Expected much more.",
                "Average read, some parts drag on too long.",
                "Brilliant! Will definitely read again. Five stars!",
                "Not worth the hype. Overrated and poorly executed.",
                "Incredible depth and insight. A masterpiece.",
                "Couldn't finish it. Boring and pretentious.",
                "Perfect condition, fast delivery. The book itself is wonderful.",
                "The ending ruined everything. So frustrating!",
                "Informative and well-researched. Exactly what I needed.",
                "Too technical for casual readers. Dense and hard to follow."
            ] * 7,  # Repeat to get 100 samples
            'helpful_votes': np.random.randint(0, 50, 100),
            'total_votes': np.random.randint(1, 100, 100),
            'review_time': pd.date_range(start='2023-01-01', periods=100, freq='D')
        })
        
        # Calculate helpfulness ratio
        sample_reviews['helpfulness'] = sample_reviews['helpful_votes'] / sample_reviews['total_votes']
        
        return sample_reviews.head(100)  # Return first 100 unique
    
    def extract_emoji_features(self, text):
        """
        Extract emoji sentiment features
        Based on EEBERT research showing emojis significantly improve accuracy [citation:4]
        """
        emoji_list = []
        emoji_sentiment_scores = {
            '😊': 0.9, '❤️': 0.9, '👍': 0.8, '🎉': 0.9, '😍': 1.0,
            '😢': -0.8, '😠': -0.9, '👎': -0.8, '💔': -0.7, '😡': -1.0,
            '🤔': 0.0, '😐': 0.0, '😶': 0.0
        }
        
        # Extract emojis from text
        for char in text:
            if char in emoji.EMOJI_DATA:
                emoji_list.append(char)
        
        # Calculate emoji sentiment
        emoji_sentiment = 0
        for e in emoji_list:
            if e in emoji_sentiment_scores:
                emoji_sentiment += emoji_sentiment_scores[e]
        
        return {
            'emoji_count': len(emoji_list),
            'emoji_sentiment': emoji_sentiment / max(len(emoji_list), 1),
            'has_emoji': len(emoji_list) > 0
        }
    
    def analyze_review(self, text, rating=None):
        """
        Comprehensive review analysis combining text, emojis, and ratings
        """
        # VADER sentiment
        vader_scores = self.vader.polarity_scores(text)
        
        # Emoji features
        emoji_features = self.extract_emoji_features(text)
        
        # Star rating based sentiment (if available)
        rating_sentiment = None
        if rating:
            if rating >= 4:
                rating_sentiment = 'positive'
            elif rating <= 2:
                rating_sentiment = 'negative'
            else:
                rating_sentiment = 'neutral'
        
        # Combine signals for final sentiment
        text_sentiment = 'positive' if vader_scores['compound'] >= 0.05 else ('negative' if vader_scores['compound'] <= -0.05 else 'neutral')
        
        # Ensemble decision
        if rating_sentiment and emoji_features['has_emoji']:
            # Weighted combination
            signals = [text_sentiment, rating_sentiment]
            if emoji_features['emoji_sentiment'] > 0.3:
                signals.append('positive')
            elif emoji_features['emoji_sentiment'] < -0.3:
                signals.append('negative')
            
            # Majority vote
            from collections import Counter
            final_sentiment = Counter(signals).most_common(1)[0][0]
        else:
            final_sentiment = text_sentiment
        
        return {
            'text': text,
            'vader_scores': vader_scores,
            'text_sentiment': text_sentiment,
            'rating_sentiment': rating_sentiment,
            'emoji_features': emoji_features,
            'final_sentiment': final_sentiment,
            'confidence': abs(vader_scores['compound']) + (0.2 if emoji_features['has_emoji'] else 0)
        }
    
    def analyze_batch(self, df):
        """Analyze multiple reviews"""
        results = []
        for _, row in df.iterrows():
            analysis = self.analyze_review(row['review_text'], row['rating'])
            results.append({
                'review_id': row['review_id'],
                'rating': row['rating'],
                'helpfulness': row['helpfulness'],
                'vader_compound': analysis['vader_scores']['compound'],
                'text_sentiment': analysis['text_sentiment'],
                'rating_sentiment': analysis['rating_sentiment'],
                'final_sentiment': analysis['final_sentiment'],
                'emoji_count': analysis['emoji_features']['emoji_count'],
                'confidence': analysis['confidence']
            })
        
        return pd.DataFrame(results)

# Initialize analyzer
amazon_analyzer = AmazonReviewAnalyzer()

# Load sample data
amazon_reviews = amazon_analyzer.load_sample_data()
print("Amazon Reviews Sample:")
print(amazon_reviews[['review_id', 'rating', 'review_text', 'helpfulness']].head())