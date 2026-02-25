class MultiSourceAnalyzer:
    """
    Comprehensive analyzer for cross-source sentiment comparison
    """
    
    def __init__(self):
        self.amazon_analyzer = AmazonReviewAnalyzer()
        self.social_analyzer = SocialMediaAnalyzer()
        self.news_analyzer = NewsAnalyzer()
        
    def collect_all_data(self):
        """Collect and analyze data from all sources"""
        
        # 1. Amazon Reviews
        print("Collecting Amazon review data...")
        amazon_raw = self.amazon_analyzer.load_sample_data()
        amazon_results = self.amazon_analyzer.analyze_batch(amazon_raw)
        amazon_results['source'] = 'Amazon Reviews'
        amazon_results['platform'] = 'E-commerce'
        
        # 2. Social Media
        print("Collecting social media data...")
        social_raw = self.social_analyzer.generate_sample_social_data(300)
        social_results = self.social_analyzer.analyze_batch(social_raw)
        social_results['source'] = 'Social Media'
        
        # 3. News
        print("Collecting news data...")
        bbc_raw = self.news_analyzer.generate_sample_news(source='bbc', n_samples=100)
        financial_raw = self.news_analyzer.generate_sample_news(source='financial', n_samples=100)
        
        bbc_results = self.news_analyzer.analyze_batch(bbc_raw, is_financial=False)
        bbc_results['source'] = 'BBC News'
        bbc_results['platform'] = 'News'
        
        financial_results = self.news_analyzer.analyze_batch(financial_raw, is_financial=True)
        financial_results['source'] = 'Financial News'
        financial_results['platform'] = 'News'
        
        # Combine all results
        all_results = pd.concat([
            amazon_results,
            social_results,
            bbc_results,
            financial_results
        ], ignore_index=True)
        
        return all_results
    
    def generate_comparison_dashboard(self, results_df):
        """
        Create comprehensive cross-source comparison dashboard
        """
        fig = plt.figure(figsize=(20, 15))
        fig.patch.set_facecolor('#f8f9fa')
        
        # Define grid
        gs = fig.add_gridspec(3, 4, hspace=0.3, wspace=0.3)
        
        # 1. Sentiment distribution by source
        ax1 = fig.add_subplot(gs[0, :2])
        
        # Prepare data
        source_sentiment = pd.crosstab(
            results_df['source'], 
            results_df['final_sentiment' if 'final_sentiment' in results_df.columns else 'combined_sentiment'],
            normalize='index'
        ) * 100
        
        source_sentiment.plot(kind='bar', ax=ax1, 
                             color=['#2ecc71', '#e74c3c', '#3498db'],
                             edgecolor='black')
        ax1.set_title('Sentiment Distribution by Source', fontsize=14, fontweight='bold')
        ax1.set_xlabel('Data Source')
        ax1.set_ylabel('Percentage (%)')
        ax1.legend(title='Sentiment')
        ax1.tick_params(axis='x', rotation=45)
        ax1.grid(True, alpha=0.3, axis='y')
        
        # 2. Confidence scores comparison
        ax2 = fig.add_subplot(gs[0, 2:4])
        
        sources = results_df['source'].unique()
        confidence_data = []
        for source in sources:
            source_data = results_df[results_df['source'] == source]
            if 'confidence' in source_data.columns:
                confidence_data.append(source_data['confidence'].values)
            elif 'vader_score' in source_data.columns:
                confidence_data.append(np.abs(source_data['vader_score']).values)
        
        bp = ax2.boxplot(confidence_data, labels=sources, patch_artist=True)
        for patch, color in zip(bp['boxes'], plt.cm.Set3(np.linspace(0, 1, len(sources)))):
            patch.set_facecolor(color)
        
        ax2.set_title('Analysis Confidence by Source', fontsize=14, fontweight='bold')
        ax2.set_xlabel('Data Source')
        ax2.set_ylabel('Confidence / |Score|')
        ax2.tick_params(axis='x', rotation=45)
        ax2.grid(True, alpha=0.3, axis='y')
        
        # 3. Rating vs Sentiment (Amazon specific)
        ax3 = fig.add_subplot(gs[1, 0])
        amazon_data = results_df[results_df['source'] == 'Amazon Reviews']
        if not amazon_data.empty and 'rating' in amazon_data.columns:
            rating_sentiment = amazon_data.groupby('rating')['vader_compound'].mean()
            rating_sentiment.plot(kind='line', marker='o', ax=ax3, color='#2E86AB', linewidth=2)
            ax3.set_title('Amazon: Rating vs Sentiment', fontsize=12, fontweight='bold')
            ax3.set_xlabel('Star Rating')
            ax3.set_ylabel('Avg Sentiment Score')
            ax3.grid(True, alpha=0.3)
            ax3.set_xticks(range(1, 6))
        
        # 4. Social Media Platform Comparison
        ax4 = fig.add_subplot(gs[1, 1])
        social_data = results_df[results_df['source'] == 'Social Media']
        if not social_data.empty and 'platform' in social_data.columns:
            platform_sentiment = social_data.groupby('platform')['sentiment_compound'].mean()
            colors = ['#3498db', '#2ecc71', '#e74c3c', '#f39c12']
            platform_sentiment.plot(kind='bar', ax=ax4, color=colors)
            ax4.set_title('Social Media: Sentiment by Platform', fontsize=12, fontweight='bold')
            ax4.set_xlabel('Platform')
            ax4.set_ylabel('Avg Sentiment Score')
            ax4.tick_params(axis='x', rotation=45)
            ax4.axhline(y=0, color='black', linestyle='-', alpha=0.3)
            ax4.grid(True, alpha=0.3, axis='y')
        
        # 5. Toxicity Analysis (Social Media)
        ax5 = fig.add_subplot(gs[1, 2])
        if not social_data.empty and 'toxicity_score' in social_data.columns:
            platform_toxicity = social_data.groupby('platform')['toxicity_score'].mean()
            platform_toxicity.plot(kind='bar', ax=ax5, color='#e74c3c', alpha=0.7)
            ax5.set_title('Social Media: Toxicity by Platform', fontsize=12, fontweight='bold')
            ax5.set_xlabel('Platform')
            ax5.set_ylabel('Avg Toxicity Score')
            ax5.tick_params(axis='x', rotation=45)
            ax5.axhline(y=0.3, color='red', linestyle='--', alpha=0.5, label='Toxicity Threshold')
            ax5.legend()
            ax5.grid(True, alpha=0.3, axis='y')
        
        # 6. News Topic Analysis
        ax6 = fig.add_subplot(gs[1, 3])
        bbc_data = results_df[results_df['source'] == 'BBC News']
        if not bbc_data.empty and 'topic' in bbc_data.columns:
            topic_sentiment = bbc_data.groupby('topic')['vader_score'].mean()
            topic_sentiment.sort_values().plot(kind='barh', ax=ax6, color='#3498db')
            ax6.set_title('BBC News: Sentiment by Topic', fontsize=12, fontweight='bold')
            ax6.set_xlabel('Avg Sentiment Score')
            ax6.set_ylabel('Topic')
            ax6.axvline(x=0, color='black', linestyle='-', alpha=0.3)
            ax6.grid(True, alpha=0.3, axis='x')
        
        # 7. Temporal Trends (simulated)
        ax7 = fig.add_subplot(gs[2, :2])
        
        # Add date column if not present
        if 'date' not in results_df.columns:
            results_df['date'] = pd.date_range(start='2024-01-01', periods=len(results_df), freq='D')
        
        # Group by source and date
        for source in sources:
            source_data = results_df[results_df['source'] == source].copy()
            if len(source_data) > 5:  # Only plot if enough data
                source_data = source_data.sort_values('date')
                source_data['rolling_sentiment'] = source_data['vader_compound' if 'vader_compound' in source_data.columns else 'vader_score'].rolling(5, min_periods=1).mean()
                ax7.plot(source_data['date'], source_data['rolling_sentiment'], 
                        label=source, linewidth=2, marker='o', markersize=3)
        
        ax7.set_title('Sentiment Trends Over Time', fontsize=14, fontweight='bold')
        ax7.set_xlabel('Date')
        ax7.set_ylabel('Sentiment Score')
        ax7.legend(loc='upper right')
        ax7.axhline(y=0, color='black', linestyle='-', alpha=0.3)
        ax7.grid(True, alpha=0.3)
        
        # 8. Summary Statistics
        ax8 = fig.add_subplot(gs[2, 2:4])
        ax8.axis('off')
        
        summary_text = "📊 MULTI-SOURCE ANALYSIS SUMMARY\n"
        summary_text += "="*40 + "\n\n"
        
        for source in sources:
            source_data = results_df[results_df['source'] == source]
            summary_text += f"🔹 {source}\n"
            summary_text += f"   Samples: {len(source_data)}\n"
            
            if 'final_sentiment' in source_data.columns:
                sentiment_col = 'final_sentiment'
            else:
                sentiment_col = 'combined_sentiment'
            
            sentiment_dist = source_data[sentiment_col].value_counts(normalize=True)
            for sentiment in ['positive', 'negative', 'neutral']:
                if sentiment in sentiment_dist.index:
                    pct = sentiment_dist[sentiment] * 100
                    summary_text += f"   {sentiment.title()}: {pct:.1f}%\n"
            
            if 'confidence' in source_data.columns:
                avg_conf = source_data['confidence'].mean()
            else:
                avg_conf = source_data['vader_score' if 'vader_score' in source_data.columns else 'vader_compound'].abs().mean()
            
            summary_text += f"   Avg Confidence: {avg_conf:.2f}\n\n"
        
        ax8.text(0.1, 0.95, summary_text, fontsize=10, va='top', family='monospace',
                bbox=dict(boxstyle='round', facecolor='#f0f2f5', alpha=0.9))
        
        plt.suptitle('CROSS-SOURCE SENTIMENT ANALYSIS DASHBOARD\nAmazon Reviews · Social Media · News Articles', 
                    fontsize=18, fontweight='bold', y=1.02)
        plt.tight_layout()
        plt.show()
        
        return results_df

# Run comprehensive analysis
print("="*70)
print("MULTI-SOURCE SENTIMENT ANALYSIS")
print("="=70)

# Initialize multi-source analyzer
multi_analyzer = MultiSourceAnalyzer()

# Collect and analyze all data
all_results = multi_analyzer.collect_all_data()

# Generate comparison dashboard
results_with_dates = multi_analyzer.generate_comparison_dashboard(all_results)