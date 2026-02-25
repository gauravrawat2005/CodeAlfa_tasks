from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score

class TrendAnalyzer:
    """
    Analyze and predict sentiment trends over time
    Implements techniques from LSTM-based public opinion prediction [citation:1]
    """
    
    def __init__(self, data):
        self.data = data
        self.scaler = MinMaxScaler()
        
    def aggregate_daily_sentiment(self):
        """Aggregate sentiment by day for trend analysis"""
        daily = self.data.copy()
        daily['date'] = daily['timestamp'].dt.date
        daily_sentiment = daily.groupby('date').agg({
            'sentiment_score': ['mean', 'std', 'count'],
            'engagement': 'sum',
            'platform': lambda x: x.mode()[0] if not x.mode().empty else 'unknown'
        }).round(3)
        
        daily_sentiment.columns = ['avg_sentiment', 'sentiment_std', 'volume', 'total_engagement', 'top_platform']
        return daily_sentiment.reset_index()
    
    def detect_sentiment_shifts(self, window=7, threshold=0.3):
        """
        Detect significant shifts in public sentiment
        Used in analyzing public reactions to events [citation:3]
        """
        daily = self.aggregate_daily_sentiment()
        daily['rolling_avg'] = daily['avg_sentiment'].rolling(window=window).mean()
        daily['rolling_std'] = daily['avg_sentiment'].rolling(window=window).std()
        
        # Detect shifts (Z-score > threshold)
        daily['z_score'] = (daily['avg_sentiment'] - daily['rolling_avg']) / daily['rolling_std']
        daily['significant_shift'] = abs(daily['z_score']) > threshold
        daily['shift_direction'] = daily['z_score'].apply(
            lambda x: 'positive' if x > threshold else ('negative' if x < -threshold else 'none')
        )
        
        return daily
    
    def predict_trend(self, days_to_predict=30):
        """
        Predict future sentiment trends using machine learning
        Based on LSTM models for public opinion prediction [citation:1]
        """
        daily = self.aggregate_daily_sentiment()
        
        # Create features for time series prediction
        for i in range(1, 8):  # Use last 7 days as features
            daily[f'sentiment_lag_{i}'] = daily['avg_sentiment'].shift(i)
        
        # Add rolling statistics
        daily['rolling_mean_7'] = daily['avg_sentiment'].rolling(7).mean()
        daily['rolling_std_7'] = daily['avg_sentiment'].rolling(7).std()
        
        # Remove rows with NaN
        daily_clean = daily.dropna()
        
        # Prepare features and target
        feature_cols = [col for col in daily_clean.columns if 'lag_' in col or 'rolling_' in col]
        X = daily_clean[feature_cols]
        y = daily_clean['avg_sentiment']
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # Train model
        model = RandomForestRegressor(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)
        
        # Evaluate
        y_pred = model.predict(X_test)
        mse = mean_squared_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)
        
        # Feature importance
        feature_importance = pd.DataFrame({
            'feature': feature_cols,
            'importance': model.feature_importances_
        }).sort_values('importance', ascending=False)
        
        return {
            'model': model,
            'mse': mse,
            'r2': r2,
            'feature_importance': feature_importance,
            'predictions': pd.DataFrame({
                'actual': y_test,
                'predicted': y_pred
            })
        }

# Initialize trend analyzer
trend_analyzer = TrendAnalyzer(opinion_data)

# Detect sentiment shifts
sentiment_shifts = trend_analyzer.detect_sentiment_shifts()
significant_shifts = sentiment_shifts[sentiment_shifts['significant_shift']]
print(f"Detected {len(significant_shifts)} significant sentiment shifts")

# Predict future trends
trend_prediction = trend_analyzer.predict_trend()
print(f"\nTrend Prediction Model Performance:")
print(f"MSE: {trend_prediction['mse']:.4f}")
print(f"R²: {trend_prediction['r2']:.4f}")