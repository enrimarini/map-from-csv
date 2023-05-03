import pandas as pd
import folium
from folium.plugins import FastMarkerCluster
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

    html.Div(id='map-graph')
])

# Define the callback
@app.callback(
    Output('map-graph', 'children'),
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

    m = folium.Map(location=[filtered_data['location-lat'].mean(), filtered_data['location-long'].mean()], zoom_start=10)

    marker_cluster = FastMarkerCluster(
        data=list(zip(filtered_data['location-lat'],
    filtered_data['location-long'], filtered_data['date'].astype(str), filtered_data['time'])),
        callback="""\
        function (row) {
            var marker = L.marker(new L.LatLng(row[0], row[1]));
            var popup = L.popup().setContent('<p>Date: ' + row[2] + '<br>Time: ' + row[3] + '</p>');
            marker.bindPopup(popup);
            return marker;
        }
        """
    ).add_to(m)

    return html.Iframe(srcDoc=m._repr_html_(), width='100%', height='600')

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
