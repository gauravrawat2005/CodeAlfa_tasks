class SentimentAnalyzer:
    def __init__(self, model_type='logistic'):
        self.preprocessor = TextPreprocessor()
        self.vader = VADERSentimentAnalyzer()
        
        # Train best model on all data
        if model_type == 'logistic':
            self.pipeline = Pipeline([
                ('vectorizer', TfidfVectorizer(max_features=1000, ngram_range=(1, 2))),
                ('classifier', LogisticRegression(random_state=42, max_iter=1000))
            ])
        else:
            self.pipeline = Pipeline([
                ('vectorizer', TfidfVectorizer(max_features=1000, ngram_range=(1, 2))),
                ('classifier', MultinomialNB())
            ])
        
        # Train on all data
        self.pipeline.fit(df['cleaned_text'], df['sentiment'])
        
    def predict(self, text, method='ensemble'):
        """
        Predict sentiment of input text
        method: 'vader', 'ml', or 'ensemble'
        """
        cleaned = self.preprocessor.preprocess(text)
        
        if method == 'vader':
            sentiment, score = self.vader.classify(text)
            confidence = abs(self.vader.analyze(text)['compound'])
            return sentiment, confidence, score
            
        elif method == 'ml':
            pred = self.pipeline.predict([cleaned])[0]
            if hasattr(self.pipeline.named_steps['classifier'], 'predict_proba'):
                proba = self.pipeline.predict_proba([cleaned])[0]
                confidence = max(proba)
            else:
                confidence = 0.7  # Default confidence
                
            sentiment = ['Negative', 'Neutral', 'Positive'][pred + 1]
            return sentiment, confidence, pred
            
        else:  # ensemble
            # Get both predictions
            vader_sentiment, vader_conf, vader_score = self.predict(text, 'vader')
            ml_sentiment, ml_conf, ml_score = self.predict(text, 'ml')
            
            # Weighted combination
            vader_weight = 0.4
            ml_weight = 0.6
            
            # Combine scores
            combined_score = vader_weight * vader_score + ml_weight * ml_score
            
            # Determine sentiment based on combined score
            if combined_score >= 0.3:
                sentiment = 'Positive'
            elif combined_score <= -0.3:
                sentiment = 'Negative'
            else:
                sentiment = 'Neutral'
                
            confidence = (vader_weight * vader_conf + ml_weight * ml_conf) / (vader_weight + ml_weight)
            
            return sentiment, confidence, combined_score
    
    def analyze_batch(self, texts):
        """Analyze multiple texts"""
        results = []
        for text in texts:
            sentiment, confidence, score = self.predict(text)
            results.append({
                'text': text,
                'sentiment': sentiment,
                'confidence': confidence,
                'score': score
            })
        return pd.DataFrame(results)

# Initialize analyzer
analyzer = SentimentAnalyzer(model_type='logistic')

# Test with new examples
test_texts = [
    "I absolutely love this product! It's the best thing ever!",
    "This is terrible, I want my money back. Complete disappointment.",
    "It's okay, nothing special but does the job.",
    "The customer service was amazing and the product exceeded expectations!",
    "Worst experience ever, would give zero stars if I could.",
    "Average quality, decent for the price point."
]

print("Real-time Sentiment Analysis:")
print("="*60)
results_df = analyzer.analyze_batch(test_texts)
for _, row in results_df.iterrows():
    sentiment = row['sentiment']
    confidence = row['confidence']
    
    # Color coding for display
    if sentiment == 'Positive':
        color = '\033[92m'  # Green
    elif sentiment == 'Negative':
        color = '\033[91m'  # Red
    else:
        color = '\033[94m'  # Blue
        
    reset = '\033[0m'
    
    print(f"\nText: {row['text']}")
    print(f"Sentiment: {color}{sentiment}{reset} (Confidence: {confidence:.1%})")