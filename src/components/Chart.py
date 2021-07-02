import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
import plotly.express as px

from services import data_service, time_service

def serve_layout(parsed_data, criteria):
    criteria_sums = data_service.sum_time_by_criteria(parsed_data, criteria)
    total_time = data_service.sum_time(criteria_sums)
    
    fig = px.pie(criteria_sums, values='Time (decimal)',
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
            dbc.Col([dcc.Graph(figure=fig)])
        ])
    ])