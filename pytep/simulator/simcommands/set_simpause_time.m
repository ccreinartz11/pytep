function [] = set_simpause_time(simpause_time)
    set_param('MultiLoop_mode3/t_simpause','Value', string(simpause_time));
end

