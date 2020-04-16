import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
import numpy as np

df = pd.read_excel("D:/dataset/outlier.xlsx")
print(df)

sexe = df["Sexe"].unique()
sexe = np.append(sexe,'tous')
print(sexe)
app = dash.Dash()

app.layout = html.Div(children=[
    html.H1(children='Patients with HTA'),
    html.Div(children='''patients number by age range having HTA'''),
    html.Div([
        dcc.Dropdown(
            id="Sexe",
            options=[{
                 'label': i,'value': i
            } for i in sexe],
                value='All sexe'),
        ],
        style={'width': '25%',
               'display': 'inline-block'}),
        dcc.Graph(id='graph-hta'),
     ])
@app.callback(
    dash.dependencies.Output('graph-hta', 'figure'),
    [dash.dependencies.Input('Sexe', 'value')])
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
