class EmotionLexicons:
    """Comprehensive emotion lexicons from multiple sources"""
    
    def __init__(self):
        self.lexicons = {}
        self.load_nrc_lexicon()
        self.load_liec_lexicon()
        
    def load_nrc_lexicon(self):
        """NRC Emotion Lexicon (simulated)"""
        # In practice, you would load the actual NRC lexicon file
        # Here's a sample of emotion-word associations
        self.nrc_lexicon = {
            'joy': ['happy', 'joy', 'delight', 'pleasure', 'bliss', 'cheer', 'excitement',
                   'thrilled', 'ecstatic', 'glad', 'pleased', 'wonderful', 'fantastic',
                   'great', 'love', 'amazing', 'beautiful', 'perfect', 'blessed'],
            'sadness': ['sad', 'grief', 'sorrow', 'heartbroken', 'depressed', 'gloomy',
                       'miserable', 'down', 'upset', 'disappointed', 'crying', 'ache',
                       'hopeless', 'melancholy', 'hurt', 'pain', 'suffering'],
            'anger': ['angry', 'furious', 'mad', 'outrage', 'rage', 'hate', 'irritated',
                     'frustrated', 'annoyed', 'hostile', 'bitter', 'resentment', 
                     'infuriated', 'livid', 'seething'],
            'fear': ['fear', 'afraid', 'scared', 'terrified', 'anxious', 'worried',
                    'panic', 'dread', 'horror', 'nervous', 'threatened', 'vulnerable',
                    'apprehensive', 'uneasy', 'alarmed'],
            'surprise': ['surprise', 'shock', 'amaze', 'astonish', 'stun', 'unexpected',
                        'speechless', 'incredible', 'mind-blowing', 'remarkable',
                        'staggering', 'astounding'],
            'disgust': ['disgust', 'revolting', 'repulsive', 'gross', 'vile', 'nauseating',
                       'appalled', 'repulsed', 'loathsome', 'distasteful', 'offensive',
                       'sickening', 'contemptible']
        }
        
    def load_liec_lexicon(self):
        """LIWC-style emotion lexicon (simulated)"""
        self.liec_lexicon = {
            'positive_emotion': ['love', 'happy', 'joy', 'hope', 'grateful', 'excited',
                                'wonderful', 'fantastic', 'amazing', 'beautiful'],
            'negative_emotion': ['hate', 'angry', 'sad', 'fear', 'terrible', 'awful',
                                'horrible', 'pain', 'hurt', 'suffer'],
            'anxiety': ['worry', 'fear', 'nervous', 'anxious', 'terrified', 'scared',
                       'panic', 'dread'],
            'anger': ['anger', 'hate', 'furious', 'mad', 'rage', 'frustrated', 'annoyed'],
            'sadness': ['sad', 'grief', 'depressed', 'heartbroken', 'crying', 'sorrow']
        }
    
    def get_emotion_words(self, emotion):
        """Get words associated with specific emotion"""
        return self.nrc_lexicon.get(emotion, [])
    
    def get_all_emotions(self):
        """Get list of all emotions"""
        return list(self.nrc_lexicon.keys())

# Initialize lexicons
emotion_lexicons = EmotionLexicons()
print("Emotion Lexicons Loaded:")
print(f"Emotions covered: {', '.join(emotion_lexicons.get_all_emotions())}")