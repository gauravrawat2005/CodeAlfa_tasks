class NewsAnalyzer:
    """
    Sentiment analyzer for news articles and headlines
    Based on Business Insider Financial dataset [citation:3] and BBC News dataset [citation:9]
    """
    
    def __init__(self):
        self.vader = SentimentIntensityAnalyzer()
        
        # Financial sentiment lexicon
        self.financial_positive = [
            'profit', 'gain', 'growth', 'rise', 'surge', 'boom', 'rally',
            'upgrade', 'beat', 'exceed', 'positive', 'strong', 'record'
        ]
        
        self.financial_negative = [
            'loss', 'decline', 'fall', 'drop', 'slump', 'crash', 'downgrade',
            'miss', 'weak', 'negative', 'concern', 'risk', 'uncertainty'
        ]
        
    def generate_sample_news(self, source='bbc', n_samples=100):
        """
        Generate sample news data
        For BBC News: multi-topic articles [citation:9]
        For Business Insider: financial news [citation:3]
        """
        if source == 'bbc':
            return self._generate_bbc_news(n_samples)
        else:
            return self._generate_financial_news(n_samples)
    
    def _generate_bbc_news(self, n_samples):
        """Generate BBC-style news with various topics [citation:9]"""
        topics = ['business', 'technology', 'politics', 'sport', 'entertainment']
        
        headlines = {
            'business': [
                "Economy shows signs of recovery as growth exceeds expectations",
                "Major company announces job cuts amid restructuring",
                "New trade deal could boost exports by 15%",
                "Inflation rises faster than predicted, concern for households",
                "Tech startup valued at $1 billion after successful funding round"
            ],
            'technology': [
                "Breakthrough in AI research promises revolutionary applications",
                "Social media platform faces criticism over data privacy",
                "New smartphone release breaks pre-order records",
                "Cybersecurity experts warn of increasing threats",
                "Green technology investment reaches all-time high"
            ],
            'politics': [
                "Government announces major policy shift on climate change",
                "Election results show unexpected swing in key regions",
                "International summit aims to address global challenges",
                "Minister resigns following controversy",
                "Public approval ratings improve after successful initiative"
            ],
            'sport': [
                "Home team secures dramatic victory in final minutes",
                "Star player signs record-breaking contract",
                "Championship race heats up as season progresses",
                "Olympic preparations face budget challenges",
                "Young athlete breaks long-standing world record"
            ],
            'entertainment': [
                "Blockbuster movie breaks box office records opening weekend",
                "Popular streaming series renewed for third season",
                "Award ceremony celebrates diverse talent",
                "Musician announces world tour dates",
                "Controversial art exhibition draws large crowds"
            ]
        }
        
        news_data = []
        for i in range(n_samples):
            topic = np.random.choice(topics)
            headline = np.random.choice(headlines[topic])
            
            # Generate article content
            if 'positive' in headline.lower() or 'record' in headline.lower() or 'boost' in headline.lower():
                sentiment_bias = 'positive'
            elif 'concern' in headline.lower() or 'criticism' in headline.lower() or 'resign' in headline.lower():
                sentiment_bias = 'negative'
            else:
                sentiment_bias = 'neutral'
            
            news_data.append({
                'article_id': f'bbc_{i}',
                'source': 'BBC News',
                'topic': topic,
                'headline': headline,
                'content': f"{headline} " + " ".join(["Lorem ipsum"] * np.random.randint(20, 100)),
                'publication_date': pd.Timestamp.now() - pd.Timedelta(days=np.random.randint(0, 30)),
                'sentiment_bias': sentiment_bias,
                'word_count': np.random.randint(200, 800),
                'reading_time_min': np.random.randint(2, 10)
            })
        
        return pd.DataFrame(news_data)
    
    def _generate_financial_news(self, n_samples):
        """Generate financial news based on Business Insider dataset [citation:3]"""
        companies = ['Apple', 'Microsoft', 'Google', 'Amazon', 'Tesla', 'JPMorgan', 'Goldman Sachs']
        
        headlines = [
            "Company reports record quarterly profits, shares surge",
            "Company stock falls after earnings miss expectations",
            "Company announces major acquisition in strategic move",
            "Analysts upgrade Company rating citing strong growth",
            "Company faces regulatory scrutiny over business practices",
            "Company's new product launch exceeds market expectations",
            "Company cuts guidance amid economic uncertainty",
            "Investors optimistic about Company's future prospects",
            "Company CEO steps down, shares volatile",
            "Company expands into emerging markets"
        ]
        
        news_data = []
        for i in range(n_samples):
            company = np.random.choice(companies)
            headline = np.random.choice(headlines).replace('Company', company)
            
            # Determine sentiment from headline
            if any(word in headline.lower() for word in ['record', 'surge', 'upgrade', 'exceeds', 'optimistic', 'expands']):
                sentiment = 'positive'
            elif any(word in headline.lower() for word in ['falls', 'miss', 'regulatory', 'cuts', 'steps down']):
                sentiment = 'negative'
            else:
                sentiment = 'neutral'
            
            news_data.append({
                'article_id': f'financial_{i}',
                'source': 'Business Insider',
                'company': company,
                'headline': headline,
                'content': headline,
                'publication_date': pd.Timestamp.now() - pd.Timedelta(days=np.random.randint(0, 30)),
                'sentiment': sentiment,
                'stock_impact': np.random.choice(['positive', 'negative', 'neutral']) if sentiment != 'neutral' else 'neutral'
            })
        
        return pd.DataFrame(news_data)
    
    def analyze_headline(self, headline, is_financial=False):
        """
        Analyze news headline sentiment
        """
        # VADER sentiment
        vader_scores = self.vader.polarity_scores(headline)
        
        # Financial-specific lexicon matching
        if is_financial:
            headline_lower = headline.lower()
            positive_matches = sum(1 for word in self.financial_positive if word in headline_lower)
            negative_matches = sum(1 for word in self.financial_negative if word in headline_lower)
            
            financial_score = (positive_matches - negative_matches) / max(positive_matches + negative_matches, 1)
            
            # Combine with VADER
            combined_score = (vader_scores['compound'] + financial_score) / 2
        else:
            combined_score = vader_scores['compound']
            financial_score = None
        
        return {
            'headline': headline,
            'vader_score': vader_scores['compound'],
            'vader_sentiment': 'positive' if vader_scores['compound'] >= 0.05 else ('negative' if vader_scores['compound'] <= -0.05 else 'neutral'),
            'financial_score': financial_score,
            'combined_score': combined_score,
            'combined_sentiment': 'positive' if combined_score >= 0.05 else ('negative' if combined_score <= -0.05 else 'neutral')
        }
    
    def analyze_batch(self, df, headline_column='headline', is_financial=False):
        """Analyze multiple news headlines"""
        results = []
        for _, row in df.iterrows():
            analysis = self.analyze_headline(row[headline_column], is_financial)
            results.append({
                'article_id': row.get('article_id', ''),
                'source': row.get('source', ''),
                'topic': row.get('topic', ''),
                'headline': row[headline_column],
                'vader_score': analysis['vader_score'],
                'vader_sentiment': analysis['vader_sentiment'],
                'combined_score': analysis['combined_score'],
                'combined_sentiment': analysis['combined_sentiment'],
                'is_financial': is_financial
            })
        
        return pd.DataFrame(results)

# Initialize news analyzer
news_analyzer = NewsAnalyzer()

# Generate news samples
bbc_news = news_analyzer.generate_sample_news(source='bbc', n_samples=100)
financial_news = news_analyzer.generate_sample_news(source='financial', n_samples=100)

print("\nBBC News Sample:")
print(bbc_news[['topic', 'headline', 'sentiment_bias']].head())

print("\nFinancial News Sample:")
print(financial_news[['company', 'headline', 'sentiment']].head())