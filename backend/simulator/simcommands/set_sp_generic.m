function [] = set_sp_generic(block_name, val_before, val_after, duration, delay)
    set_param(strcat('MultiLoop_mode3/', block_name),...
        'SP_before', string(val_before),...
        'SP_after', string(val_after),...
        'deltaT_Ramp', string(duration),...
        'tRampStart', string(delay)...
        )
end
