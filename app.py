import dash
from dash import dcc, html
import plotly.graph_objs as go
from dash.dependencies import Input, Output
import numpy as np
import random
import requests

app = dash.Dash(__name__)

def generate_wave_water_level():
    x = np.linspace(0, 10, 100)
    base_wave = np.sin(x) * random.uniform(0.8, 1.2) * 10 + random.uniform(30, 70)
    return x, base_wave

def generate_random_ph_tds():
    ph_value = round(random.uniform(6.5, 8.5), 2)
    tds_value = round(random.uniform(100, 500), 2)
    return ph_value, tds_value

app.layout = html.Div([
    html.H1("Aqua Sentinel - Water Quality Monitoring", style={'textAlign': 'center', 'color': '#00AEEF', 'backgroundColor': 'black'}),
    
    dcc.Graph(id='water-level-chart', config={'displayModeBar': False}, style={'backgroundColor': 'black'}),
    
    html.Div([
        html.H3("pH Level", style={'color': '#FFA500'}),
        html.Button(id='ph-level', style={'fontSize': '24px', 'fontWeight': 'bold', 'borderRadius': '50%', 'width': '100px', 'height': '100px', 'backgroundColor': '#FFA500', 'color': 'black'}),
        
        html.H3("TDS Level (ppm)", style={'color': '#00FF00'}),
        html.Button(id='tds-level', style={'fontSize': '24px', 'fontWeight': 'bold', 'borderRadius': '50%', 'width': '100px', 'height': '100px', 'backgroundColor': '#00FF00', 'color': 'black'})
    ], style={'textAlign': 'center', 'marginTop': '20px', 'backgroundColor': 'black'}),

    dcc.Interval(id='data-update', interval=1000, n_intervals=0),  
    dcc.Interval(id='interval', interval=3000, n_intervals=0)  
], style={'backgroundColor': 'black'})

@app.callback(
    Output('water-level-chart', 'figure'),
    Input('data-update', 'n_intervals')
)
def update_wave_graph(n):
    x, y = generate_wave_water_level()
    
    figure = {
        'data': [
            go.Scatter(x=x, y=y, mode='lines', line=dict(color='#00AEEF', width=3), fill='tozeroy', name='Water Level')
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

@app.callback(
    [Output('ph-level', 'children'), Output('tds-level', 'children')],
    Input('interval', 'n_intervals')
)
def update_data(n):
    ph_value, tds_value = generate_random_ph_tds()
    return ph_value, f"{tds_value} ppm"

if __name__ == '__main__':
    app.run_server(debug=True, port=8050)
