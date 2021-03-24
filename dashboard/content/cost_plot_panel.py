import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

from dashboard.app import app

import pytep.siminterface as simulation_interface
siminterface = simulation_interface.SimInterface()

cost_plot_panel = html.Div(
    [
        dcc.Dropdown(options=[{'label': 'Operating Cost', 'value': 'cost'}],
                     value='cost',
                     multi=False,
                     clearable=False,
                     id='dropdown_cost'),
        dcc.Graph(figure={}, className="w-100 h-75", id="graph_cost_panel")
    ],
    id="cost-plot-panel",
    className="w-100 h-100",
)


@app.callback(
    Output(component_id='cost-plot-panel', component_property='figure'),
    Input(component_id='dropdown_cost', component_property='value')
)
def plot_cost(dropdown_label):
    time = siminterface.timed_var("time")
    data = siminterface.operating_cost()
    col_unit = "$ per h"
    fig = px.line(x=time['time'], y=data["cost"])
    fig.update_layout(
        xaxis_title='time',
        yaxis_title=col_unit
        )
    fig.update_layout(autosize=True)
    return fig
