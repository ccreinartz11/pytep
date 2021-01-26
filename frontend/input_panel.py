import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output, ALL, State, MATCH, ALLSMALLER
from app import app

f_vars = ["f1", "f2", "f3", "f4"]
m_vars = ["m1", "m2", "m3", "m4"] + f_vars

input_panel = html.Div(
    [
        html.Div(
            children=[
                html.Button("Run Simulation", id="b_runsim", type="submit"),
                html.Button("Add mvar", id="b_add_mvar", type="submit"),
            ]
        ),
        html.Div(
            id="container_mvar",
            children=[],
            className='w-100 h-100',
        ),
        html.Div(id="container_runsim"),
        html.Div(id="container_rem")
        # html.Div(id='container_fvar', children=[], style=dict(width='33%',background="red")),
    ]
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
            style={},
            children=[
                html.Div(
                    id={"type": "outputblob", "index": n_clicks},
                ),
                dcc.Dropdown(
                    id={"type": "m_dropdown", "index": n_clicks},
                    options=[{"label": x, "value": x} for x in m_vars],
                    style={
                        "width": "10%",
                        "display": "inline-block",
                        "min-width": "100px",
                    },
                    value=None,
                    clearable=False,
                ),
                dcc.Input(
                    id={"type": "m_start", "index": n_clicks},
                    style={"width": "10%"},
                    value="Start",
                    type="text",
                ),
                dcc.Input(
                    id={"type": "m_stop", "index": n_clicks},
                    style={"width": "10%"},
                    value="Stop",
                    type="text",
                ),
                dcc.Input(
                    id={"type": "m_mag", "index": n_clicks},
                    style={"width": "10%"},
                    value="Magnitude",
                    type="text",
                ),
                # html.Button('X', id='b_remove_mvar', type='submit'),
                html.Button(
                    "X", id={"type": "b_remove_mvar", "index": n_clicks}, type="submit"
                ),
            ],
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
        State(component_id={"type": "m_mag", "index": ALL}, component_property="value"),
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


