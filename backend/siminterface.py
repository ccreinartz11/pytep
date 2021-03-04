import pandas as pd
import numpy as np
import pickle
import pathlib
from collections.abc import Iterable

from utils.singleton import Singleton
from backend.matlab_bridge import MatlabBridge

#  setup logger
import logging
import logging.config
import json
from pythonjsonlogger import jsonlogger

with open(pathlib.Path(__file__).parent.parent.absolute() / "loginfo.json") as f:
    config = json.load(f)
    logging.config.dictConfig(config)

logger = logging.getLogger(__name__)


class SimInterface(metaclass=Singleton):

    def __init__(self):
        self._matlab_bridge = None
        self._process_data = pd.DataFrame()
        self._process_units = pd.DataFrame()
        self._setpoint_data = pd.DataFrame()
        self._cost_data = pd.DataFrame()
        self._idv_data = pd.DataFrame()
        self._internal_sp_info = None
        self._logger = logging.getLogger(__name__)

    def simulate(self):
        """
        Start/Continue the the active simulation until it is paused or terminates.
        """
        self._matlab_bridge.run_until_paused()

    def update(self):
        """
        Fetches current simulation data from the MATLAB workspace and updates process_data, setpoint_data, idv_data and
        cost_data.
        """
        #  ???: Should the workspace refresh only be here? Does the workspace ever need to be updated otherwise?
        self._update_process_data()
        self._update_setpoint_data()
        self._update_idv_data()
        self._update_cost_data()

    def reset(self):
        """
        Resets the simulation environment to it's initial condition. All unsaved simulation results are lost on reset.
        On reset, the active simulation is stopped, the MATLAB workspace is cleared fully and then reloaded from an
        initialization script in MATLAB.
        :func:`~backend.siminterface.SimInterface.update` is called to reset the internal variables of the SimInterface.
        """
        self._matlab_bridge.stop_simulation()
        self._matlab_bridge.reset_workspace()
        self._matlab_bridge.reset_simulink_blocks()
        self.update()

    def extend_simulation(self, duration=5):
        """
        Sets the time in hours until the simulation is automatically paused after a call to :func:`~backend.siminterface.SimInterface.simulate`.

        Parameters
        ----------
        duration: float
            Additional simulation time in hours.
        """
        time = self._matlab_bridge.get_workspace_variable("tout")
        if isinstance(time, Iterable):
            current_time = time[-1]
        else:
            current_time = time
        self._matlab_bridge.set_simpause_time(current_time + duration)

    def _update_process_data(self):
        new_process_data = self._fetch_process_data()
        new_process_data = pd.DataFrame(
            data=new_process_data, columns=self._process_data.columns
        )
        self._process_data = new_process_data  # FIXME: It would be better if the new process data was appended

    def _update_setpoint_data(self):
        setpoint_data = self._fetch_setpoint_data()
        setpoint_data = pd.DataFrame(
            data=setpoint_data, columns=self._setpoint_data.columns
        )
        self._setpoint_data = setpoint_data

    def _update_cost_data(self):
        cost_data = self._fetch_cost_data()
        if isinstance(cost_data, float):
            cost_data = [cost_data]
        cost_data = pd.DataFrame(
            data=cost_data, columns=self._cost_data.columns
        )
        self._cost_data = cost_data

    def _update_idv_data(self):
        idv_data = self._fetch_idv_data()
        idv_data = pd.DataFrame(
            data=idv_data, columns=self._idv_data.columns
        )
        self._idv_data = idv_data

    def _fetch_process_data(self):
        time = self._matlab_bridge.get_workspace_variable("tout")
        if not isinstance(time, Iterable):
            time = np.asarray(time).reshape(1, 1)
        process_vars = self._matlab_bridge.get_workspace_variable("simout")
        time_and_pv = np.hstack((time, process_vars))
        return time_and_pv

    def _fetch_setpoint_data(self):
        setpoints = self._matlab_bridge.get_workspace_variable("setpoints")
        return setpoints

    def _fetch_cost_data(self):
        cost = self._matlab_bridge.get_workspace_variable("OpCost")
        return cost
    
    def _fetch_idv_data(self):
        idvs = self._matlab_bridge.get_workspace_variable("idv_list")
        return idvs

    def _load_dataframes(self):
        setupinfo_path = pathlib.Path(__file__).parent / "setupinfo"
        with open(setupinfo_path / "process_var_labels.pkl", "rb") as pv_label_file:
            pv_labels = pickle.load(pv_label_file)
        self._process_data = pd.DataFrame(columns=pv_labels)
        with open(setupinfo_path / "setpoint_labels.pkl", "rb") as setpoint_label_file:
            setpoint_labels = pickle.load(setpoint_label_file)
        self._setpoint_data = pd.DataFrame(columns=setpoint_labels)
        with open(setupinfo_path / "process_var_units.pkl", "rb") as pv_units_file:
            pv_units = pickle.load(pv_units_file)
        self._process_units = pd.DataFrame(data=[pv_units], columns=pv_labels)
        with open(setupinfo_path / "idv_labels.pkl", "rb") as idv_label_file:
            idv_labels = pickle.load(idv_label_file)
        self._idv_data = pd.DataFrame(columns=idv_labels)
        # pure dummy init for cost data
        self._cost_data = pd.DataFrame(data=[0], columns=["cost"])

    def process_data_labels(self):
        """
        Returns the columns of the dataframe that is returned when calling :func:`~backend.siminterface.SimInterface.process_data`.

        Returns
        -------
        process_data_columns : list
            List of processdata labels
        """
        return self._process_data.columns.tolist()

    def timed_var(self, var_name):
        """
        Returns a dataframe with columns ["time", "var_name"], containing the time series representing the current
        simulation output.

        Parameters
        ----------
        var_name: string
            :func:`~backend.siminterface.SimInterface.process_data_labels` returns a list of feasible variable names.

        Returns
        -------
        timed_var : pandas dataframe
            Dataframe with columns ["time", "var_name"]
        """
        if var_name == "time":
            return self._process_data[["time"]]
        return self._process_data[["time", var_name]]

    @property
    def process_data(self):
        """
        Returns a dataframe containing the process data timeseries.

        Returns
        -------
        process_data: pandas dataframe
        """
        return self._process_data

    # @process_data.setter
    # def process_data(self, data):
    #     self._process_data = data

    def current_sim_time(self):
        """
        Getter for the current simulation time in hours.

        Returns
        -------
        simulation_time: float
        """
        return self._process_data["time"].values[-1]

    def operating_cost(self):
        """
        Getter for the operating cost time series of the active simulation.

        Returns
        -------
        Operating cost: pandas dataframe
            Pandas dataframe containing a "Cost" column.
        """
        return self._cost_data

    @staticmethod
    def setup():
        """
        Setup for the SimInterface. The first initialization of SimInterface should be done using this method. Any
        following initialization should be done using the regular constructor, which will return the already existing
        SimInterface object (SimInterface is a singleton class).

        Returns
        -------
        simulation interface: backend.siminterface.SimInterface()
            Fully initialized simulation interface for the Tennessee Eastman Simulator.
        """
        si = SimInterface()
        mb = MatlabBridge()
        si._matlab_bridge = mb
        si._load_dataframes()
        si._setup_internal_sp_info()
        si.reset()
        return si

    def get_var_unit(self, var_label):
        """
        Returns the unit of any process variable included in the dictionary returned when calling :func:`~backend.siminterface.SimInterface.process_data`

        Parameters
        ----------
        var_label: Label of the process variable for which the unit will be returned.

        Returns
        -------
        var unit: string
        """
        return self._process_units[var_label][0]

    # set faults (idv)

    def set_idv(self, idv_idx, value, delay=0):
        current_time = list(self._process_data['time'])[-1]
        values_before_step, values_after_step, step_times = self._matlab_bridge.get_idv_input_block_params()
        values_after_step[0, idv_idx-1] = value
        step_times[0, idv_idx-1] = current_time + delay
        self._log_idv_change(idv_idx, value, current_time)
        self._matlab_bridge.set_idv_input_block_params(values_before_step, values_after_step, step_times)

    def get_idv(self, idv_idx):
        idv_label = "IDV{}".format(idv_idx)
        return self._idv_data[idv_label].values[-1]

    def _log_idv_change(self, idv_idx, target_val, start_time):
        log = self._idv_change_log_message(idv_idx, target_val, start_time)
        logger.info(log)

    @staticmethod
    def _idv_change_log_message(idv_idx, target_val, start_time):
        log = {
            "simulation_command": "idv_change",
            "idv_idx": idv_idx,
            "simulation_time": start_time,
            "target_value": target_val
        }
        return log

    # setpoint commands

    def _setup_internal_sp_info(self):
        """Generates a dictionary containing setpoint labels as keys and correponding utility functions (getter/setter)
        in the matlab_bridge as values.
        """

        sp_info = {
            "ProductionSP": {"setter": self._matlab_bridge.set_production_sp},
            "StripLevelSP": {"setter": self._matlab_bridge.set_strip_level_sp},
            "SepLevelSP": {"setter": self._matlab_bridge.set_sep_level_sp},
            "ReactorLevelSP": {"setter": self._matlab_bridge.set_reactor_level_sp},
            "ReactorPressSP": {"setter": self._matlab_bridge.set_reactor_press_sp},
            "MolePctGSP": {"setter": self._matlab_bridge.set_g_in_product_sp},
            "YASP": {"setter": self._matlab_bridge.set_ya_sp},
            "YACSP": {"setter": self._matlab_bridge.set_yac_sp},
            "ReactorTempSP": {"setter": self._matlab_bridge.set_reactor_temp_sp},
            "RecycleValvePosSP": {"setter": self._matlab_bridge.set_recycle_valve_sp},
            "SteamValvePosSP": {"setter": self._matlab_bridge.set_steam_valve_sp},
            "AgitatorSpeedSP": {"setter": self._matlab_bridge.set_agitator_sp}
        }
        self._internal_sp_info = sp_info

    def ramp_production(self, target_val=None, duration=None, slope=None):
        label = 'ProductionSP'
        self._ramp_setpoint(label, target_val, duration, slope)

    def ramp_stripper_level(self, target_val=None, duration=None, slope=None):
        label = 'StripLevelSP'
        self._ramp_setpoint(label, target_val, duration, slope)

    def ramp_separator_level(self, target_val=None, duration=None, slope=None):
        label = 'SepLevelSP'
        self._ramp_setpoint(label, target_val, duration, slope)

    def ramp_reactor_level(self, target_val=None, duration=None, slope=None):
        label = 'ReactorLevelSP'
        self._ramp_setpoint(label, target_val, duration, slope)

    def ramp_reactor_pressure(self, target_val=None, duration=None, slope=None):
        label = 'ReactorPressSP'
        self._ramp_setpoint(label, target_val, duration, slope)

    def ramp_g_in_product(self, target_val=None, duration=None, slope=None):
        label = 'MolePctGSP'
        self._ramp_setpoint(label, target_val, duration, slope)

    def ramp_ya(self, target_val=None, duration=None, slope=None):
        label = 'YASP'
        self._ramp_setpoint(label, target_val, duration, slope)

    def ramp_yac(self, target_val=None, duration=None, slope=None):
        label = 'YACSP'
        self._ramp_setpoint(label, target_val, duration, slope)

    def ramp_reactor_temp(self, target_val=None, duration=None, slope=None):
        label = 'ReactorTempSP'
        self._ramp_setpoint(label, target_val, duration, slope)

    def ramp_recycle_valve_pos(self, target_val=None, duration=None, slope=None):
        label = 'RecycleValvePosSP'
        self._ramp_setpoint(label, target_val, duration, slope)

    def ramp_steam_valve_pos(self, target_val=None, duration=None, slope=None):
        label = 'SteamValvePosSP'
        self._ramp_setpoint(label, target_val, duration, slope)

    def ramp_agitator_speed(self, target_val=None, duration=None, slope=None):
        label = 'AgitatorSpeedSP'
        self._ramp_setpoint(label, target_val, duration, slope)

    def _ramp_setpoint(self, setpoint_label, target_val=None, duration=None, slope=None):
        # TODO: Add delay (default value: 0)
        """Generic setpoint ramp generation. The setpoint ramp profile starts at the current simulation time and current
        setpoint value and follows the ramp profile specified by the target value, duration and slope.
        Only two of the profile defining parameters may be set simultaneously (if all three are set, 'slope' is ignored).

        Parameters
        ----------
        setpoint_label: Label as specified in the setpoint_labels.pkl in backend/setupinfo
        target_val (float): Target value of setpoint to be assumed after ramp profile completed.
        duration (float): Duration in (h) of ramp profile.
        slope (float): Value change/(h) of the ramp profile.
        """

        current_sp_val = list(self._setpoint_data[setpoint_label])[-1]
        current_time = list(self._process_data['time'])[-1]
        sp_set_func = self._internal_sp_info[setpoint_label]["setter"]

        if not any([target_val, duration]):
            raise ValueError("Either target_val or duration has to be set for the method to execute.")
        if all([target_val, duration, slope]):
            UserWarning("_ramp_setpoint method was called with target_val, "
                        "duration and slope specified. Slope is ignored.")
            slope = None
        if slope is None:
            sp_set_func(before=current_sp_val, after=target_val, duration=duration, start_time=current_time)
        elif duration is None:
            dur = abs((target_val-current_sp_val)/slope)
            sp_set_func(before=current_sp_val, after=target_val, duration=dur, start_time=current_time)
        elif target_val is None:
            target_val = current_sp_val + slope * duration
            sp_set_func(before=current_sp_val, after=target_val, duration=duration, start_time=current_time)
        else:
            raise ValueError("_ramp_setpoint was called with incorrect parameter configuration.")
        
        self._log_setpoint_ramp(setpoint_label, target_val, duration, current_time)

    def _log_setpoint_ramp(self, setpoint_label, target_val, duration, start_time):
        log = self._setpoint_ramp_log_message(setpoint_label, target_val, duration, start_time)
        logger.info(log)

    @staticmethod
    def _setpoint_ramp_log_message(setpoint_label, target_val, duration, start_time):
        log = {
            "simulation_command": "setpoint_ramp",
            "setpoint_label": setpoint_label,
            "simulation_time": start_time,
            "target_value": target_val,
            "duration": duration
        }
        return log




