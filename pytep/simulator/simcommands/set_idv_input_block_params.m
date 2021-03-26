function [] = set_idv_input_block_params(values_before, values_after, step_times)
    block_name = "MultiLoop_mode3/IDVInput";
    set_param(block_name, ...
    "Before", mat2str(values_before), ...
    "After", mat2str(values_after), ...
    "Time", mat2str(step_times))
end
