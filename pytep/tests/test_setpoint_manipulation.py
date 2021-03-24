import pytep.siminterface

si = pytep.siminterface.SimInterface.setup()


def test_production_ramp():
    si.reset()
    si.extend_simulation(10)
    si.ramp_production(target_val=24, duration=5)
    si.simulate()
    si.update()
    assert si._setpoint_data['ProductionSP'].values[-1] == 24.0


def test_strip_level_ramp():
    si.reset()
    si.extend_simulation(10)
    si.ramp_stripper_level(target_val=60, duration=5)
    si.simulate()
    si.update()
    assert si._setpoint_data['StripLevelSP'].values[-1] == 60


def test_separator_level_ramp():
    si.reset()
    si.extend_simulation(10)
    si.ramp_separator_level(target_val=60, duration=5)
    si.simulate()
    si.update()
    assert si._setpoint_data['SepLevelSP'].values[-1] == 60


def test_reactor_level_ramp():
    si.reset()
    si.extend_simulation(10)
    si.ramp_reactor_level(target_val=60, duration=5)
    si.simulate()
    si.update()
    assert si._setpoint_data['ReactorLevelSP'].values[-1] == 60


def test_reactor_press_ramp():
    si.reset()
    si.extend_simulation(10)
    si.ramp_reactor_pressure(target_val=2750, duration=5)
    si.simulate()
    si.update()
    assert si._setpoint_data['ReactorPressSP'].values[-1] == 2750


def test_g_in_product_ramp():
    si.reset()
    si.extend_simulation(10)
    si.ramp_g_in_product(target_val=53, duration=5)
    si.simulate()
    si.update()
    assert si._setpoint_data['MolePctGSP'].values[-1] == 53


def test_ya_sp_ramp():
    si.reset()
    si.extend_simulation(10)
    si.ramp_ya(target_val=60, duration=5)
    si.simulate()
    si.update()
    assert si._setpoint_data['YASP'].values[-1] == 60


def test_yac_sp_ramp():
    si.reset()
    si.extend_simulation(10)
    si.ramp_yac(target_val=60, duration=5)
    si.simulate()
    si.update()
    assert si._setpoint_data['YACSP'].values[-1] == 60


def test_reactor_temp_ramp():
    si.reset()
    si.extend_simulation(10)
    si.ramp_reactor_temp(target_val=130, duration=5)
    si.simulate()
    si.update()
    assert si._setpoint_data['ReactorTempSP'].values[-1] == 130


def test_recycle_valve_pos_ramp():
    si.reset()
    si.extend_simulation(10)
    si.ramp_recycle_valve_pos(target_val=15, duration=5)
    si.simulate()
    si.update()
    assert si._setpoint_data['RecycleValvePosSP'].values[-1] == 15


def test_steam_valve_pos_ramp():
    si.reset()
    si.extend_simulation(10)
    si.ramp_steam_valve_pos(target_val=2, duration=5)
    si.simulate()
    si.update()
    assert si._setpoint_data['SteamValvePosSP'].values[-1] == 2


def test_agitator_speed_ramp():
    si.reset()
    si.extend_simulation(10)
    si.ramp_agitator_speed(target_val=80, duration=5)
    si.simulate()
    si.update()
    assert si._setpoint_data['AgitatorSpeedSP'].values[-1] == 80

