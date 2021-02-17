function [status] = get_simulation_status()
    status = get_param(gcs, 'SimulationStatus');
end

