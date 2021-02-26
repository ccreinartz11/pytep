block_name = "MultiLoop_mode3/IDVInput";
set_param(block_name, "Before", mat2str(idv_init(1,:)))
set_param(block_name, "After", mat2str(idv_init(2,:)))
set_param(block_name, "Time", mat2str(idv_init(3,:)))
clearvars block_name