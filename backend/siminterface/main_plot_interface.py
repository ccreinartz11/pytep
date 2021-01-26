import pandas as pd

from utils.singleton import Singleton


class MainPlotInterface(metaclass=Singleton):

    def __init__(self):
        self._data = pd.DataFrame()

    def labels(self):
        return self._data.columns.tolist()

    def timed_var(self, var_name):
        """Returns a dataframe with columns `time` and `var_name`"""
        if var_name == 'time':
            return self._data[['time']]
        return self._data[['time', var_name]]

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, data):
        self._data = data

    @staticmethod
    def dummy_interface():
        interface = MainPlotInterface()
        dummy_data = pd.read_pickle('./frontend/dummy_frame.pkl')
        interface.data = dummy_data
        return interface
