import matlab.engine
from backend.engineutils import get_workspace
from backend.engineutils import set_variable

from pathlib import Path


class MatlabBridge:
    def __init__(self, model="MultiLoop_mode3"):
        self.model = model
        self.start_engine()
        simulator_dir = Path(__file__).parent.parent / 'simulator'
        self.eng.eval("addpath('{}')".format(str(simulator_dir)), nargout=0)
        # self.eng.eval("addpath('../simulator')", nargout=0)
        print("Added path to simulator")
        self.eng.eval("load('InitVariables.mat')", nargout=0)
        print("Loaded InitVariables.mat")
        self.load_simulink()
        print("Loaded Simulink Model")
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

# set_variable(tep.eng, 'tspan', matlab.double([0,1]))
tep.run_simulink()
tep.eng.saveSimulationState(nargout=0)
tep.eng.prepareSimulation(nargout=0)
tep.run_simulink()
tep.save_workspace("dummy_simout.mat")

