import time

import pytep.matlab_bridge as matlab_bridge

bridge = matlab_bridge.MatlabBridge()


def test_sim_status_query():
    status_before_start = bridge.get_sim_status()
    bridge.set_simpause_time(1)
    bridge.start_simulation()
    status_during_sim = bridge.get_sim_status()
    time.sleep(2)
    status_after_sim = bridge.get_sim_status()
    bridge.set_simpause_time(2)
    bridge.continue_simulation()
    status_during_sim2 = bridge.get_sim_status()
    time.sleep(2)
    status_after_sim2 = bridge.get_sim_status()
    bridge.stop_simulation()
    status_after_stop = bridge.get_sim_status()

    assert status_before_start == 'stopped'
    assert status_during_sim == 'running'
    assert status_after_sim == 'paused'
    assert status_during_sim2 == 'running'
    assert status_after_sim2 == 'paused'
    assert status_after_stop == 'stopped'


def test_blocking_process_until_sim_paused():
    bridge.set_simpause_time(2)
    bridge.run_until_paused()
    status = bridge.get_sim_status()
    assert status == 'paused'


def test_reset_workspace():
    seed_init = bridge.get_workspace_variable('seed')
    bridge.set_workspace_variable('seed', 15000)
    seed_15000 = bridge.get_workspace_variable('seed')
    bridge.reset_workspace()
    seed_after_reset = bridge.get_workspace_variable('seed')
    assert seed_15000 == 15000
    assert seed_init == seed_after_reset
