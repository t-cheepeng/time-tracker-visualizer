import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import plotly.express as px

from app import app
from components import GroupBy
from services import data_service, parser_service, time_service
import constants as const

layout = html.Div([
    GroupBy.layout,
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
        dbc.Col(id='chart-container')
            ])
])


@app.callback(Output('chart-container', 'children'),
              Input('dropdown-selector', 'value'),
              Input('memory-store', 'data'),
              Input('group-by-criteria', 'value'))
def update_chart(selected, data, criteria):
    if data is None:
        # No valid data in memory store
        raise PreventUpdate
    
    df = parser_service.parse_json_to_df(data)
    fig = None
    group_sum = None

    if selected == 'Averaged':
        group_sum = data_service.sum_time_by_criteria(
            df, criteria)
        fig = px.pie(group_sum, values=const.time_in_decmial,
                 names=criteria[0], title='An Averaged 24hr')
    elif selected == 'Weekday':
        group_sum = data_service.sum_time_by_workweek(df, True)
        fig = px.pie(group_sum, values=const.time_in_decmial,
                     names=criteria[0], title='An Averaged Weekday')
    elif selected == 'Weekend':
        group_sum = data_service.sum_time_by_workweek(df, False)
        fig = px.pie(group_sum, values=const.time_in_decmial,
                     names=criteria[0], title='An Averaged Weekend')
    else:
        return None

    total_time = data_service.sum_time(group_sum)
    # Upate labels from decimal to hours
    fig.update_traces(text=[time_service.convert_to_hrs_for_display(
        group_sum.iloc(0)[i][1], total_time) for i in range(0, len(group_sum))])

    return dcc.Graph(figure=fig)
