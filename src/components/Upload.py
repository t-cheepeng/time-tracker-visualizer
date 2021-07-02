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
    style={
        'width': '100%',
        'height': '60px',
        'lineHeight': '60px',
        'borderWidth': '1px',
        'borderStyle': 'dashed',
        'borderRadius': '5px',
        'textAlign': 'center',
        'margin': '10px'
    },
    multiple=False
)

@app.callback(Output('output-data-upload', 'children'),
              Output('upload-data', 'style'),
              Input('upload-data', 'contents'),
              Input('group-by-criteria', 'value'),
              Input('upload-data', 'style'),
              State('upload-data', 'filename'))
def update_visualizer(content, criteria, upload_box, filename):
    if content is not None:
        parsed = parser_service.parse_data(content, filename)
        # TODO: check if df here has been renamed in columns
        # TODO: store data in dcc.Store
        if parsed.empty:
            return Error.layout, upload_box
        else:
            upload_box_update = upload_box.copy()
            upload_box_update['background'] = '#b4ffb4' # faded green
            return Chart.serve_layout(parsed, criteria), upload_box_update

    return None, upload_box
