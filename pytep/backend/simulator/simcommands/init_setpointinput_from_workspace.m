block_names = ["ProductionSP", "StripLevelSP", "SepLevelSP", "ReactorLevelSP",...
    "ReactorPressSP", "MolePctGSP", "YASP", "YACSP", "ReactorTempSP", ...
    "RecycleValvePosSP", "SteamValvePosSP", "AgitatorSpeedSP"];

for idx = 1:12
    block_name = block_names(idx);
    set_sp_generic(block_name, setpoint_init(1, idx), setpoint_init(2, idx), ...
        setpoint_init(3, idx), setpoint_change_duration);
end

clearvars block_name block_names idx