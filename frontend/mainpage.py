import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc

from frontend.main_plots_panel import main_plots_panel
from frontend.input_panel import input_panel

fixed_plots_panel = html.Div("Fixed plots here.")

mainpage = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Row(
                            dbc.Col(input_panel),
                            className="h-50 overflow-auto",
                            style={"box-sizing": "border-box"},
                        ),
                        dbc.Row(
                            dbc.Col(fixed_plots_panel),
                            className="h-50 overflow-auto",
                        ),
                    ],
                    className="h-100 overflow-auto",
                    width=4,
                    id="left-column",
                ),
                dbc.Col(
                    main_plots_panel,
                    width=8,
                    className="h-100",
                    id="right-column",
                    style={"background-color": "blue"},
                ),
            ],
            className="h-100",
            no_gutters=True,
        )
    ],
    className="full-page-box no-overflow",
)

