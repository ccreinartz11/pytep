import pandas as pd

import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import plotly.express as px

from app import app
from frontend.plotting import dummy_scatter

dummy_frame = pd.read_pickle('./frontend/dummy_frame.pkl')
dummy_labels = dummy_frame.columns.tolist()

main_plots_panel = html.Div(
    [
        dbc.Row(
            [
                dbc.Col([
                    dcc.Dropdown(options=[{'label': label, 'value': label} for label in dummy_labels],
                                 value=['time'],
                                 multi=False,
                                 clearable=False,
                                 id='dropdown_p1'),
                    dcc.Graph(figure={}, className="w-100 h-100", id="graph_p1")],
                    className="w-50 h-100",
                    id="main-plot-one",
                    style={"background-color": "blue", "border": "solid"},
                ),
                dbc.Col(
                    dcc.Graph(figure={}, className="w-100 h-100"),
                    className="w-50 h-100",
                    id="main-plot-two",
                    style={"background-color": "blue", "border": "solid"},
                ),
            ],
            className="h-25",
        ),
        dbc.Row(
            [
                dbc.Col(
                    dcc.Graph(figure={}, className="w-100 h-100"),
                    className="w-50 h-100",
                    id="main-plot-three",
                    style={"background-color": "blue", "border": "solid"},
                ),
                dbc.Col(
                    dcc.Graph(figure={}, className="w-100 h-100"),
                    className="w-50 h-100",
                    id="main-plot-four",
                    style={"background-color": "blue", "border": "solid"},
                ),
            ],
            className="h-25",
        ),
        dbc.Row(
            [
                dbc.Col(
                    dcc.Graph(figure={}, className="w-100 h-100"),
                    className="w-50 h-100",
                    id="main-plot-five",
                    style={"background-color": "blue", "border": "solid"},
                ),
                dbc.Col(
                    dcc.Graph(figure={}, className="w-100 h-100"),
                    className="w-50 h-100",
                    id="main-plot-six",
                    style={"background-color": "blue", "border": "solid"},
                ),
            ],
            className="h-25",
        ),
        dbc.Row(
            [
                dbc.Col(
                    dcc.Graph(figure={}, className="w-100 h-100"),
                    className="w-50 h-100",
                    id="main-plot-seven",
                    style={"background-color": "blue", "border": "solid"},
                ),
                dbc.Col(
                    dcc.Graph(figure={}, className="w-100 h-100"),
                    className="w-50 h-100",
                    id="main-plot-eight",
                    style={"background-color": "blue", "border": "solid"},
                ),
            ],
            className="h-25",
        ),
    ],
    id="main-plots-panel",
    className="h-100 w-100",
)


@app.callback(
    Output(component_id='graph_p1', component_property='figure'),
    Input(component_id='dropdown_p1', component_property='value')
)
def plot_on_p1(column_label):
    fig = px.scatter(x=dummy_frame['time'], y=dummy_frame[column_label])
    fig.update_layout(xaxis_title='time',
                      yaxis_title=column_label)
    fig.update_layout(autosize=True)
    return fig
