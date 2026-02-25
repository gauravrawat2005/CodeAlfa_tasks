class ProductInsightEngine:
    """
    Extract product development insights from customer feedback
    Based on TechSmith's approach to survey sentiment analysis [citation:2]
    """
    
    def __init__(self):
        self.aspect_analyzer = self._initialize_aspect_analyzer()
        
    def _initialize_aspect_analyzer(self):
        """Create aspect-based sentiment analysis capability"""
        # Product aspects to track
        self.aspects = {
            'usability': ['easy', 'difficult', 'confusing', 'intuitive', 'clunky'],
            'performance': ['slow', 'fast', 'crash', 'lag', 'responsive'],
            'features': ['missing', 'need', 'would like', 'wish', 'could use'],
            'pricing': ['expensive', 'cheap', 'worth', 'value', 'cost'],
            'support': ['help', 'customer service', 'response', 'fixed', 'issue']
        }
        return self.aspects
    
    def analyze_product_feedback(self, feedback_data):
        """
        Extract actionable product insights from customer feedback
        """
        aspect_scores = {aspect: {'positive': 0, 'negative': 0, 'total': 0} 
                        for aspect in self.aspects}
        
        feature_requests = []
        pain_points = []
        
        for _, row in feedback_data.iterrows():
            text = row['feedback'].lower()
            
            # Track aspect sentiment
            for aspect, keywords in self.aspects.items():
                for keyword in keywords:
                    if keyword in text:
                        aspect_scores[aspect]['total'] += 1
                        if row['sentiment'] > 0:
                            aspect_scores[aspect]['positive'] += 1
                        elif row['sentiment'] < 0:
                            aspect_scores[aspect]['negative'] += 1
                        
                        # Extract specific feedback
                        if 'need' in text or 'would like' in text:
                            feature_requests.append({
                                'feature': text,
                                'aspect': aspect,
                                'sentiment': row['sentiment']
                            })
                        elif any(word in text for word in ['broken', 'doesn\'t', 'issue', 'problem']):
                            pain_points.append({
                                'issue': text,
                                'aspect': aspect,
                                'urgency': abs(row['sentiment']) if row['sentiment'] < 0 else 0
                            })
        
        # Calculate net sentiment by aspect
        for aspect in aspect_scores:
            total = aspect_scores[aspect]['total']
            if total > 0:
                aspect_scores[aspect]['net_sentiment'] = (
                    aspect_scores[aspect]['positive'] - aspect_scores[aspect]['negative']
                ) / total
            else:
                aspect_scores[aspect]['net_sentiment'] = 0
        
        return {
            'aspect_sentiment': aspect_scores,
            'top_feature_requests': sorted(feature_requests, 
                                          key=lambda x: x['sentiment'], reverse=True)[:10],
            'critical_pain_points': sorted(pain_points, 
                                          key=lambda x: x['urgency'], reverse=True)[:10],
            'priority_matrix': self._create_priority_matrix(aspect_scores)
        }
    
    def _create_priority_matrix(self, aspect_scores):
        """Create impact vs urgency matrix for product decisions"""
        matrix = []
        for aspect, scores in aspect_scores.items():
            if scores['total'] > 0:
                impact = scores['positive'] / scores['total']  # % positive
                urgency = scores['negative'] / scores['total']  # % negative
                volume = scores['total']
                
                matrix.append({
                    'aspect': aspect,
                    'impact': impact,
                    'urgency': urgency,
                    'volume': volume,
                    'priority': 'high' if urgency > 0.3 and volume > 10 else
                               'medium' if urgency > 0.15 else 'low'
                })
        
        return sorted(matrix, key=lambda x: x['urgency'], reverse=True)

# Example: Product feedback analysis
product_feedback = pd.DataFrame({
    'feedback': [
        "The new interface is so intuitive! Love the drag and drop feature.",
        "Why can't I export to PDF? This basic feature is missing.",
        "App keeps crashing when I try to save large files.",
        "Great value for money, best tool I've used.",
        "Customer support took 3 days to respond to my issue.",
        "Would love to see collaboration features added.",
        "The learning curve is too steep for new users.",
        "Perfect for my needs, exactly what I was looking for."
    ] * 25,  # Repeat for more data
    'sentiment': [0.8, -0.6, -0.9, 0.7, -0.4, 0.3, -0.5, 0.9] * 25
})

product_engine = ProductInsightEngine()
insights = product_engine.analyze_product_feedback(product_feedback)

print("\n🔧 Product Development Insights:")
print(f"Top priority aspect: {insights['priority_matrix'][0]['aspect']} "
      f"(urgency: {insights['priority_matrix'][0]['urgency']:.1%})")
print(f"Critical pain points: {len(insights['critical_pain_points'])}")
print(f"Feature requests: {len(insights['top_feature_requests'])}")