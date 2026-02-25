class AdvancedEmotionDetector:
    """Combines lexicon-based features with ML"""
    
    def __init__(self):
        self.lexicon_detector = LexiconEmotionDetector()
        self.preprocessor = emotion_preprocessor
        self.label_encoder = LabelEncoder()
        self.model = None
        self.vectorizer = None
        
    def extract_enhanced_features(self, texts):
        """Extract comprehensive features for emotion detection"""
        features_list = []
        
        for text in texts:
            # Basic features
            tokens = self.preprocessor.preprocess(text)
            text_lower = text.lower()
            
            feature_dict = {
                'length': len(text),
                'word_count': len(tokens),
                'unique_words': len(set(tokens)),
                'exclamation_count': text.count('!'),
                'question_count': text.count('?'),
                'capitalized_words': sum(1 for word in tokens if word.isupper()),
                'avg_word_length': np.mean([len(word) for word in tokens]) if tokens else 0
            }
            
            # Lexicon-based emotion scores
            lexicon_result = self.lexicon_detector.detect_emotions(text)
            for emotion, score in lexicon_result['all_scores'].items():
                feature_dict[f'lexicon_{emotion}'] = score
            
            # POS tags features (simplified)
            pos_tags = nltk.pos_tag(tokens)
            adjectives = sum(1 for _, tag in pos_tags if tag.startswith('JJ'))
            adverbs = sum(1 for _, tag in pos_tags if tag.startswith('RB'))
            verbs = sum(1 for _, tag in pos_tags if tag.startswith('VB'))
            
            feature_dict['adjective_ratio'] = adjectives / max(len(tokens), 1)
            feature_dict['adverb_ratio'] = adverbs / max(len(tokens), 1)
            feature_dict['verb_ratio'] = verbs / max(len(tokens), 1)
            
            # Intensity markers
            intensity_words = ['very', 'really', 'extremely', 'absolutely', 'completely']
            feature_dict['intensity_markers'] = sum(1 for word in tokens if word in intensity_words)
            
            features_list.append(feature_dict)
        
        return pd.DataFrame(features_list)
    
    def train(self, texts, emotions):
        """Train the advanced emotion detector"""
        # Extract features
        X_features = self.extract_enhanced_features(texts)
        
        # Add TF-IDF features
        self.vectorizer = TfidfVectorizer(max_features=500, ngram_range=(1, 2))
        X_tfidf = self.vectorizer.fit_transform(texts)
        
        # Combine features
        from scipy.sparse import hstack, csr_matrix
        X_combined = hstack([csr_matrix(X_features.values), X_tfidf])
        
        # Encode labels
        y_encoded = self.label_encoder.fit_transform(emotions)
        
        # Train model
        self.model = RandomForestClassifier(n_estimators=200, random_state=42)
        self.model.fit(X_combined, y_encoded)
        
        # Cross-validation
        cv_scores = cross_val_score(self.model, X_combined, y_encoded, cv=5)
        
        return {
            'cv_mean': cv_scores.mean(),
            'cv_std': cv_scores.std(),
            'feature_importance': dict(zip(
                list(X_features.columns) + list(self.vectorizer.get_feature_names_out()),
                self.model.feature_importances_
            ))
        }
    
    def predict(self, text, return_details=False):
        """Predict emotions with detailed explanation"""
        # Extract features
        X_features = self.extract_enhanced_features([text])
        X_tfidf = self.vectorizer.transform([text])
        
        from scipy.sparse import hstack, csr_matrix
        X_combined = hstack([csr_matrix(X_features.values), X_tfidf])
        
        # Predict
        pred = self.model.predict(X_combined)[0]
        proba = self.model.predict_proba(X_combined)[0]
        
        emotion = self.label_encoder.inverse_transform([pred])[0]
        
        if return_details:
            # Get feature importance for this prediction
            feature_importance = {}
            for feature, importance in zip(
                list(X_features.columns) + list(self.vectorizer.get_feature_names_out()),
                self.model.feature_importances_
            ):
                feature_importance[feature] = importance
            
            return {
                'emotion': emotion,
                'confidence': max(proba),
                'probabilities': dict(zip(self.label_encoder.classes_, proba)),
                'feature_importance': feature_importance
            }
        else:
            return emotion

# Initialize and train advanced detector
print("Training Advanced Emotion Detector...")
advanced_detector = AdvancedEmotionDetector()
training_results = advanced_detector.train(df['text'].tolist(), df['emotion'].tolist())

print(f"\nCross-validation Score: {training_results['cv_mean']:.2%} (+/- {training_results['cv_std']:.2%})")