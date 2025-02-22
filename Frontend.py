import dash
from dash import dcc, html
import plotly.graph_objs as go
from dash.dependencies import Input, Output, State
import numpy as np
import random

app = dash.Dash(_name_)

# Function to simulate wave-like water level data
def generate_wave_water_level(stable=False):
    x = np.linspace(0, 10, 100)
    if stable:
        base_wave = np.ones_like(x) * 40  # Stable flat wave
    else:
        base_wave = np.sin(x) * random.uniform(0.8, 1.2) * 10 + random.uniform(30, 70)
    return x, base_wave

# Function to generate random pH and TDS values
def generate_random_ph_tds():
    ph_value = round(random.uniform(6.5, 8.5), 2)
    tds_value = round(random.uniform(100, 500), 2)
    return ph_value, tds_value

# App layout
app.layout = html.Div([
    html.H1("Aqua Sentinel - Water Quality Monitoring", 
            style={'textAlign': 'center', 'color': '#00AEEF', 'backgroundColor': 'black'}),

    dcc.Graph(id='water-level-chart', config={'displayModeBar': False}, 
              style={'backgroundColor': 'black'}),

    html.Div([
        html.H3("pH Level", style={'color': '#FFA500'}),
        html.Button(id='ph-level', children="--", 
                    style={'fontSize': '24px', 'fontWeight': 'bold', 'borderRadius': '50%', 
                           'width': '100px', 'height': '100px', 'backgroundColor': '#FFA500', 
                           'color': 'black'}),

        html.H3("TDS Level (ppm)", style={'color': '#00FF00'}),
        html.Button(id='tds-level', children="-- ppm", 
                    style={'fontSize': '24px', 'fontWeight': 'bold', 'borderRadius': '50%', 
                           'width': '100px', 'height': '100px', 'backgroundColor': '#00FF00', 
                           'color': 'black'})
    ], style={'textAlign': 'center', 'marginTop': '20px', 'backgroundColor': 'black'}),

    html.Button("Regulate Water Flow", id='toggle-wave-btn', n_clicks=0, 
                style={'marginTop': '20px', 'padding': '10px', 'fontSize': '18px', 
                       'borderRadius': '10px', 'backgroundColor': '#008CBA', 'color': 'white', 
                       'border': 'none', 'cursor': 'pointer'}),

    dcc.Store(id='wave-state', data={'stable': False}),  # Store wave state

    dcc.Interval(id='data-update', interval=1000, n_intervals=0),  
    dcc.Interval(id='interval', interval=3000, n_intervals=0)  
], style={'backgroundColor': 'black', 'textAlign': 'center'})

# Callback to toggle wave movement on/off
@app.callback(
    Output('wave-state', 'data'),
    Input('toggle-wave-btn', 'n_clicks'),
    State('wave-state', 'data')
)
def toggle_wave(n_clicks, wave_state):
    if n_clicks % 2 == 1:
        return {'stable': True}  # Stop the wave
    return {'stable': False}  # Resume wave movement

# Callback to update wave graph
@app.callback(
    Output('water-level-chart', 'figure'),
    [Input('data-update', 'n_intervals'), Input('wave-state', 'data')]
)
def update_wave_graph(n, wave_state):
    x, y = generate_wave_water_level(stable=wave_state['stable'])

    figure = {
        'data': [
            go.Scatter(x=x, y=y, mode='lines', line=dict(color='#00AEEF', width=3), 
                       fill='tozeroy', name='Water Level')
        ],
        'layout': go.Layout(
            title='Real-Time Water Flow',
            xaxis={'visible': False},
            yaxis={'visible': False},
            plot_bgcolor='black',
            paper_bgcolor='black',
            font=dict(color='white'),
            showlegend=False
        )
    }
    return figure

# Callback to update pH and TDS levels
@app.callback(
    [Output('ph-level', 'children'), Output('tds-level', 'children')],
    Input('interval', 'n_intervals')
)
def update_data(n):
    ph_value, tds_value = generate_random_ph_tds()
    return ph_value, f"{tds_value} ppm"

if _name_ == '_main_':
    app.run_server(debug=True, port=8050)
