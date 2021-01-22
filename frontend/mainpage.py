import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc

from frontend.plotting import eight_subplots, three_subplots

input_panel = html.Div("Input panel", id="input-panel")

fixed_plots_panel = main_plots_panel = html.Div([
    dcc.Graph(id="main-plots", figure=three_subplots),
], id="fixed-plots-panel")

main_plots_panel = html.Div([
    dcc.Graph(id="fixed-plots", figure=eight_subplots),
], id="main-plots-panel")

mainpage = html.Div([
    dbc.Row([
        dbc.Col([
            dbc.Row(dbc.Col(input_panel), className="h-50"),
            dbc.Row(dbc.Col(fixed_plots_panel), className="h-50")
        ], width=4, id="left-column", className="h-100"),
        dbc.Col(main_plots_panel, width=8, className="h-100", id="right-column")
    ], className="full-page-box")
]
)

