import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

import constants

layout = dbc.Row([
    dbc.Label(html_for='group-by-criteria', children=['Group By: '], className='col-2 col-form-label'),
    dcc.Dropdown(
        id='group-by-criteria',
        options=constants.group_by_options,
        value=[constants.tags],
        multi=True,
        style={'width':'70%'},
        className='col-10'
    ),
    ], className='form-group'
)  
