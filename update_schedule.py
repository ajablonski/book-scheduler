from sched import *
import pickle
import sys

# Arguments: data file, title

current_page = int(get_arg_with_flag('-p'))
data_file_name = get_arg_with_flag('-i')
data_file_dir = get_arg_with_flag('-d')
title = get_arg_with_flag('-t')
columns = int(get_arg_with_flag('-c'))

if data_file_dir == 0:
	data_file_dir = os.getcwd() + '\\'

if current_page == 0:
	current_page = get_current_progress(title)[0]
	
if data_file_name == 0:
	data_file_name = 'pickle.dat'
	
if columns == 0:
	columns = 1

with open(data_file_dir + data_file_name, 'r') as data_file:
	bookPart = pickle.load(data_file)

book = BookSchedule(bookPart._stop_file_path, bookPart._start, bookPart._end)

book.update_schedule(current_page)

book.write_schedule_to_file(data_file_dir + '/' + date.today().isoformat() + '.txt', columns)

with open(data_file_dir + data_file_name, 'w') as data_file:
	pickle.dump(book, data_file)
