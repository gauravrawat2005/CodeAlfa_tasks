class ProductionSentimentAnalyzer:
    """
    Complete sentiment analysis system ready for production deployment
    """
    def __init__(self, model_path=None):
        self.preprocessor = TextPreprocessor()
        self.vader = SentimentIntensityAnalyzer()
        self.model = None
        self.vectorizer = None
        self.metrics = {}
        
    def train(self, texts, labels, test_size=0.2):
        """Train the sentiment analysis model"""
        # Preprocess texts
        cleaned_texts = [self.preprocessor.preprocess(text) for text in texts]
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            cleaned_texts, labels, test_size=test_size, random_state=42
        )
        
        # Create pipeline
        self.vectorizer = TfidfVectorizer(max_features=2000, ngram_range=(1, 3))
        self.model = LogisticRegression(random_state=42, max_iter=1000, class_weight='balanced')
        
        # Transform and train
        X_train_vec = self.vectorizer.fit_transform(X_train)
        self.model.fit(X_train_vec, y_train)
        
        # Evaluate
        X_test_vec = self.vectorizer.transform(X_test)
        y_pred = self.model.predict(X_test_vec)
        
        # Store metrics
        self.metrics = {
            'accuracy': accuracy_score(y_test, y_pred),
            'confusion_matrix': confusion_matrix(y_test, y_pred),
            'classification_report': classification_report(y_test, y_pred)
        }
        
        return self.metrics
    
    def predict(self, text, return_probabilities=False):
        """
        Predict sentiment for a single text
        """
        # Clean text
        cleaned = self.preprocessor.preprocess(text)
        
        # Vectorize
        vec = self.vectorizer.transform([cleaned])
        
        # Predict
        prediction = self.model.predict(vec)[0]
        
        if return_probabilities:
            probabilities = self.model.predict_proba(vec)[0]
            return {
                'sentiment': ['Negative', 'Neutral', 'Positive'][prediction + 1],
                'score': prediction,
                'probabilities': {
                    'negative': probabilities[0],
                    'neutral': probabilities[1],
                    'positive': probabilities[2]
                },
                'confidence': max(probabilities)
            }
        else:
            return {
                'sentiment': ['Negative', 'Neutral', 'Positive'][prediction + 1],
                'score': prediction
            }
    
    def predict_batch(self, texts):
        """Predict sentiment for multiple texts"""
        cleaned_texts = [self.preprocessor.preprocess(text) for text in texts]
        vec = self.vectorizer.transform(cleaned_texts)
        predictions = self.model.predict(vec)
        
        results = []
        for text, pred in zip(texts, predictions):
            results.append({
                'text': text,
                'sentiment': ['Negative', 'Neutral', 'Positive'][pred + 1],
                'score': pred
            })
        
        return pd.DataFrame(results)
    
    def explain_prediction(self, text):
        """
        Explain which words influenced the prediction
        """
        cleaned = self.preprocessor.preprocess(text)
        vec = self.vectorizer.transform([cleaned])
        
        # Get feature names and coefficients
        feature_names = self.vectorizer.get_feature_names_out()
        coefficients = self.model.coef_[0]
        
        # Get non-zero features for this text
        non_zero_idx = vec.nonzero()[1]
        
        word_contributions = []
        for idx in non_zero_idx:
            word = feature_names[idx]
            coef = coefficients[idx]
            word_contributions.append({
                'word': word,
                'coefficient': coef,
                'contribution': 'positive' if coef > 0 else 'negative'
            })
        
        # Sort by absolute coefficient value
        word_contributions.sort(key=lambda x: abs(x['coefficient']), reverse=True)
        
        return word_contributions[:10]  # Return top 10 influencing words

# Example usage
print("\n" + "="*60)
print("PRODUCTION-READY SENTIMENT ANALYZER")
print("="*60)

# Initialize and train
prod_analyzer = ProductionSentimentAnalyzer()
metrics = prod_analyzer.train(df['text'].tolist(), df['sentiment'].tolist())

print(f"\nModel Training Complete!")
print(f"Accuracy: {metrics['accuracy']:.2%}")
print(f"\nClassification Report:\n{metrics['classification_report']}")

# Test predictions
test_phrases = [
    "This is absolutely wonderful! I'm so happy with my purchase.",
    "Terrible experience, would never recommend to anyone.",
    "It's okay, nothing special but it works."
]

print("\nSample Predictions:")
for phrase in test_phrases:
    result = prod_analyzer.predict(phrase, return_probabilities=True)
    print(f"\nText: {phrase}")
    print(f"Sentiment: {result['sentiment']} (Confidence: {result['confidence']:.1%})")
    
    # Show explanation
    explanation = prod_analyzer.explain_prediction(phrase)
    print("Top influencing words:")
    for word in explanation[:3]:
        print(f"  - {word['word']}: {word['contribution']} impact ({word['coefficient']:.3f})")