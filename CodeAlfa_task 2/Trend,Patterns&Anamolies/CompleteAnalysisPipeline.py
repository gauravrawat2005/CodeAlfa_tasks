def run_complete_analysis(self, generate_report=True):
    """Run all analyses and generate comprehensive report"""
    
    results = {}
    
    # Run all analyses
    results['trends'] = self.analyze_trends()
    results['patterns'] = self.detect_patterns()
    results['anomalies'] = self.detect_anomalies()
    results['seasonality'] = self.analyze_seasonality()
    results['correlations'] = self.find_correlation_patterns()
    
    # Generate summary report
    if generate_report:
        self.generate_pattern_report(results)
    
    return results

def generate_pattern_report(self, results):
    """Generate HTML report of all findings"""
    
    html = f"""
    <html>
    <head>
        <title>Pattern Analysis Report: {self.name}</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 40px; }}
            h1 {{ color: #2c3e50; border-bottom: 3px solid #3498db; }}
            h2 {{ color: #34495e; margin-top: 30px; }}
            .summary {{ background: #ecf0f1; padding: 20px; border-radius: 5px; }}
            .trend-up {{ color: green; }}
            .trend-down {{ color: red; }}
            .anomaly {{ background: #ffebee; padding: 10px; margin: 5px; border-radius: 3px; }}
            .pattern {{ background: #e8f5e8; padding: 10px; margin: 5px; border-radius: 3px; }}
            table {{ border-collapse: collapse; width: 100%; }}
            th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
            th {{ background-color: #3498db; color: white; }}
        </style>
    </head>
    <body>
        <h1>Pattern Analysis Report: {self.name}</h1>
        
        <div class="summary">
            <h2>Executive Summary</h2>
            <p>Dataset Size: {len(self.df):,} rows × {len(self.df.columns)} columns</p>
            <p>Significant Trends Found: {len(results['trends'])}</p>
            <p>Anomalies Detected: {sum(v.get('count', 0) for v in results['anomalies'].get('statistical_outliers', {{}}).values())}</p>
            <p>Seasonal Patterns: {len(results['seasonality'])}</p>
        </div>
        
        <h2>Key Findings</h2>
        
        <h3>📈 Top Trends</h3>
        <table>
            <tr>
                <th>Variable</th>
                <th>Trend</th>
                <th>R²</th>
                <th>Significance</th>
            </tr>
    """
    
    # Add trend data
    for col, info in list(results['trends'].items())[:5]:
        color = "green" if info['slope'] > 0 else "red" if info['slope'] < 0 else "black"
        html += f"""
            <tr>
                <td>{col}</td>
                <td style="color: {color};">{info['trend_direction']}</td>
                <td>{info.get('r_squared', 0):.3f}</td>
                <td>{"Significant" if info.get('p_value', 1) < 0.05 else "Not significant"}</td>
            </tr>
        """
    
    html += """
        </table>
        
        <h3>⚠️ Top Anomalies</h3>
        <table>
            <tr>
                <th>Variable</th>
                <th>Anomaly Count</th>
                <th>Percentage</th>
            </tr>
    """
    
    # Add anomaly data
    for col, info in list(results['anomalies'].get('statistical_outliers', {}).items())[:5]:
        html += f"""
            <tr>
                <td>{col}</td>
                <td>{info['count']}</td>
                <td>{info['percentage']:.1f}%</td>
            </tr>
        """
    
    html += """
        </table>
        
        <h2>Recommendations</h2>
        <ul>
    """
    
    # Generate recommendations based on findings
    if results['trends']:
        html += "<li>Monitor significant trends for strategic planning</li>"
    if results['anomalies']:
        html += "<li>Investigate detected anomalies for root causes</li>"
    if results['seasonality']:
        html += "<li>Account for seasonal patterns in forecasting</li>"
    if results['correlations'].get('strong_correlations'):
        html += "<li>Consider causal relationships in correlated variables</li>"
    
    html += """
        </ul>
    </body>
    </html>
    """
    
    with open('pattern_analysis_report.html', 'w') as f:
        f.write(html)
    
    print("\n📄 Pattern analysis report generated: pattern_analysis_report.html")