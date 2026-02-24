"""
TABLEAU PERFORMANCE OPTIMIZATION

1. Data Preparation:
   - Extract data instead of live connection when possible
   - Aggregate data at appropriate level
   - Remove unnecessary columns
   - Create joins in database rather than Tableau
   - Use data source filters to limit rows

2. Visualization Optimization:
   - Limit number of marks (use data densification carefully)
   - Avoid overly complex calculations in calculated fields
   - Use context filters for large datasets
   - Minimize use of table calculations
   - Optimize image sizes if used

3. Dashboard Loading:
   - Use show/hide containers for optional content
   - Limit number of worksheets per dashboard (5-7 max)
   - Use dashboard actions instead of multiple identical filters
   - Set appropriate default filters
   - Consider using parameters instead of filters for some use cases
"""