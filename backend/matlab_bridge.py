import matlab
import matlab.engine
import numpy as np
from pathlib import Path


import backend.engineutils as engineutils


class MatlabBridge:
    def __init__(self, model="MultiLoop_mode3", sim_path=None):
        self._model = model
        self._sim_path = Path(__file__).parent / 'simulator' if sim_path is None else sim_path
        self._eng = matlab.engine.start_matlab()
        self.dir_to_path(self._sim_path)
        self._load_simulink()
        self._load_workspace()
        return

    def start_engine(self):
        self._eng = matlab.engine.start_matlab()
        return True

    def stop_engine(self):
        self._eng.quit()

    def load_simulink(self):
        self._eng.load_system(self._model)

    def dir_to_path(self, dir_path):
        self._eng.eval("addpath('{}')".format(str(dir_path)), nargout=0)

    def _load_workspace(self):
        self._eng.eval("load('InitVariables.mat')", nargout=0)

    def run_simulink(self):
        self._eng.eval("sim('{}',tspan)".format(self._model), nargout=0)

    def save_workspace(self, name):
        self._eng.eval("save('{}')".format(name), nargout=0)

    def get_workspace_variable(self, name):
        """Fetches workspace variable from matlab workspace to python.
        Numeric primitives are returned as np.floats.
        Vectors are returned as np.arrays.
        Matrices are returned as np.arrays.
        """
        var = engineutils.get_variable(self._eng, name)
        if isinstance(var, float):
            var = np.float64(var)
        elif isinstance(var, list):
            var = np.asarray(var)
        return var

    def set_workspace_variable(self, name, value):
        """Sets matlab workspace variable from python.
        1d arrays are set as vectors.
        2d arrays are set as matrices.
        """
        if isinstance(value, np.ndarray):
            var = value.tolist()
        else:
            var = value
        engineutils.set_variable(self._eng, name, var)

    # TODO: Belongs in Siminterface
    def get_process_vars(self):
        time = np.asarray(engineutils.get_variable(self._eng, 'tout'))
        process_vars = np.asarray(engineutils.get_variable(self._eng, 'simout'))
        simout = np.hstack((time, process_vars))
        return simout

    def prep_next_iteration(self):
        self._eng.prepNextSimIteration(nargout=0)

    def _load_simulink(self):
        pass

