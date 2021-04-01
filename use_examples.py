### Example number one (creation of 1/3 of the novelty in my CCE tep paper in 14 lines)

from pytep.siminterface import SimInterface

tep_interface = SimInterface.setup()

save_dir = "./example_save_dir"
gains = [0.85, 0.9, 0.95, 1, 1.05, 1.1, 1.15]
for sp in tep_interface.setpoint_labels:
    sp_value = tep_interface.current_setpoint_value(sp)
    for g in gains:
        sp_target = g * sp_value
        tep_interface.reset()
        tep_interface.extend_simulation(100)
        tep_interface.ramp_setpoint(sp, sp_target, duration=0, delay=30)
        tep_interface.simulate()
        tep_interface.save(save_dir)


### Example number two (showcasing the interactive capabilities of pytep - not possible with any other simulator rn)

from pytep.siminterface import SimInterface
from planning.greedy_tep_planner import GreedyTEPPlanner

tep_interface = SimInterface.setup()
tep_interface.setup()
planner = GreedyTEPPlanner()
save_dir = "./example_save_dir"

planning_complete = False
current_tep_state = tep_interface.latest_process_data()
while not planner.goal_reached(current_tep_state):
    best_action = planner.plan(current_tep_state)
    tep_interface.ramp_setpoint(**best_action)
    tep_interface.extend_simulation(1)
    tep_interface.simulate()
    current_tep_state = tep_interface.latest_process_data()
    tep_interface.log_process_data()
tep_interface.save(save_dir)