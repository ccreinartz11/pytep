import matlab.engine  # The program doesn't execute if this is not imported before the simulation interface
import backend.siminterface

import time

n_pauses = [1, 2, 5, 10, 15, 20]

si = backend.siminterface.SimInterface.setup()

elapsed_times = {}
times_between_pauses = {}
total_sim_time = 50

# first simulation after start of the engine takes ca. 8 seconds longer than any following (no effect on results though)
si.reset()
print("Initial simtime: {}".format(si.process_data["time"].values[-1]))
t_start = time.perf_counter()
si.extend_simulation(total_sim_time)
si.simulate()
si.update()
t_end = time.perf_counter()

print("Time first run: {}".format(t_end-t_start))

# first simulation after start of the engine takes ca. 8 seconds longer than any following (no effect on results though)
si.reset()
print("Initial simtime: {}".format(si.process_data["time"].values[-1]))
t_start = time.perf_counter()
si.extend_simulation(total_sim_time)
si.simulate()
si.update()
t_end = time.perf_counter()

print("Time second run: {}".format(t_end-t_start))

# print("Final simtime: {}".format(si.process_data["time"].values[-1]))
# print(f"Simtime between pauses: {total_sim_time}")
# print("Elapsed real time {}".format(t_end-t_start))
#
# for np in n_pauses:
#     si.reset()
#     time_between_pauses = total_sim_time/np
#     print("Initial simtime: {}".format(si.process_data["time"].values[-1]))
#     t_start = time.perf_counter()
#     for counter in range(np):
#         si.extend_simulation(time_between_pauses)
#         si.simulate()
#         si.update()
#     t_end = time.perf_counter()
#     elapsed_times[np] = t_end - t_start
#     times_between_pauses[np] = time_between_pauses
#     print("Final simtime: {}".format(si.process_data["time"].values[-1]))
#     print(f"Simtime between pauses: {time_between_pauses}")
#     print("Elapsed real time {}".format(t_end-t_start))
#
# print(elapsed_times)
