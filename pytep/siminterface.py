import matlab.engine
import pandas as pd
import numpy as np
import pickle
import pathlib
from collections.abc import Iterable

from pytep.utils.singleton import Singleton
from pytep.matlab_bridge import MatlabBridge

#  setup logger
import logging
import logging.config
import json

# with open(pathlib.Path(__file__).parent.absolute() / "loginfo.json") as f:
#     config = json.load(f)
#     logging.config.dictConfig(config)
#
# logger = logging.getLogger(__name__)


class SimInterface(metaclass=Singleton):

    def __init__(self):
        self._matlab_bridge = None
        self._process_data = pd.DataFrame()
        self._process_units = pd.DataFrame()
        self._manipulated_variables = pd.DataFrame()
        self._manipulated_var_units = pd.DataFrame()
        self._setpoint_data = pd.DataFrame()
        self._setpoint_labels = list()
        self._cost_data = pd.DataFrame()
        self._idv_data = pd.DataFrame()
        self._internal_sp_info = None

    def simulate(self, duration=None):
        """
        Start/Continue the the active simulation until it is paused or terminates.
        """
        if duration is not None:
            self.extend_simulation(duration)
        self._matlab_bridge.run_until_paused()
        self.update()

    def update(self):
        """
        Fetches current simulation data from the MATLAB workspace and updates process_data, setpoint_data, idv_data and
        cost_data.
        """
        # TODO: Check here if there even is new data. Skip if not.
        try:
            current_sim_time = self.current_sim_time()
        except IndexError:
            Warning("Current sim time is empty. This should not happen with proper initialization. "
                    "Current sim time is set to 0.")
            current_sim_time = 0
        if current_sim_time == 0:
            self._init_internal_variables()
        else:
            self._matlab_bridge.isolate_recent_data_in_workspace(current_sim_time)
            self._update_process_data()
            self._update_setpoint_data()
            self._update_idv_data()
            self._update_cost_data()
            self._update_manipulated_variables()

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
        self._init_internal_variables()

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

    def save_all(self, save_dir):
        """
        Saves the time, process data, manipulated variables, setpoint data, cost data and idv data as separate pickled
        dataframes in the specified save directory. Multiple saves in the same save_dir will result in older files being
        overwritten.
        Parameters
        ----------
        save_dir: pathlib.Path, string
            Directory in which the simulation data should be saved.
        """

        pd_save_path = pathlib.Path(save_dir) / "process_data.pkl"
        self._process_data.to_pickle(pd_save_path)

        sp_save_path = pathlib.Path(save_dir) / "setpoint_data.pkl"
        self._setpoint_data.to_pickle(sp_save_path)

        idv_save_path = pathlib.Path(save_dir) / "idv_data.pkl"
        self._idv_data.to_pickle(idv_save_path)

        cost_save_path = pathlib.Path(save_dir) / "cost_data.pkl"
        self._cost_data.to_pickle(cost_save_path)

        manipulated_vars_path = pathlib.Path(save_dir) / "manipulated_vars.pkl"
        self._manipulated_variables.to_pickle(manipulated_vars_path)

    def _init_internal_variables(self):
        """
        Fetches current simulation data from the MATLAB workspace and updates process_data, setpoint_data, idv_data and
        cost_data.
        """
        self._init_process_data()
        self._init_setpoint_data()
        self._init_idv_data()
        self._init_cost_data()
        self._init_manipulated_variables()

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
        try:
            new_process_data = self._fetch_new_process_data()
            if new_process_data.size == 0:
                return  # no new process data
            new_process_data = pd.DataFrame(
                data=new_process_data, columns=self._process_data.columns
            )
            self._process_data = pd.concat([self._process_data, new_process_data], axis=0)
        except ValueError:
            pass

    def _init_process_data(self):
        new_process_data = self._fetch_process_data()
        new_process_data = pd.DataFrame(
            data=new_process_data, columns=self._process_data.columns
        )
        self._process_data = new_process_data

    def _update_manipulated_variables(self):
        try:
            new_manipulated_variables = self._fetch_new_manipulated_variables()
            if new_manipulated_variables.size == 0:
                return  # no new manipulated variables
            new_manipulated_variables = pd.DataFrame(
                data=new_manipulated_variables, columns=self._manipulated_variables.columns
            )
            self._manipulated_variables = pd.concat([self._manipulated_variables, new_manipulated_variables], axis=0)
        except ValueError:
            pass

    def _init_manipulated_variables(self):
        new_manipulated_variables = self._fetch_manipulated_variables()
        new_manipulated_variables = pd.DataFrame(
            data=new_manipulated_variables, columns=self._manipulated_variables.columns
        )
        self._manipulated_variables = new_manipulated_variables

    def _update_setpoint_data(self):
        try:
            new_data = self._fetch_new_setpoint_data()
            new_data = pd.DataFrame(
                data=new_data, columns=self._setpoint_data.columns
            )
            self._setpoint_data = pd.concat([self._setpoint_data, new_data], axis=0)
        except ValueError:
            pass  # This is executed if there is no new data since the last update

    def _init_setpoint_data(self):
        setpoint_data = self._fetch_setpoint_data()
        setpoint_data = pd.DataFrame(
            data=setpoint_data, columns=self._setpoint_data.columns
        )
        self._setpoint_data = setpoint_data

    def _update_cost_data(self):
        try:
            new_data = self._fetch_new_cost_data()
            new_data = pd.DataFrame(
                data=new_data, columns=self._cost_data.columns
            )
            self._cost_data = pd.concat([self._cost_data, new_data], axis=0)
        except ValueError:
            pass

    def _init_cost_data(self):
        cost_data = self._fetch_cost_data()
        if isinstance(cost_data, float):
            cost_data = [cost_data]
        cost_data = pd.DataFrame(
            data=cost_data, columns=self._cost_data.columns
        )
        self._cost_data = cost_data

    def _update_idv_data(self):
        try:
            new_data = self._fetch_new_idv_data()
            new_data = pd.DataFrame(
                data=new_data, columns=self._idv_data.columns
            )
            self._idv_data = pd.concat([self._idv_data, new_data], axis=0)
        except ValueError:
            pass

    def _init_idv_data(self):
        idv_data = self._fetch_idv_data()
        idv_data = pd.DataFrame(
            data=idv_data, columns=self._idv_data.columns
        )
        self._idv_data = idv_data

    def _fetch_new_process_data(self):
        time = self._matlab_bridge.get_workspace_variable("latest_tout")
        if time.size == 0:
            return np.asarray([])  # no new processdata
        if not isinstance(time, Iterable):
            time = np.asarray(time).reshape(1, 1)
        process_vars = self._matlab_bridge.get_workspace_variable("latest_simout")
        time_and_pv = np.hstack((time, process_vars))
        return time_and_pv

    def _fetch_process_data(self):
        time = self._matlab_bridge.get_workspace_variable("tout")
        if not isinstance(time, Iterable):
            time = np.asarray(time).reshape(1, 1)
        process_vars = self._matlab_bridge.get_workspace_variable("simout")
        time_and_pv = np.hstack((time, process_vars))
        return time_and_pv

    def _fetch_new_manipulated_variables(self):
        vars = self._matlab_bridge.get_workspace_variable("latest_xmv")
        return vars

    def _fetch_manipulated_variables(self):
        vars = self._matlab_bridge.get_workspace_variable("xmv")
        return vars

    def _fetch_new_setpoint_data(self):
        setpoints = self._matlab_bridge.get_workspace_variable("latest_setpoints")
        return setpoints

    def _fetch_setpoint_data(self):
        setpoints = self._matlab_bridge.get_workspace_variable("setpoints")
        return setpoints

    def _fetch_new_cost_data(self):
        # TODO: Check if this fails if only one new time is returned or if no new data is present
        cost = self._matlab_bridge.get_workspace_variable("latest_op_cost")
        return cost

    def _fetch_cost_data(self):
        cost = self._matlab_bridge.get_workspace_variable("OpCost")
        return cost

    def _fetch_new_idv_data(self):
        idvs = self._matlab_bridge.get_workspace_variable("latest_idv_list")
        return idvs

    def _fetch_idv_data(self):
        idvs = self._matlab_bridge.get_workspace_variable("idv_list")
        return idvs

    def _load_dataframes(self):
        setupinfo_path = pathlib.Path(__file__).parent / "setupinfo"
        with open(setupinfo_path / "process_var_labels.pkl", "rb") as pv_label_file:
            pv_labels = pickle.load(pv_label_file)
        self._process_data = pd.DataFrame(columns=pv_labels)
        with open(setupinfo_path / "xmv_labels.pkl", "rb") as xmv_label_file:
            xmv_labels = pickle.load(xmv_label_file)
        self._manipulated_variables = pd.DataFrame(columns=xmv_labels)
        with open(setupinfo_path / "setpoint_labels.pkl", "rb") as setpoint_label_file:
            setpoint_labels = pickle.load(setpoint_label_file)
        self._setpoint_data = pd.DataFrame(columns=setpoint_labels)
        self._setpoint_labels = setpoint_labels
        with open(setupinfo_path / "process_var_units.pkl", "rb") as pv_units_file:
            pv_units = pickle.load(pv_units_file)
        self._process_units = pd.DataFrame(data=[pv_units], columns=pv_labels)
        with open(setupinfo_path / "xmv_units.pkl", "rb") as xmv_units_file:
            xmv_units = pickle.load(xmv_units_file)
        self._manipulated_var_units = pd.DataFrame(data=[xmv_units], columns=xmv_labels)
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
    
    def current_process_data(self):
        """
        Returns a dataframe containing a single row representing the current simulation state (process data).
        Returns
        -------
        process_data: pandas dataframe
        """
        return self._process_data.tail(1)

    @property
    def manipulated_variables(self):
        """Returns a dataframe containing the manipulated variables timeseries.

        Returns
        -------
        manipulated_variables: pandas dataframe
        """
        return self._manipulated_variables

    def current_manipulated_variables(self):
        """
        Returns a dataframe containing a single row representing the current simulation state (manipulated_variables).
        Returns
        -------
        manipulated_variables: pandas dataframe
        """
        return self._manipulated_variables.tail(1)

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

    def current_operating_cost(self):
        return self._cost_data.tail(1)

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
        """
        Set the fault magnitude and delay in hours before the magnitude is changed from its current value for
        one idv (IDV1-IDV28).

        Parameters
        ----------
        idv_idx: int
            Index of the idv (IDV1-IDV28) TODO: Include link to relevant paper here.
        value: float
            Activation flag for the IDV. Value between 0 and 1.
        delay:
            Delay in hours before the idv value is changed from it's current value.
        """
        current_time = list(self._process_data['time'])[-1]
        values_before_step, values_after_step, step_times = self._matlab_bridge.get_idv_input_block_params()
        values_after_step[0, idv_idx-1] = value
        step_times[0, idv_idx-1] = current_time + delay
        self._log_idv_change(idv_idx, value, current_time)
        self._matlab_bridge.set_idv_input_block_params(values_before_step, values_after_step, step_times)

    def get_idv(self, idv_idx):
        """
        Getter for the current magnitude value of one of the 28 process faults.

        Parameters
        ----------
        idv_idx: int
            Value between 1 and 28

        Returns
        -------
            idv_magnitude: float
                Value between 0 and 1
        """
        idv_label = "IDV{}".format(idv_idx)
        return self._idv_data[idv_label].values[-1]

    def _log_idv_change(self, idv_idx, target_val, start_time):
        log = self._idv_change_log_message(idv_idx, target_val, start_time)
        # logger.debug(log)

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

    def current_setpoint_value(self, setpoint_label):
        cur = self._setpoint_data.tail(1)
        cur_val = cur[setpoint_label].values[0]
        return cur_val

    def current_setpoints(self):
        return self._setpoint_data.tail(1)

    @property
    def setpoint_labels(self):
        return self._setpoint_labels

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
        """Initiates a ramp profile for the production setpoint at at the current simulation time. The ramp will start
        immediately, when :func:`~backend.siminterface.SimInterface.simulate` is called.
        The setpoint ramp profile starts at the current simulation time and current setpoint value and follows a ramp
        profile specified by the target value, duration and slope.
        Only two of the profile defining parameters may be set simultaneously (if all three are set, 'slope' is ignored).

        Parameters
        ----------
        target_val : float, optional
            Value of the setpoint after the ramp profile is completed.
        duration : float, optional (default: 0.0)
            Duration of the change from the current setpoint value to the `target_val` in (hours).
            Step change for duration = 0, ramp otherwise
        slope : float, optional
            Slope of the ramp profile of the setpoint change in setpoint_change/hour. Not considered if `target_val` and
            `duration` are also both specified.
        """
        label = 'ProductionSP'
        self.ramp_setpoint(label, target_val, duration, slope)

    def ramp_stripper_level(self, target_val=None, duration=None, slope=None):
        """Initiates a ramp profile for the stripper level setpoint at at the current simulation time. The ramp will start
        immediately, when :func:`~backend.siminterface.SimInterface.simulate` is called.
        The setpoint ramp profile starts at the current simulation time and current setpoint value and follows a ramp
        profile specified by the target value, duration and slope.
        Only two of the profile defining parameters may be set simultaneously (if all three are set, 'slope' is ignored).

        Parameters
        ----------
        target_val : float, optional
            Value of the setpoint after the ramp profile is completed.
        duration : float, optional (default: 0.0)
            Duration of the change from the current setpoint value to the `target_val` in (hours).
            Step change for duration = 0, ramp otherwise
        slope : float, optional
            Slope of the ramp profile of the setpoint change in setpoint_change/hour. Not considered if `target_val` and
            `duration` are also both specified.
        """
        label = 'StripLevelSP'
        self.ramp_setpoint(label, target_val, duration, slope)

    def ramp_separator_level(self, target_val=None, duration=None, slope=None):
        """Initiates a ramp profile for the separator level setpoint at at the current simulation time. The ramp will start
        immediately, when :func:`~backend.siminterface.SimInterface.simulate` is called.
        The setpoint ramp profile starts at the current simulation time and current setpoint value and follows a ramp
        profile specified by the target value, duration and slope.
        Only two of the profile defining parameters may be set simultaneously (if all three are set, 'slope' is ignored).

        Parameters
        ----------
        target_val : float, optional
            Value of the setpoint after the ramp profile is completed.
        duration : float, optional (default: 0.0)
            Duration of the change from the current setpoint value to the `target_val` in (hours).
            Step change for duration = 0, ramp otherwise
        slope : float, optional
            Slope of the ramp profile of the setpoint change in setpoint_change/hour. Not considered if `target_val` and
            `duration` are also both specified.
        """
        label = 'SepLevelSP'
        self.ramp_setpoint(label, target_val, duration, slope)

    def ramp_reactor_level(self, target_val=None, duration=None, slope=None):
        """Initiates a ramp profile for the reactor level setpoint at at the current simulation time. The ramp will start
        immediately, when :func:`~backend.siminterface.SimInterface.simulate` is called.
        The setpoint ramp profile starts at the current simulation time and current setpoint value and follows a ramp
        profile specified by the target value, duration and slope.
        Only two of the profile defining parameters may be set simultaneously (if all three are set, 'slope' is ignored).

        Parameters
        ----------
        target_val : float, optional
            Value of the setpoint after the ramp profile is completed.
        duration : float, optional (default: 0.0)
            Duration of the change from the current setpoint value to the `target_val` in (hours).
            Step change for duration = 0, ramp otherwise
        slope : float, optional
            Slope of the ramp profile of the setpoint change in setpoint_change/hour. Not considered if `target_val` and
            `duration` are also both specified.
        """
        label = 'ReactorLevelSP'
        self.ramp_setpoint(label, target_val, duration, slope)

    def ramp_reactor_pressure(self, target_val=None, duration=None, slope=None):
        """Initiates a ramp profile for the reactor pressure setpoint at at the current simulation time. The ramp will start
        immediately, when :func:`~backend.siminterface.SimInterface.simulate` is called.
        The setpoint ramp profile starts at the current simulation time and current setpoint value and follows a ramp
        profile specified by the target value, duration and slope.
        Only two of the profile defining parameters may be set simultaneously (if all three are set, 'slope' is ignored).

        Parameters
        ----------
        target_val : float, optional
            Value of the setpoint after the ramp profile is completed.
        duration : float, optional (default: 0.0)
            Duration of the change from the current setpoint value to the `target_val` in (hours).
            Step change for duration = 0, ramp otherwise
        slope : float, optional
            Slope of the ramp profile of the setpoint change in setpoint_change/hour. Not considered if `target_val` and
            `duration` are also both specified.
        """
        label = 'ReactorPressSP'
        self.ramp_setpoint(label, target_val, duration, slope)

    def ramp_g_in_product(self, target_val=None, duration=None, slope=None):
        """Initiates a ramp profile for the mole percent of compoent g in the product stream (indicator of process quality) setpoint at at the current simulation time. The ramp will start
        immediately, when :func:`~backend.siminterface.SimInterface.simulate` is called.
        The setpoint ramp profile starts at the current simulation time and current setpoint value and follows a ramp
        profile specified by the target value, duration and slope.
        Only two of the profile defining parameters may be set simultaneously (if all three are set, 'slope' is ignored).

        Parameters
        ----------
        target_val : float, optional
            Value of the setpoint after the ramp profile is completed.
        duration : float, optional (default: 0.0)
            Duration of the change from the current setpoint value to the `target_val` in (hours).
            Step change for duration = 0, ramp otherwise
        slope : float, optional
            Slope of the ramp profile of the setpoint change in setpoint_change/hour. Not considered if `target_val` and
            `duration` are also both specified.
        """
        label = 'MolePctGSP'
        self.ramp_setpoint(label, target_val, duration, slope)

    def ramp_ya(self, target_val=None, duration=None, slope=None):
        """Initiates a ramp profile for the yA setpoint at at the current simulation time. The ramp will start
        immediately, when :func:`~backend.siminterface.SimInterface.simulate` is called.
        The setpoint ramp profile starts at the current simulation time and current setpoint value and follows a ramp
        profile specified by the target value, duration and slope.
        Only two of the profile defining parameters may be set simultaneously (if all three are set, 'slope' is ignored).

        Parameters
        ----------
        target_val : float, optional
            Value of the setpoint after the ramp profile is completed.
        duration : float, optional (default: 0.0)
            Duration of the change from the current setpoint value to the `target_val` in (hours).
            Step change for duration = 0, ramp otherwise
        slope : float, optional
            Slope of the ramp profile of the setpoint change in setpoint_change/hour. Not considered if `target_val` and
            `duration` are also both specified.
        """
        label = 'YASP'
        self.ramp_setpoint(label, target_val, duration, slope)

    def ramp_yac(self, target_val=None, duration=None, slope=None):
        """Initiates a ramp profile for the yAC setpoint at at the current simulation time. The ramp will start
        immediately, when :func:`~backend.siminterface.SimInterface.simulate` is called.
        The setpoint ramp profile starts at the current simulation time and current setpoint value and follows a ramp
        profile specified by the target value, duration and slope.
        Only two of the profile defining parameters may be set simultaneously (if all three are set, 'slope' is ignored).

        Parameters
        ----------
        target_val : float, optional
            Value of the setpoint after the ramp profile is completed.
        duration : float, optional (default: 0.0)
            Duration of the change from the current setpoint value to the `target_val` in (hours).
            Step change for duration = 0, ramp otherwise
        slope : float, optional
            Slope of the ramp profile of the setpoint change in setpoint_change/hour. Not considered if `target_val` and
            `duration` are also both specified.
        """
        label = 'YACSP'
        self.ramp_setpoint(label, target_val, duration, slope)

    def ramp_reactor_temp(self, target_val=None, duration=None, slope=None):
        """Initiates a ramp profile for the reactor temperature setpoint at at the current simulation time. The ramp will start
        immediately, when :func:`~backend.siminterface.SimInterface.simulate` is called.
        The setpoint ramp profile starts at the current simulation time and current setpoint value and follows a ramp
        profile specified by the target value, duration and slope.
        Only two of the profile defining parameters may be set simultaneously (if all three are set, 'slope' is ignored).

        Parameters
        ----------
        target_val : float, optional
            Value of the setpoint after the ramp profile is completed.
        duration : float, optional (default: 0.0)
            Duration of the change from the current setpoint value to the `target_val` in (hours).
            Step change for duration = 0, ramp otherwise
        slope : float, optional
            Slope of the ramp profile of the setpoint change in setpoint_change/hour. Not considered if `target_val` and
            `duration` are also both specified.
        """
        label = 'ReactorTempSP'
        self.ramp_setpoint(label, target_val, duration, slope)

    def ramp_recycle_valve_pos(self, target_val=None, duration=None, slope=None):
        """Initiates a ramp profile for the recycle valve position setpoint at at the current simulation time. The ramp will start
        immediately, when :func:`~backend.siminterface.SimInterface.simulate` is called.
        The setpoint ramp profile starts at the current simulation time and current setpoint value and follows a ramp
        profile specified by the target value, duration and slope.
        Only two of the profile defining parameters may be set simultaneously (if all three are set, 'slope' is ignored).

        Parameters
        ----------
        target_val : float, optional
            Value of the setpoint after the ramp profile is completed.
        duration : float, optional (default: 0.0)
            Duration of the change from the current setpoint value to the `target_val` in (hours).
            Step change for duration = 0, ramp otherwise
        slope : float, optional
            Slope of the ramp profile of the setpoint change in setpoint_change/hour. Not considered if `target_val` and
            `duration` are also both specified.
        """
        label = 'RecycleValvePosSP'
        self.ramp_setpoint(label, target_val, duration, slope)

    def ramp_steam_valve_pos(self, target_val=None, duration=None, slope=None):
        """Initiates a ramp profile for the steam valve position setpoint at at the current simulation time. The ramp will start
        immediately, when :func:`~backend.siminterface.SimInterface.simulate` is called.
        The setpoint ramp profile starts at the current simulation time and current setpoint value and follows a ramp
        profile specified by the target value, duration and slope.
        Only two of the profile defining parameters may be set simultaneously (if all three are set, 'slope' is ignored).

        Parameters
        ----------
        target_val : float, optional
            Value of the setpoint after the ramp profile is completed.
        duration : float, optional (default: 0.0)
            Duration of the change from the current setpoint value to the `target_val` in (hours).
            Step change for duration = 0, ramp otherwise
        slope : float, optional
            Slope of the ramp profile of the setpoint change in setpoint_change/hour. Not considered if `target_val` and
            `duration` are also both specified.
        """
        label = 'SteamValvePosSP'
        self.ramp_setpoint(label, target_val, duration, slope)

    def ramp_agitator_speed(self, target_val=None, duration=None, slope=None):
        """Initiates a ramp profile for the agitator speed setpoint at at the current simulation time. The ramp will start
        immediately, when :func:`~backend.siminterface.SimInterface.simulate` is called.
        The setpoint ramp profile starts at the current simulation time and current setpoint value and follows a ramp
        profile specified by the target value, duration and slope.
        Only two of the profile defining parameters may be set simultaneously (if all three are set, 'slope' is ignored).

        Parameters
        ----------
        target_val : float, optional
            Value of the setpoint after the ramp profile is completed.
        duration : float, optional (default: 0.0)
            Duration of the change from the current setpoint value to the `target_val` in (hours).
            Step change for duration = 0, ramp otherwise
        slope : float, optional
            Slope of the ramp profile of the setpoint change in setpoint_change/hour. Not considered if `target_val` and
            `duration` are also both specified.
        """
        label = 'AgitatorSpeedSP'
        self.ramp_setpoint(label, target_val, duration, slope)

    def ramp_setpoint(self, setpoint_label, target_val=None, duration=None, slope=None, delay=0):
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
        delay (float): Delay until the ramp transition is initiated
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
            sp_set_func(before=current_sp_val, after=target_val, duration=duration, start_time=current_time+delay)
        elif duration is None:
            dur = abs((target_val-current_sp_val)/slope)
            sp_set_func(before=current_sp_val, after=target_val, duration=dur, start_time=current_time+delay)
        elif target_val is None:
            target_val = current_sp_val + slope * duration
            sp_set_func(before=current_sp_val, after=target_val, duration=duration, start_time=current_time+delay)
        else:
            raise ValueError("_ramp_setpoint was called with incorrect parameter configuration.")
        
        self._log_setpoint_ramp(setpoint_label, target_val, duration, current_time+delay)

    def _log_setpoint_ramp(self, setpoint_label, target_val, duration, start_time):
        log = self._setpoint_ramp_log_message(setpoint_label, target_val, duration, start_time)
        # logger.debug(log)

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




