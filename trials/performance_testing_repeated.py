import pytep.siminterface

import time
import pandas as pd
from pathlib import Path
import pickle

si = pytep.siminterface.SimInterface.setup()

elapsed_times = {}
times_between_pauses = {}
total_sim_time = 50

# first simulation after start of the engine takes ca. 8 seconds longer than any following (no effect on results though)
si.reset()
t_start = time.perf_counter()
si.extend_simulation(50)
si.simulate()
si.update()
print("Final simtime: {}".format(si.process_data["time"].values[-1]))
t_end = time.perf_counter()

a = range(1, 11)
tbp = [0.05] + [aa/10 for aa in a] + [2, 3, 4, 5]

perf_data = pd.DataFrame(columns=tbp)

for idx in range(1):
    elapsed_times = {}
    a = range(1, 11)
    tbp = [0.05] + [aa / 10 for aa in a] + [2, 3, 4, 5, 10, 25, 50]
    for time_between_pauses in reversed(tbp):
        si.reset()
        current_time = 0
        print("Initial simtime: {}".format(si.process_data["time"].values[-1]))
        t_start = time.perf_counter()
        while current_time < total_sim_time:
            extend_time = min(time_between_pauses, total_sim_time-current_time)
            si.extend_simulation(extend_time)
            si.simulate()
            current_time = current_time + extend_time
        t_end = time.perf_counter()
        elapsed_times[time_between_pauses] = t_end - t_start
        print("Final simtime: {}".format(si.process_data["time"].values[-1]))
        print(f"Simtime between pauses: {time_between_pauses}")
        print("Elapsed real time {}".format(t_end-t_start))
    perf_data = perf_data.append(elapsed_times, ignore_index=True)
    perf_data.to_pickle(Path(__file__).parent / 'performance_50hour_simulations.pkl')


