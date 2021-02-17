function [] = set_sp_generic(val_before, val_after, duration, delay)
    set_param('MultiLoop_mode3/BoundedRamp ',...
        'SP_before', string(val_before),...
        'SP_after', string(val_after),...
        'deltaT_Ramp', string(duration),...
        'tRampStart', string(delay)...
        )
end
