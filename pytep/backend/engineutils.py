"""Functions that simplify the interaction with the matlab engine in python"""


def get_workspace(engine):
    """Gets and returns the MATLAB workspace

    Parameters
    ----------
    engine : MATLAB engine
        A MATLAB engine object

    Returns
    -------
    Dictionary
        Dictionary containing key-value pairs for each variable and its value from the MATLAB workspace
    """
    return engine.workspace


def set_variable(engine, var, val):
    """Sets a MATLAB workspace variable from Python

    Parameters
    ----------
    engine : MATLAB engine
        A MATLAB engine object
    var : string
        string containing the variable name to set in the workspace
    val : np.floats, np.arrays
        1d arrays are set as vectors.
        2d arrays are set as matrices.
    """
    engine.workspace[var] = val


def get_variable(engine, var):
    """Gets a workspace variable from the MATLAB workspace to Python.

    Parameters
    ----------
    engine : MATLAB engine
        A MATLAB engine object
    var : string
        string containing the variable name to get from the workspace

    Returns
    -------
    np.floats, np.arrays
        Numeric primitives are returned as np.floats.
        Vectors are returned as np.arrays.
        Matrices are returned as np.arrays.
    """
    return engine.workspace[var]
