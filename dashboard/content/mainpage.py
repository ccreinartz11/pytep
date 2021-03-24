import dash_html_components as html
import dash_bootstrap_components as dbc

from dashboard.content.main_plots_panel import main_plots_panel
from dashboard.content.input_panel import input_panel
from dashboard.content.cost_plot_panel import cost_plot_panel

mainpage = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Row(
                            dbc.Col(input_panel),
                            className="h-75",
                            style={"box-sizing": "border-box"},
                        ),
                        dbc.Row(
                            dbc.Col(cost_plot_panel),
                            className="h-25",
                            style={"background-color": "black"},
                        ),
                    ],
                    width=4,
                    className="h-100",
                    id="left-column"
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

