class DataQualityDetector:
    """
    Comprehensive data quality detection and issue identification
    """
    def __init__(self, df, dataset_name="Dataset"):
        self.df = df
        self.dataset_name = dataset_name
        self.issues = {}
        self.quality_score = 100
        
    def run_full_quality_check(self):
        """Run all quality checks and generate report"""
        print(f"\n{'='*60}")
        print(f"DATA QUALITY REPORT: {self.dataset_name}")
        print(f"{'='*60}")
        print(f"Dataset Shape: {self.df.shape}")
        print(f"Memory Usage: {self.df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")
        
        # Run all checks
        self.check_missing_values()
        self.check_duplicates()
        self.check_data_types()
        self.check_outliers()
        self.check_inconsistencies()
        self.check_distribution_issues()
        self.check_correlations()
        
        # Generate summary
        self.generate_summary()
        self.create_quality_dashboard()
        
        return self.issues
    
    def check_missing_values(self):
        """Detect missing value patterns"""
        missing = self.df.isnull().sum()
        missing_pct = (missing / len(self.df)) * 100
        
        issues_found = []
        
        # Columns with missing values
        cols_with_missing = missing[missing > 0]
        
        if len(cols_with_missing) > 0:
            print(f"\n📊 MISSING VALUES DETECTED:")
            for col, count in cols_with_missing.items():
                pct = missing_pct[col]
                print(f"  • {col}: {count} missing ({pct:.2f}%)")
                
                if pct > 30:
                    issues_found.append(f"High missing rate in {col} ({pct:.2f}%)")
                    self.quality_score -= 15
                elif pct > 10:
                    issues_found.append(f"Moderate missing rate in {col} ({pct:.2f}%)")
                    self.quality_score -= 5
                    
            # Visualize missing patterns
            if len(cols_with_missing) > 0:
                fig, axes = plt.subplots(1, 2, figsize=(15, 5))
                
                # Missing value matrix
                msno.matrix(self.df, ax=axes[0], sparkline=False)
                axes[0].set_title('Missing Value Matrix')
                
                # Missing value heatmap
                msno.heatmap(self.df, ax=axes[1])
                axes[1].set_title('Missing Value Correlation')
                
                plt.tight_layout()
                plt.show()
        else:
            print("\n✅ No missing values detected")
            
        self.issues['missing_values'] = issues_found
        
    def check_duplicates(self):
        """Detect duplicate records"""
        duplicate_rows = self.df.duplicated().sum()
        duplicate_pct = (duplicate_rows / len(self.df)) * 100
        
        issues_found = []
        
        if duplicate_rows > 0:
            print(f"\n📊 DUPLICATES DETECTED:")
            print(f"  • {duplicate_rows} duplicate rows ({duplicate_pct:.2f}%)")
            
            if duplicate_pct > 10:
                issues_found.append(f"High duplicate rate ({duplicate_pct:.2f}%)")
                self.quality_score -= 10
            elif duplicate_pct > 5:
                issues_found.append(f"Moderate duplicate rate ({duplicate_pct:.2f}%)")
                self.quality_score -= 5
                
            # Check for partial duplicates
            for col in self.df.select_dtypes(include=['object']).columns[:3]:
                duplicate_values = self.df[col].duplicated().sum()
                if duplicate_values > 0:
                    duplicate_value_pct = (duplicate_values / len(self.df)) * 100
                    print(f"  • {col}: {duplicate_values} duplicate values ({duplicate_value_pct:.2f}%)")
        else:
            print("\n✅ No duplicate rows detected")
            
        self.issues['duplicates'] = issues_found
        
    def check_data_types(self):
        """Detect data type inconsistencies"""
        issues_found = []
        
        print(f"\n📊 DATA TYPE ANALYSIS:")
        
        for col in self.df.columns:
            dtype = self.df[col].dtype
            
            # Check for mixed types
            unique_types = self.df[col].apply(type).unique()
            if len(unique_types) > 1:
                issues_found.append(f"Mixed types in {col}: {unique_types}")
                self.quality_score -= 5
                print(f"  ⚠️ {col}: Mixed types detected - {unique_types}")
            
            # Check numeric columns that might be categorical
            if dtype in ['int64', 'float64']:
                unique_values = self.df[col].nunique()
                if unique_values < 10 and unique_values > 0:
                    issues_found.append(f"{col} might be categorical (only {unique_values} unique values)")
                    print(f"  ℹ️ {col}: Only {unique_values} unique values - consider categorical type")
            
            # Check for date columns stored as strings
            if dtype == 'object':
                try:
                    pd.to_datetime(self.df[col])
                    issues_found.append(f"{col} should be datetime type")
                    print(f"  ⚠️ {col}: Should be datetime type")
                except:
                    pass
                    
        self.issues['data_types'] = issues_found
        
    def check_outliers(self):
        """Detect outliers using multiple methods"""
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        issues_found = []
        
        if len(numeric_cols) > 0:
            print(f"\n📊 OUTLIER DETECTION:")
            
            fig, axes = plt.subplots(2, 3, figsize=(15, 10))
            axes = axes.flatten()
            plot_idx = 0
            
            for col in numeric_cols[:6]:  # Limit to 6 columns for visualization
                data = self.df[col].dropna()
                
                # Z-score method
                z_scores = np.abs(stats.zscore(data))
                outliers_z = np.sum(z_scores > 3)
                pct_outliers_z = (outliers_z / len(data)) * 100
                
                # IQR method
                Q1 = data.quantile(0.25)
                Q3 = data.quantile(0.75)
                IQR = Q3 - Q1
                outliers_iqr = np.sum((data < (Q1 - 1.5 * IQR)) | (data > (Q3 + 1.5 * IQR)))
                pct_outliers_iqr = (outliers_iqr / len(data)) * 100
                
                if pct_outliers_iqr > 5:
                    issues_found.append(f"High outlier percentage in {col}: {pct_outliers_iqr:.2f}%")
                    self.quality_score -= 10
                    print(f"  ⚠️ {col}: {outliers_iqr} outliers ({pct_outliers_iqr:.2f}%)")
                elif pct_outliers_iqr > 1:
                    issues_found.append(f"Moderate outliers in {col}: {pct_outliers_iqr:.2f}%")
                    self.quality_score -= 5
                    print(f"  ℹ️ {col}: {outliers_iqr} outliers ({pct_outliers_iqr:.2f}%)")
                
                # Visualization
                if plot_idx < 6:
                    axes[plot_idx].boxplot(data)
                    axes[plot_idx].set_title(f'{col}\nOutliers: {pct_outliers_iqr:.1f}%')
                    axes[plot_idx].set_ylabel('Value')
                    plot_idx += 1
            
            # Hide unused subplots
            for i in range(plot_idx, 6):
                axes[i].set_visible(False)
                
            plt.suptitle('Outlier Detection - Box Plots', fontsize=14, fontweight='bold')
            plt.tight_layout()
            plt.show()
        else:
            print("\nℹ️ No numeric columns for outlier detection")
            
        self.issues['outliers'] = issues_found
        
    def check_inconsistencies(self):
        """Detect data inconsistencies"""
        issues_found = []
        
        print(f"\n📊 DATA INCONSISTENCY CHECK:")
        
        for col in self.df.select_dtypes(include=['object']).columns:
            # Check for leading/trailing spaces
            has_spaces = self.df[col].astype(str).str.contains('^\s|\s$').any()
            if has_spaces:
                issues_found.append(f"Leading/trailing spaces in {col}")
                print(f"  ⚠️ {col}: Contains leading/trailing spaces")
                self.quality_score -= 2
            
            # Check for inconsistent case
            if self.df[col].dtype == 'object':
                case_mixed = self.df[col].astype(str).str.contains('[A-Z]').any() and \
                            self.df[col].astype(str).str.contains('[a-z]').any()
                if case_mixed:
                    print(f"  ℹ️ {col}: Mixed case detected")
            
            # Check for special characters
            special_chars = self.df[col].astype(str).str.contains('[^a-zA-Z0-9\s]').any()
            if special_chars:
                print(f"  ℹ️ {col}: Contains special characters")
            
            # Check value distributions for categorical columns
            if self.df[col].nunique() < 20:
                value_counts = self.df[col].value_counts()
                print(f"  📊 {col} value distribution:")
                for val, count in value_counts.head().items():
                    pct = (count / len(self.df)) * 100
                    print(f"      {val}: {count} ({pct:.1f}%)")
                    
        self.issues['inconsistencies'] = issues_found
        
    def check_distribution_issues(self):
        """Check for distribution problems"""
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        issues_found = []
        
        if len(numeric_cols) > 0:
            print(f"\n📊 DISTRIBUTION ANALYSIS:")
            
            fig, axes = plt.subplots(2, 3, figsize=(15, 10))
            axes = axes.flatten()
            plot_idx = 0
            
            for col in numeric_cols[:6]:
                data = self.df[col].dropna()
                
                # Normality test
                if len(data) > 3 and len(data) < 5000:
                    _, p_value = stats.shapiro(data)
                    if p_value < 0.05:
                        issues_found.append(f"{col} is not normally distributed (p={p_value:.4f})")
                        print(f"  ℹ️ {col}: Not normally distributed (p={p_value:.4f})")
                
                # Skewness
                skewness = data.skew()
                if abs(skewness) > 2:
                    issues_found.append(f"High skewness in {col}: {skewness:.2f}")
                    print(f"  ⚠️ {col}: Highly skewed ({skewness:.2f})")
                    self.quality_score -= 5
                elif abs(skewness) > 1:
                    print(f"  ℹ️ {col}: Moderately skewed ({skewness:.2f})")
                
                # Kurtosis
                kurtosis = data.kurtosis()
                if abs(kurtosis) > 3:
                    print(f"  ℹ️ {col}: High kurtosis ({kurtosis:.2f})")
                
                # Visualization
                if plot_idx < 6:
                    axes[plot_idx].hist(data, bins=30, edgecolor='black', alpha=0.7)
                    axes[plot_idx].axvline(data.mean(), color='red', linestyle='--', label=f'Mean: {data.mean():.2f}')
                    axes[plot_idx].axvline(data.median(), color='green', linestyle='--', label=f'Median: {data.median():.2f}')
                    axes[plot_idx].set_title(f'{col}\nSkewness: {skewness:.2f}')
                    axes[plot_idx].legend()
                    plot_idx += 1
            
            # Hide unused subplots
            for i in range(plot_idx, 6):
                axes[i].set_visible(False)
                
            plt.suptitle('Distribution Analysis - Histograms', fontsize=14, fontweight='bold')
            plt.tight_layout()
            plt.show()
            
        self.issues['distribution'] = issues_found
        
    def check_correlations(self):
        """Check for problematic correlations"""
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        issues_found = []
        
        if len(numeric_cols) > 1:
            print(f"\n📊 CORRELATION ANALYSIS:")
            
            # Calculate correlation matrix
            corr_matrix = self.df[numeric_cols].corr()
            
            # Find highly correlated pairs
            high_corr = []
            for i in range(len(corr_matrix.columns)):
                for j in range(i+1, len(corr_matrix.columns)):
                    corr_value = corr_matrix.iloc[i, j]
                    if abs(corr_value) > 0.8:
                        high_corr.append((corr_matrix.columns[i], 
                                         corr_matrix.columns[j], 
                                         corr_value))
            
            if high_corr:
                issues_found.append(f"High correlations detected: {len(high_corr)} pairs")
                print(f"  ⚠️ Highly correlated pairs:")
                for col1, col2, corr in high_corr:
                    print(f"      {col1} vs {col2}: {corr:.3f}")
                    self.quality_score -= 2
            
            # Visualization
            plt.figure(figsize=(10, 8))
            mask = np.triu(np.ones_like(corr_matrix), k=1)
            sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0,
                       mask=mask, square=True, linewidths=1,
                       cbar_kws={"shrink": 0.8})
            plt.title('Correlation Matrix (Upper Triangle)')
            plt.tight_layout()
            plt.show()
            
        self.issues['correlations'] = issues_found
        
    def generate_summary(self):
        """Generate quality score and summary"""
        print(f"\n{'='*60}")
        print(f"QUALITY ASSESSMENT SUMMARY")
        print(f"{'='*60}")
        
        # Calculate final quality score
        self.quality_score = max(0, self.quality_score)
        
        # Determine quality grade
        if self.quality_score >= 90:
            grade = "A (Excellent)"
            color = 'green'
        elif self.quality_score >= 75:
            grade = "B (Good)"
            color = 'blue'
        elif self.quality_score >= 60:
            grade = "C (Fair)"
            color = 'orange'
        else:
            grade = "D (Poor)"
            color = 'red'
            
        print(f"Quality Score: {self.quality_score:.1f}/100 - Grade: {grade}")
        
        # Count issues by category
        total_issues = sum(len(issues) for issues in self.issues.values())
        print(f"Total Issues Detected: {total_issues}")
        
        print(f"\nIssues by Category:")
        for category, issues in self.issues.items():
            if issues:
                print(f"  • {category.replace('_', ' ').title()}: {len(issues)}")
        
        # Priority recommendations
        print(f"\n🔍 PRIORITY RECOMMENDATIONS:")
        priority_issues = []
        for category, issues in self.issues.items():
            priority_issues.extend(issues)
        
        for i, issue in enumerate(priority_issues[:5], 1):
            print(f"  {i}. {issue}")
            
    def create_quality_dashboard(self):
        """Create visual quality dashboard"""
        fig = plt.figure(figsize=(15, 8))
        
        # Quality gauge
        ax1 = plt.subplot(2, 3, 1)
        self._create_quality_gauge(ax1)
        
        # Issues by category
        ax2 = plt.subplot(2, 3, 2)
        categories = []
        counts = []
        for cat, issues in self.issues.items():
            if issues:
                categories.append(cat.replace('_', ' ').title())
                counts.append(len(issues))
        
        if counts:
            colors = plt.cm.RdYlGn_r(np.linspace(0.2, 0.8, len(counts)))
            ax2.barh(categories, counts, color=colors)
            ax2.set_xlabel('Number of Issues')
            ax2.set_title('Issues by Category')
        
        # Data completeness
        ax3 = plt.subplot(2, 3, 3)
        completeness = (1 - self.df.isnull().sum() / len(self.df)) * 100
        ax3.barh(range(len(completeness)), completeness.values)
        ax3.set_yticks(range(len(completeness)))
        ax3.set_yticklabels(completeness.index)
        ax3.set_xlabel('Completeness (%)')
        ax3.set_title('Data Completeness by Column')
        ax3.set_xlim(0, 100)
        
        # Memory usage
        ax4 = plt.subplot(2, 3, 4)
        memory_usage = self.df.memory_usage(deep=True)[1:] / 1024  # KB
        ax4.pie(memory_usage.values, labels=memory_usage.index, autopct='%1.1f%%')
        ax4.set_title('Memory Usage Distribution')
        
        # Data types distribution
        ax5 = plt.subplot(2, 3, 5)
        dtype_counts = self.df.dtypes.value_counts()
        ax5.pie(dtype_counts.values, labels=dtype_counts.index.astype(str), autopct='%1.1f%%')
        ax5.set_title('Data Types Distribution')
        
        # Quality score over time placeholder
        ax6 = plt.subplot(2, 3, 6)
        ax6.text(0.5, 0.5, f'Quality Score:\n{self.quality_score:.1f}/100', 
                ha='center', va='center', fontsize=20, fontweight='bold')
        ax6.text(0.5, 0.3, f'Grade: {grade}', ha='center', va='center', fontsize=14)
        ax6.axis('off')
        
        plt.suptitle(f'Data Quality Dashboard - {self.dataset_name}', fontsize=16, fontweight='bold')
        plt.tight_layout()
        plt.show()
        
    def _create_quality_gauge(self, ax):
        """Create gauge chart for quality score"""
        # Gauge parameters
        angles = np.linspace(0, np.pi, 100)
        scores = np.linspace(0, 100, 100)
        
        # Create gauge background
        ax.plot(np.cos(angles), np.sin(angles), 'k-', linewidth=2)
        ax.plot([-1, 1], [0, 0], 'k-', linewidth=2)
        
        # Add score indicator
        score_angle = (self.quality_score / 100) * np.pi
        x_indicator = np.cos(score_angle)
        y_indicator = np.sin(score_angle)
        ax.plot([0, x_indicator], [0, y_indicator], 'r-', linewidth=3)
        
        # Add score labels
        ax.text(-0.9, -0.2, '0', ha='center', va='center')
        ax.text(0.9, -0.2, '100', ha='center', va='center')
        ax.text(0, 0.5, f'{self.quality_score:.1f}', ha='center', va='center', 
               fontsize=16, fontweight='bold')
        
        ax.set_xlim(-1.2, 1.2)
        ax.set_ylim(-0.3, 1.2)
        ax.set_aspect('equal')
        ax.axis('off')
        ax.set_title('Quality Score Gauge')