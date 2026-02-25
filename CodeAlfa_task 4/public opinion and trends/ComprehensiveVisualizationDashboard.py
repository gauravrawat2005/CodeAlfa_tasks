class PublicOpinionDashboard:
    """
    Interactive dashboard for public opinion visualization
    Implements real-time sentiment visualization techniques [citation:9]
    """
    
    def __init__(self, data, trend_data, emotion_correlations):
        self.data = data
        self.trend_data = trend_data
        self.emotion_correlations = emotion_correlations
        
    def create_dashboard(self):
        """Create comprehensive multi-panel visualization"""
        
        fig = plt.figure(figsize=(20, 15))
        fig.patch.set_facecolor('#f8f9fa')
        
        # Define grid
        gs = fig.add_gridspec(3, 4, hspace=0.3, wspace=0.3)
        
        # 1. Overall Sentiment Distribution
        ax1 = fig.add_subplot(gs[0, 0])
        sentiment_counts = self.data['sentiment_label'].value_counts()
        colors = {'positive': '#2ecc71', 'negative': '#e74c3c', 'neutral': '#3498db'}
        bars = ax1.bar(sentiment_counts.index, sentiment_counts.values, 
                      color=[colors.get(x, '#95a5a6') for x in sentiment_counts.index])
        ax1.set_title('Overall Public Sentiment', fontsize=14, fontweight='bold')
        ax1.set_xlabel('Sentiment')
        ax1.set_ylabel('Count')
        for bar in bars:
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height,
                    f'{int(height)}', ha='center', va='bottom')
        
        # 2. Sentiment Timeline with Event Detection
        ax2 = fig.add_subplot(gs[0, 1:3])
        ax2.plot(self.trend_data['date'], self.trend_data['avg_sentiment'], 
                color='#2E86AB', linewidth=2, marker='o', markersize=3, label='Daily Sentiment')
        ax2.fill_between(self.trend_data['date'], 
                        self.trend_data['avg_sentiment'] - self.trend_data['sentiment_std'],
                        self.trend_data['avg_sentiment'] + self.trend_data['sentiment_std'],
                        alpha=0.2, color='#2E86AB', label='±1 Std Dev')
        
        # Highlight significant shifts
        shifts = self.trend_data[self.trend_data['significant_shift']]
        for _, shift in shifts.iterrows():
            color = 'green' if shift['shift_direction'] == 'positive' else 'red'
            ax2.axvline(x=shift['date'], color=color, alpha=0.3, linestyle='--')
        
        ax2.axhline(y=0, color='black', linestyle='-', alpha=0.3)
        ax2.set_title('Sentiment Timeline with Event Detection', fontsize=14, fontweight='bold')
        ax2.set_xlabel('Date')
        ax2.set_ylabel('Average Sentiment Score')
        ax2.legend(loc='upper right')
        ax2.grid(True, alpha=0.3)
        
        # 3. Platform Comparison
        ax3 = fig.add_subplot(gs[0, 3])
        platform_sentiment = self.data.groupby('platform')['sentiment_score'].mean().sort_values()
        platform_sentiment.plot(kind='barh', ax=ax3, color='#A23B72')
        ax3.set_title('Sentiment by Platform', fontsize=14, fontweight='bold')
        ax3.set_xlabel('Avg Sentiment')
        ax3.set_ylabel('Platform')
        
        # 4. Emotion Correlation Heatmap
        ax4 = fig.add_subplot(gs[1, :2])
        sns.heatmap(self.emotion_correlations, annot=True, fmt='.2f', 
                   cmap='coolwarm', center=0, ax=ax4,
                   cbar_kws={'label': 'Correlation'})
        ax4.set_title('Emotion Correlation Matrix', fontsize=14, fontweight='bold')
        
        # 5. Topic Sentiment Analysis
        ax5 = fig.add_subplot(gs[1, 2:4])
        topic_sentiment = self.data.groupby('topic')['sentiment_score'].mean().sort_values()
        colors_topic = ['#2ecc71' if x > 0.1 else '#e74c3c' if x < -0.1 else '#3498db' 
                       for x in topic_sentiment.values]
        topic_sentiment.plot(kind='barh', ax=ax5, color=colors_topic)
        ax5.set_title('Sentiment by Topic', fontsize=14, fontweight='bold')
        ax5.set_xlabel('Avg Sentiment')
        ax5.set_ylabel('Topic')
        ax5.axvline(x=0, color='black', linestyle='-', alpha=0.3)
        
        # 6. Volume Analysis
        ax6 = fig.add_subplot(gs[2, 0])
        volume_by_platform = self.data.groupby('platform').size()
        volume_by_platform.plot(kind='pie', ax=ax6, autopct='%1.1f%%', 
                              colors=plt.cm.Set3(np.linspace(0, 1, len(volume_by_platform))))
        ax6.set_title('Discussion Volume by Platform', fontsize=14, fontweight='bold')
        ax6.set_ylabel('')
        
        # 7. Engagement Analysis
        ax7 = fig.add_subplot(gs[2, 1])
        sentiment_bins = pd.cut(self.data['sentiment_score'], bins=10)
        engagement_by_sentiment = self.data.groupby(sentiment_bins)['engagement'].mean()
        engagement_by_sentiment.plot(kind='line', marker='o', ax=ax7, color='#F18F01')
        ax7.set_title('Engagement by Sentiment Intensity', fontsize=14, fontweight='bold')
        ax7.set_xlabel('Sentiment Score Range')
        ax7.set_ylabel('Avg Engagement')
        ax7.grid(True, alpha=0.3)
        
        # 8. Regional Analysis
        ax8 = fig.add_subplot(gs[2, 2])
        region_sentiment = self.data.groupby('region')['sentiment_score'].mean()
        region_sentiment.plot(kind='bar', ax=ax8, color=plt.cm.Paired(np.linspace(0, 1, len(region_sentiment))))
        ax8.set_title('Regional Sentiment', fontsize=14, fontweight='bold')
        ax8.set_xlabel('Region')
        ax8.set_ylabel('Avg Sentiment')
        ax8.axhline(y=0, color='black', linestyle='-', alpha=0.3)
        ax8.tick_params(axis='x', rotation=45)
        
        # 9. Prediction Performance
        ax9 = fig.add_subplot(gs[2, 3])
        ax9.axis('off')
        
        # Add prediction metrics and insights
        insights_text = """
        📊 PUBLIC OPINION INSIGHTS
        
        Key Findings:
        • Overall sentiment leans {overall}
        • Most discussed topics: {top_topics}
        • Highest engagement on {top_platform}
        • Emotion correlations show {emotion_pattern}
        
        Trend Analysis:
        • {shift_count} significant sentiment shifts detected
        • Prediction model R²: {r2:.3f}
        • Most predictive features: {top_features}
        
        Recommendations:
        • Monitor {volatile_topic} topic closely
        • Focus engagement on {positive_platform}
        • Investigate negative sentiment in {negative_topic}
        """.format(
            overall='positive' if self.data['sentiment_score'].mean() > 0.1 else 
                   ('negative' if self.data['sentiment_score'].mean() < -0.1 else 'neutral'),
            top_topics=', '.join(self.data['topic'].value_counts().head(3).index),
            top_platform=self.data.groupby('platform')['engagement'].mean().idxmax(),
            emotion_pattern='strong joy-anger inverse' if self.emotion_correlations.loc['joy', 'anger'] < -0.5 else 'mixed',
            shift_count=len(self.trend_data[self.trend_data['significant_shift']]),
            r2=trend_prediction['r2'],
            top_features=', '.join(trend_prediction['feature_importance'].head(2)['feature'].tolist()),
            volatile_topic=self.data.groupby('topic')['sentiment_score'].std().idxmax(),
            positive_platform=self.data.groupby('platform')['sentiment_score'].mean().idxmax(),
            negative_topic=self.data.groupby('topic')['sentiment_score'].mean().idxmin()
        )
        
        ax9.text(0.1, 0.95, insights_text, fontsize=10, va='top', family='monospace',
                bbox=dict(boxstyle='round', facecolor='#f0f2f5', alpha=0.9))
        
        plt.suptitle('PUBLIC OPINION ANALYSIS DASHBOARD\nReal-time Sentiment Monitoring and Trend Detection', 
                    fontsize=18, fontweight='bold', y=1.02)
        plt.tight_layout()
        plt.show()

# Prepare data for dashboard
daily_sentiment = trend_analyzer.aggregate_daily_sentiment()
daily_with_shifts = trend_analyzer.detect_sentiment_shifts()
emotion_corr = emotion_analyzer.emotion_correlation_matrix()

# Create dashboard
dashboard = PublicOpinionDashboard(opinion_data, daily_with_shifts, emotion_corr)
dashboard.create_dashboard()