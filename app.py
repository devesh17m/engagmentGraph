import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output
import webbrowser

def create_interactive_post_graph(csv_file_path):
    # Load the CSV file
    df = pd.read_csv(csv_file_path)
    
    # Ensure necessary columns are present
    if 'total_reactions/Like' not in df.columns or 'total_reactions/Love' not in df.columns or 'post_id' not in df.columns or 'post_url' not in df.columns or 'post_date' not in df.columns:
        print("The necessary columns ('total_reactions/Like', 'total_reactions/Love', 'post_id', 'post_url', 'post_date') are missing from the CSV file.")
        return
    
    # Convert post_date to datetime if it's not already
    df['post_date'] = pd.to_datetime(df['post_date'])
    
    # Calculate the sum of total reactions (Like + Love)
    df['total_reactions_sum'] = df['total_reactions/Like'] + df['total_reactions/Love']
    
    # Sort the DataFrame by the total reactions sum and select the top 30 posts
    df_top30 = df.sort_values(by='total_reactions_sum', ascending=False).head(30)
    
    # Create the Dash app
    app = Dash(__name__)
    
    # Create the Plotly figure for the top 30 posts with gradient color
    fig = px.scatter(
        df_top30,
        x='post_date',  # Use post_date on the x-axis
        y='total_reactions_sum',
        title='Top 30 Posts by Total Reactions (Like + Love)',
        labels={'post_date': 'Post Date', 'total_reactions_sum': 'Total Reactions (Like + Love)'},
        color='total_reactions_sum',  # Gradient color based on reaction sum
        hover_data=['post_url', 'total_reactions/Like', 'total_reactions/Love', 'post_id'],  # More data for hover, including post_id
        template='plotly_white',
        color_continuous_scale=px.colors.sequential.Plasma,  # Plasma gradient scale
        size='total_reactions_sum',  # Size of the markers based on total reactions
        size_max=20  # Maximum size of the markers
    )
    
    # Set custom hover template to make it larger and clickable
    fig.update_traces(
        marker_line_width=0,  # No borders around the markers
        marker=dict(opacity=1),  # Full opacity for solid colors
        hovertemplate=(
            '<b>Post Date:</b> %{x}<br>'
            '<b>Total Reactions:</b> %{y}<br>'
            '<b>Likes:</b> %{customdata[2]}<br>'
            '<b>Loves:</b> %{customdata[1]}<br>'
            '<b><a href="%{customdata[0]}" target="_blank">View Post</a></b><extra></extra>'
        )  # Custom hover text with clickable link
    )
    
    # Update layout to format x-axis for dates and hide unnecessary labels
    fig.update_layout(
        font=dict(family="Arial", size=12, color="black"),
        plot_bgcolor='white',
        paper_bgcolor='white',
        title_font=dict(size=20, color='black'),
        xaxis=dict(
            title_font=dict(size=14, color='black'),
            tickformat='%Y-%m-%d',  # Display dates in a readable format
            tickmode='linear',  # Ensure all post dates are shown
            showticklabels=True,  # Keep x-axis labels for dates
        ),
        yaxis=dict(
            title_font=dict(size=14, color='black'),
        ),
        width=1200,  # Increase width of the graph for better display
        height=600,  # Adjust height to make it more spacious
        margin=dict(l=120, r=20, t=60, b=100)  # Adjust margins to fit labels
    )
    
    # Define the layout of the Dash app
    app.layout = html.Div([
        html.H1("Top 30 Posts by Total Reactions"),
        dcc.Graph(
            id='post-reaction-scatter',
            figure=fig
        ),
        dcc.Location(id='url', refresh=True)
    ])
    
    # Define callback to capture click event and open the post URL
    @app.callback(
        Output('url', 'href'),
        Input('post-reaction-scatter', 'clickData')
    )
    def open_post_url(clickData):
        if clickData is not None:
            # Extract post URL from clickData
            post_url = clickData['points'][0]['customdata'][0]
            
            # Print type and value for debugging
            print(f"URL Type: {type(post_url)}")
            print(f"URL Value: {post_url}")
            
            # Ensure post_url is a string
            if isinstance(post_url, str):
                webbrowser.open(post_url)  # Opens the URL in the browser
                return post_url
            else:
                print("Error: post_url is not a string")
                return None
        return None
    
    return app

# Create the app instance
app = create_interactive_post_graph('bangladeshislamichhatrashibir_merged.csv')

if __name__ == '__main__':
    app.run_server(debug=True)
