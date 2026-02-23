import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from scipy.signal import find_peaks
from sklearn.ensemble import IsolationForest
import warnings
warnings.filterwarnings('ignore')

class DataPatternAnalyzer:
    """Comprehensive tool for identifying trends, patterns, and anomalies"""
    
    def __init__(self, df, name="Dataset"):
        self.df = df
        self.name = name
        self.patterns_found = {}
        self.anomalies_detected = {}
        
    def analyze_complete(self):
        """Run complete pattern analysis pipeline"""
        
        print(f"\n{'#'*60}")
        print(f"# COMPLETE PATTERN ANALYSIS: {self.name}")
        print(f"{'#'*60}")
        
        # Step 1: Trend Analysis
        print("\n📈 STEP 1: TREND ANALYSIS")
        print("-" * 40)
        self.analyze_trends()
        
        # Step 2: Pattern Detection
        print("\n🔄 STEP 2: PATTERN DETECTION")
        print("-" * 40)
        self.detect_patterns()
        
        # Step 3: Anomaly Detection
        print("\n⚠️ STEP 3: ANOMALY DETECTION")
        print("-" * 40)
        self.detect_anomalies()
        
        # Step 4: Seasonality Analysis
        print("\n📅 STEP 4: SEASONALITY ANALYSIS")
        print("-" * 40)
        self.analyze_seasonality()
        
        # Step 5: Correlation Patterns
        print("\n🔗 STEP 5: CORRELATION PATTERNS")
        print("-" * 40)
        self.find_correlation_patterns()
        
        return self.patterns_found