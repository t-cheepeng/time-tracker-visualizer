import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
import plotly.express as px

from services import data_service, time_service

def serve_layout(parsed_data):
    tag_sum = data_service.sum_time_by_tag(parsed_data)
    total_time = data_service.sum_time(tag_sum)
    
    fig = px.pie(tag_sum, values='Time (decimal)',
                names='Tag', title='An Averaged 24hr')
    fig.update_traces(text=[time_service.convert_to_hrs_for_display(
        tag_sum.iloc(0)[i][1], total_time) for i in range(0, len(tag_sum))])

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
