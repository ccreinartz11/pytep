from pytep.siminterface import SimInterface
from itertools import product
from pathlib import Path

tep = SimInterface.setup()

save_dir = Path("./save_scenarios").absolute()
durations = [0, 10, 20, 30, 40]
gains = [0.85, 0.9, 0.95, 1, 1.05, 1.1, 1.15]
for sp in tep.setpoint_labels:
    sp_value = tep.current_setpoint_value(sp)
    for d, g in product(durations, gains):
        sp_target = g * sp_value
        tep.reset()
        tep.ramp_setpoint(sp, sp_target,
                          duration=d, delay=30)
        tep.simulate(duration=1)
        tep.save_all(save_dir)


### Example number two (showcasing the interactive capabilities of pytep - not possible with any other simulator rn)

# from pytep.siminterface import SimInterface
# from planning.greedy_tep_planner import GreedyTEPPlanner
# 
# tep = SimInterface.setup()
# tep.setup()
# planner = GreedyTEPPlanner()
# save_dir = "./example_save_dir"
# 
# planning_complete = False
# current_tep_state = tep.latest_process_data()
# while not planner.goal_reached(current_tep_state):
#     best_action = planner.plan(current_tep_state)
#     tep.ramp_setpoint(**best_action)
#     tep.extend_simulation(1)
#     tep.simulate()
#     current_tep_state = tep.latest_process_data()
#     tep.log_process_data()
# tep.save(save_dir)