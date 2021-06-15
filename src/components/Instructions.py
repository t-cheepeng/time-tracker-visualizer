import dash_html_components as html

layout = html.Div([
    html.H3(children='Instructions'),
    html.Ol(children=[
            html.Li(
                ['Head to ', html.A(href='https://clockify.me/tracker', children='Clockify')]),
            html.Li(children='Click on REPORTS in the sidebar.'),
            html.Li(children='Select the range of data you wish to visualize.'),
            html.Li(
                children='Under the second panel, select the Group By for "Tag", followed by "Description". '),
            html.Li(
                children='Click on Export > Save as CSV in the first panel and save the file.'),
            html.Li(children='Upload the saved csv file over to the box below.')
            ]),
    html.Hr(),
    html.P(children='This visualizer assumes this data structure and that tracking is done by tagging the particular activity.'),
])
