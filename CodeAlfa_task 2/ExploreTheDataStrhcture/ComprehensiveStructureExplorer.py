class DataStructureExplorer:
    """Complete toolkit for exploring data structure"""
    
    def __init__(self, df, name="Dataset"):
        self.df = df
        self.name = name
        self.structure_summary = {}
        
    def explore_completely(self):
        """Run complete exploration pipeline"""
        
        print(f"\n{'#'*60}")
        print(f"# COMPLETE DATA STRUCTURE EXPLORATION: {self.name}")
        print(f"{'#'*60}")
        
        # Step 1: Initial Overview
        print("\n📌 STEP 1: INITIAL OVERVIEW")
        print("-" * 40)
        self.structure_summary['overview'] = initial_data_overview(self.df, self.name)
        
        # Step 2: Variable Analysis
        print("\n📌 STEP 2: VARIABLE-LEVEL ANALYSIS")
        print("-" * 40)
        self.structure_summary['variables'] = analyze_variables(self.df)
        display_variable_analysis(self.structure_summary['variables'])
        
        # Step 3: Structure Visualization
        print("\n📌 STEP 3: STRUCTURE VISUALIZATION")
        print("-" * 40)
        self.structure_summary['visualization'] = visualize_data_structure(self.df)
        
        # Step 4: Correlation Analysis (if applicable)
        print("\n📌 STEP 4: CORRELATION ANALYSIS")
        print("-" * 40)
        if len(self.df.select_dtypes(include=[np.number]).columns) >= 2:
            self.structure_summary['correlations'] = analyze_correlation_structure(self.df)
        else:
            print("Skipping correlation analysis - insufficient numeric columns")
        
        # Step 5: Data Quality Assessment
        print("\n📌 STEP 5: DATA QUALITY ASSESSMENT")
        print("-" * 40)
        self.structure_summary['quality'] = data_quality_report(self.df)
        
        return self.structure_summary
    
    def generate_report(self, output_file='data_structure_report.html'):
        """Generate HTML report"""
        
        html = f"""
        <html>
        <head>
            <title>Data Structure Report: {self.name}</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 40px; }}
                h1 {{ color: #2c3e50; }}
                h2 {{ color: #34495e; margin-top: 30px; }}
                .summary {{ background: #ecf0f1; padding: 20px; border-radius: 5px; }}
                .metric {{ display: inline-block; margin: 10px; padding: 15px; background: white; border-radius: 5px; }}
                table {{ border-collapse: collapse; width: 100%; }}
                th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
                th {{ background-color: #3498db; color: white; }}
            </style>
        </head>
        <body>
            <h1>Data Structure Report: {self.name}</h1>
            
            <div class="summary">
                <h2>Dataset Summary</h2>
                <div class="metric">Rows: {self.df.shape[0]:,}</div>
                <div class="metric">Columns: {self.df.shape[1]}</div>
                <div class="metric">Memory: {self.structure_summary['overview']['memory']:.2f} MB</div>
            </div>
            
            <h2>Column Details</h2>
            <table>
                <tr>
                    <th>Column</th>
                    <th>Type</th>
                    <th>Missing %</th>
                    <th>Unique Values</th>
                </tr>
        """
        
        for col, info in self.structure_summary['variables'].items():
            html += f"""
                <tr>
                    <td>{col}</td>
                    <td>{info['data_type']}</td>
                    <td>{info['null_percentage']:.1f}%</td>
                    <td>{info['unique_values']:,}</td>
                </tr>
            """
        
        html += """
            </table>
        </body>
        </html>
        """
        
        with open(output_file, 'w') as f:
            f.write(html)
        
        print(f"\n📄 Report generated: {output_file}")
        return output_file

# Example usage
explorer = DataStructureExplorer(df, "Customer Dataset")
structure = explorer.explore_completely()
explorer.generate_report('customer_data_structure.html')