import matlab.engine


class MatlabBridge:

    def __init__(self, model="hi"):
        self.model = model
        self.startEngine()

        
        self.eng.eval("addpath('Simulator')", nargout=0)
        print("Added path to simulator")
        self.eng.eval("load('InitVariables.mat')", nargout=0)
        print("Loaded InitVariables.mat")
        return
        
    def startEngine(self):
        # Raises "EngineError" is Matlab can't be started 
        # Implemented a check for this, to report it to the user
        self.eng = matlab.engine.start_matlab()

    def stopEngine(self):
        self.eng.quit()

    def load_simulink(self):
        self.eng.eval("load_system({})".format(self.model), nargout=0)

    def run_simulink(self):
        self.eng.eval("sim('MultiLoop_mode3')", nargout=0)
        return 1

tep = MatlabBridge()
<<<<<<< HEAD
tep.run_simulink()
print(tep.run_simulink())
=======
>>>>>>> origin/dev
