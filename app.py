# import pandas as pd
# import plotly.express as px
# from dash import Dash, dcc, html, Input, Output

# def create_interactive_post_graph(csv_file_path):
#     # Load the CSV file
#     df = pd.read_csv(csv_file_path)
    
#     # Ensure necessary columns are present
#     required_columns = ['total_reactions/Like', 'total_reactions/Love', 'post_id', 'post_url', 'post_date']
#     if not all(col in df.columns for col in required_columns):
#         print("The necessary columns are missing from the CSV file.")
#         return
    
#     # Convert post_date to datetime if it's not already
#     df['post_date'] = pd.to_datetime(df['post_date'])
    
#     # Calculate the sum of total reactions (Like + Love)
#     df['total_reactions_sum'] = df['total_reactions/Like'] + df['total_reactions/Love']
    
#     # Sort the DataFrame by the total reactions sum and select the top 30 posts
#     df_top30 = df.sort_values(by='total_reactions_sum', ascending=False).head(30)
    
#     # Create the Dash app
#     app = Dash(__name__)
    
#     # Create the Plotly figure for the top 30 posts with gradient color
#     fig = px.scatter(
#         df_top30,
#         x='post_date',
#         y='total_reactions_sum',
#         title='Top 30 Posts by Total Reactions (Like + Love)',
#         labels={'post_date': 'Post Date', 'total_reactions_sum': 'Total Reactions (Like + Love)'},
#         color='total_reactions_sum',
#         hover_data=['post_url', 'total_reactions/Like', 'total_reactions/Love', 'post_id'],
#         template='plotly_white',
#         color_continuous_scale=px.colors.sequential.Plasma,
#         size='total_reactions_sum',
#         size_max=20
#     )
    
#     # Set custom hover template to make it larger and clickable
#     fig.update_traces(
#         marker_line_width=0,
#         marker=dict(opacity=1),
#         hovertemplate=(
#             '<b>Post Date:</b> %{x}<br>'
#             '<b>Total Reactions:</b> %{y}<br>'
#             '<b>Likes:</b> %{customdata[2]}<br>'
#             '<b>Loves:</b> %{customdata[1]}<br>'
#             '<b><a href="%{customdata[0]}" target="_blank">View Post</a></b><extra></extra>'
#         )
#     )
    
#     # Update layout to format x-axis for dates and hide unnecessary labels
#     fig.update_layout(
#         font=dict(family="Arial", size=12, color="black"),
#         plot_bgcolor='white',
#         paper_bgcolor='white',
#         title_font=dict(size=20, color='black'),
#         xaxis=dict(
#             title_font=dict(size=14, color='black'),
#             tickformat='%Y-%m-%d',
#             tickmode='linear',
#             showticklabels=True,
#         ),
#         yaxis=dict(
#             title_font=dict(size=14, color='black'),
#         ),
#         width=1200,
#         height=600,
#         margin=dict(l=120, r=20, t=60, b=100)
#     )
    
#     # Define the layout of the Dash app
#     app.layout = html.Div([
#         html.H1("Top 30 Posts by Total Reactions"),
#         dcc.Graph(
#             id='post-reaction-scatter',
#             figure=fig
#         ),
#         dcc.Location(id='url', refresh=True)
#     ])
    
#     # Define callback to capture click event and open the post URL
#     @app.callback(
#         Output('url', 'href'),
#         Input('post-reaction-scatter', 'clickData')
#     )
#     def update_post_url(clickData):
#         if clickData is not None:
#             post_url = clickData['points'][0]['customdata'][0]
#             return post_url
#         return None
    
#     return app

# # Create the app instance
# app = create_interactive_post_graph('bangladeshislamichhatrashibir_cleaned.csv')

# if __name__ == '__main__':
    
#     import os
#     port = int(os.getenv('PORT', 8050))  # Default to 8050 if PORT is not set
#     app.run_server(host='0.0.0.0', port=port, debug=True)

from dash import Dash, dcc, html
import os

# Create a simple Dash app
app = Dash(__name__)

# Define the layout of the Dash app
app.layout = html.Div([
    html.H1("Hello, Render!"),
    dcc.Graph(
        id='test-graph',
        figure={
            'data': [{
                'x': [1, 2, 3],
                'y': [4, 5, 6],
                'type': 'bar',
                'name': 'Test Data',
            }],
            'layout': {
                'title': 'Simple Bar Chart',
                'xaxis': {'title': 'X Axis'},
                'yaxis': {'title': 'Y Axis'}
            }
        }
    )
])

# Run the server
if __name__ == '__main__':
    port = int(os.getenv('PORT', 8050))  # Default to 8050 if PORT is not set
    app.run_server(host='0.0.0.0', port=port, debug=True)
