function [before, after, step_times] = get_idv_input_block_params()
    block_name = "MultiLoop_mode3/IDVInput";
    before = str2num(get_param(block_name, "Before"));
    after = str2num(get_param(block_name, "After"));
    step_times = str2num(get_param(block_name, "Time"));
end

