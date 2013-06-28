from sched import *
import pickle
import sys
import argparse

parser = argparse.ArgumentParser(description = 'Update existing schedule for book')

parser.add_argument('-i', '--df-name', default = 'pickle.dat', help = 'data file name')
parser.add_argument('-d', '--df-dir', default = os.getcwd() + '\\', help = 'data file directory')
parser.add_argument('-t', '--title', default = '', help = 'book title')
parser.add_argument('-c', '--columns', default = 0, type=int,
	help='number of columns to show')
parser.add_argument('-p', '--page', default = 0, type=int, help='current page of book')

args = parser.parse_args(sys.argv)

if args.page == 0:
	args.page = get_current_progress(args.title)[0]

with open(args.df_dir + args.df_name, 'r') as data_file:
	bookPart = pickle.load(data_file)

book = BookSchedule(bookPart._stop_file_path, bookPart._start, bookPart._end)

book.update_schedule(current_page)

book.write_schedule_to_file(args.df_dir  + '/' + date.today().isoformat() + '.txt', args.columns)

with open(args.df_dir + args.df_name, 'w') as data_file:
	pickle.dump(book, data_file)
