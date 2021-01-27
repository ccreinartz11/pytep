"""Functions that simplify the interaction with the matlab engine in python"""


def get_workspace(engine):
    engine.evalc("C = who;")
    var_names = engine.workspace["C"]
    workspace = {v: engine.workspace[v] for v in var_names}
    return workspace


def set_variable(engine, var, val):
    engine.workspace[var] = val


def get_variable(engine, var):
    return engine.workspace[var]
