import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

import constants

layout = dbc.Row([
    html.Span("Group By: "),
    dcc.Dropdown(
        id='group-by-criteria',
        options=constants.group_by_options,
        # TODO: Somehow fix this group by thing to match standardised column names
        value=constants.group_by_criteria[:2],
        multi=True,
        style={'width':'70%'}
    ),
    ],
)  


   