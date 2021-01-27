import pandas as pd
import pickle
import pathlib

from utils.singleton import Singleton
from backend.matlab_bridge import MatlabBridge


class SimInterface(metaclass=Singleton):

    def __init__(self):
        self._matlab_bridge = None
        self._process_data = pd.DataFrame()
        self._process_units = pd.DataFrame()
        self._setpoints = pd.DataFrame()

    @staticmethod
    def setup():
        si = SimInterface()
        mb = MatlabBridge()
        si.matlab_bridge = mb
        return si

    @staticmethod
    def dummy_setup():
        interface = SimInterface()
        dummy_data = pd.read_pickle('./frontend/dummy_frame.pkl')
        interface.process_vars = dummy_data
        return interface

    @staticmethod
    def setup_no_engine():
        si = SimInterface()
        si._load_dataframes()
        return si

    def _load_dataframes(self):
        setupinfo_path = pathlib.Path(__file__).parent / 'setupinfo'
        with open(setupinfo_path / 'process_var_labels.pkl', 'rb') as pv_label_file:
            pv_labels = pickle.load(pv_label_file)
        self._process_data = pd.DataFrame(columns=pv_labels)
        with open(setupinfo_path / 'setpoint_labels.pkl', 'rb') as setpoint_label_file:
            setpoint_labels = pickle.load(setpoint_label_file)
        self._setpoints = pd.DataFrame(columns=setpoint_labels)
        with open(setupinfo_path / 'process_var_units.pkl', 'rb') as pv_units_file:
            pv_units = pickle.load(pv_units_file)
        self._process_units = pd.DataFrame(data=[pv_units], columns=pv_labels)

    @property
    def matlab_bridge(self):
        return self._matlab_bridge

    @matlab_bridge.setter
    def matlab_bridge(self, matlab_bridge):
        self._matlab_bridge = matlab_bridge

    def plot_labels(self):
        return self._process_data.columns.tolist()

    def timed_var(self, var_name):
        """Returns a dataframe with columns `time` and `var_name`"""
        if var_name == 'time':
            return self._process_data[['time']]
        return self._process_data[['time', var_name]]

    @property
    def process_vars(self):
        return self._process_data

    @process_vars.setter
    def process_vars(self, data):
        self._process_data = data

