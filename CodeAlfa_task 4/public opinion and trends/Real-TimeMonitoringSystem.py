class RealTimeMonitor:
    """
    Real-time public opinion monitoring system
    Implements techniques for continuous sentiment tracking [citation:9]
    """
    
    def __init__(self, data_stream):
        self.data_stream = data_stream
        self.alerts = []
        self.baseline_stats = self._calculate_baseline()
        
    def _calculate_baseline(self):
        """Calculate baseline statistics for anomaly detection"""
        return {
            'mean_sentiment': self.data_stream['sentiment_score'].mean(),
            'std_sentiment': self.data_stream['sentiment_score'].std(),
            'emotion_baselines': {
                emotion: self.data_stream[emotion].mean() 
                for emotion in ['joy', 'anger', 'sadness', 'fear', 'surprise']
            }
        }
    
    def monitor_new_data(self, new_data_point):
        """
        Monitor incoming data and trigger alerts for significant changes
        Used in real-time public opinion tracking [citation:7][citation:9]
        """
        # Calculate z-score for new sentiment
        z_score = (new_data_point['sentiment_score'] - self.baseline_stats['mean_sentiment']) / self.baseline_stats['std_sentiment']
        
        alerts = []
        
        # Check for significant sentiment shift
        if abs(z_score) > 2:
            alerts.append({
                'type': 'sentiment_anomaly',
                'severity': 'high' if abs(z_score) > 3 else 'medium',
                'message': f"Unusual sentiment detected (z-score: {z_score:.2f})",
                'timestamp': new_data_point['timestamp']
            })
        
        # Check for emotion spikes
        for emotion in ['anger', 'fear']:  # Focus on negative emotions
            emotion_value = new_data_point[emotion]
            baseline = self.baseline_stats['emotion_baselines'][emotion]
            
            if emotion_value > baseline + 2 * self.data_stream[emotion].std():
                alerts.append({
                    'type': f'{emotion}_spike',
                    'severity': 'high',
                    'message': f"Spike in {emotion} detected",
                    'timestamp': new_data_point['timestamp']
                })
        
        return alerts
    
    def generate_alert_summary(self, time_window='24h'):
        """Generate summary of recent alerts"""
        recent_alerts = [a for a in self.alerts if 
                        a['timestamp'] > datetime.now() - timedelta(hours=24)]
        
        alert_types = {}
        for alert in recent_alerts:
            alert_types[alert['type']] = alert_types.get(alert['type'], 0) + 1
        
        return {
            'total_alerts': len(recent_alerts),
            'alert_types': alert_types,
            'critical_alerts': sum(1 for a in recent_alerts if a['severity'] == 'high'),
            'latest_alerts': recent_alerts[-5:] if recent_alerts else []
        }

# Simulate real-time monitoring
monitor = RealTimeMonitor(opinion_data)

# Simulate new data points
new_points = [
    {'timestamp': datetime.now(), 'sentiment_score': -0.8, 'joy': 0.1, 'anger': 0.7, 'sadness': 0.1, 'fear': 0.05, 'surprise': 0.05},
    {'timestamp': datetime.now() + timedelta(minutes=5), 'sentiment_score': 0.9, 'joy': 0.8, 'anger': 0.05, 'sadness': 0.05, 'fear': 0.05, 'surprise': 0.05},
]

print("\nReal-Time Monitoring Alerts:")
for point in new_points:
    alerts = monitor.monitor_new_data(point)
    for alert in alerts:
        print(f"⚠️ {alert['message']} (Severity: {alert['severity']})")