class EmotionTextPreprocessor:
    def __init__(self):
        self.lemmatizer = WordNetLemmatizer()
        self.stop_words = set(stopwords.words('english'))
        # Keep emotion-bearing words
        emotion_words = set()
        for words in emotion_lexicons.nrc_lexicon.values():
            emotion_words.update(words)
        self.stop_words = self.stop_words - emotion_words
        
    def preprocess(self, text):
        """Advanced preprocessing for emotion detection"""
        # Convert to lowercase
        text = text.lower()
        
        # Remove punctuation but keep exclamation marks (emotion indicators)
        text = re.sub(r'[^\w\s!]', '', text)
        
        # Tokenize
        tokens = word_tokenize(text)
        
        # Remove stopwords but keep emotion words
        tokens = [self.lemmatizer.lemmatize(token) for token in tokens 
                 if token not in self.stop_words or token in emotion_lexicons.get_all_emotions()]
        
        return tokens
    
    def extract_emotion_features(self, tokens):
        """Extract features specifically for emotion detection"""
        features = {
            'exclamation_count': sum(1 for token in tokens if '!' in token),
            'capitalization_ratio': sum(1 for token in tokens if token.isupper()) / max(len(tokens), 1),
            'word_count': len(tokens),
            'unique_words': len(set(tokens))
        }
        
        # Emotion lexicon matches
        for emotion in emotion_lexicons.get_all_emotions():
            emotion_words = emotion_lexicons.get_emotion_words(emotion)
            features[f'{emotion}_words'] = sum(1 for token in tokens if token in emotion_words)
            features[f'{emotion}_ratio'] = features[f'{emotion}_words'] / max(len(tokens), 1)
        
        return features

# Initialize preprocessor
emotion_preprocessor = EmotionTextPreprocessor()

# Apply preprocessing
df['tokens'] = df['text'].apply(emotion_preprocessor.preprocess)
df['features'] = df['tokens'].apply(emotion_preprocessor.extract_emotion_features)

print("Sample Preprocessed Text:")
for i in range(3):
    print(f"\nOriginal: {df['text'].iloc[i]}")
    print(f"Tokens: {df['tokens'].iloc[i]}")
    print(f"Features: {df['features'].iloc[i]}")