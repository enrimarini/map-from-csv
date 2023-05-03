import pandas as pd
import plotly.express as px
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output

# Load the data
data = pd.read_csv('newdata4.csv')
data['date'] = pd.to_datetime(data['date'], format='%m/%d/%Y')
data['month'] = data['date'].dt.month
data['year'] = data['date'].dt.year
data['hour'] = pd.to_datetime(data['time'], format='%H:%M:%S').dt.hour
data['time_of_day'] = data['hour'].apply(lambda x: 'AM' if x < 12 else 'PM')
data['day'] = data['date'].apply(lambda x: x.day)


# Update the column to include the year, month, and time of day
data['year_month_time_of_day_numeral'] = data['year'].astype(str) + '_' + data['month'].astype(str) + '_' + data['time_of_day'] + '_' + data['day'].astype(str)

# Create the app
app = dash.Dash(__name__)

# Define the layout
app.layout = html.Div([
    html.H1("Interactive Map with Filters"),

    html.Div([
        html.Label('Select Month:'),
        dcc.Dropdown(
            id='month-dropdown',
            options=[{'label': month, 'value': month} for month in data['month'].unique()],
            value=data['month'].unique().tolist(),
            multi=True,
            placeholder="Select Month(s)"
        ),
    ], style={'width': '20%', 'display': 'inline-block'}),

    html.Div([
        html.Label('Select Year:'),
        dcc.Dropdown(
            id='year-dropdown',
            options=[{'label': year, 'value': year} for year in data['year'].unique()],
            value=data['year'].unique().tolist(),
            multi=True,
            placeholder="Select Year(s)"
        ),
    ], style={'width': '10%', 'display': 'inline-block'}),

    html.Div([
        html.Label('Select Time of Day'),
        dcc.Dropdown(
            id='time_of_day-dropdown',
            options=[{'label': time_of_day, 'value': time_of_day} for time_of_day in data['time_of_day'].unique()],
            value=data['time_of_day'].unique().tolist(),
            multi=True,
            placeholder="Select Time of Day (AM/PM)"
        ),
    ], style={'width': '10%', 'display': 'inline-block'}),

    html.Div([
        html.Label('Select Day'),
        dcc.Dropdown(
            id='day-dropdown',
            options=[{'label': day, 'value': day} for day in range(1, 32)],
            value=data['day'].unique().tolist(),
            multi=True,
            placeholder="Select Day"
        ),
    ], style={'width': '60%', 'display': 'inline-block'}),

    dcc.Graph(id='map-graph')
])

# Define the callback
@app.callback(
    Output('map-graph', 'figure'),
    Input('month-dropdown', 'value'),
    Input('year-dropdown', 'value'),
    Input('time_of_day-dropdown', 'value'),
    Input('day-dropdown', 'value')
)

def update_map(selected_months, selected_years, selected_time_of_day, selected_days):
    filtered_data = data[
        data['month'].isin(selected_months) &
        data['year'].isin(selected_years) &
        data['time_of_day'].isin(selected_time_of_day) &
        data['day'].isin(selected_days)
    ]

    fig = px.scatter_mapbox(
        filtered_data,
        lat='location-lat',
        lon='location-long',
        hover_name='date',
        hover_data=['time'],
        zoom=10,
        height=600,
        color='year_month_time_of_day_numeral',  # Use the updated column to assign colors
        color_discrete_sequence=px.colors.qualitative.Plotly,  # Color palette
    )

    fig.update_traces(marker=dict(size=15))  # Increase this value to make the points larger

    fig.update_layout(mapbox_style='open-street-map', margin={'r': 0, 't': 0, 'l': 0, 'b': 0})
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
