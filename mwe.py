import matlab.engine


class MatlabBridge:

    def __init__(self, model):
        self.model = model
        self.startEngine()
        return
        
    def startEngine(self):
        # Raises "EngineError" is Matlab can't be started 
        # Implemented a check for this, to report it to the user
        self.eng = matlab.engine.start_matlab()

    def stopEngine(self):
        self.eng.quit()

    def load_simulink(self):
        self.eng.eval("load_system({})".format(self.model), nargout=0)


tep = MatlabBridge()
