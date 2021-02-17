clearvars;
loadSimEnvironment;
r1_0 = 500;
% SetPoint_Init(2,1) = 40;
% SetPoint_Init(3,1) = 20;
sim('MultiLoop_mode3', [0, 10]);
simout_save = simout(2:end,:);
tout_save = tout(2:end);
xmv_save = xmv(2:end,:);
setpoint_save = setpoints(2:end,:);

xInitial = xFinal;
sim('MultiLoop_mode3', [10, 20]);
simout = [simout_save; simout(2:end,:)];
tout = [tout_save; tout(2:end)];
xmv = [xmv_save; xmv(2:end,:)];
setpoints = [setpoint_save; setpoints(2:end,:)];