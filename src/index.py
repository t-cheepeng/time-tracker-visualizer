import dash_bootstrap_components as dbc
import dash_html_components as html

from app import app
from components import Instructions, Upload

app.layout = dbc.Container([
        html.H1(children='Time Tracker Visualizer'),
        html.Hr(),

        Instructions.layout,
        Upload.layout,

        html.Div(id='output-data-upload'),
    ])
    
if __name__ == '__main__':
    app.run_server(debug=True)
