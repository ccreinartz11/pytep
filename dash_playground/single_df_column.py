import json

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px

import os
import pandas as pd

dir_path = os.path.dirname(os.path.realpath(__file__))
file_path = os.path.join(dir_path, "tep_data.pkl")
tep_data = pd.read_pickle(file_path)

fig = px.line(tep_data[0], title="sample figure", height=300)

app = dash.Dash(__name__)

app.layout = html.Div(
    [
        dcc.Graph(id="graph", figure=fig),
        dcc.Graph(id="graph2", figure=fig),
        html.Pre(
            id="structure",
            style={
                "border": "thin lightgrey solid",
                "overflowY": "scroll",
                "height": "200px",
            },
        ),
    ]
)


@app.callback(Output("structure", "children"), [Input("graph", "figure")])
def display_structure(fig_json):
    return json.dumps(fig_json, indent=2)


app.run_server(debug=True)
