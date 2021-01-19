import json

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px

import os
import pandas as pd

dir_path = os.path.dirname(os.path.realpath(__file__))
file_path = os.path.join(dir_path, 'tep_data.pkl')
tep_data = pd.read_pickle(file_path)

fig = px.line(
    tep_data[0],
    title="sample figure", height=300
)
#
# app = dash.Dash()
#
# app.layout = html.Div([
#     html.Div([
#         html.Div([
#             html.H3('Column 1'),
#             dcc.Graph(id='g1', figure=fig)
#         ], className="six columns"),
#
#         html.Div([
#             html.H3('Column 2'),
#             dcc.Graph(id='g2', figure=fig)
#         ], className="six columns"),
#     ], className="row")
# ])

app = dash.Dash()
app.layout = html.Div([
    html.Div([
        html.Div([
            html.H3('Column 1'),
            dcc.Graph(id='g1', figure={'data': [{'y': [1, 2, 3]}]})
        ], className="six columns"),

        html.Div([
            html.H3('Column 2'),
            dcc.Graph(id='g2', figure={'data': [{'y': [1, 2, 3]}]})
        ], className="six columns"),
    ], className="row")
])

app.css.config.serve_locally = False
app.css.append_css({
    'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'
})

if __name__ == '__main__':
    app.run_server(debug=True)

