from sched import *
import sys
import pickle

STOP_DEFAULT_NAME = '\stop.dat'
OUTPUT_DEFAULT_NAME = 'a.out'

# Arguments: title, stop_folder, end MM/DD/YYYY, start MM/DD/YYYY (optional), 
		
		
def display_help():
	print "Incorrect input"
	

# Check for output variable
start = get_arg_with_flag('-s')
end = get_arg_with_flag('-e')
title = get_arg_with_flag('-t')
output_file = get_arg_with_flag('-o')
output_dir = get_arg_with_flag('-d')
stop_file = get_arg_with_flag('-p')
columns = int(get_arg_with_flag('-c'))


if start != 0:
	start = datetime.strptime(start, '%m/%d/%Y').date()
else:
	start = date.today()

if end != 0:
	end = datetime.strptime(end, '%m/%d/%Y').date()
else:
	display_help()
	
if output_file == 0:
	output_file = OUTPUT_DEFAULT_NAME
	
if output_dir == 0:
	output_dir = os.getcwd() + '\\'
	
if stop_file == 0:
	stop_file = STOP_DEFAULT_NAME
stop_file = output_dir + stop_file

if columns == 0:
	columns = 1

book = BookSchedule(stop_file, start, end)

book.pickle_to_file(output_dir + 'pickle.dat')

book.write_schedule_to_file(output_dir + output_file, columns)
