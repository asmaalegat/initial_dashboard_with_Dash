import dash_html_components as html
import dash_bootstrap_components as dbc
import dash
from app import app
from dash.dependencies import Input, Output, State
import pandas as pd
import numpy as np
import base64
import io

@app.callback(
    Output('app-1-display-value', 'children'),
    [Input('app-1-dropdown', 'value')])
def display_value(value):
    return 'You have selected "{}"'.format(value)

@app.callback(
    Output('app-2-display-value', 'children'),
    [Input('app-2-dropdown', 'value')])
def display_value(value):
    return 'You have selected "{}"'.format(value)
# -----------------------------------------------------------------------------

# @app.callback(Output("page-content", "children"),
#               [Input("url", "pathname")])
# def render_page_content(pathname):
#     if pathname in ["/", "/apps/app1"]:
#         return html.P("This is the content of page 1!")
#     elif pathname == "/apps/app2":
#         return
#     elif pathname == "/apps":
#         return html.P("Oh cool, this is page 3!")
#     # If the user tries to reach a different page, return a 404 message
#     return dbc.Jumbotron(
#         [
#             html.H1("404: Not found", className="text-danger"),
#             html.Hr(),
#             html.P(f"The pathname {pathname} was not recognised..."),
#         ]
#     )

@app.callback(
    dash.dependencies.Output('graph-hta', 'figure'),
    [dash.dependencies.Input('upload-data', 'contents'),
     dash.dependencies.Input('upload-data', 'filename')]
)
def update_table(contents, filename):
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    df = pd.read_excel(io.BytesIO(decoded))


@app.callback(
    dash.dependencies.Output('container-button-basic', 'children'),
    [dash.dependencies.Input('submit-val', 'n_clicks')])

def nombre_click(n_clicks, value):
    return 'The input value was "{}"'.format(
        n_clicks
    )

