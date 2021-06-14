from pandas.core import groupby
import clockify_parser
import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import time_service
import dash_html_components as html
import plotly.express as px

# Styles
upload_data_style = {
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        }

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = dbc.Container([
    html.H1(children='Time Tracker Visualizer'),
    html.Hr(),

    html.H3(children='Instructions'),
    html.Ol(children=[
        html.Li(['Head to ', html.A(href='https://clockify.me/tracker', children='Clockify')]),
        html.Li(children='Click on REPORTS in the sidebar.'),
        html.Li(children='Select the range of data you wish to visualize.'),
        html.Li(children='Under the second panel (scroll to the bottom of the page), select the two crtieria to Group By.'),
        html.Li(children='Indicate the two criteria below respectively'),
        html.Li(children='Click on Export > Save as CSV in the first panel and save the file.'),
        html.Li(children='Upload the saved csv file over to the box below.')
    ]),
    html.Hr(id='placeholder'),

    html.P(children='This visualizer assumes this data structure and that tracking is done by tagging the particular activity.'),
    html.Div([
        "Group By: ",
        dcc.Dropdown(
            id='group-by-criteria-1',
            options=[
                {'label': 'Project', 'value': 'Project'},
                {'label': 'Client', 'value': 'Client'},
                {'label': 'User', 'value': 'User'},
                {'label': 'Groups', 'value': 'Groups'},
                {'label': 'Tag', 'value': 'Tag'},
                {'label': 'Date', 'value': 'Date'},
            ],
            value='Tag',
            style={
                'display': 'inline-block', 
                'flex':'1'
                }
        ),

        # Not in use yet
        dcc.Dropdown(
            id='group-by-criteria-2',
            options=[
                {'label': '(None)', 'value': '(None)'},
                {'label': 'Project', 'value': 'Project'},
                {'label': 'Task', 'value': 'Task'},
                {'label': 'Client', 'value': 'Client'},
                {'label': 'User', 'value': 'User'},
                {'label': 'Groups', 'value': 'Groups'},
                {'label': 'Tag', 'value': 'Tag'},
                {'label': 'Description', 'value': 'Description'},
                {'label': 'Date', 'value': 'Date'},
            ],
            placeholder="Criteria 2",
            style={
                'display': 'inline-block', 
                'flex':'1'
                }
        ),
    ],
    style={
        'display':'flex',
        'width' : '50%',
        'margin': '10px'
    }),

    html.Button('Reset', id='reset-button', n_clicks=0),

    dcc.Upload(
        id='upload-data',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Click to Upload', style={"text-decoration": "underline"})
        ]),
        style=upload_data_style,    
        multiple=False
    ),
    dbc.Container(id='output-data-upload'),
])

criteria = [None] * 10
@app.callback(Output('placeholder', 'id'),
              Input('group-by-criteria-1', 'value'),
              Input('group-by-criteria-2', 'value'))
def update_criteria_1(criteria_1, criteria_2):
    criteria[0] = criteria_1
    criteria[1] = criteria_2
    return 'placeholder'


@app.callback(Output('output-data-upload', 'children'),
              Output('upload-data', 'style'),
              Input('upload-data', 'contents'),
              Input('reset-button', 'n_clicks'),
              State('upload-data', 'filename'))
def update_visualizer(content, reset_clicks, filename):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if 'reset-button' in changed_id:
        return [None, upload_data_style]

    if content is not None:
        parsed = clockify_parser.parse_data(content, filename)

        if parsed.empty:
            return html.H4(['There was error processing the file uploaded or the file was empty.']), upload_data_style
        
        for i in range(len(criteria)):
            if criteria[i] is None: break
            parsed = parsed.groupby(criteria[i], as_index=False)

        sum_by_tag = parsed['Time (decimal)'].sum()
        total_time = sum_by_tag['Time (decimal)'].sum()
        fig = px.pie(sum_by_tag, values='Time (decimal)', names='Tag', title='An Averaged 24hr')
        fig.update_traces(text=[time_service.convert_to_hrs_for_display(sum_by_tag.iloc(0)[i][1], total_time) for i in range(0, len(sum_by_tag))])

        upload_data_style2 = upload_data_style.copy()
        upload_data_style2['background-color'] = 'lightgreen'
        output_data_upload_children = [
            dbc.Row([
                dbc.Col([
                        dcc.Dropdown(
                            id='dropdown-selector',
                            options=[
                                {'label': 'Averaged', 'value': 'Averaged'},
                                {'label': 'Weekday', 'value': 'Weekday'},
                                {'label': 'Weekend', 'value': 'Weekend'}
                            ],
                            value='Averaged',
                            multi=False,
                            searchable=False,
                            placeholder='Select Chart Type...'
                        ),
                    ], width=4, className='p-3'),
                ]),
            dbc.Row([
                dbc.Col([dcc.Graph(figure=fig)])
            ])
        ]
        return output_data_upload_children, upload_data_style2
    return [None, upload_data_style]

@app.callback(Output('upload-data', 'contents'),
              Input('reset-button', 'n_clicks')) 
def reset_contents(reset_button):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if 'reset-button' in changed_id:
        return None

if __name__ == '__main__':
    app.run_server(debug=True)

