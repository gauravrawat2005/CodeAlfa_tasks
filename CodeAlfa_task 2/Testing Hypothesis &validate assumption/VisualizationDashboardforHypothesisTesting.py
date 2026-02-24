class HypothesisTestingDashboard:
    """
    Comprehensive dashboard for hypothesis testing
    """
    def __init__(self, data):
        self.data = data
        self.results = {}
    
    def analyze_hypothesis(self, hypothesis_type, **kwargs):
        """
        Main analysis method
        """
        if hypothesis_type == 'difference':
            self._analyze_difference(**kwargs)
        elif hypothesis_type == 'relationship':
            self._analyze_relationship(**kwargs)
        elif hypothesis_type == 'distribution':
            self._analyze_distribution(**kwargs)
        
        self._create_dashboard()
    
    def _analyze_difference(self, group_col, value_col):
        """Analyze differences between groups"""
        groups = self.data[group_col].unique()
        
        # Statistical tests
        if len(groups) == 2:
            g1 = self.data[self.data[group_col] == groups[0]][value_col]
            g2 = self.data[self.data[group_col] == groups[1]][value_col]
            
            # Multiple tests for robustness
            self.results['t_test'] = stats.ttest_ind(g1, g2)
            self.results['mannwhitney'] = stats.mannwhitneyu(g1, g2)
            self.results['effect_size'] = (g2.mean() - g1.mean()) / g1.std()
        
        self.results['group_means'] = self.data.groupby(group_col)[value_col].mean()
        self.results['group_stds'] = self.data.groupby(group_col)[value_col].std()
    
    def _create_dashboard(self):
        """Create visualization dashboard"""
        fig = plt.figure(figsize=(16, 10))
        
        # 1. Distribution plot
        ax1 = plt.subplot(2, 3, 1)
        for group in self.results.get('group_means', {}).index:
            group_data = self.data[self.data.iloc[:, 0] == group].iloc[:, 1]
            sns.kdeplot(group_data, label=f'Group {group}', ax=ax1)
        ax1.set_title('Distribution by Group')
        ax1.legend()
        
        # 2. Box plot
        ax2 = plt.subplot(2, 3, 2)
        self.data.boxplot(column=self.data.columns[1], by=self.data.columns[0], ax=ax2)
        ax2.set_title('Box Plot Comparison')
        
        # 3. Bar plot with error bars
        ax3 = plt.subplot(2, 3, 3)
        means = self.results.get('group_means', {})
        stds = self.results.get('group_stds', {})
        x_pos = range(len(means))
        ax3.bar(x_pos, means.values, yerr=stds.values, capsize=5)
        ax3.set_xticks(x_pos)
        ax3.set_xticklabels(means.index)
        ax3.set_title('Means with Standard Deviations')
        
        # 4. Test results
        ax4 = plt.subplot(2, 3, 4)
        ax4.axis('off')
        
        results_text = "STATISTICAL TEST RESULTS\n"
        results_text += "="*30 + "\n\n"
        
        for test_name, test_result in self.results.items():
            if test_name not in ['group_means', 'group_stds']:
                if isinstance(test_result, tuple) and len(test_result) == 2:
                    results_text += f"{test_name}:\n"
                    results_text += f"  Statistic: {test_result[0]:.4f}\n"
                    results_text += f"  P-value: {test_result[1]:.4f}\n"
                    results_text += f"  Significant: {'Yes' if test_result[1] < 0.05 else 'No'}\n\n"
                elif test_name == 'effect_size':
                    results_text += f"Effect size (Cohen's d): {test_result:.4f}\n"
        
        ax4.text(0.1, 0.9, results_text, fontsize=10, 
                verticalalignment='top', fontfamily='monospace',
                transform=ax4.transAxes)
        
        # 5. QQ plot for normality check
        ax5 = plt.subplot(2, 3, 5)
        stats.probplot(self.data.iloc[:, 1], dist="norm", plot=ax5)
        ax5.set_title('Q-Q Plot (Normality Check)')
        
        # 6. Confidence intervals
        ax6 = plt.subplot(2, 3, 6)
        for i, group in enumerate(self.results.get('group_means', {}).index):
            group_data = self.data[self.data.iloc[:, 0] == group].iloc[:, 1]
            ci = stats.t.interval(0.95, len(group_data)-1, 
                                 loc=group_data.mean(), 
                                 scale=stats.sem(group_data))
            ax6.errorbar(i, group_data.mean(), 
                        yerr=[[group_data.mean() - ci[0]], [ci[1] - group_data.mean()]],
                        fmt='o', capsize=5, capthick=2)
        
        ax6.set_xticks(range(len(self.results.get('group_means', {}))))
        ax6.set_xticklabels(self.results.get('group_means', {}).index)
        ax6.set_ylabel('Mean')
        ax6.set_title('95% Confidence Intervals')
        
        plt.suptitle('Hypothesis Testing Dashboard', fontsize=14, fontweight='bold')
        plt.tight_layout()
        plt.show()

# Usage
dashboard = HypothesisTestingDashboard(test_data)
dashboard.analyze_hypothesis('difference', 
                            group_col='group', 
                            value_col='value')