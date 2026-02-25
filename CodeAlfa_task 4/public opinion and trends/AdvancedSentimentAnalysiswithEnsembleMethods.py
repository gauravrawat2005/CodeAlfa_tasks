class EnsembleSentimentAnalyzer:
    """
    Hybrid sentiment analysis combining multiple approaches
    Based on research showing ensemble methods outperform single models [citation:9][citation:10]
    """
    
    def __init__(self):
        # Rule-based sentiment
        self.vader = SentimentIntensityAnalyzer()
        
        # Transformer-based model (DistilBERT for efficiency)
        self.model_name = "distilbert-base-uncased-finetuned-sst-2-english"
        try:
            self.transformer_pipeline = pipeline(
                "sentiment-analysis",
                model=self.model_name,
                tokenizer=self.model_name,
                max_length=512,
                truncation=True
            )
        except:
            print("Transformer model not available, using fallback")
            self.transformer_pipeline = None
        
    def analyze_vader(self, text):
        """VADER sentiment analysis"""
        scores = self.vader.polarity_scores(text)
        return {
            'compound': scores['compound'],
            'positive': scores['pos'],
            'negative': scores['neg'],
            'neutral': scores['neu']
        }
    
    def analyze_transformer(self, text):
        """Transformer-based sentiment analysis"""
        if self.transformer_pipeline:
            try:
                result = self.transformer_pipeline(text)[0]
                # Convert to VADER-like scale
                score = result['score']
                if result['label'] == 'POSITIVE':
                    return {'compound': score, 'confidence': score}
                else:
                    return {'compound': -score, 'confidence': score}
            except:
                pass
        return {'compound': 0, 'confidence': 0.5}
    
    def ensemble_analysis(self, text, weights=None):
        """
        Combine multiple models for robust sentiment analysis
        Default weights: 0.4 VADER, 0.6 Transformer [citation:9]
        """
        if weights is None:
            weights = {'vader': 0.4, 'transformer': 0.6}
        
        # Get individual predictions
        vader_result = self.analyze_vader(text)
        transformer_result = self.analyze_transformer(text)
        
        # Weighted combination
        ensemble_score = (
            weights['vader'] * vader_result['compound'] +
            weights['transformer'] * transformer_result['compound']
        )
        
        # Calculate confidence based on model agreement
        confidence = 1 - abs(vader_result['compound'] - transformer_result['compound']) / 2
        
        return {
            'ensemble_score': ensemble_score,
            'ensemble_sentiment': 'positive' if ensemble_score > 0.1 else ('negative' if ensemble_score < -0.1 else 'neutral'),
            'vader_score': vader_result['compound'],
            'transformer_score': transformer_result['compound'],
            'confidence': confidence,
            'vader_details': vader_result
        }

# Initialize analyzer
ensemble_analyzer = EnsembleSentimentAnalyzer()

# Test with sample texts
test_texts = [
    "This new policy is absolutely amazing! It will change everything for the better.",
    "The government's handling of this crisis is completely unacceptable.",
    "I have mixed feelings about the recent announcement.",
    "Why is nobody talking about the real issues here?",
    "This is the best news I've heard all year!",
    "The situation is getting worse every day."
]

print("\nEnsemble Sentiment Analysis Results:")
for text in test_texts:
    result = ensemble_analyzer.ensemble_analysis(text)
    print(f"\nText: {text[:50]}...")
    print(f"Ensemble: {result['ensemble_sentiment']} (score: {result['ensemble_score']:.3f})")
    print(f"Confidence: {result['confidence']:.1%}")