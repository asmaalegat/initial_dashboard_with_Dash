import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import base64

app1_layout = html.Div([
    html.H3('App 1'),
    dcc.Dropdown(
        id='app-1-dropdown',
        options=[
            {'label': 'App 1 - {}'.format(i), 'value': i} for i in [
                'NYC', 'MTL', 'LA'
            ]
        ]
    ),
    html.Div(id='app-1-display-value'),
    dcc.Link('Go to App 2', href='/apps/app2')
])



# -------------------------------------------------------------------------------
image_filename = 'logo.png' # replace with your own image
encoded_image = base64.b64encode(open(image_filename, 'rb').read()).decode('ascii')

sidebar_header = dbc.Row(
    [
        dbc.Col(
            html.Img(src='data:image/png;base64,{}'.format(encoded_image))
                ),
        dbc.Col(
            html.Button(
                html.Span(className="navbar-toggler-icon"),
                className="navbar-toggler",
                id="toggle",
            ),
            width="auto",
            align="center",
        ),
    ]
)


app2_layout = html.Div([
    html.H3('App 2'),
    dcc.Dropdown(
        id='app-2-dropdown',
        options=[
            {'label': 'App 2 - {}'.format(i), 'value': i} for i in [
                'NYC', 'MTL', 'LA'
            ]
        ]
    ),
    html.Div(id='app-2-display-value'),
    dcc.Link('Go to App 1', href='/apps/app1')
])


sidebar = html.Div(
    [
        sidebar_header,
        html.Div(
            [
                html.Hr(),
                html.P(
                    "Welcome user",
                    className="lead",
                ),
                html.Hr(),
            ],
            id="blurb",
        ),
        dbc.Collapse(
            dbc.Nav(
                [
                    dbc.NavLink("Page 1", href="/apps/app1", id="page-1-link"),
                    dbc.NavLink("Page 2", href="/apps/app2", id="page-2-link"),
                    dbc.NavLink("Page 3", href="/apps/app3", id="page-3-link"),
                ],
                vertical=True,
                pills=True,

            ),
            id="collapse",
        ),
    ],
    id="sidebar",
)

upload_button = html.Div(
    [
        html.H1("File Browser"),
        html.H2("Upload"),
        dcc.Upload(
            id="upload-data",
            children=html.Button('Select file', id='submit-val', n_clicks=0),


            multiple=True,
        ),
        html.Div(id='container-button-basic',
             children='Enter a value and press submit'),
        html.H2("File List"),
        html.Ul(id="file-list"),
    ],
    style={"max-width": "500px"},
)



layout1 = html.Div([sidebar,app1_layout])
layout2 = html.Div([sidebar,app2_layout])
layout3 = html.Div([sidebar,upload_button])