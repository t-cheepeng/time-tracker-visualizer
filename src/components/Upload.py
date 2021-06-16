import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

from app import app
from services import parser_service
from components import Chart, Error

layout = dcc.Upload(
    id='upload-data',
    children=html.Div([
        'Drag and Drop or ',
        html.A('Click to Upload', style={"text-decoration": "underline"}) 
    ]),
    className='upload-box',
    multiple=False
)

@app.callback(Output('output-data-upload', 'children'),
              Output('upload-data', 'className'),
              Input('upload-data', 'contents'),
              Input('group-by-criteria', 'value'),
              Input('upload-data', 'className'),
              State('upload-data', 'filename'))
def update_visualizer(content, criteria, class_name, filename):
    if content is not None:
        parsed = parser_service.parse_data(content, filename)
        
        if parsed.empty:
            return (Error.layout, class_name)
        else:
            return (Chart.serve_layout(parsed, criteria), class_name + (' bg-faded-green'))

    return [None, class_name]
