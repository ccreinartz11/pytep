import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

app = dash.Dash(__name__)

row = dbc.Container(
        dbc.Row(
            [
                dbc.Col(html.Div("Left column"), width=4),
                dbc.Col(html.Div("Right column"), width=8)
            ]
        )
)

app.layout = row

app.run_server(debug=True)
