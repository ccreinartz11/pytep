import numpy as np

import pytep.matlab_bridge as matlab_bridge


bridge = matlab_bridge.MatlabBridge()


def test_passing_float():
    b = bridge
    b.set_workspace_variable('nine', 9.0)
    var = b.get_workspace_variable('nine')
    assert isinstance(var, np.float)
    assert var == 9.0


def test_passing_1d_array():
    b = bridge
    vector = np.asarray([1, 2, 3])
    b.set_workspace_variable('vector', vector)
    var = b.get_workspace_variable('vector')
    assert isinstance(var, np.ndarray)
    assert (var == vector).all()


def test_passing_2d_array():
    b = bridge
    vector = np.asarray([[1, 2, 3], [4, 5, 6]])
    b.set_workspace_variable('vector', vector)
    var = b.get_workspace_variable('vector')
    assert isinstance(var, np.ndarray)
    assert (var == vector).all()
    
    
def test_setpoint_change():
    b = bridge
    b.set_production_sp(after=24, duration=5, start_time=5)
    b.set_simpause_time(15)
    b.run_until_paused()
    setpoints = b.get_workspace_variable('setpoints')
    assert setpoints[-1, 0] == 24


