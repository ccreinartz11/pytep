import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc

from frontend.main_plots_panel import main_plots_panel
from frontend.plotting import three_subplots

input_panel = html.Div("Input panel", id="input-panel")

# fixed_plots_panel = html.Div([
#     dcc.Graph(id="fixed-plots", figure=three_subplots),
# ], id="fixed-plots-panel")

fixed_plots_panel = html.Div("Fixed plots here.")

mainpage = html.Div([
    dbc.Row([
        dbc.Col([
            dbc.Row(dbc.Col(input_panel), className="h-50", style={"background-color": "grey"}),
            dbc.Row(dbc.Col(fixed_plots_panel), className="h-50", style={"background-color": "black"})
        ], width=4, id="left-column"),
        dbc.Col(main_plots_panel, width=8, className="h-100", id="right-column", style={"background-color": "blue"})
    ], className="h-100")
], className="full-page-box"
)

