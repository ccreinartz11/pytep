import plotly.graph_objects as go
from plotly.subplots import make_subplots

import dash
import dash_core_components as dcc
import dash_html_components as html


fig = make_subplots(rows=4, cols=2, start_cell="bottom-left")

fig.add_trace(go.Scatter(x=[1, 2, 3], y=[4, 5, 6]), row=1, col=1)

fig.add_trace(go.Scatter(x=[20, 30, 40], y=[50, 60, 70]), row=1, col=2)

fig.add_trace(go.Scatter(x=[300, 400, 500], y=[600, 700, 800]), row=2, col=1)

fig.add_trace(go.Scatter(x=[4000, 5000, 6000], y=[7000, 8000, 9000]), row=2, col=2)

fig.add_trace(go.Scatter(x=[1, 2, 3], y=[4, 5, 6]), row=3, col=1)

fig.add_trace(go.Scatter(x=[20, 30, 40], y=[50, 60, 70]), row=3, col=2)

fig.add_trace(go.Scatter(x=[300, 400, 500], y=[600, 700, 800]), row=4, col=1)

fig.add_trace(go.Scatter(x=[4000, 5000, 6000], y=[7000, 8000, 9000]), row=4, col=2)

app = dash.Dash(__name__)

app.layout = html.Div(
    [
        dcc.Graph(id="graph", figure=fig),
        html.Pre(
            id="structure",
            style={
                "border": "thin lightgrey solid",
                "overflowY": "scroll",
                "height": "400px",
            },
        ),
    ]
)

app.run_server(debug=True)
