class InteractiveDashboard:
    """
    Create interactive Dash dashboard
    """
    def __init__(self, df, title="Data Analysis Dashboard"):
        self.df = df
        self.title = title
        self.app = dash.Dash(__name__)
        self.setup_layout()
        self.setup_callbacks()
    
    def setup_layout(self):
        """Setup dashboard layout"""
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        categorical_cols = self.df.select_dtypes(include=['object', 'category']).columns
        
        self.app.layout = html.Div([
            html.H1(self.title, style={'text-align': 'center', 'color': '#2c3e50'}),
            
            # KPI Cards
            html.Div([
                html.Div([
                    html.H3('Total Records'),
                    html.H2(f"{len(self.df):,}", style={'color': '#3498db'})
                ], className='kpi-card'),
                
                html.Div([
                    html.H3('Total Columns'),
                    html.H2(f"{len(self.df.columns)}", style={'color': '#e74c3c'})
                ], className='kpi-card'),
                
                html.Div([
                    html.H3('Numeric Columns'),
                    html.H2(f"{len(numeric_cols)}", style={'color': '#2ecc71'})
                ], className='kpi-card'),
                
                html.Div([
                    html.H3('Categorical Columns'),
                    html.H2(f"{len(categorical_cols)}", style={'color': '#f39c12'})
                ], className='kpi-card'),
            ], style={'display': 'flex', 'justify-content': 'space-around', 
                     'margin': '20px', 'padding': '20px'}),
            
            # Controls
            html.Div([
                html.Div([
                    html.Label('Select X Axis:'),
                    dcc.Dropdown(
                        id='x-axis',
                        options=[{'label': col, 'value': col} for col in self.df.columns],
                        value=self.df.columns[0] if len(self.df.columns) > 0 else None
                    )
                ], style={'width': '30%', 'display': 'inline-block', 'margin': '10px'}),
                
                html.Div([
                    html.Label('Select Y Axis:'),
                    dcc.Dropdown(
                        id='y-axis',
                        options=[{'label': col, 'value': col} for col in self.df.columns],
                        value=self.df.columns[1] if len(self.df.columns) > 1 else None
                    )
                ], style={'width': '30%', 'display': 'inline-block', 'margin': '10px'}),
                
                html.Div([
                    html.Label('Select Chart Type:'),
                    dcc.Dropdown(
                        id='chart-type',
                        options=[
                            {'label': 'Scatter Plot', 'value': 'scatter'},
                            {'label': 'Line Chart', 'value': 'line'},
                            {'label': 'Bar Chart', 'value': 'bar'},
                            {'label': 'Box Plot', 'value': 'box'},
                            {'label': 'Histogram', 'value': 'histogram'}
                        ],
                        value='scatter'
                    )
                ], style={'width': '30%', 'display': 'inline-block', 'margin': '10px'})
            ], style={'text-align': 'center', 'margin': '20px'}),
            
            # Main chart
            dcc.Graph(id='main-chart'),
            
            # Additional charts row
            html.Div([
                dcc.Graph(id='chart-2', style={'width': '48%', 'display': 'inline-block'}),
                dcc.Graph(id='chart-3', style={'width': '48%', 'display': 'inline-block'})
            ]),
            
            # Data table
            html.H3('Data Preview', style={'margin-top': '30px'}),
            html.Div([
                dash.dash_table.DataTable(
                    id='data-table',
                    columns=[{"name": i, "id": i} for i in self.df.columns],
                    data=self.df.head(100).to_dict('records'),
                    page_size=10,
                    style_table={'overflowX': 'auto'},
                    style_cell={'textAlign': 'left', 'padding': '10px'},
                    style_header={'backgroundColor': '#3498db', 'color': 'white', 'fontWeight': 'bold'}
                )
            ])
        ])
    
    def setup_callbacks(self):
        """Setup interactive callbacks"""
        @self.app.callback(
            [Output('main-chart', 'figure'),
             Output('chart-2', 'figure'),
             Output('chart-3', 'figure')],
            [Input('x-axis', 'value'),
             Input('y-axis', 'value'),
             Input('chart-type', 'value')]
        )
        def update_charts(x_col, y_col, chart_type):
            # Main chart
            if chart_type == 'scatter':
                main_fig = px.scatter(self.df, x=x_col, y=y_col, 
                                     title=f'{x_col} vs {y_col}')
            elif chart_type == 'line':
                main_fig = px.line(self.df, x=x_col, y=y_col, 
                                  title=f'{x_col} vs {y_col}')
            elif chart_type == 'bar':
                main_fig = px.bar(self.df, x=x_col, y=y_col, 
                                 title=f'{x_col} vs {y_col}')
            elif chart_type == 'box':
                main_fig = px.box(self.df, x=x_col, y=y_col, 
                                 title=f'Box Plot of {y_col} by {x_col}')
            elif chart_type == 'histogram':
                main_fig = px.histogram(self.df, x=x_col, 
                                       title=f'Distribution of {x_col}')
            
            # Additional charts
            numeric_cols = self.df.select_dtypes(include=[np.number]).columns
            
            if len(numeric_cols) > 0:
                # Correlation heatmap
                corr_matrix = self.df[numeric_cols[:6]].corr()
                chart2_fig = px.imshow(corr_matrix, 
                                      text_auto=True,
                                      title='Correlation Heatmap')
                
                # Distribution of selected column
                if x_col in numeric_cols:
                    chart3_fig = px.histogram(self.df, x=x_col, 
                                             title=f'Distribution of {x_col}',
                                             marginal='box')
                else:
                    # Bar chart of categorical
                    value_counts = self.df[x_col].value_counts().head(10)
                    chart3_fig = px.bar(x=value_counts.index, 
                                       y=value_counts.values,
                                       title=f'Top 10 {x_col} Categories')
            else:
                chart2_fig = px.scatter(title='No numeric data available')
                chart3_fig = px.scatter(title='No numeric data available')
            
            return main_fig, chart2_fig, chart3_fig
    
    def run(self, debug=True, port=8050):
        """Run the dashboard"""
        self.app.run_server(debug=debug, port=port)