import dash
import dash_bootstrap_components as dbc
from flask import Flask, send_from_directory


server = Flask(__name__)
app = dash.Dash(__name__,external_stylesheets=[dbc.themes.BOOTSTRAP],
                meta_tags=[
                    {"name": "viewport", "content": "width=device-width, initial-scale=1"}
                ],server=server
                )
# server = app.server
app.config.suppress_callback_exceptions = True


