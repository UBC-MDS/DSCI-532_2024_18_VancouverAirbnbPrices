import plotly.graph_objects as go
import pandas as pd

def create_map(df_filtered):
    '''Outputs a map with inputs from sidebar'''
    color_bins = [0, 150, 300, 700, float('inf')]
    color_palette = ['#FED976', '#FD8F3C', '#E3211C', '#7F0F27']
    
    df_filtered.reset_index(drop=True, inplace=True)
    df_filtered['color'] = pd.cut(df_filtered['price_adjusted'], bins=color_bins, labels=color_palette)
    
    fig = go.Figure()

    # Add map markers
    fig.add_trace(go.Scattermapbox(
        lat=df_filtered["latitude"],
        lon=df_filtered["longitude"],
        mode="markers",
        text=[str(df_filtered["neighbourhood_cleansed"][i]) + '<br>' + "Price: $" + str(df_filtered["price_adjusted"][i]) + '<br>' + "Accommodates: " + str(df_filtered["accommodates"][i]) for i in range(df_filtered.shape[0])],
        hoverinfo='text',
        marker=dict(
            size=8,
            opacity=0.7,
            color=df_filtered["color"],
            showscale=False, 
            cmin=0,
            cmax=len(color_palette) - 1
        ),
        showlegend=False  
    ))

    # Add invisible legend markers
    for i, color in enumerate(color_palette):
        fig.add_trace(go.Scattermapbox(
            lat=[0],
            lon=[0],
            mode='markers',
            marker=dict(
                color=color,
                size=10,  
                opacity=1  
            ),
            showlegend=True,
            name=f'${color_bins[i]} - ${color_bins[i + 1]}'
        ))

    # Update layout
    fig.update_layout(
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
        mapbox_style="carto-positron",
        mapbox_zoom=11,
        mapbox_center={"lat": df_filtered["latitude"].mean(), "lon": df_filtered["longitude"].mean()},
        legend=dict(orientation="h", yanchor="bottom", y=0, xanchor="center", x=0.5, title=None),
    )

    return fig