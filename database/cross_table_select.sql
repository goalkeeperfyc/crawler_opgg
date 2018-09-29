select * from time_shift.all_program_information, time_shift.first_play_parallel_machine where 
(channel='江苏卫视' and program_name='非诚勿扰' and program_start < '2018-01-06 23:05:10' and is_first_play='1')
 order by program_start desc;
