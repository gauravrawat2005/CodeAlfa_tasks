# VADER (Valence Aware Dictionary and sEntiment Reasoner)
class VADERSentimentAnalyzer:
    def __init__(self):
        self.analyzer = SentimentIntensityAnalyzer()
        
    def analyze(self, text):
        """Get sentiment scores"""
        scores = self.analyzer.polarity_scores(text)
        return scores
    
    def classify(self, text, threshold=0.05):
        """Classify text as positive, negative, or neutral"""
        scores = self.analyze(text)
        compound = scores['compound']
        
        if compound >= threshold:
            return 'Positive', 1
        elif compound <= -threshold:
            return 'Negative', -1
        else:
            return 'Neutral', 0

# Apply VADER
vader = VADERSentimentAnalyzer()

df['vader_scores'] = df['text'].apply(vader.analyze)
df['vader_sentiment'] = df['vader_scores'].apply(lambda x: 'Positive' if x['compound'] >= 0.05 
                                                  else ('Negative' if x['compound'] <= -0.05 else 'Neutral'))
df['vader_compound'] = df['vader_scores'].apply(lambda x: x['compound'])

# Calculate accuracy
vader_accuracy = accuracy_score(df['sentiment_label'], df['vader_sentiment'])

print("VADER Sentiment Analysis Results:")
print(f"Accuracy: {vader_accuracy:.2%}")
print("\nSample Results:")
print(df[['text', 'sentiment_label', 'vader_sentiment', 'vader_compound']].head(10))