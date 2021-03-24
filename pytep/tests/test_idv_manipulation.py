import pytep.siminterface


si = pytep.siminterface.SimInterface.setup()


def test_idv_manipulation_no_delay():
    si.reset()
    si.extend_simulation(1)
    si.set_idv(1, 0.5)
    si.simulate()
    si.update()
    assert si.get_idv(1) == 0.5


def test_idv_manipulation_with_delay():
    si.reset()
    si.extend_simulation(1)
    si.set_idv(2, 0.5, delay=1.5)
    si.simulate()
    si.update()
    before_activation = si.get_idv(2)
    si.extend_simulation(1)
    si.simulate()
    si.update()
    after_activation = si.get_idv(2)
    assert before_activation == 0
    assert after_activation == 0.5

