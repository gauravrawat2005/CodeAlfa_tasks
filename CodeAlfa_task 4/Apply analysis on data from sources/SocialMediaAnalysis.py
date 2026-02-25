class SocialMediaAnalyzer:
    """
    Sentiment and toxicity analyzer for social media content
    Based on MADOC dataset covering multiple platforms [citation:2][citation:8]
    """
    
    def __init__(self):
        self.vader = SentimentIntensityAnalyzer()
        
        # Toxicity lexicon (simplified)
        self.toxic_words = [
            'hate', 'stupid', 'idiot', 'dumb', 'loser', 'terrible', 'awful',
            'worst', 'useless', 'pathetic', 'disgusting', 'repulsive'
        ]
        
        # Platform-specific characteristics
        self.platforms = ['Bluesky', 'Koo', 'Reddit', 'Voat']
        
    def generate_sample_social_data(self, n_samples=200):
        """
        Generate sample social media posts mimicking MADOC structure [citation:2]
        """
        platforms = np.random.choice(self.platforms, n_samples)
        
        sample_posts = []
        for i, platform in enumerate(platforms):
            # Generate platform-appropriate content
            if platform == 'Reddit':
                post = self._generate_reddit_post()
            elif platform == 'Bluesky':
                post = self._generate_bluesky_post()
            elif platform == 'Koo':
                post = self._generate_koo_post()
            else:  # Voat
                post = self._generate_voat_post()
            
            sample_posts.append({
                'post_id': f'{platform.lower()}_{i}',
                'platform': platform,
                'content': post['text'],
                'timestamp': pd.Timestamp.now() - pd.Timedelta(days=np.random.randint(0, 365)),
                'likes': np.random.randint(0, 1000),
                'reposts': np.random.randint(0, 100),
                'replies': np.random.randint(0, 50),
                'user_followers': np.random.randint(0, 10000),
                'toxicity_score': post.get('toxicity', np.random.random()),
                'hashtags': post.get('hashtags', [])
            })
        
        return pd.DataFrame(sample_posts)
    
    def _generate_reddit_post(self):
        texts = [
            "I completely agree with this viewpoint. Well said!",
            "This is the worst take I've ever seen. You're clearly misinformed.",
            "Has anyone else experienced this issue? Looking for advice.",
            "Great discussion everyone! Thanks for the insights.",
            "Mods please remove this spam content.",
            "Can someone explain this to me? I'm confused.",
            "This post is gold! Thanks for sharing."
        ]
        return {'text': np.random.choice(texts), 'toxicity': np.random.random() * 0.3}
    
    def _generate_bluesky_post(self):
        texts = [
            "Just finished an amazing book! Highly recommend 📚 #reading",
            "Feeling grateful today. Life is beautiful ✨",
            "Why is everyone so negative? Let's spread some positivity!",
            "New blog post is up! Check it out at link 🔗",
            "Beautiful sunset today! Nature is incredible 🌅"
        ]
        hashtags = np.random.choice(['#reading', '#life', '#nature', '#tech'], 2, replace=False).tolist()
        return {'text': np.random.choice(texts), 'hashtags': hashtags, 'toxicity': np.random.random() * 0.2}
    
    def _generate_koo_post(self):
        texts = [
            "Great to see the community growing! 🇮🇳",
            "What are your thoughts on the latest update?",
            "Supporting local businesses today! #VocalForLocal",
            "Learning so much from everyone here. Thank you!"
        ]
        return {'text': np.random.choice(texts), 'toxicity': np.random.random() * 0.15}
    
    def _generate_voat_post(self):
        texts = [
            "Unpopular opinion: I actually think this is overrated.",
            "Can we have a real discussion without censorship?",
            "This is exactly what I've been saying for years.",
            "The truth needs to be told, no matter what."
        ]
        return {'text': np.random.choice(texts), 'toxicity': 0.3 + np.random.random() * 0.5}  # Higher toxicity baseline for Voat
    
    def analyze_post(self, post):
        """Analyze individual social media post"""
        text = post['content']
        
        # VADER sentiment
        vader_scores = self.vader.polarity_scores(text)
        
        # Toxicity detection
        text_lower = text.lower()
        toxic_matches = sum(1 for word in self.toxic_words if word in text_lower)
        toxicity_level = min(toxic_matches / max(len(text.split()), 1) * 10, 1.0)  # Normalize
        
        # Engagement metrics as signal
        engagement_score = np.log1p(post['likes'] + post['reposts'] + post['replies']) / 10
        
        # Platform bias adjustment
        platform_bias = {
            'Bluesky': 0.1,  # Generally positive
            'Koo': 0.05,      # Neutral-positive
            'Reddit': 0.0,    # Neutral
            'Voat': -0.2      # Negative bias [citation:8]
        }
        
        adjusted_sentiment = vader_scores['compound'] + platform_bias.get(post['platform'], 0)
        
        return {
            'post_id': post['post_id'],
            'platform': post['platform'],
            'sentiment_compound': adjusted_sentiment,
            'sentiment_label': 'positive' if adjusted_sentiment >= 0.05 else ('negative' if adjusted_sentiment <= -0.05 else 'neutral'),
            'toxicity_score': toxicity_level,
            'engagement_score': engagement_score,
            'is_toxic': toxicity_level > 0.3,
            'vader_original': vader_scores['compound']
        }
    
    def analyze_batch(self, df):
        """Analyze multiple social media posts"""
        results = []
        for _, row in df.iterrows():
            analysis = self.analyze_post(row)
            results.append(analysis)
        
        return pd.DataFrame(results)

# Initialize social media analyzer
social_analyzer = SocialMediaAnalyzer()

# Generate sample data
social_posts = social_analyzer.generate_sample_social_data(500)
print("\nSocial Media Posts Sample (MADOC-style):")
print(social_posts.groupby('platform').size())
print(social_posts[['platform', 'content', 'likes', 'replies']].head())