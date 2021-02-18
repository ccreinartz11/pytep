import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output, ALL, State, MATCH, ALLSMALLER
from app import app

import backend.siminterface as simulation_interface
siminterface = simulation_interface.SimInterface()

f_vars = ["f1", "f2", "f3", "f4"]
m_vars = ["m1", "m2", "m3", "m4"]
io_type = ["Step", "Ramp"]

input_panel = html.Div(
    [
        html.Div(
            children=[
                html.Button("Run Simulation", id="b_runsim", type="submit", className='btn btn-primary'),
                html.Button("Add mvar", id="b_add_mvar", type="submit"),
                html.Button("Add fvar", id="b_add_fvar", type="submit"),
            ]
        ),
        html.Div(
            id="container_mvar",
            children=[],
            #className='w-100 h-100',
        ),
        html.Div(
            id="container_fvar",
            children=[],
            className='w-100 h-100',
        ),
        html.Div(id="container_runsim"),
        html.Div(id="container_rem")
    ], className="fitted-image"
)


@app.callback(
    Output("container_mvar", "children"),
    [
        Input("b_add_mvar", "n_clicks"),
        Input(
            component_id={"type": "b_remove_mvar", "index": ALL},
            component_property="n_clicks",
        ),
    ],
    [State("container_mvar", "children")],
    prevent_initial_call=True,
)
def add_mvar_row(n_clicks, n_clicks2, childdiv):

    ctx = dash.callback_context
    triggered_id = ctx.triggered[0]["prop_id"].split(".")[0]
    print(triggered_id)

    if triggered_id == "b_add_mvar":
        new_mvar = html.Div(
            id=str(n_clicks),
            children=[
            dbc.Row([
                dbc.Col([
                    dcc.Dropdown(
                        id={"type": "m_dropdown", "index": n_clicks},
                        options=[{"label": x, "value": x} for x in m_vars],
                        style={
                            "width": "100%",
                            "display": "inline-block",
                            "min-width": "100px",
                        },
                        value=None,
                        clearable=False,
                        searchable=False,
                    ),  
                ],
                width=2),
                dbc.Col([
                    html.Div("Hello")
                ],
                width=2)
            ],
            style={"background-color": "blue"}),
            dbc.Row([
                dbc.Col([
                    dcc.Dropdown(
                        id={"type": "m_io_dropdown", "index": n_clicks},
                        options=[{"label": x, "value": x} for x in io_type],
                        style={
                            "display": "inline-block",
                            "min-width": "100px",
                            "margin-bottom": "-5px",
                        },
                        value=None,
                        clearable=False,
                    ),
                    dbc.Input(
                        id={"type": "m_mag", "index": n_clicks},
                        style={
                            "display": "inline-block",
                            "width": "100px",
                            "margin-top": "0px",
                            "vertical-align": "top"
                        },
                        placeholder="Magnitude",
                        type="text",
                    ),
                    dbc.Input(
                        id={"type": "m_stop", "index": n_clicks},
                        style={
                            "display": "inline-block",
                            "width": "100px",
                            "margin-top": "0px",
                            "vertical-align": "top"
                        },
                        placeholder="Duration",
                        type="text",
                        disabled=False,
                    ),
                    html.Button(
                        "X", id={"type": "b_remove_mvar", "index": n_clicks}, type="submit"
                    ),
                ])
            ], style={"background-color": "red"})
            ]
        )
        childdiv.append(new_mvar)

    if "b_remove_mvar" in triggered_id:
        idx = (triggered_id.partition(",")[0])[9:]
        for i, e in enumerate(childdiv):
            if e["props"]["id"] == idx:
                del childdiv[int(i)]
                continue

    return childdiv


@app.callback(
    Output({"index": MATCH, "type": "m_mag"}, "disabled"),
    Input({"index": MATCH, "type": "m_io_dropdown"}, "value")
)
def disable_box(step):
    return True if step == "Step" else False

@app.callback(
    Output("container_runsim", "children"),
    [Input("b_runsim", "n_clicks")],
    state=[
        State(
            component_id={"type": "m_dropdown", "index": ALL},
            component_property="value",
        ),
        State(
            component_id={"type": "m_start", "index": ALL}, component_property="value"
        ),
        State(
            component_id={"type": "m_stop", "index": ALL}, component_property="value"
        ),
        State(
            component_id={"type": "m_mag", "index": ALL}, component_property="value"
        ),
    ],
)
def run_simulation(n_clicks, v_dropdown, v_tb_start, v_tb_stop, v_tb_mag):
    if n_clicks is not None:
        print("Run simulation pressed")
        print("With the following arguments:")
        print(v_dropdown)
        print(v_tb_start)
        print(v_tb_stop)
        print(v_tb_mag)
        siminterface.extend_simulation()
        siminterface.simulate()
        siminterface.update()


