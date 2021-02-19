import backend.siminterface

si = backend.siminterface.SimInterface.setup()


def test_production_ramp():
    si.extend_simulation(10)
    si.ramp_production(target_val=25, duration=5)
    si.ramp_agitator(target_val=90, slope=10)
    si.simulate()
    si.update()
    agit = si._setpoint_data['AgitatorSettingSP'].values
    assert si._setpoint_data['ProductionSP'].values[-1] == 25.0
