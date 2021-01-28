xInitial = xFinal;
SetPoint_Init(1,:) = setpoints(end);
SetPoint_Init(2,:) = setpoints(end);
SetPoint_Init(3,:) = zeros(1,12);
IDV_Init(1,:) = idv;
IDV_Init(2,:) = idv;
IDV_Init(3,:) = zeros(1,28);

tspan = [t, t+5];

