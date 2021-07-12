import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

from app import app
from services import data_service, parser_service
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
              Output('memory-store', 'data'),
              Input('upload-data', 'contents'),
              Input('upload-data', 'style'),
              State('upload-data', 'filename'))
def update_visualizer(content, upload_box, filename):
    if content is not None:
        parsed = parser_service.parse_data(content, filename)
        if parsed.empty:
            return Error.layout, upload_box, None
        else:
            upload_box_update = upload_box.copy()
            upload_box_update['background'] = '#b4ffb4' # faded green
            splitted = data_service.split_carryovers(parsed)
            colours = data_service.get_discret_colour_map(parsed)
            return Chart.layout, upload_box_update, {'data': parser_service.parse_df_to_json(splitted), 'colours': colours}

    return None, upload_box, None
