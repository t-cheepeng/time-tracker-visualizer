import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.express as px

from app import app
from services import data_service, time_service
import constants as const

def serve_layout(parsed_data, criteria):
    criteria_sums = data_service.sum_time_by_criteria(parsed_data, criteria)
    total_time = data_service.sum_time(criteria_sums)
    
    fig = px.pie(criteria_sums, values=const.time_in_decmial,
                names=criteria[0], title='An Averaged 24hr')
    fig.update_traces(text=[time_service.convert_to_hrs_for_display(
        criteria_sums.iloc(0)[i][1], total_time) for i in range(0, len(criteria_sums))])

    return html.Div([
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
            dbc.Col(id='chart-container', children=[dcc.Graph(figure=fig)])
        ])
    ])

@app.callback(Output('chart-container', 'children'),
              Input('dropdown-selector', 'value'))
def update_chart(selected):
    if selected == 'Averaged':
        # TODO: Return back correct charts
        return []
    elif selected == 'Weekday':
        return []
    elif selected == 'Weekend':
        return []
    else:
        return []

