import pandas as pd

from utils.singleton import Singleton


class MainPlotInterface(metaclass=Singleton):

    def __init__(self):
        self._process_vars = pd.DataFrame()

    def labels(self):
        return self._process_vars.columns.tolist()

    def timed_var(self, var_name):
        """Returns a dataframe with columns `time` and `var_name`"""
        if var_name == 'time':
            return self._process_vars[['time']]
        return self._process_vars[['time', var_name]]

    @property
    def process_vars(self):
        return self._process_vars

    @process_vars.setter
    def process_vars(self, data):
        self._process_vars = data

    @staticmethod
    def dummy_interface():
        interface = MainPlotInterface()
        dummy_data = pd.read_pickle('./frontend/dummy_frame.pkl')
        interface.process_vars = dummy_data
        return interface
