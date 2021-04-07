# Example one

from pytep.siminterface import SimInterface
from itertools import product
from pathlib import Path

tep = SimInterface.setup()

save_dir = Path("./example_save").absolute()
durations = [0, 10, 20, 30, 40]
gains = [0.85, 0.9, 0.95, 1, 1.05, 1.1, 1.15]
for sp in tep.setpoint_labels:
    sp_value = tep.current_setpoint_value(sp)
    for d, g in product(durations, gains):
        sp_target = g * sp_value
        tep.reset()
        tep.ramp_setpoint(sp, sp_target,
                          duration=d, delay=30)
        tep.simulate(duration=100)
        tep.save_all(save_dir)

# Example two


from pytep.siminterface import SimInterface
from planning.tep_planner import TEPPlanner

tep = SimInterface.setup()
plnnr = TEPPlanner()

save_dir = Path("./example_save").absolute()
tep_state = tep.current_process_data()
while not plnnr.goal_reached(tep_state):
    best_action = plnnr.plan(tep_state)
    tep.ramp_setpoint(**best_action)
    tep.simulate(1)
    tep_state = tep.current_process_data()
tep.save_all(save_dir)
