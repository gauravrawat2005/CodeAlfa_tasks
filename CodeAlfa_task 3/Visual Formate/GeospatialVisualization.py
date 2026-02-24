def create_geospatial_visualization(df, lat_col, lon_col, value_col=None):
    """Create geospatial visualizations"""
    
    # Base map scatter plot
    fig = px.scatter_mapbox(df, 
                           lat=lat_col, 
                           lon=lon_col,
                           color=value_col if value_col else None,
                           size=value_col if value_col else None,
                           hover_name=df.index,
                           hover_data=df.columns[:3],
                           zoom=3,
                           height=600)
    
    fig.update_layout(mapbox_style="open-street-map")
    fig.update_layout(title='Geospatial Distribution')
    fig.show()
    
    # Density mapbox
    fig = px.density_mapbox(df, 
                           lat=lat_col, 
                           lon=lon_col,
                           z=value_col if value_col else None,
                           radius=10,
                           zoom=3,
                           height=600)
    
    fig.update_layout(mapbox_style="stamen-terrain")
    fig.update_layout(title='Density Map')
    fig.show()