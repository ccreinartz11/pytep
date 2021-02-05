"""Functions that simplify the interaction with the matlab engine in python"""


def get_workspace(engine):
    return engine.workspace


def set_variable(engine, var, val):
    engine.workspace[var] = val


def get_variable(engine, var):
    return engine.workspace[var]
