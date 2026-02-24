class DataVisualizer:
    """
    Comprehensive data visualization toolkit
    """
    def __init__(self, df, title_prefix="Analysis"):
        self.df = df
        self.title_prefix = title_prefix
        
    def create_univariate_plots(self, columns=None):
        """Create univariate visualizations"""
        if columns is None:
            columns = self.df.columns[:6]  # Limit to first 6 columns
        
        numeric_cols = self.df[columns].select_dtypes(include=[np.number]).columns
        categorical_cols = self.df[columns].select_dtypes(include=['object', 'category']).columns
        
        n_plots = len(numeric_cols) + len(categorical_cols)
        if n_plots == 0:
            print("No suitable columns for univariate plots")
            return
        
        fig, axes = plt.subplots(2, 3, figsize=(15, 10))
        axes = axes.flatten()
        plot_idx = 0
        
        # Histograms for numeric columns
        for col in numeric_cols[:3]:  # Limit to 3 numeric
            if plot_idx < 6:
                data = self.df[col].dropna()
                
                # Histogram with KDE
                axes[plot_idx].hist(data, bins=30, density=True, alpha=0.7, 
                                   color='skyblue', edgecolor='black')
                sns.kdeplot(data, color='red', ax=axes[plot_idx])
                
                # Add statistics
                axes[plot_idx].axvline(data.mean(), color='green', linestyle='--', 
                                      label=f'Mean: {data.mean():.2f}')
                axes[plot_idx].axvline(data.median(), color='orange', linestyle='--', 
                                      label=f'Median: {data.median():.2f}')
                
                axes[plot_idx].set_title(f'{col}\nSkewness: {data.skew():.2f}')
                axes[plot_idx].set_xlabel(col)
                axes[plot_idx].set_ylabel('Density')
                axes[plot_idx].legend()
                plot_idx += 1
        
        # Bar plots for categorical columns
        for col in categorical_cols[:3]:  # Limit to 3 categorical
            if plot_idx < 6:
                value_counts = self.df[col].value_counts().head(10)
                
                # Horizontal bar plot
                colors = plt.cm.viridis(np.linspace(0, 1, len(value_counts)))
                axes[plot_idx].barh(range(len(value_counts)), value_counts.values, color=colors)
                axes[plot_idx].set_yticks(range(len(value_counts)))
                axes[plot_idx].set_yticklabels(value_counts.index)
                axes[plot_idx].set_xlabel('Count')
                axes[plot_idx].set_title(f'{col} (Top 10)')
                
                # Add value labels
                for i, v in enumerate(value_counts.values):
                    axes[plot_idx].text(v, i, f' {v}', va='center')
                plot_idx += 1
        
        # Hide unused subplots
        for i in range(plot_idx, 6):
            axes[i].set_visible(False)
        
        plt.suptitle(f'{self.title_prefix} - Univariate Analysis', fontsize=14, fontweight='bold')
        plt.tight_layout()
        plt.show()
    
    def create_bivariate_plots(self, x_col, y_col, hue_col=None):
        """Create bivariate visualizations"""
        fig = plt.figure(figsize=(15, 10))
        
        # 1. Scatter plot with regression
        ax1 = plt.subplot(2, 3, 1)
        if hue_col and hue_col in self.df.columns:
            scatter = ax1.scatter(self.df[x_col], self.df[y_col], 
                                 c=pd.factorize(self.df[hue_col])[0], 
                                 cmap='viridis', alpha=0.6)
            plt.colorbar(scatter, ax=ax1, label=hue_col)
        else:
            ax1.scatter(self.df[x_col], self.df[y_col], alpha=0.6, c='blue')
            
            # Add regression line
            z = np.polyfit(self.df[x_col].dropna(), self.df[y_col].dropna(), 1)
            p = np.poly1d(z)
            x_sorted = np.sort(self.df[x_col].dropna())
            ax1.plot(x_sorted, p(x_sorted), "r--", alpha=0.8, 
                    label=f'R² = {np.corrcoef(self.df[x_col], self.df[y_col])[0,1]**2:.3f}')
            ax1.legend()
        
        ax1.set_xlabel(x_col)
        ax1.set_ylabel(y_col)
        ax1.set_title(f'Scatter Plot: {x_col} vs {y_col}')
        
        # 2. Hexbin plot for density
        ax2 = plt.subplot(2, 3, 2)
        hb = ax2.hexbin(self.df[x_col], self.df[y_col], gridsize=30, cmap='YlOrRd')
        plt.colorbar(hb, ax=ax2, label='Count')
        ax2.set_xlabel(x_col)
        ax2.set_ylabel(y_col)
        ax2.set_title('Hexbin Density Plot')
        
        # 3. Box plot (if hue provided)
        ax3 = plt.subplot(2, 3, 3)
        if hue_col and hue_col in self.df.columns:
            self.df.boxplot(column=y_col, by=hue_col, ax=ax3)
            ax3.set_title(f'{y_col} by {hue_col}')
        else:
            # Create artificial groups for box plot
            bins = pd.qcut(self.df[x_col], q=4, labels=['Q1', 'Q2', 'Q3', 'Q4'])
            self.df.assign(group=bins).boxplot(column=y_col, by='group', ax=ax3)
            ax3.set_title(f'{y_col} by {x_col} Quartiles')
        
        # 4. Violin plot
        ax4 = plt.subplot(2, 3, 4)
        if hue_col and hue_col in self.df.columns:
            sns.violinplot(data=self.df, x=hue_col, y=y_col, ax=ax4)
        else:
            # Create groups for violin plot
            self.df['temp_group'] = pd.cut(self.df[x_col], bins=4)
            sns.violinplot(data=self.df, x='temp_group', y=y_col, ax=ax4)
            ax4.set_xlabel(f'{x_col} Groups')
        
        # 5. Joint distribution
        ax5 = plt.subplot(2, 3, 5)
        sns.kdeplot(data=self.df, x=x_col, y=y_col, cmap='viridis', fill=True, ax=ax5)
        ax5.set_title('KDE Contour Plot')
        
        # 6. Correlation and statistics
        ax6 = plt.subplot(2, 3, 6)
        ax6.axis('off')
        
        correlation = self.df[[x_col, y_col]].corr().iloc[0, 1]
        
        stats_text = f"""
        BIVARIATE STATISTICS
        {'='*25}
        
        Correlation: {correlation:.4f}
        R-squared: {correlation**2:.4f}
        
        {x_col} Statistics:
        Mean: {self.df[x_col].mean():.2f}
        Std: {self.df[x_col].std():.2f}
        
        {y_col} Statistics:
        Mean: {self.df[y_col].mean():.2f}
        Std: {self.df[y_col].std():.2f}
        
        Covariance: {self.df[[x_col, y_col]].cov().iloc[0, 1]:.2f}
        """
        
        ax6.text(0.1, 0.5, stats_text, fontsize=10, 
                verticalalignment='center', fontfamily='monospace')
        
        plt.suptitle(f'{self.title_prefix} - Bivariate Analysis', fontsize=14, fontweight='bold')
        plt.tight_layout()
        plt.show()
    
    def create_multivariate_plots(self):
        """Create multivariate visualizations"""
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns[:6]  # Limit to 6
        
        if len(numeric_cols) < 2:
            print("Need at least 2 numeric columns for multivariate analysis")
            return
        
        fig = plt.figure(figsize=(16, 12))
        
        # 1. Correlation heatmap
        ax1 = plt.subplot(2, 3, 1)
        corr_matrix = self.df[numeric_cols].corr()
        mask = np.triu(np.ones_like(corr_matrix), k=1)
        sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0,
                   mask=mask, square=True, linewidths=1, ax=ax1,
                   cbar_kws={"shrink": 0.8})
        ax1.set_title('Correlation Matrix (Upper Triangle)')
        
        # 2. Parallel coordinates
        ax2 = plt.subplot(2, 3, 2)
        from pandas.plotting import parallel_coordinates
        
        # Normalize data for parallel coordinates
        normalized_df = self.df[numeric_cols].copy()
        for col in normalized_df.columns:
            normalized_df[col] = (normalized_df[col] - normalized_df[col].min()) / \
                                 (normalized_df[col].max() - normalized_df[col].min())
        
        # Add a dummy class for coloring
        normalized_df['class'] = pd.qcut(normalized_df.iloc[:, 0], q=3, 
                                         labels=['Low', 'Medium', 'High'])
        
        parallel_coordinates(normalized_df, 'class', ax=ax2, colormap='viridis')
        ax2.set_title('Parallel Coordinates Plot')
        ax2.legend(bbox_to_anchor=(1.05, 1))
        
        # 3. Radar chart for first few rows
        ax3 = plt.subplot(2, 3, 3, projection='polar')
        categories = numeric_cols[:5]
        N = len(categories)
        angles = [n / float(N) * 2 * np.pi for n in range(N)]
        angles += angles[:1]
        
        # Plot first 3 rows as examples
        for i in range(min(3, len(self.df))):
            values = self.df.loc[i, categories].values
            values = (values - values.min()) / (values.max() - values.min())  # Normalize
            values = np.append(values, values[0])
            ax3.plot(angles, values, 'o-', linewidth=2, label=f'Row {i}')
            ax3.fill(angles, values, alpha=0.25)
        
        ax3.set_xticks(angles[:-1])
        ax3.set_xticklabels(categories)
        ax3.set_title('Radar Chart (Sample Rows)')
        ax3.legend(bbox_to_anchor=(1.05, 1))
        
        # 4. 3D Scatter plot
        ax4 = plt.subplot(2, 3, 4, projection='3d')
        if len(numeric_cols) >= 3:
            x, y, z = numeric_cols[:3]
            scatter = ax4.scatter(self.df[x], self.df[y], self.df[z], 
                                 c=self.df[numeric_cols[3]] if len(numeric_cols) > 3 else 'blue',
                                 cmap='viridis', alpha=0.6)
            ax4.set_xlabel(x)
            ax4.set_ylabel(y)
            ax4.set_zlabel(z)
            ax4.set_title('3D Scatter Plot')
            if len(numeric_cols) > 3:
                plt.colorbar(scatter, ax=ax4, label=numeric_cols[3], shrink=0.5)
        
        # 5. Andrews curves
        ax5 = plt.subplot(2, 3, 5)
        from pandas.plotting import andrews_curves
        
        # Sample data for Andrews curves
        sample_df = self.df[numeric_cols[:4]].head(50).copy()
        sample_df['class'] = pd.qcut(sample_df.iloc[:, 0], q=3, 
                                     labels=['Low', 'Medium', 'High'])
        andrews_curves(sample_df, 'class', ax=ax5, colormap='viridis')
        ax5.set_title("Andrews Curves")
        ax5.legend(bbox_to_anchor=(1.05, 1))
        
        # 6. Summary statistics
        ax6 = plt.subplot(2, 3, 6)
        ax6.axis('off')
        
        summary_stats = self.df[numeric_cols].describe().round(2)
        summary_text = "MULTIVARIATE SUMMARY\n"
        summary_text += "="*30 + "\n\n"
        summary_text += summary_stats.to_string()
        
        ax6.text(0.1, 0.5, summary_text, fontsize=8, 
                verticalalignment='center', fontfamily='monospace')
        
        plt.suptitle(f'{self.title_prefix} - Multivariate Analysis', fontsize=14, fontweight='bold')
        plt.tight_layout()
        plt.show()
    
    def create_time_series_plots(self, date_col, value_cols=None):
        """Create time series visualizations"""
        if value_cols is None:
            value_cols = self.df.select_dtypes(include=[np.number]).columns[:4]
        
        # Ensure date column is datetime
        self.df[date_col] = pd.to_datetime(self.df[date_col])
        self.df = self.df.sort_values(date_col)
        
        fig = plt.figure(figsize=(16, 12))
        
        # 1. Line plot for each value column
        ax1 = plt.subplot(2, 3, 1)
        for col in value_cols:
            ax1.plot(self.df[date_col], self.df[col], label=col, linewidth=2)
        ax1.set_xlabel('Date')
        ax1.set_ylabel('Value')
        ax1.set_title('Time Series Line Plot')
        ax1.legend()
        ax1.tick_params(axis='x', rotation=45)
        
        # 2. Rolling statistics
        ax2 = plt.subplot(2, 3, 2)
        window = min(30, len(self.df) // 10)
        
        for col in value_cols[:2]:  # Limit to 2 columns for clarity
            rolling_mean = self.df[col].rolling(window=window).mean()
            rolling_std = self.df[col].rolling(window=window).std()
            
            ax2.plot(self.df[date_col], self.df[col], alpha=0.3, label=f'{col} (original)')
            ax2.plot(self.df[date_col], rolling_mean, linewidth=2, label=f'{col} ({window}-period MA)')
            ax2.fill_between(self.df[date_col], 
                            rolling_mean - rolling_std, 
                            rolling_mean + rolling_std, 
                            alpha=0.2)
        
        ax2.set_xlabel('Date')
        ax2.set_ylabel('Value')
        ax2.set_title(f'Rolling Statistics (window={window})')
        ax2.legend()
        ax2.tick_params(axis='x', rotation=45)
        
        # 3. Seasonal decomposition (if enough data)
        ax3 = plt.subplot(2, 3, 3)
        if len(self.df) >= 14:  # Need at least 2 weeks for weekly seasonality
            from statsmodels.tsa.seasonal import seasonal_decompose
            
            # Use first value column for decomposition
            col = value_cols[0]
            
            # Ensure regular frequency
            ts_data = self.df.set_index(date_col)[col].dropna()
            if len(ts_data) > 30:
                try:
                    decomposition = seasonal_decompose(ts_data, model='additive', period=7)
                    
                    ax3.plot(ts_data.index, decomposition.trend, label='Trend', linewidth=2)
                    ax3.set_xlabel('Date')
                    ax3.set_ylabel('Trend')
                    ax3.set_title('Trend Component')
                    ax3.tick_params(axis='x', rotation=45)
                except:
                    ax3.text(0.5, 0.5, 'Insufficient data for decomposition', 
                            ha='center', va='center')
        else:
            ax3.text(0.5, 0.5, 'Insufficient data for decomposition', 
                    ha='center', va='center')
        
        # 4. Autocorrelation plot
        ax4 = plt.subplot(2, 3, 4)
        from pandas.plotting import autocorrelation_plot
        
        for col in value_cols[:2]:
            autocorrelation_plot(self.df[col].dropna(), ax=ax4, label=col)
        ax4.set_title('Autocorrelation')
        ax4.legend()
        
        # 5. Seasonal box plot (if daily data)
        ax5 = plt.subplot(2, 3, 5)
        if len(self.df) >= 7:
            # Extract day of week
            self.df['day_of_week'] = self.df[date_col].dt.day_name()
            
            # Box plot by day of week
            data_to_plot = [self.df[self.df['day_of_week'] == day][value_cols[0]].dropna() 
                           for day in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 
                                      'Friday', 'Saturday', 'Sunday']
                           if day in self.df['day_of_week'].values]
            
            bp = ax5.boxplot(data_to_plot, patch_artist=True)
            
            # Color boxes
            colors = plt.cm.viridis(np.linspace(0, 1, len(data_to_plot)))
            for patch, color in zip(bp['boxes'], colors):
                patch.set_facecolor(color)
            
            ax5.set_xticklabels([day[:3] for day in ['Monday', 'Tuesday', 'Wednesday', 
                                                     'Thursday', 'Friday', 'Saturday', 'Sunday']
                                if day in self.df['day_of_week'].values])
            ax5.set_title(f'Seasonal Pattern - {value_cols[0]}')
            ax5.set_ylabel(value_cols[0])
        
        # 6. Summary statistics
        ax6 = plt.subplot(2, 3, 6)
        ax6.axis('off')
        
        summary_text = "TIME SERIES SUMMARY\n"
        summary_text += "="*25 + "\n\n"
        summary_text += f"Date Range: {self.df[date_col].min()} to {self.df[date_col].max()}\n"
        summary_text += f"Total Periods: {len(self.df)}\n"
        summary_text += f"Frequency: {self.df[date_col].diff().mode().iloc[0]}\n\n"
        
        for col in value_cols:
            summary_text += f"{col}:\n"
            summary_text += f"  Mean: {self.df[col].mean():.2f}\n"
            summary_text += f"  Std: {self.df[col].std():.2f}\n"
            summary_text += f"  Trend: {'Increasing' if self.df[col].iloc[-1] > self.df[col].iloc[0] else 'Decreasing'}\n"
        
        ax6.text(0.1, 0.5, summary_text, fontsize=10, 
                verticalalignment='center', fontfamily='monospace')
        
        plt.suptitle(f'{self.title_prefix} - Time Series Analysis', fontsize=14, fontweight='bold')
        plt.tight_layout()
        plt.show()
    
    def create_interactive_plots(self):
        """Create interactive visualizations using Plotly"""
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        categorical_cols = self.df.select_dtypes(include=['object', 'category']).columns
        
        # 1. Interactive scatter matrix
        if len(numeric_cols) >= 2:
            fig = px.scatter_matrix(self.df[numeric_cols[:4]], 
                                   dimensions=numeric_cols[:4],
                                   title=f'{self.title_prefix} - Scatter Matrix',
                                   opacity=0.7)
            fig.show()
        
        # 2. 3D Scatter plot
        if len(numeric_cols) >= 3:
            fig = px.scatter_3d(self.df, 
                               x=numeric_cols[0], 
                               y=numeric_cols[1], 
                               z=numeric_cols[2],
                               color=categorical_cols[0] if len(categorical_cols) > 0 else None,
                               title=f'{self.title_prefix} - 3D Scatter Plot',
                               opacity=0.7)
            fig.show()
        
        # 3. Parallel coordinates
        if len(numeric_cols) >= 2:
            # Normalize data
            normalized_df = self.df[numeric_cols].copy()
            for col in normalized_df.columns:
                normalized_df[col] = (normalized_df[col] - normalized_df[col].min()) / \
                                     (normalized_df[col].max() - normalized_df[col].min())
            
            # Add categorical dimension if available
            if len(categorical_cols) > 0:
                normalized_df['category'] = self.df[categorical_cols[0]]
                color_col = 'category'
            else:
                color_col = normalized_df.columns[0]
            
            fig = px.parallel_coordinates(normalized_df, 
                                         color=color_col,
                                         title=f'{self.title_prefix} - Parallel Coordinates')
            fig.show()
        
        # 4. Sunburst chart for hierarchical data
        if len(categorical_cols) >= 2:
            # Create hierarchical counts
            hierarchy = self.df.groupby(list(categorical_cols[:2])).size().reset_index(name='count')
            
            fig = px.sunburst(hierarchy, 
                            path=list(categorical_cols[:2]), 
                            values='count',
                            title=f'{self.title_prefix} - Hierarchical View')
            fig.show()
    
    def create_dashboard_components(self):
        """Create components for dashboard"""
        components = {}
        
        # KPI Cards
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) > 0:
            components['kpis'] = {
                'total_records': len(self.df),
                'total_columns': len(self.df.columns),
                'avg_' + numeric_cols[0]: self.df[numeric_cols[0]].mean(),
                'max_' + numeric_cols[0]: self.df[numeric_cols[0]].max(),
                'min_' + numeric_cols[0]: self.df[numeric_cols[0]].min()
            }
        
        # Distribution plots
        components['distributions'] = {}
        for col in numeric_cols[:3]:
            fig = px.histogram(self.df, x=col, nbins=30, 
                              title=f'Distribution of {col}')
            components['distributions'][col] = fig
        
        # Correlation heatmap
        if len(numeric_cols) > 1:
            corr_matrix = self.df[numeric_cols].corr()
            fig = px.imshow(corr_matrix, 
                          text_auto=True, 
                          aspect="auto",
                          color_continuous_scale='RdBu_r',
                          title='Correlation Heatmap')
            components['correlation'] = fig
        
        return components