function [] = stop_simulation()
    set_param(gcs, 'SimulationCommand', 'stop')
end

