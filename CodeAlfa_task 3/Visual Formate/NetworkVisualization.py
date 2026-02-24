import networkx as nx

def create_network_visualization(adjacency_matrix, node_labels=None):
    """Create network graph visualization"""
    
    # Create graph
    G = nx.Graph(adjacency_matrix)
    
    fig, axes = plt.subplots(1, 2, figsize=(15, 6))
    
    # Basic network
    pos = nx.spring_layout(G)
    nx.draw(G, pos, ax=axes[0], with_labels=node_labels is not None,
            node_color='lightblue', node_size=500, 
            font_size=10, font_weight='bold')
    axes[0].set_title('Network Graph')
    
    # Degree distribution
    degrees = [G.degree(n) for n in G.nodes()]
    axes[1].hist(degrees, bins=20, edgecolor='black', alpha=0.7)
    axes[1].set_xlabel('Degree')
    axes[1].set_ylabel('Frequency')
    axes[1].set_title('Degree Distribution')
    
    plt.tight_layout()
    plt.show()
    
    # Interactive network with Plotly
    if len(G.nodes()) <= 100:  # Limit for interactive
        pos = nx.spring_layout(G)
        
        edge_trace = []
        for edge in G.edges():
            x0, y0 = pos[edge[0]]
            x1, y1 = pos[edge[1]]
            edge_trace.append(go.Scatter(x=[x0, x1, None], y=[y0, y1, None],
                                        mode='lines', line=dict(width=1, color='#888')))
        
        node_x = []
        node_y = []
        for node in G.nodes():
            x, y = pos[node]
            node_x.append(x)
            node_y.append(y)
        
        node_trace = go.Scatter(x=node_x, y=node_y, mode='markers+text',
                               text=list(G.nodes()) if node_labels else None,
                               marker=dict(size=20, color='lightblue',
                                         line=dict(width=2))))
        
        fig = go.Figure(data=edge_trace + [node_trace],
                       layout=go.Layout(title='Interactive Network Graph',
                                       showlegend=False,
                                       hovermode='closest'))
        fig.show()