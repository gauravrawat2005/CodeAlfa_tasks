class DataQualityPipeline:
    """
    Automated pipeline for data quality detection
    """
    def __init__(self, df):
        self.df = df
        self.quality_report = {}
        
    def run_pipeline(self):
        """Run complete quality detection pipeline"""
        print("🚀 Starting Data Quality Pipeline...")
        print("="*60)
        
        # Step 1: Basic statistics
        print("\n📊 Step 1: Basic Statistics")
        self._basic_statistics()
        
        # Step 2: Data quality detection
        print("\n🔍 Step 2: Running Quality Detector")
        detector = DataQualityDetector(self.df)
        self.quality_report['issues'] = detector.run_full_quality_check()
        
        # Step 3: Specialized checks
        print("\n🎯 Step 3: Specialized Checks")
        self._specialized_checks()
        
        # Step 4: Generate recommendations
        print("\n💡 Step 4: Generating Recommendations")
        recommendations = self._generate_recommendations()
        
        # Step 5: Create final report
        print("\n📑 Step 5: Creating Final Report")
        self._create_final_report(recommendations)
        
        return self.quality_report
    
    def _basic_statistics(self):
        """Calculate basic dataset statistics"""
        stats = {
            'rows': len(self.df),
            'columns': len(self.df.columns),
            'memory_usage': self.df.memory_usage(deep=True).sum() / 1024**2,
            'numeric_cols': len(self.df.select_dtypes(include=[np.number]).columns),
            'categorical_cols': len(self.df.select_dtypes(include=['object']).columns),
            'datetime_cols': len(self.df.select_dtypes(include=['datetime64']).columns)
        }
        
        print(f"  • Rows: {stats['rows']:,}")
        print(f"  • Columns: {stats['columns']}")
        print(f"  • Memory: {stats['memory_usage']:.2f} MB")
        print(f"  • Numeric columns: {stats['numeric_cols']}")
        print(f"  • Categorical columns: {stats['categorical_cols']}")
        print(f"  • Datetime columns: {stats['datetime_cols']}")
        
        self.quality_report['basic_stats'] = stats
    
    def _specialized_checks(self):
        """Run specialized checks based on data types"""
        specialized_issues = {}
        
        # Time series check
        datetime_cols = self.df.select_dtypes(include=['datetime64']).columns
        if len(datetime_cols) > 0 and len(self.df.select_dtypes(include=[np.number]).columns) > 0:
            print("  • Running time series checks...")
            ts_issues = detect_time_series_issues(
                self.df, 
                datetime_cols[0], 
                self.df.select_dtypes(include=[np.number]).columns[0]
            )
            specialized_issues['time_series'] = ts_issues
        
        # Categorical checks
        cat_cols = self.df.select_dtypes(include=['object']).columns
        if len(cat_cols) > 0:
            print("  • Running categorical data checks...")
            cat_issues = detect_categorical_issues(self.df, cat_cols[:5])
            specialized_issues['categorical'] = cat_issues
        
        # Text checks (if applicable)
        text_cols = [col for col in cat_cols if self.df[col].astype(str).str.len().mean() > 50]
        if len(text_cols) > 0:
            print("  • Running text data checks...")
            text_issues = detect_text_issues(self.df, text_cols[0])
            specialized_issues['text'] = text_issues
        
        self.quality_report['specialized_issues'] = specialized_issues
    
    def _generate_recommendations(self):
        """Generate actionable recommendations"""
        recommendations = []
        
        # Missing value recommendations
        missing_issues = self.quality_report.get('issues', {}).get('missing_values', [])
        if missing_issues:
            for issue in missing_issues:
                if 'high missing rate' in issue.lower():
                    col = issue.split('in ')[-1].split(' ')[0]
                    recommendations.append({
                        'priority': 'HIGH',
                        'issue': issue,
                        'action': f"Consider dropping {col} or using advanced imputation",
                        'impact': 'Data completeness and model performance'
                    })
                elif 'moderate missing' in issue.lower():
                    recommendations.append({
                        'priority': 'MEDIUM',
                        'issue': issue,
                        'action': 'Use mean/mode imputation or create missing indicator',
                        'impact': 'Statistical power'
                    })
        
        # Outlier recommendations
        outlier_issues = self.quality_report.get('issues', {}).get('outliers', [])
        if outlier_issues:
            for issue in outlier_issues:
                if 'high outlier percentage' in issue.lower():
                    recommendations.append({
                        'priority': 'HIGH',
                        'issue': issue,
                        'action': 'Consider winsorization or transformation',
                        'impact': 'Model stability and accuracy'
                    })
        
        # Display recommendations
        print("\n🔧 RECOMMENDATIONS:")
        print("-" * 60)
        for i, rec in enumerate(recommendations, 1):
            print(f"\n{i}. [{rec['priority']}] {rec['issue']}")
            print(f"   Action: {rec['action']}")
            print(f"   Impact: {rec['impact']}")
        
        return recommendations
    
    def _create_final_report(self, recommendations):
        """Create final quality report"""
        report = {
            'timestamp': datetime.now().isoformat(),
            'dataset_shape': self.df.shape,
            'quality_score': self.quality_report.get('issues', {}).get('quality_score', 0),
            'total_issues': sum(len(v) for v in self.quality_report.get('issues', {}).items() 
                               if isinstance(v, list)),
            'recommendations': recommendations
        }
        
        # Save report
        report_df = pd.DataFrame([report])
        report_df.to_csv(f'data_quality_report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv', 
                        index=False)
        
        print(f"\n✅ Pipeline complete! Report saved.")
        return report