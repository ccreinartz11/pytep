import matlab.engine
import numpy as np
from pathlib import Path


import backend.engineutils as engineutils

class MatlabBridge:
    def __init__(self, model="MultiLoop_mode3"):
        self.model = model
        self.start_engine()
        simulator_dir = Path(__file__).parent / 'simulator'
        print(str(simulator_dir))
        self.eng.eval("addpath('{}')".format(str(simulator_dir)), nargout=0)
        self.load_simulink()
        self.eng.eval("load('InitVariables.mat')", nargout=0)
        return

    def start_engine(self):
        # Raises "EngineError" is Matlab can't be started
        # Implemented a check for this, to report it to the user
        self.eng = matlab.engine.start_matlab()

    def stop_engine(self):
        self.eng.quit()

    def load_simulink(self):
        self.eng.load_system(self.model)

    def run_simulink(self):
        self.eng.eval("sim('{}',tspan)".format(self.model), nargout=0)

    def save_workspace(self, name):
        self.eng.eval("save('{}')".format(name), nargout=0)
        print("Workspace has been saved to {}.mat".format(name))

    def get_process_vars(self):
        time = np.asarray(engineutils.get_variable(self.eng, 'tout'))
        process_vars = np.asarray(engineutils.get_variable(self.eng, 'simout'))
        simout = np.hstack((time, process_vars))
        return simout

