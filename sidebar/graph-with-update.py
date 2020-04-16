import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
import numpy as np
import base64
import io
import dash_bootstrap_components as dbc



app = dash.Dash(__name__,external_stylesheets=[dbc.themes.BOOTSTRAP],
                meta_tags=[
                    {"name": "viewport", "content": "width=device-width, initial-scale=1"}
                ],
                )

app.layout = html.Div(children=[
    dcc.Upload(
        id='upload-data',
        children=html.Div([
            dbc.Button("Select Files", id="upload-button", className="mr-2"),
        ])
        # Allow multiple files to be uploaded
        # multiple=True
    ),
    html.H1(children='Patients with HTA'),
    html.Div(children='''patients number by age range having HTA'''),
    html.Div([
        dcc.Dropdown(
            id="Sexe",
            options=[
                {'label': 'Tous','value': 'tous'},
                {'label': 'Femme','value': 'femme'},
                {'label': 'Homme','value': 'homme'}

            ],
                value='All sexe'),
        ],
        style={'width': '25%',
               'display': 'inline-block'}),
        dcc.Graph(id='graph-hta'),
     ])



@app.callback(
    dash.dependencies.Output('graph-hta', 'figure'),
    [dash.dependencies.Input('upload-data', 'contents'),
     dash.dependencies.Input('upload-data', 'filename'),
     dash.dependencies.Input('Sexe', 'value')]
)

def update_graph(contents, filename,Sexe):
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    df = pd.read_excel(io.BytesIO(decoded))
    sexe = df["Sexe"].unique()
    sexe = np.append(sexe, 'tous')
    print(sexe)
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
