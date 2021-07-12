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
    dbc.Row([dbc.Col(id='pie')]),
    dbc.Row([dbc.Col(id='histogram')])
])


@app.callback(Output('pie', 'children'),
              Output('histogram', 'children'),
              Input('dropdown-selector', 'value'),
              Input('memory-store', 'data'),
              Input('group-by-criteria', 'value'))
def update_charts(selected, data, criteria):
    if data is None:
        # No data in memory store
        raise PreventUpdate

    df = parser_service.parse_json_to_df(data['data'])
    colour_map = data['colours']    
    pie_chart = None
    group_sum = None

    # ===== Building Pie Chart ======
    if selected == 'Averaged':
        group_sum = data_service.sum_time_by_criteria(
            df, criteria)
        pie_chart = px.pie(group_sum, values=const.time_in_decmial, color=const.tags, color_discrete_map=colour_map,
                           names=criteria[0], title='An Averaged 24hr')
    elif selected == 'Weekday':
        group_sum = data_service.sum_time_by_workweek(df, True)
        pie_chart = px.pie(group_sum, values=const.time_in_decmial, color=const.tags, color_discrete_map=colour_map,
                           names=criteria[0], title='An Averaged Weekday')
    elif selected == 'Weekend':
        group_sum = data_service.sum_time_by_workweek(df, False)
        pie_chart = px.pie(group_sum, values=const.time_in_decmial, color=const.tags, color_discrete_map=colour_map,
                           names=criteria[0], title='An Averaged Weekend')
    else:
        return None, None

    total_time = data_service.sum_time(group_sum)    
    # Upate labels from decimal to hours
    pie_chart.update_traces(text=[time_service.convert_to_hrs_for_display(
        group_sum.iloc(0)[i][1], total_time) for i in range(0, len(group_sum))])

    # ===== Building Stacked Bar Chart ======
    # Hacky way to get gantt charts on plotly to work with time based data. See https://stackoverflow.com/questions/63714679/plotting-gannt-chart-using-timestamps
    df['barstart'] = '1970-01-01 ' + df[const.start_time].astype(str)
    df['barend'] = '1970-01-01 ' + df[const.end_time].astype(str)
    
    num_of_days = len(df[const.start_date].unique())
    stacked_bar = px.timeline(df, x_start='barstart', x_end='barend', y=const.start_date, height=(num_of_days * const.gantt_bar_height),
                              color=const.tags, color_discrete_map=colour_map, title='Time Spent Each Day')
    stacked_bar.update_layout(xaxis=dict(tickformat = '%H:%M'))

    return dcc.Graph(figure=pie_chart), dcc.Graph(figure=stacked_bar)
