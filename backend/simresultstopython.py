import matlab.engine
import numpy as np
import pandas as pd
from engineutils import get_workspace
from engineutils import set_variable


class MatlabBridge:
    def __init__(self):
        self.start_engine()

        # self.eng.eval("addpath('Simulator')", nargout=0)
        # print("Added path to simulator")
        # self.eng.eval("load('InitVariables.mat')", nargout=0)
        # print("Loaded InitVariables.mat")
        # self.load_simulink()
        # print("Loaded Simulink Model")
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
        self.eng.eval("sim('MultiLoop_mode3',tspan)", nargout=0)
        return 1

    def save_workspace(self, name):
        self.eng.eval("save('{}')".format(name), nargout=0)
        print("Workspace has been saved to {}.mat".format(name))


tep = MatlabBridge()
tep.eng.eval("load('dummy_simout.mat')", nargout=0)
sim_pv = np.asarray(tep.eng.eval("simout"))
sim_time = np.asarray(tep.eng.eval("tout"))
sim_out = pd.DataFrame(np.hstack([sim_time, sim_pv]))
pd.to_pickle(sim_out, "simout/pv_all.pkl")
print("Finished.")
