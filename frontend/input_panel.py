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
        dbc.Row(dbc.Col([
            html.Button("Run Simulation", id="b_runsim", type="submit", className='btn btn-primary'),
            html.Button("Stop Simulation", id="b_stopsim", type="submit", className='btn btn-primary'),
            html.Button("Add mvar", id="b_add_mvar", type="submit", className='btn btn-primary'),
            html.Button("Add fvar", id="b_add_fvar", type="submit", className='btn btn-primary'),
            dbc.Input(
                    id="sim_duration",
                    placeholder="Simulation duration",
                    type="text",
                    style={
                        "display": "inline-block",
                        },
                    className="form-control w-25",
                )
        ], className="w-100"), className="w-100"
        ),
        dbc.Row(dbc.Col([
            html.Div(
                id="container_mvar",
                children=[],
                className="w-100 overflow-auto"),
        ]), className="h-50 overflow-auto", style={"background-color":"green"}),
        dbc.Row(dbc.Col([
            html.Div(
                id="container_fvar",
                children=[],
                className='w-100 overflow-auto',
            ),
            html.Div(id="container_runsim", className="h-0"),
            html.Div(id="container_rem", className="h-0")
        ]), className="h-50 overflow-auto", style={"background-color":"yellow"})
    ],
    className="h-100 overflow-auto"
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
                        },
                        value=None,
                        clearable=False,
                        searchable=False,
                    ),  
                ],
                className="w-50"),
                
                dbc.Col([
                    html.Div("Hello")
                ],
                className="w-50"),
            ],
            style={"background-color": "blue"},
            no_gutters=True),
            dbc.Row([
                dbc.Col([
                    dcc.Dropdown(
                        id={"type": "m_io_dropdown", "index": n_clicks},
                        options=[{"label": x, "value": x} for x in io_type],
                        style={
                            "display": "inline-block",
                            "width": "100%"
                        },
                        value=None,
                        clearable=False,
                        searchable=False,
                        
                    )],
                    className="w-30"
                    ),
                dbc.Col([
                    dbc.Input(
                        id={"type": "m_mag", "index": n_clicks},
                        style={
                            "display": "inline-block",
                            "width": "100%",
                            "margin-top": "0px",
                            "vertical-align": "top"
                        },
                        placeholder="Magnitude",
                        type="text",
                    )],
                    className="w-30",
                    ),
                dbc.Col([
                    dbc.Input(
                        id={"type": "m_duration", "index": n_clicks},
                        style={
                            "display": "inline-block",
                            "width": "100%",
                            "margin-top": "0px",
                            "vertical-align": "top"
                        },
                        placeholder="Duration",
                        type="text",
                        disabled=False,
                    )],
                    className="w-30",
                    ),
                dbc.Col([
                    html.Button(
                        "X", 
                        id={"type": "b_remove_mvar", "index": n_clicks}, 
                        style={
                            "width": "100%"
                        },
                        type="submit",
                    )],
                    className="w-10",
                    )],
                    style={"background-color": "red"},no_gutters=True),
                ], className="h-100")
        childdiv.append(new_mvar)

    if "b_remove_mvar" in triggered_id:
        idx = (triggered_id.partition(",")[0])[9:]
        for i, e in enumerate(childdiv):
            if e["props"]["id"] == idx:
                del childdiv[int(i)]
                continue

    return childdiv

@app.callback(
    Output("container_fvar", "children"),
    [
        Input("b_add_fvar", "n_clicks"),
        Input(
            component_id={"type": "b_remove_fvar", "index": ALL},
            component_property="n_clicks",
        ),
    ],
    [State("container_fvar", "children")],
    prevent_initial_call=True,
)
def add_fvar_row(n_clicks, n_clicks2, childdiv):

    ctx = dash.callback_context
    triggered_id = ctx.triggered[0]["prop_id"].split(".")[0]
    print(triggered_id)

    if triggered_id == "b_add_fvar":
        new_mvar = html.Div(
            id=str(n_clicks),
            children=[
            dbc.Row([
                dbc.Col([
                    dcc.Dropdown(
                        id={"type": "f_dropdown", "index": n_clicks},
                        options=[{"label": x, "value": x} for x in f_vars],
                        style={
                            "display": "inline-block",
                            "width": "100%"
                        },
                        value=None,
                        clearable=False,
                        searchable=False,
                        
                    )],
                    className="w-30"
                    ),
                dbc.Col([
                    dbc.Input(
                        id={"type": "f_mag", "index": n_clicks},
                        style={
                            "display": "inline-block",
                            "width": "100%",
                            "margin-top": "0px",
                            "vertical-align": "top"
                        },
                        placeholder="Magnitude",
                        type="text",
                    )],
                    className="w-30",
                    ),
                dbc.Col([
                    html.Button(
                        "X", 
                        id={"type": "b_remove_fvar", "index": n_clicks}, 
                        style={
                            "width": "100%"
                        },
                        type="submit",
                    )],
                    className="w-10",
                    )],
                    style={"background-color": "red"},no_gutters=True),
                ], className="h-100")
        childdiv.append(new_mvar)

    if "b_remove_fvar" in triggered_id:
        idx = (triggered_id.partition(",")[0])[9:]
        for i, e in enumerate(childdiv):
            if e["props"]["id"] == idx:
                del childdiv[int(i)]
                continue

    return childdiv


@app.callback(
    [Output({"index": MATCH, "type": "m_duration"}, "disabled"),
    Output({"index": MATCH, "type": "m_duration"}, "value")],
    Input({"index": MATCH, "type": "m_io_dropdown"}, "value"),
    State({"index": MATCH, "type": "m_duration"}, "value"),
)
def disable_box(step, val):
    dis = True if step == "Step" else False
    val = None if step == "Step" else val

    return dis, val

@app.callback(
    Output("container_runsim", "children"),
    [Input("b_runsim", "n_clicks")],
    state=[
        State(component_id="sim_duration", component_property="value"),
        State(component_id={"type": "m_dropdown", "index": ALL}, component_property="value"),
        State(component_id={"type": "m_io_dropdown", "index": ALL}, component_property="value"),
        State(component_id={"type": "m_duration", "index": ALL}, component_property="value"),
        State(component_id={"type": "m_mag", "index": ALL}, component_property="value"),
        State(component_id={"type": "f_dropdown", "index": ALL}, component_property="value"),
        State(component_id={"type": "f_mag", "index": ALL}, component_property="value"),
    ],
)
def run_simulation(n_clicks, sim_duration, m_dd, m_type, m_dur, m_mag, f_dd, f_mag):
    if n_clicks is not None:
        print("Run simulation pressed")
        print("With the following arguments:")
        print(sim_duration)
        print(m_dd)
        print(m_type)
        print(m_mag)
        print(m_dur)
        print("And the following faults:")
        print(f_dd)
        print(f_mag)
        
        #siminterface.simulate()
        #siminterface.update()


