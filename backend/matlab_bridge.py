import matlab.engine
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
        print('Starting simulation')
        self.eng.eval("sim('{}',[0 2])".format(self.model), nargout=0)
        print('Finished simulation.')

    def save_workspace(self, name):
        self.eng.eval("save('{}')".format(name), nargout=0)
        print("Workspace has been saved to {}.mat".format(name))

    def get_simulation_output(self):
        print('Getting sim output.')
        simout = engineutils.get_variable(self.eng, 'simout')
        print(simout)

