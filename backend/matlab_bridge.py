import matlab
import matlab.engine
import numpy as np
from pathlib import Path
import time
from collections.abc import Iterable


import backend.engineutils as engineutils


class MatlabBridge:
    def __init__(self, model="MultiLoop_mode3", sim_path=None):
        self._model = model
        self._sim_path = (
            Path(__file__).parent / "simulator" if sim_path is None else sim_path
        )
        self._eng = matlab.engine.start_matlab()
        self.dir_to_path(self._sim_path)
        self._load_simulink()
        self._load_workspace()
        return

    def start_engine(self):
        self._eng = matlab.engine.start_matlab()
        return True

    def stop_engine(self):
        self._eng.quit()

    def run_simulation(self):
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

    def run_until_paused(self):
        self.run_simulation()
        self.block_until_sim_paused()

    def block_until_sim_paused(self):
        while not self.get_sim_status() == "paused":
            time.sleep(0.01)

    def start_simulation(self):
        self._eng.start_simulation(nargout=0)

    def continue_simulation(self):
        self._eng.continue_simulation(nargout=0)

    def pause_simulation(self):
        self._eng.pause_simulation(nargout=0)

    def stop_simulation(self):
        self._eng.stop_simulation(nargout=0)

    def get_sim_status(self):
        return self._eng.get_simulation_status(nargout=1)

    def set_simpause_time(self, absolute_pause_time):
        self._eng.set_simpause_time(float(absolute_pause_time), nargout=0)

    def save_workspace(self, name):
        self._eng.eval("save('{}')".format(name), nargout=0)

    def get_workspace_variable(self, name):
        """Fetches workspace variable from matlab workspace to python.
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

    def set_workspace_variable(self, name, value):
        """Sets matlab workspace variable from python.
        1d arrays are set as vectors.
        2d arrays are set as matrices.
        """
        if isinstance(value, np.ndarray):
            var = value.tolist()
        else:
            var = value
        engineutils.set_variable(self._eng, name, var)

    def _clear_workspace(self):
        self._eng.eval("clearvars", nargout=0)

    def reset_workspace(self):
        self._clear_workspace()
        self._load_workspace()

    def _load_simulink(self):
        self._eng.load_system(self._model)

    def dir_to_path(self, dir_path):
        self._eng.eval("addpath(genpath('{}'))".format(str(dir_path)), nargout=0)

    def _load_workspace(self):
        self._eng.eval("loadSimEnvironment", nargout=0)

    # Setpoint modification methods

    def set_production_sp(self, before=None, after=None, duration=0, start_time=None):
        block_name = "production_sp"
        self._set_sp_block_generic(block_name, before, after, duration, start_time)

    def get_production_sp(self):
        block_name = "production_sp"
        bef, aft, dur, t_start = self._eng.get_sp_generic(block_name, nargout=4)
        return bef, aft, dur, t_start

    def set_strip_level_sp(self, before=None, after=None, duration=0, start_time=None):
        block_name = "strip_level_sp"
        self._set_sp_block_generic(block_name, before, after, duration, start_time)

    def get_strip_level_sp(self):
        block_name = "strip_level_sp"
        bef, aft, dur, t_start = self._eng.get_sp_generic(block_name, nargout=4)
        return bef, aft, dur, t_start

    def set_sep_level_sp(self, before=None, after=None, duration=0, start_time=None):
        block_name = "sep_level_sp"
        self._set_sp_block_generic(block_name, before, after, duration, start_time)

    def get_sep_level_sp(self):
        block_name = "sep_level_sp"
        bef, aft, dur, t_start = self._eng.get_sp_generic(block_name, nargout=4)
        return bef, aft, dur, t_start

    def set_reactor_level_sp(self, before=None, after=None, duration=0, start_time=None):
        block_name = "reactor_level_sp"
        self._set_sp_block_generic(block_name, before, after, duration, start_time)

    def get_reactor_level_sp(self):
        block_name = "reactor_level_sp"
        bef, aft, dur, t_start = self._eng.get_sp_generic(block_name, nargout=4)
        return bef, aft, dur, t_start

    def set_reactor_press_sp(self, before=None, after=None, duration=0, start_time=None):
        block_name = "reactor_press_sp"
        self._set_sp_block_generic(block_name, before, after, duration, start_time)

    def get_reactor_press_sp(self):
        block_name = "reactor_press_sp"
        bef, aft, dur, t_start = self._eng.get_sp_generic(block_name, nargout=4)
        return bef, aft, dur, t_start

    def set_g_in_product_sp(self, before=None, after=None, duration=0, start_time=None):
        block_name = "g_in_product_sp"
        self._set_sp_block_generic(block_name, before, after, duration, start_time)

    def get_g_in_product_sp(self):
        block_name = "g_in_product_sp"
        bef, aft, dur, t_start = self._eng.get_sp_generic(block_name, nargout=4)
        return bef, aft, dur, t_start

    def set_ya_sp(self, before=None, after=None, duration=0, start_time=None):
        block_name = "ya_sp"
        self._set_sp_block_generic(block_name, before, after, duration, start_time)

    def get_ya_sp(self):
        block_name = "ya_sp"
        bef, aft, dur, t_start = self._eng.get_sp_generic(block_name, nargout=4)
        return bef, aft, dur, t_start

    def set_yac_sp(self, before=None, after=None, duration=0, start_time=None):
        block_name = "yac_sp"
        self._set_sp_block_generic(block_name, before, after, duration, start_time)

    def get_yac_sp(self):
        block_name = "yac_sp"
        bef, aft, dur, t_start = self._eng.get_sp_generic(block_name, nargout=4)
        return bef, aft, dur, t_start

    def set_reactor_temp_sp(self, before=None, after=None, duration=0, start_time=None):
        block_name = "reactor_temp_sp"
        self._set_sp_block_generic(block_name, before, after, duration, start_time)

    def get_reactor_temp_sp(self):
        block_name = "reactor_temp_sp"
        bef, aft, dur, t_start = self._eng.get_sp_generic(block_name, nargout=4)
        return bef, aft, dur, t_start

    def set_recycle_valve_sp(self, before=None, after=None, duration=0, start_time=None):
        block_name = "recycle_valve_sp"
        self._set_sp_block_generic(block_name, before, after, duration, start_time)

    def get_recycle_valve_sp(self):
        block_name = "recycle_valve_sp"
        bef, aft, dur, t_start = self._eng.get_sp_generic(block_name, nargout=4)
        return bef, aft, dur, t_start

    def set_steam_valve_sp(self, before=None, after=None, duration=0, start_time=None):
        block_name = "steam_valve_sp"
        self._set_sp_block_generic(block_name, before, after, duration, start_time)

    def get_steam_valve_sp(self):
        block_name = "steam_valve_sp"
        bef, aft, dur, t_start = self._eng.get_sp_generic(block_name, nargout=4)
        return bef, aft, dur, t_start

    def set_agitator_sp(self, before=None, after=None, duration=0, start_time=None):
        block_name = "agitator_sp"
        self._set_sp_block_generic(block_name, before, after, duration, start_time)

    def get_agitator_sp(self):
        block_name = "agitator_sp"
        bef, aft, dur, t_start = self._eng.get_sp_generic(block_name, nargout=4)
        return bef, aft, dur, t_start

    def _set_sp_block_generic(self, block_name, before=None, after=None, duration=0, start_time=None):
        """Sets all parameters of a generic setpoint block in the simulink model.

        Parameters
        ----------
        blockname: Name of the simulink block
        before: Value of the setpoint before a change is initiated (default: current setpoint value)
        after: Value of the setpoint before a change is initiated (default: current setpoint value)
        duration: Duration of the change from 'before' to 'after' in (h). Step change for duration == 0, ramp otherwise. (default: 0)
        start_time: Time in (h) at which the change from 'before' to 'after' is initiated(default: current simulation time)
        """

        if None in [before, after]:
            bef, aft, dur, t_start = self._eng.get_sp_generic(block_name, nargout=4)
            if before is None:
                before = bef
            if after is None:
                after = aft
            if start_time is None:
                t = self.get_workspace_variable('tout')
                current_time = t[-1]
                start_time = current_time
        self._eng.set_sp_generic(block_name, before, after, duration, start_time, nargout=0)
