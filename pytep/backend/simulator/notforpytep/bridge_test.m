loadSimEnvironment;
load_system('MultiLoop_mode3');
set_simpause_time(5);
for i = 1:10
    continue_simulation();
    get_param(gcs, 'SimulationStatus')
    while strcmp(get_param(gcs, 'SimulationStatus'), 'running')
        pause(0.1)
    end
    update_workspace();
    strcat("Time: ", string(tout(end)))
    set_simpause_time(tout(end) + 5);
end

%bdclose all