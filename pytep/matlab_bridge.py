import matlab.engine
import numpy as np
from pathlib import Path
import time
from collections.abc import Iterable

import pytep.engineutils as engineutils


class MatlabBridge:
    def __init__(self, model="MultiLoop_mode3", sim_path=None):
        self._model = model
        self._sim_path = (
            Path(__file__).parent / "simulator" if sim_path is None else sim_path
        )
        self._eng = matlab.engine.start_matlab()
        self.add_dir_to_matlab_path(self._sim_path)
        self._load_simulink()
        self._load_workspace()
        self._init_setpoint_blocks_from_workspace()
        return

    def start_engine(self):
        """Starts an instance of the MATLAB engine

        Returns
        -------
        bool
            Returns True when the MATLAB engine is started
        """
        self._eng = matlab.engine.start_matlab()
        return True

    def stop_engine(self):
        """Terminates the running MATLAB engine
        """
        self._eng.quit()

    #  Simulation Commands

    def run_until_paused(self):
        """Runs the Simulink Simulation until it is paused or stopped
        """
        self.run_simulation()
        self.block_until_sim_paused()

    def run_simulation(self):
        """Runs the Simulink simulation with the appropriate command, given the current state of the Simulink model
        Possible states: Stopped, Paused, Running (Warns the user that its running)
        """
        sim_status = self.get_sim_status()
        if sim_status == "stopped":
            self.start_simulation()
        elif sim_status == "paused":
            self.continue_simulation()
        elif sim_status == "running":
            UserWarning(
                "run_simulation was called, but the simulation was already running."
            )
        else:
            UserWarning(
                "Unexpected simulation status '{}' encountered.".format(sim_status)
            )

    def block_until_sim_paused(self):
        """Waits until the Simulink simulation completes the simulation or is paused, and then returns
        """
        while not self.get_sim_status() in ["paused", "stopped"]:
            time.sleep(0.001)

    def start_simulation(self):
        """Send the start command to the active Simulink simulation
        """
        self._eng.start_simulation(nargout=0)

    def continue_simulation(self):
        """Send the continue command to the active Simulink simulation
        """
        self._eng.continue_simulation(nargout=0)

    def pause_simulation(self):
        """Send the pause command to the active Simulink simulation
        """
        self._eng.pause_simulation(nargout=0)

    def stop_simulation(self):
        """Send the stop command to the active Simulink simulation
        """
        self._eng.stop_simulation(nargout=0)

    #  Initialization and reset

    def reset_workspace(self):
        """Resets the MATLAB workspace to the initial values
        """
        self._clear_workspace()
        self._load_workspace()

    def reset_simulink_blocks(self):
        """Resets all the block parameters in the Simulink diagram to the correct initial values
        """
        self._init_setpoint_blocks_from_workspace()
        self._init_idv_block_from_workspace()

    def _init_idv_block_from_workspace(self):
        self._eng.init_idvinput_from_workspace(nargout=0)

    def _init_setpoint_blocks_from_workspace(self):
        self._eng.init_setpointinput_from_workspace(nargout=0)

    def _clear_workspace(self):
        self._eng.eval("clearvars", nargout=0)

    def _load_workspace(self):
        self._eng.eval("loadSimEnvironment", nargout=0)

    def _load_simulink(self):
        self._eng.load_system(self._model)

    def add_dir_to_matlab_path(self, dir_path):
        """Add a directory to the MATLAB path

        Parameters
        ----------
        dir_path : string
            string containing the desired path, to be added to the MATLAB path
        """
        self._eng.eval("addpath(genpath('{}'))".format(str(dir_path)), nargout=0)

    # Fault modificatiion (IDVs)

    def set_idv_input_block_params(self, values_before, values_after, step_times):
        """Setting the parameters for the idv (faults) block

        Parameters
        ----------
        values_before : float
            np.array (28 by 1) of floats for corresponding idv (faults), between 0 and 1
        values_after : float
            np.array (28 by 1) of floats for corresponding idv (faults), between 0 and 1
        step_times : float
            Absolute simulation time of which the idv (fault) change occurs (stepping from value_before to value_after)
        """
        vb = matlab.double(values_before[0].tolist())
        va = matlab.double(values_after[0].tolist())
        st = matlab.double(step_times[0].tolist())
        self._eng.set_idv_input_block_params(vb, va, st, nargout=0)

    def get_idv_input_block_params(self):
        """Gets and returns the values for the idv (faults) block

        Returns
        -------
        values_before : float
            np.array (28 by 1) of floats for corresponding idv (faults), between 0 and 1
        values_after : float
            np.array (28 by 1) of floats for corresponding idv (faults), between 0 and 1
        step_times : float
            Absolute simulation time of which the idv (fault) change occurs (stepping from value_before to value_after)
        """
        values_before, values_after, step_times = self._eng.get_idv_input_block_params(nargout=3)
        aa = np.asarray
        return aa(values_before), aa(values_after), aa(step_times)

    # Setpoint modification
    def set_production_sp(self, before=None, after=None, duration=0.0, start_time=None):
        """Setting the Producion setpoint

        Parameters
        ----------
        before : float, optional
            Value of the setpoint before a change is initiated, by default the current setpoint value
        after : float, optional
            Value of the setpoint after a change is initiated, by default the current setpoint value
        duration : float, optional
            Duration of the change from 'before' to 'after' in (hours). Step change for duration = 0, ramp otherwise, by default 0.0
        start_time : float, optional
            Absolute simulation time in hours at which the change from 'before' to 'after' is initiated, by default the current simulation time
        """
        block_name = "ProductionSP"
        self._set_sp_block_generic(block_name, before, after, duration, start_time)

    def get_production_sp(self):
        """Gets and returns the values for the Production setpoint

        Returns
        -------
        before : float
            Value of the setpoint before a change is initiated
        after : float
            Value of the setpoint after a change is initiated
        duration : float
            Duration of the change from 'before' to 'after' in (hours)
        t_start : float
            Absolute simulation time in hours at which the change from 'before' to 'after' is initiated
        """
        block_name = "ProductionSP"
        bef, aft, dur, t_start = self._eng.get_sp_generic(block_name, nargout=4)
        return bef, aft, dur, t_start

    def set_strip_level_sp(self, before=None, after=None, duration=0.0, start_time=None):
        """Setting the Stripper Level setpoint

        Parameters
        ----------
        before : float, optional
            Value of the setpoint before a change is initiated, by default the current setpoint value
        after : float, optional
            Value of the setpoint after a change is initiated, by default the current setpoint value
        duration : float, optional
            Duration of the change from 'before' to 'after' in (hours). Step change for duration = 0, ramp otherwise, by default 0.0
        start_time : float, optional
            Absolute simulation time in hours at which the change from 'before' to 'after' is initiated, by default the current simulation time
        """
        block_name = "StripLevelSP"
        self._set_sp_block_generic(block_name, before, after, duration, start_time)

    def get_strip_level_sp(self):
        """Gets and returns the values for the Stripper Level setpoint

        Returns
        -------
        before : float
            Value of the setpoint before a change is initiated
        after : float
            Value of the setpoint after a change is initiated
        duration : float
            Duration of the change from 'before' to 'after' in (hours)
        t_start : float
            Absolute simulation time in hours at which the change from 'before' to 'after' is initiated
        """
        block_name = "StripLevelSP"
        bef, aft, dur, t_start = self._eng.get_sp_generic(block_name, nargout=4)
        return bef, aft, dur, t_start

    def set_sep_level_sp(self, before=None, after=None, duration=0.0, start_time=None):
        """Setting the Seperation Level setpoint

        Parameters
        ----------
        before : float, optional
            Value of the setpoint before a change is initiated, by default the current setpoint value
        after : float, optional
            Value of the setpoint after a change is initiated, by default the current setpoint value
        duration : float, optional
            Duration of the change from 'before' to 'after' in (hours). Step change for duration = 0, ramp otherwise, by default 0.0
        start_time : float, optional
            Absolute simulation time in hours at which the change from 'before' to 'after' is initiated, by default the current simulation time
        """
        block_name = "SepLevelSP"
        self._set_sp_block_generic(block_name, before, after, duration, start_time)

    def get_sep_level_sp(self):
        """Gets and returns the values for the Seperation Level setpoint

        Returns
        -------
        before : float
            Value of the setpoint before a change is initiated
        after : float
            Value of the setpoint after a change is initiated
        duration : float
            Duration of the change from 'before' to 'after' in (hours)
        t_start : float
            Absolute simulation time in hours at which the change from 'before' to 'after' is initiated
        """
        block_name = "SepLevelSP"
        bef, aft, dur, t_start = self._eng.get_sp_generic(block_name, nargout=4)
        return bef, aft, dur, t_start

    def set_reactor_level_sp(self, before=None, after=None, duration=0.0, start_time=None):
        """Setting the Reactor Level setpoint

        Parameters
        ----------
        before : float, optional
            Value of the setpoint before a change is initiated, by default the current setpoint value
        after : float, optional
            Value of the setpoint after a change is initiated, by default the current setpoint value
        duration : float, optional
            Duration of the change from 'before' to 'after' in (hours). Step change for duration = 0, ramp otherwise, by default 0.0
        start_time : float, optional
            Absolute simulation time in hours at which the change from 'before' to 'after' is initiated, by default the current simulation time
        """
        block_name = "ReactorLevelSP"
        self._set_sp_block_generic(block_name, before, after, duration, start_time)

    def get_reactor_level_sp(self):
        """Gets and returns the values for the Reactor Level setpoint

        Returns
        -------
        before : float
            Value of the setpoint before a change is initiated
        after : float
            Value of the setpoint after a change is initiated
        duration : float
            Duration of the change from 'before' to 'after' in (hours)
        t_start : float
            Absolute simulation time in hours at which the change from 'before' to 'after' is initiated
        """
        block_name = "ReactorLevelSP"
        bef, aft, dur, t_start = self._eng.get_sp_generic(block_name, nargout=4)
        return bef, aft, dur, t_start

    def set_reactor_press_sp(self, before=None, after=None, duration=0.0, start_time=None):
        """Setting the Reactor Pressure setpoint

        Parameters
        ----------
        before : float, optional
            Value of the setpoint before a change is initiated, by default the current setpoint value
        after : float, optional
            Value of the setpoint after a change is initiated, by default the current setpoint value
        duration : float, optional
            Duration of the change from 'before' to 'after' in (hours). Step change for duration = 0, ramp otherwise, by default 0.0
        start_time : float, optional
            Absolute simulation time in hours at which the change from 'before' to 'after' is initiated, by default the current simulation time
        """
        block_name = "ReactorPressSP"
        self._set_sp_block_generic(block_name, before, after, duration, start_time)

    def get_reactor_press_sp(self):
        """Gets and returns the values for the Reactor Pressure setpoint

        Returns
        -------
        before : float
            Value of the setpoint before a change is initiated
        after : float
            Value of the setpoint after a change is initiated
        duration : float
            Duration of the change from 'before' to 'after' in (hours)
        t_start : float
            Absolute simulation time in hours at which the change from 'before' to 'after' is initiated
        """
        block_name = "ReactorPressSP"
        bef, aft, dur, t_start = self._eng.get_sp_generic(block_name, nargout=4)
        return bef, aft, dur, t_start

    def set_g_in_product_sp(self, before=None, after=None, duration=0.0, start_time=None):
        """Setting the mole percentage of component g in the product (Quality) setpoint

        Parameters
        ----------
        before : float, optional
            Value of the setpoint before a change is initiated, by default the current setpoint value
        after : float, optional
            Value of the setpoint after a change is initiated, by default the current setpoint value
        duration : float, optional
            Duration of the change from 'before' to 'after' in (hours). Step change for duration = 0, ramp otherwise, by default 0.0
        start_time : float, optional
            Absolute simulation time in hours at which the change from 'before' to 'after' is initiated, by default the current simulation time
        """
        block_name = "MolePctGSP"
        self._set_sp_block_generic(block_name, before, after, duration, start_time)

    def get_g_in_product_sp(self):
        """Gets and returns the values for the mole percentage of component g in the product (Quality) setpoint

        Returns
        -------
        before : float
            Value of the setpoint before a change is initiated
        after : float
            Value of the setpoint after a change is initiated
        duration : float
            Duration of the change from 'before' to 'after' in (hours)
        t_start : float
            Absolute simulation time in hours at which the change from 'before' to 'after' is initiated
        """
        block_name = "MolePctGSP"
        bef, aft, dur, t_start = self._eng.get_sp_generic(block_name, nargout=4)
        return bef, aft, dur, t_start

    def set_ya_sp(self, before=None, after=None, duration=0.0, start_time=None):
        """Setting the YA setpoint

        Parameters
        ----------
        before : float, optional
            Value of the setpoint before a change is initiated, by default the current setpoint value
        after : float, optional
            Value of the setpoint after a change is initiated, by default the current setpoint value
        duration : float, optional
            Duration of the change from 'before' to 'after' in (hours). Step change for duration = 0, ramp otherwise, by default 0.0
        start_time : float, optional
            Absolute simulation time in hours at which the change from 'before' to 'after' is initiated, by default the current simulation time
        """
        block_name = "YASP"
        self._set_sp_block_generic(block_name, before, after, duration, start_time)

    def get_ya_sp(self):
        """Gets and returns the values for the YA setpoint

        Returns
        -------
        before : float
            Value of the setpoint before a change is initiated
        after : float
            Value of the setpoint after a change is initiated
        duration : float
            Duration of the change from 'before' to 'after' in (hours)
        t_start : float
            Absolute simulation time in hours at which the change from 'before' to 'after' is initiated
        """
        block_name = "YASP"
        bef, aft, dur, t_start = self._eng.get_sp_generic(block_name, nargout=4)
        return bef, aft, dur, t_start

    def set_yac_sp(self, before=None, after=None, duration=0.0, start_time=None):
        """Setting the YAC setpoint

        Parameters
        ----------
        before : float, optional
            Value of the setpoint before a change is initiated, by default the current setpoint value
        after : float, optional
            Value of the setpoint after a change is initiated, by default the current setpoint value
        duration : float, optional
            Duration of the change from 'before' to 'after' in (hours). Step change for duration = 0, ramp otherwise, by default 0.0
        start_time : float, optional
            Absolute simulation time in hours at which the change from 'before' to 'after' is initiated, by default the current simulation time
        """
        block_name = "YACSP"
        self._set_sp_block_generic(block_name, before, after, duration, start_time)

    def get_yac_sp(self):
        """Gets and returns the values for the YAC setpoint

        Returns
        -------
        before : float
            Value of the setpoint before a change is initiated
        after : float
            Value of the setpoint after a change is initiated
        duration : float
            Duration of the change from 'before' to 'after' in (hours)
        t_start : float
            Absolute simulation time in hours at which the change from 'before' to 'after' is initiated
        """
        block_name = "YACSP"
        bef, aft, dur, t_start = self._eng.get_sp_generic(block_name, nargout=4)
        return bef, aft, dur, t_start

    def set_reactor_temp_sp(self, before=None, after=None, duration=0.0, start_time=None):
        """Setting the Reactor Temperature setpoint

        Parameters
        ----------
        before : float, optional
            Value of the setpoint before a change is initiated, by default the current setpoint value
        after : float, optional
            Value of the setpoint after a change is initiated, by default the current setpoint value
        duration : float, optional
            Duration of the change from 'before' to 'after' in (hours). Step change for duration = 0, ramp otherwise, by default 0.0
        start_time : float, optional
            Absolute simulation time in hours at which the change from 'before' to 'after' is initiated, by default the current simulation time
        """
        block_name = "ReactorTempSP"
        self._set_sp_block_generic(block_name, before, after, duration, start_time)

    def get_reactor_temp_sp(self):
        """Gets and returns the values for the Reactor Temperature setpoint

        Returns
        -------
        before : float
            Value of the setpoint before a change is initiated
        after : float
            Value of the setpoint after a change is initiated
        duration : float
            Duration of the change from 'before' to 'after' in (hours)
        t_start : float
            Absolute simulation time in hours at which the change from 'before' to 'after' is initiated
        """
        block_name = "ReactorTempSP"
        bef, aft, dur, t_start = self._eng.get_sp_generic(block_name, nargout=4)
        return bef, aft, dur, t_start

    def set_recycle_valve_sp(self, before=None, after=None, duration=0.0, start_time=None):
        """Setting the Recycle Valve setpoint

        Parameters
        ----------
        before : float, optional
            Value of the setpoint before a change is initiated, by default the current setpoint value
        after : float, optional
            Value of the setpoint after a change is initiated, by default the current setpoint value
        duration : float, optional
            Duration of the change from 'before' to 'after' in (hours). Step change for duration = 0, ramp otherwise, by default 0.0
        start_time : float, optional
            Absolute simulation time in hours at which the change from 'before' to 'after' is initiated, by default the current simulation time
        """
        block_name = "RecycleValvePosSP"
        self._set_sp_block_generic(block_name, before, after, duration, start_time)

    def get_recycle_valve_sp(self):
        """Gets and returns the values for the Recycle Valve setpoint

        Returns
        -------
        before : float
            Value of the setpoint before a change is initiated
        after : float
            Value of the setpoint after a change is initiated
        duration : float
            Duration of the change from 'before' to 'after' in (hours)
        t_start : float
            Absolute simulation time in hours at which the change from 'before' to 'after' is initiated
        """
        block_name = "RecycleValvePosSP"
        bef, aft, dur, t_start = self._eng.get_sp_generic(block_name, nargout=4)
        return bef, aft, dur, t_start

    def set_steam_valve_sp(self, before=None, after=None, duration=0.0, start_time=None):
        """Setting the Steam Valve setpoint

        Parameters
        ----------
        before : float, optional
            Value of the setpoint before a change is initiated, by default the current setpoint value
        after : float, optional
            Value of the setpoint after a change is initiated, by default the current setpoint value
        duration : float, optional
            Duration of the change from 'before' to 'after' in (hours). Step change for duration = 0, ramp otherwise, by default 0.0
        start_time : float, optional
            Absolute simulation time in hours at which the change from 'before' to 'after' is initiated, by default the current simulation time
        """
        block_name = "SteamValvePosSP"
        self._set_sp_block_generic(block_name, before, after, duration, start_time)

    def get_steam_valve_sp(self):
        """Gets and returns the values for the Steam Valve setpoint

        Returns
        -------
        before : float
            Value of the setpoint before a change is initiated
        after : float
            Value of the setpoint after a change is initiated
        duration : float
            Duration of the change from 'before' to 'after' in (hours)
        t_start : float
            Absolute simulation time in hours at which the change from 'before' to 'after' is initiated
        """
        block_name = "SteamValvePosSP"
        bef, aft, dur, t_start = self._eng.get_sp_generic(block_name, nargout=4)
        return bef, aft, dur, t_start

    def set_agitator_sp(self, before=None, after=None, duration=0.0, start_time=None):
        """Setting the Agitator setpoint

        Parameters
        ----------
        before : float, optional
            Value of the setpoint before a change is initiated, by default the current setpoint value
        after : float, optional
            Value of the setpoint after a change is initiated, by default the current setpoint value
        duration : float, optional
            Duration of the change from 'before' to 'after' in (hours). Step change for duration = 0, ramp otherwise, by default 0.0
        start_time : float, optional
            Absolute simulation time in hours at which the change from 'before' to 'after' is initiated, by default the current simulation time
        """
        block_name = "AgitatorSpeedSP"
        self._set_sp_block_generic(block_name, before, after, duration, start_time)

    def get_agitator_sp(self):
        """Gets and returns the values for the Agitator setpoint

        Returns
        -------
        before : float
            Value of the setpoint before a change is initiated
        after : float
            Value of the setpoint after a change is initiated
        duration : float
            Duration of the change from 'before' to 'after' in (hours)
        t_start : float
            Absolute simulation time in hours at which the change from 'before' to 'after' is initiated
        """
        block_name = "AgitatorSpeedSP"
        bef, aft, dur, t_start = self._eng.get_sp_generic(block_name, nargout=4)
        return bef, aft, dur, t_start

    def _set_sp_block_generic(self, block_name, before=None, after=None, duration=0.0, start_time=None):
        """Sets all parameters of a generic setpoint block in the simulink model.

        Parameters
        ----------
        block_name : string
            Name of the Simulink Block
        before : float, optional
            Value of the setpoint before a change is initiated, by default the current setpoint value
        after : float, optional
            Value of the setpoint after a change is initiated, by default the current setpoint value
        duration : float, optional
            Duration of the change from 'before' to 'after' in (hours). Step change for duration = 0, ramp otherwise, by default 0.0
        start_time : float, optional
            Absolute simulation time in hours at which the change from 'before' to 'after' is initiated, by default the current simulation time
        """
        if None in [before, after]:
            bef, aft, dur, _ = self._eng.get_sp_generic(block_name, nargout=4)
            if before is None:
                before = bef
            if after is None:
                after = aft
            if start_time is None:
                t = self.get_workspace_variable('tout')
                current_time = t[-1]
                start_time = current_time
        self._eng.set_sp_generic(block_name, float(before), float(after), float(duration), float(start_time), nargout=0)

    # Data queries, setters and other utility methods

    def get_sim_status(self):
        """Provides the simulation status of the active Simulink model

        Returns
        -------
        status : string
            Takes on the values 'stopped' | 'updating' | 'initializing' | 'running' | 'paused' | 'terminating' | 'external'
        """
        return self._eng.get_simulation_status(nargout=1)

    def save_workspace(self, name):
        """Saves the workspace to a .mat file with the specifed name

        Parameters
        ----------
        name : mat file (.mat)
            Workspace saved in the .mat format
        """
        self._eng.eval("save('{}')".format(name), nargout=0)

    def get_workspace_variable(self, name):
        """Fetches a workspace variable from the MATLAB workspace to Python.

        Parameters
        ----------
        name : string
            Name of the desired workspace variable to obtain

        Returns
        -------
        np.floats, np.arrays
            Numeric primitives are returned as np.floats.
            Vectors are returned as np.arrays.
            Matrices are returned as np.arrays.
        """
        var = engineutils.get_variable(self._eng, name)
        if isinstance(var, float):
            var = np.float64(var)
        elif isinstance(var, Iterable):
            var = np.asarray(var)
        return var

    def set_simpause_time(self, absolute_pause_time):
        """Pauses Simulink simulation time at a specified time (in hours)

        Parameters
        ----------
        absolute_pause_time : float
            Absolute pause time in hours (i.e at hour 10.5)
        """
        self._eng.set_simpause_time(float(absolute_pause_time), nargout=0)

    def set_workspace_variable(self, name, value):
        """Sets a MATLAB workspace variable from Python

        Parameters
        ----------
        name : string
            string identifier for desired workspace variable
        value : np.floats, np.arrays
            1d arrays are set as vectors.
            2d arrays are set as matrices.
        """
        if isinstance(value, np.ndarray):
            if value.dtype in [int, float]:
                var = matlab.double(value.tolist())
            else:
                var = value.tolist()  # converted to cell-array in matlab
        elif isinstance(value, np.float):
            var = float(value)
        else:
            var = value
        engineutils.set_variable(self._eng, name, var)

    def isolate_recent_data_in_workspace(self, ref_time):
        """Extracts the parts of the timeseries simulation data in the MATLAB workspace for which t_sim > ref_time and
        and stores them in separate arrays in the MATlAB workspace.
        Created arrays are: latest_tout, latest_op_cost, latest_simout, latest_xmv, latest_setpoints, latest_idv_list

        Parameters
        ----------
        ref_time: float
            Absolute simulation time.
        """
        self.set_workspace_variable("t_current", ref_time)
        self._eng.isolate_recent_data_in_workspace(nargout=0)
