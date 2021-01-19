load('TEP_state.mat', ...
    'x',...
    'sp',...
    'idv',...
    't'...
    )

load('InitVariables');
xInitial = x;
SetPoint_Init(1,:) = sp;
SetPoint_Init(2,:) = sp;
SetPoint_Init(3,:) = zeros(1,12);
IDV_Init(1,:) = idv;
IDV_Init(2,:) = idv;
IDV_Init(3,:) = zeros(1,28);

tspan = [t, t+100];

