import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc

from frontend.plotting import dummy_scatter, middle_finger

main_plots_panel = html.Div([
    dbc.Row([
        dbc.Col(dcc.Graph(figure=dummy_scatter, className="w-100 h-100"), className="w-50 h-100", id="main-plot-one", style={"background-color": "blue", "border": "solid"}),
        dbc.Col(dcc.Graph(figure=dummy_scatter, className="w-100 h-100"), className="w-50 h-100", id="main-plot-two", style={"background-color": "blue", "border": "solid"})
    ], className="h-25"),
    dbc.Row([
        dbc.Col(dcc.Graph(figure=dummy_scatter, className="w-100 h-100"), className="w-50 h-100", id="main-plot-three", style={"background-color": "blue", "border": "solid"}),
        dbc.Col(dcc.Graph(figure=dummy_scatter, className="w-100 h-100"), className="w-50 h-100", id="main-plot-four", style={"background-color": "blue", "border": "solid"})
    ], className="h-25"),
    dbc.Row([
        dbc.Col(dcc.Graph(figure=dummy_scatter, className="w-100 h-100"), className="w-50 h-100", id="main-plot-five", style={"background-color": "blue", "border": "solid"}),
        dbc.Col(dcc.Graph(figure=dummy_scatter, className="w-100 h-100"), className="w-50 h-100", id="main-plot-six", style={"background-color": "blue", "border": "solid"})
    ], className="h-25"),
    dbc.Row([
        dbc.Col(dcc.Graph(figure=dummy_scatter, className="w-100 h-100"), className="w-50 h-100", id="main-plot-seven", style={"background-color": "blue", "border": "solid"}),
        dbc.Col(dcc.Graph(figure=dummy_scatter, className="w-100 h-100"), className="w-50 h-100", id="main-plot-eight", style={"background-color": "blue", "border": "solid"})
    ], className="h-25"),
], id="main-plots-panel", className="h-100 w-100")
#
# main_plots_panel = html.Div([
#     dbc.Row([
#         dbc.Col([], className="w-50 h-100", id="main-plot-one", style={"background-color": "blue", "border": "solid"}),
#         dbc.Col([], className="w-50 h-100", id="main-plot-two", style={"background-color": "blue", "border": "solid"})
#     ], className="h-25"),
#     dbc.Row([
#         dbc.Col([], className="w-50 h-100", id="main-plot-three", style={"background-color": "blue", "border": "solid"}),
#         dbc.Col([], className="w-50 h-100", id="main-plot-four", style={"background-color": "blue", "border": "solid"})
#     ], className="h-25"),
#     dbc.Row([
#         dbc.Col([], className="w-50 h-100", id="main-plot-five", style={"background-color": "blue", "border": "solid"}),
#         dbc.Col([], className="w-50 h-100", id="main-plot-six", style={"background-color": "blue", "border": "solid"})
#     ], className="h-25"),
#     dbc.Row([
#         dbc.Col([], className="w-50 h-100", id="main-plot-seven", style={"background-color": "blue", "border": "solid"}),
#         dbc.Col([], className="w-50 h-100", id="main-plot-eight", style={"background-color": "blue", "border": "solid"})
#     ], className="h-25"),
# ], id="main-plots-panel", className="h-100 w-100")