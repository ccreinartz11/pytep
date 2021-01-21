import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.CYBORG])  # TODO: Save css locally

row = html.Div(
    [
        dbc.Row(dbc.Col(html.Div("A single column"))),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Div("One of three columns"),
                        dbc.Button("Success")
                    ]
                ),
                dbc.Col(html.Div("One of three columns")),
                dbc.Col(html.Div("One of three columns")),
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Row(dbc.Col(html.Div("A single column"))),
                        dbc.Row(dbc.Col(html.Div("A single column"))),
                        dbc.Row(dbc.Col(html.Div("A single column")))
                    ],
                    width=4
                ),
                dbc.Col(
                    [
                        dbc.Row(dbc.Col(html.Div("A single column")))
                    ]
                )
            ]
        )
    ]
)

app.layout = row

app.run_server(debug=True)
