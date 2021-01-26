import pandas as pd


class MainPlotInterface:

    def __init__(self):
        self._data = None

    def timed_var(self, var_name):
        """Returns a dataframe with columns `time` and `var_name`"""
        return self._data[['time', var_name]]

    @property
    def data(self):
        return self._data

    @property
    def data(self, data):
        self._data = data

    @staticmethod
    def dummy_interface():
        interface = MainPlotInterface()
        dummy_data = pd.read_pickle('./frontend/dummy_frame.pkl')
        interface.data = dummy_data
        return interface
