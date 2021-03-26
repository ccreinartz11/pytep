import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import plotly.express as px

from dashboard.app import app

import pytep.siminterface as simulation_interface
siminterface = simulation_interface.SimInterface()

main_plots_panel = html.Div(
    [
        dbc.Row(
            [
                dbc.Col([
                    dcc.Dropdown(options=[{'label': label, 'value': label} for label in siminterface.process_data_labels()],
                                 value='time',
                                 multi=False,
                                 clearable=False,
                                 id='dropdown_p1'),
                    dcc.Graph(figure={}, className="graph-height", id="graph_p1")],
                    className="w-50 h-100",
                    id="main-plot-one",
                    style={"background-color": "blue", "border": "solid"},
                ),
                dbc.Col([
                    dcc.Dropdown(options=[{'label': label, 'value': label} for label in siminterface.process_data_labels()],
                                 value='time',
                                 multi=False,
                                 clearable=False,
                                 id='dropdown_p2'),
                    dcc.Graph(figure={}, className="graph-height", id="graph_p2")],
                    className="w-50 h-100",
                    id="main-plot-two",
                    style={"background-color": "blue", "border": "solid"}
                )
            ],
            className="graph-container",
            no_gutters=True,
        ),
        dbc.Row(
            [
                dbc.Col([
                    dcc.Dropdown(options=[{'label': label, 'value': label} for label in siminterface.process_data_labels()],
                                 value='time',
                                 multi=False,
                                 clearable=False,
                                 id='dropdown_p3'),
                    dcc.Graph(figure={}, className="graph-height", id="graph_p3")],
                    className="w-50 h-100",
                    id="main-plot-three",
                    style={"background-color": "blue", "border": "solid"}
                ),
                dbc.Col([
                    dcc.Dropdown(options=[{'label': label, 'value': label} for label in siminterface.process_data_labels()],
                                 value='time',
                                 multi=False,
                                 clearable=False,
                                 id='dropdown_p4'),
                    dcc.Graph(figure={}, className="graph-height", id="graph_p4")],
                    className="w-50 h-100",
                    id="main-plot-four",
                    style={"background-color": "blue", "border": "solid"}
                )
            ],
            className="graph-container",
            no_gutters=True,
        ),        dbc.Row(
            [
                dbc.Col([
                    dcc.Dropdown(options=[{'label': label, 'value': label} for label in siminterface.process_data_labels()],
                                 value='time',
                                 multi=False,
                                 clearable=False,
                                 id='dropdown_p5'),
                    dcc.Graph(figure={}, className="graph-height", id="graph_p5")],
                    className="w-50 h-100",
                    id="main-plot-five",
                    style={"background-color": "blue", "border": "solid"}
                ),
                dbc.Col([
                    dcc.Dropdown(options=[{'label': label, 'value': label} for label in siminterface.process_data_labels()],
                                 value='time',
                                 multi=False,
                                 clearable=False,
                                 id='dropdown_p6'),
                    dcc.Graph(figure={}, className="graph-height", id="graph_p6")],
                    className="w-50 h-100",
                    id="main-plot-six",
                    style={"background-color": "blue", "border": "solid"}
                )
            ],
            className="graph-container",
            no_gutters=True,
        ),        dbc.Row(
            [
                dbc.Col([
                    dcc.Dropdown(options=[{'label': label, 'value': label} for label in siminterface.process_data_labels()],
                                 value='time',
                                 multi=False,
                                 clearable=False,
                                 id='dropdown_p7'),
                    dcc.Graph(figure={}, className="graph-height", id="graph_p7")],
                    className="w-50 h-100",
                    id="main-plot-seven",
                    style={"background-color": "blue", "border": "solid"}
                ),
                dbc.Col([
                    dcc.Dropdown(options=[{'label': label, 'value': label} for label in siminterface.process_data_labels()],
                                 value='time',
                                 multi=False,
                                 clearable=False,
                                 id='dropdown_p8'),
                    dcc.Graph(figure={}, className="graph-height", id="graph_p8")],
                    className="w-50 h-100",
                    id="main-plot-eight",
                    style={"background-color": "blue", "border": "solid"}
                )
            ],
            className="graph-container",
            no_gutters=True,
        ),
    ],
    id="main-plots-panel",
    className="h-100 w-100",
)


@app.callback(
    Output(component_id='graph_p1', component_property='figure'),
    Input(component_id='dropdown_p1', component_property='value')
)
def plot_on_p1(col_label):
    return line(col_label)


@app.callback(
    Output(component_id='graph_p2', component_property='figure'),
    Input(component_id='dropdown_p2', component_property='value')
)
def plot_on_p1(col_label):
    return line(col_label)

@app.callback(
    Output(component_id='graph_p3', component_property='figure'),
    Input(component_id='dropdown_p3', component_property='value')
)
def plot_on_p1(col_label):
    return line(col_label)

@app.callback(
    Output(component_id='graph_p4', component_property='figure'),
    Input(component_id='dropdown_p4', component_property='value')
)
def plot_on_p1(col_label):
    return line(col_label)


@app.callback(
    Output(component_id='graph_p5', component_property='figure'),
    Input(component_id='dropdown_p5', component_property='value')
)
def plot_on_p1(col_label):
    return line(col_label)


@app.callback(
    Output(component_id='graph_p6', component_property='figure'),
    Input(component_id='dropdown_p6', component_property='value')
)
def plot_on_p1(col_label):
    return line(col_label)


@app.callback(
    Output(component_id='graph_p7', component_property='figure'),
    Input(component_id='dropdown_p7', component_property='value')
)
def plot_on_p1(col_label):
    return line(col_label)


@app.callback(
    Output(component_id='graph_p8', component_property='figure'),
    Input(component_id='dropdown_p8', component_property='value')
)
def plot_on_p1(col_label):
    return line(col_label)


def scatter(col_label):
    data = siminterface.timed_var(col_label)
    col_unit = siminterface.get_var_unit(col_label)
    fig = px.scatter(x=data['time'], y=data[col_label])
    fig.update_layout(xaxis_title='time',
                      yaxis_title=col_unit,
                      margin={"t": 5})
    fig.update_layout(autosize=True)
    return fig


def line(col_label):
    data = siminterface.timed_var(col_label)
    col_unit = siminterface.get_var_unit(col_label)
    fig = px.line(x=data['time'], y=data[col_label])
    fig.update_layout(xaxis_title='time',
                      yaxis_title=col_unit,
                      margin={"t": 15,
                              "b": 15})
    fig.update_layout(autosize=True)
    return fig