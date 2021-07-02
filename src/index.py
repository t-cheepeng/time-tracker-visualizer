import dash_bootstrap_components as dbc
import dash_html_components as html

from app import app
from components import Instructions, Upload, GroupBy, Store

app.layout = dbc.Container([
        Store.layout,
        html.H1(children='Time Tracker Visualizer'),
        html.Hr(),

        Instructions.layout,
        GroupBy.layout,
        Upload.layout,

        html.Div(id='output-data-upload'),
    ])
    
if __name__ == '__main__':
    app.run_server(debug=True)
