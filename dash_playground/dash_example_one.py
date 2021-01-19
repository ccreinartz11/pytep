"""Imported dash example from https://plotly.com/python/creating-and-updating-figures/"""

import json

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px

fig = px.line(
    x=["a","b","c"], y=[1,3,2],
    title="sample figure", height=325
)

app = dash.Dash(__name__)

app.layout = html.Div([
    dcc.Graph(id="graph", figure=fig),
    html.Pre(
        id='structure',
        style={
            'border': 'thin lightgrey solid',
            'overflowY': 'scroll',
            'height': '275px'
        }
    )
])

@app.callback(
    Output("structure", "children"),
    [Input("graph", "figure")])
def display_structure(fig_json):
    return json.dumps(fig_json, indent=2)

app.run_server(debug=True)