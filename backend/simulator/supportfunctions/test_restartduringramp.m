clearvars;
loadSimEnvironment;
SetPoint_Init(2,2) = 90;
SetPoint_Init(3,2) = 0;
SP_deltaTRamp = 0;
sim('MultiLoop_mode3', [0, 0.2]);
simout_save = simout(2:end,:);
tout_save = tout(2:end);
xmv_save = xmv(2:end,:);
setpoint_save = setpoints(2:end,:);

controller_init = controller_out_init;
if (exist('controller_init', 'var'))
    Eadj_0 = controller_init(end, 1);
    SP17_0 = controller_init(end, 2);
    Fp_0 = controller_init(end, 3);
    r1_0 = controller_init(end, 4);
    r4_0 = controller_init(end, 5);
    r5_0 = controller_init(end, 6);
    r6_0 = controller_init(end, 6);
    r7_0 = controller_init(end, 8);
end

controller_init = controller_out_init(end, :);
integrator_init = integrator_log(end, :);
xInitial = xFinal;
SetPoint_Init(1,2) = setpoints(end, 2);
SetPoint_Init(2,2) = 90;
SetPoint_Init(3,2) = 0;
SP_deltaTRamp = 0;
sim('MultiLoop_mode3', [0, 9.8]);
simout_with_break = [simout_save; simout(2:end,:)];
tout_with_break = [tout_save; tout(2:end)+tout_save(end)];
xmv_with_break = [xmv_save; xmv(2:end,:)];
setpoints_with_break = [setpoint_save; setpoints(2:end,:)];

clearvars -except simout_with_break tout_with_break xmv_with_break setpoints_with_break

loadSimEnvironment;
SetPoint_Init(2,2) = 90;
SetPoint_Init(3,2) = 0;
SP_deltaTRamp = 0;
sim('MultiLoop_mode3', [0, 10]);
simout_without_break = simout(2:end,:);
tout_without_break = tout(2:end);
xmv_without_break = xmv(2:end,:);
setpoints_without_break = setpoints(2:end,:);

sim_diff = simout_without_break - simout_with_break;
results_identical = ~any(sim_diff(:));
disp(results_identical)
