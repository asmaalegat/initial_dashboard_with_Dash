import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd

df = pd.read_excel("D:/dataset/outlier.xlsx")
print(df)
pv = pd.pivot_table(df, index=['Tranche'], columns=["HTA"], aggfunc='size', fill_value=0)
print(pv)
trace1 = go.Bar(x=pv.index, y=pv["g1"], name='grade1')
trace2 = go.Bar(x=pv.index, y=pv["g2"], name='grade2')
trace3 = go.Bar(x=pv.index, y=pv["g3"], name='grade3')
# trace4 = go.Bar(x=pv.index, y=pv[('Quantity', 'won')], name='Won')

app = dash.Dash()

app.layout = html.Div(children=[
    html.H1(children='Patients with HTA'),
    html.Div(children='''patients number by age range having HTA'''),
    dcc.Graph(
        id='example-graph',
        figure={
            'data': [trace1, trace2, trace3],
            'layout':
            go.Layout(title='patients number by age range having HTA', barmode='stack')
        })
])

if __name__ == '__main__':
    app.run_server(debug=True)