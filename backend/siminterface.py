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

    def simulate(self):
        self._matlab_bridge.run_simulink()

    def update(self):
        self._update_process_data()

    def prep_next_iteration(self):
        self._matlab_bridge.prep_next_iteration()

    def _update_process_data(self):
        new_process_data = self._matlab_bridge.get_process_vars()
        new_process_data = pd.DataFrame(data=new_process_data, columns=self._process_data.columns)
        self._process_data = self._process_data.append(new_process_data)


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

    def plot_labels(self):
        return self._process_data.columns.tolist()

    def timed_var(self, var_name):
        """Returns a dataframe with columns `time` and `var_name`"""
        if var_name == 'time':
            return self._process_data[['time']]
        return self._process_data[['time', var_name]]

    @property
    def process_data(self):
        return self._process_data

    @process_data.setter
    def process_data(self, data):
        self._process_data = data

    @staticmethod
    def setup():
        si = SimInterface()
        mb = MatlabBridge()
        si._matlab_bridge = mb
        si._load_dataframes()
        return si

    @staticmethod
    def dummy_setup():
        interface = SimInterface()
        dummy_data = pd.read_pickle('./frontend/dummy_frame.pkl')
        interface.process_data = dummy_data
        return interface

    @staticmethod
    def setup_no_engine():
        si = SimInterface()
        si._load_dataframes()
        return si

    def get_var_unit(self, col_label):
        return self._process_units[col_label][0]


