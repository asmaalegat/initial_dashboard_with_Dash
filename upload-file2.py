import base64
import datetime
import io

import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import dash_table

import pandas as pd


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    dcc.Upload(
        id='upload-data',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select Files')
        ]),
        style={
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        },
        # Allow multiple files to be uploaded
        multiple=True
    ),
    html.Div(id='output-data-upload'),
])


def parse_contents(contents, filename, date):
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')))
        elif 'xls' in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])

    return html.Div([
        html.H5(filename),
        html.H6(datetime.datetime.fromtimestamp(date)),

        dash_table.DataTable(
            data=df.to_dict('records'),
            columns=[{'name': i, 'id': i} for i in df.columns]
        ),

        html.Hr(),  # horizontal line

        # For debugging, display the raw contents provided by the web browser
        html.Div('Raw Content'),
        html.Pre(contents[0:200] + '...', style={
            'whiteSpace': 'pre-wrap',
            'wordBreak': 'break-all'
        })
    ])


@app.callback(Output('output-data-upload', 'children'),
              [Input('upload-data', 'contents')],
              [State('upload-data', 'filename'),
               State('upload-data', 'last_modified')])
def update_output(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        children = [
            parse_contents(c, n, d) for c, n, d in
            zip(list_of_contents, list_of_names, list_of_dates)]
        return children



if __name__ == '__main__':
    app.run_server(debug=True)


# *******************************************************************************************
import base64
import datetime
import io
import plotly.graph_objs as go
import cufflinks as cf

import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import dash_table

import pandas as pd

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

colors = {
	"graphBackground": "#F5F5F5",
	"background": "#ffffff",
	"text": "#000000"
}

app.layout = html.Div([
	dcc.Upload(
		id='upload-data',
		children=html.Div([
			'Drag and Drop or ',
			html.A('Select Files')
		]),
		style={
			'width': '100%',
			'height': '60px',
			'lineHeight': '60px',
			'borderWidth': '1px',
			'borderStyle': 'dashed',
			'borderRadius': '5px',
			'textAlign': 'center',
			'margin': '10px'
		},
	),
	dcc.Graph(id='Mygraph'),
	html.Div(id='output-data-upload')
])


@app.callback(Output('Mygraph', 'figure'), [
	Input('upload-data', 'contents'),
    Input('upload-data', 'filename')
])
def update_graph(contents, filename):
    x = []
    y = []
    if contents:
        contents = contents[0]
        filename = filename[0]
        df = parse_data(contents, filename)
        # df = df.set_index(df.columns[0])
        x=df['DATE']
        y=df['TMAX']
    fig = go.Figure(
        data=[ go.Scatter(x=x, y=y, mode='lines+markers')],
        layout=go.Layout(
            plot_bgcolor=colors["graphBackground"],
            paper_bgcolor=colors["graphBackground"]
        ))
    return fig

def parse_data(contents, filename):
	columns = contents.strip().split(',')
	if len(columns) == 2:
		content_type, content_string = contents.strip().split(',')
		decoded = base64.b64decode(content_string)
	else:
		print("Expected name and stats, got", columns)


	try:
		if 'csv' in filename:
			df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
		elif 'xls' in filename:
			df = pd.read_excel(io.BytesIO(decoded))
		elif 'txt' or 'tsv' in filename:
			df = pd.read_csv(io.StringIO(decoded.decode('utf-8')), delimiter=r'\s+')
	except Exception as e:
		print(e)
		return html.Div(['There was an error processing this file.'])
	return df


@app.callback(Output('output-data-upload', 'children'),
			  [Input('upload-data', 'contents'),
			   Input('upload-data', 'filename')
			   ])
def update_table(contents, filename):
	table = html.Div()
	if contents:
		contents = contents[0]
		filename = filename[0]
		df = parse_data(contents, filename)
		table = html.Div([
			html.H5(filename),
			dash_table.DataTable(
				data=df.to_dict('rows'),
				columns=[{'name': i, 'id': i} for i in df.columns]
			),
			html.Hr(),
			html.Div('Raw Content'),
			html.Pre(contents[0:200] + '...', style={
				'whiteSpace': 'pre-wrap',
				'wordBreak': 'break-all'
			})
		])
		return table


if __name__ == '__main__':
	app.run_server(debug=True)