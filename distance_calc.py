import pandas as pd
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
from haversine import haversine, Unit

# Read and sort data
data = pd.read_csv('newdata4.csv')
data['datetime'] = pd.to_datetime(data['date'] + ' ' + data['time'])
data['date'] = pd.to_datetime(data['date'], format='%m/%d/%Y')
data['month'] = data['date'].dt.month
data['year'] = data['date'].dt.year
data['hour'] = pd.to_datetime(data['time'], format='%H:%M:%S').dt.hour
data['time_of_day'] = data['hour'].apply(lambda x: 'AM' if x < 12 else 'PM')
data = data.sort_values('datetime')

# Calculate distances
data['distance_km'] = [haversine((data['location-lat'].iloc[i], data['location-long'].iloc[i]),
                   (data['location-lat'].iloc[i+1], data['location-long'].iloc[i+1]))
                   for i in range(len(data) - 1)] + [0]
data['distance_miles'] = data['distance_km'] * 0.621371

# Initialize Dash app
app = dash.Dash(__name__)

# Create Dash layout
app.layout = html.Div([
    html.H1('Total Distance Traveled'),

    html.Div([
        html.Label('Select Day:'),
        dcc.Dropdown(
            id='day-dropdown',
            options=[{'label': day, 'value': day} for day in data['date'].dt.day.unique()],
            value=data['date'].dt.day.unique().tolist(),
            multi=True,
            placeholder="Select Day(s)"
        ),
    ], style={'width': '20%', 'display': 'inline-block'}),

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
    ], style={'width': '20%', 'display': 'inline-block'}),

    html.Div([
        html.Label('Select Time of Day'),
        dcc.Dropdown(
            id='time-dropdown',
            options=[{'label': time_of_day, 'value': time_of_day} for time_of_day in data['time_of_day'].unique()],
            value=data['time_of_day'].unique().tolist(),
            multi=True,
            placeholder="Select Time of Day (AM/PM)"
        ),
    ], style={'width': '20%', 'display': 'inline-block'}),

    html.Div(id='output')
])

# Callback function to update output
@app.callback(
    Output('output', 'children'),
    [
        Input('day-dropdown', 'value'),
        Input('month-dropdown', 'value'),
        Input('year-dropdown', 'value'),
        Input('time-dropdown', 'value')
    ]
)
def update_output(selected_days, selected_months, selected_years, selected_time_of_day):
    filtered_data = data[
        data['date'].dt.day.isin(selected_days) &
        data['month'].isin(selected_months) &
        data['year'].isin(selected_years) &
        data['time_of_day'].isin(selected_time_of_day)
    ]

    total_distance_km = filtered_data['distance_km'].sum()
    total_distance_miles = filtered_data['distance_miles'].sum()

    return f'Total distance: {total_distance_km:.2f} km / {total_distance_miles:.2f} miles'

# Run the Dash app
if __name__ == '__main__':
    app.run_server(debug=True)
