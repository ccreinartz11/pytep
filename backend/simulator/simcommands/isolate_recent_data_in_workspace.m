% use the current_time stored in the workspace to extract the simulation
% data that was added after the most recent start/continuation of the
% active simulation

latest_tout = tout(tout>t_current);
latest_op_cost = OpCost(tout>t_current);
latest_simout = simout(tout>t_current, :);
latest_xmv = xmv(tout>t_current, :);
latest_setpoints = setpoints(tout>t_current, :);
latest_idv_list = idv_list(tout>t_current, :);