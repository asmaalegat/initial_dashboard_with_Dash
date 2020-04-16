import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import os
from flask import Flask, send_from_directory
import base64
from app import app , server
from layouts import layout1, layout2 , layout3
from urllib.parse import quote as urlquote
import plotly.graph_objs as go

from sklearn.cluster import DBSCAN
import numpy as np
import pandas as pd
from pandas_profiling import ProfileReport
import matplotlib.pyplot as plt
from collections import Counter
from sklearn.impute import KNNImputer
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer
from sklearn.linear_model import BayesianRidge, LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import ExtraTreesRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import cross_val_score
from matplotlib import cm
from sklearn.preprocessing import LabelEncoder


app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/apps/app1':
         return layout1
    elif pathname == '/apps/app2':
         return layout2
    elif pathname == '/apps/app3':
         return layout3
    else:
        return '404'

@app.callback(
    [Output(f"page-{i}-link", "active") for i in range(1, 4)],
    [Input("url", "pathname")],
)
def toggle_active_links(pathname):
    if pathname == "/":
        # Treat page 1 as the homepage / index
        return True, False, False
    return [pathname == f"/apps/app{i}" for i in range(1, 4)]
# -----------------------------------------------------------------------

UPLOAD_DIRECTORY = "./uploaded-files"

if not os.path.exists(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY)
# Normally, Dash creates its own Flask server internally. By creating our own,
# we can create a route for downloading files directly:


@server.route("/download/<path:path>")
def download(path):
    """Serve a file from the upload directory."""
    return send_from_directory(UPLOAD_DIRECTORY, path, as_attachment=True)



def DM_main(data):


    return

def save_file(name, content):
    """Decode and store a file uploaded with Plotly Dash."""
    data = content.encode("utf8").split(b";base64,")[1]
    file_path = os.path.join(UPLOAD_DIRECTORY, name)
    # with open (file_path, "wb") as fp:
    #     fp.write(base64.decodebytes(data))
    # file=os.path.join(file_path + "." + "xlsx")
    df = pd.read_excel(base64.decodebytes(data))
    df = DM_main(df)
    df.to_excel(file_path, index= None)

def uploaded_files():
    """List the files in the upload directory."""
    files = []
    for filename in os.listdir(UPLOAD_DIRECTORY):
        path = os.path.join(UPLOAD_DIRECTORY, filename)
        if os.path.isfile(path):
            files.append(filename)
    return files

def file_download_link(filename):
    """Create a Plotly Dash 'A' element that downloads a file from the app."""
    location = "/download/{}".format(urlquote(filename))
    return html.Div([html.H6(filename),html.A("download", href=location)])


# html.Div([html.H6(filename),
#                     html.A("download", href=location)])


@app.callback(
    Output("file-list", "children"),
    [Input("upload-data", "filename"), Input("upload-data", "contents")],
)
def update_output(uploaded_filenames, uploaded_file_contents):
    """Save uploaded files and regenerate the file list."""

    if uploaded_filenames is not None and uploaded_file_contents is not None:
        for name, data in zip(uploaded_filenames, uploaded_file_contents):
            save_file(name, data)


    files = uploaded_files()

    if len(files) == 0:
        return [html.Li("No files yet!")]
    else:
        return [html.Li(file_download_link(filename)) for filename in files]

@app.callback(
    Output('container-button-basic', 'children'),
    [Input('submit-val', 'n_clicks')])

def nombre_click(n_clicks):
    return 'the button has been clicked {} times'.format(
        n_clicks
    )



@app.callback(
    Output('graph-hta', 'figure'),
    [Input('Sexe', 'value')],)
def update_graph(Sexe):
    if Sexe == "All sexe":
        df_plot = df.copy()
    elif Sexe == 'tous'   :
        df_plot = df.copy()
    else:
        df_plot = df[df['Sexe'] == Sexe]

    pv = pd.pivot_table(df_plot, index=['Tranche'], columns=["HTA"], aggfunc='size', fill_value=0)
    print(pv)
    trace1 = go.Bar(x=pv.index, y=pv["g1"], name='grade1')
    trace2 = go.Bar(x=pv.index, y=pv["g2"], name='grade2')
    trace3 = go.Bar(x=pv.index, y=pv["g3"], name='grade3')
    return {
        'data': [trace1, trace2, trace3],
        'layout':
            go.Layout(
                title='Customer Order Status for {}'.format(Sexe),barmode='stack')
    }



if __name__ == '__main__':
    app.run_server(debug=True)
