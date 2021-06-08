import clockify_parser
import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import time_service
import dash_html_components as html
import plotly.express as px

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = dbc.Container([
    html.H1(children='Time Tracker Visualizer'),
    html.Hr(),

    html.H3(children='Instructions'),
    html.Ol(children=[
        html.Li(['Head to ', html.A(href='https://clockify.me/tracker', children='Clockify')]),
        html.Li(children='Click on REPORTS in the sidebar.'),
        html.Li(children='Select the range of data you wish to visualize.'),
        html.Li(children='Under the second panel, select the Group By for "Tag", followed by "Description". '),
        html.Li(children='Click on Export > Save as CSV in the first panel and save the file.'),
        html.Li(children='Upload the saved csv file over to the box below.')
    ]),
    html.Hr(),

    html.P(children='This visualizer assumes this data structure and that tracking is done by tagging the particular activity.'),

    dcc.Upload(
        id='upload-data',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Click to Upload')
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
    ),
    dbc.Container(id='output-data-upload'),
])

@app.callback(Output('output-data-upload', 'children'),
              Input('upload-data', 'contents'),
              State('upload-data', 'filename'))
def update_visualizer(content, filename):
    if content is not None:
        parsed = clockify_parser.parse_data(content, filename)

        if parsed.empty:
            return html.H4(['There was error processing the file uploaded or the file was empty.'])
        
        sum_by_tag = parsed.groupby('Tag', as_index=False)['Time (decimal)'].sum()
        total_time = sum_by_tag['Time (decimal)'].sum()
        fig = px.pie(sum_by_tag, values='Time (decimal)', names='Tag', title='An Averaged 24hr')
        fig.update_traces(text=[time_service.convert_to_hrs_for_display(sum_by_tag.iloc(0)[i][1], total_time) for i in range(0, len(sum_by_tag))])
        return [
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
        

if __name__ == '__main__':
    app.run_server(debug=True)

