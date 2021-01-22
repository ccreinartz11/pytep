import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc

from frontend.plotting import dummy_scatter, middle_finger

main_plots_panel = html.Div([
    dbc.Row([
        dbc.Col([], id="main-plot-one"),
        dbc.Col([], id="main-plot-two")
    ], align="center", className="h-25"),
    dbc.Row([
        dbc.Col([], id="main-plot-three"),
        dbc.Col([], id="main-plot-four")
    ], className="h-25"),
    dbc.Row([
        dbc.Col([], id="main-plot-five"),
        dbc.Col([], id="main-plot-six")
    ], className="h-25"),
    dbc.Row([
        dbc.Col([], id="main-plot-seven"),
        dbc.Col([], id="main-plot-eight")
    ], className="h-25"),
], id="main-plots-panel", className="h=100")
