from sched import *
import pickle
import sys
import argparse

parser = argparse.ArgumentParser(description = 'Update existing schedule for book')

parser.add_argument('-d', '--df', type = os.path.normpath, default = os.path.join(os.getcwd(), 'pickle.dat'), help = 'data file directory', required=True)
parser.add_argument('-t', '--title', default = '', help = 'book title')
parser.add_argument('-c', '--columns', default = 1, type=int,
	help='number of columns to show')
parser.add_argument('-p', '--page', default = 0, type=int, help='current page of book')

args = parser.parse_args(sys.argv[1:])

if args.page == 0:
	args.page = get_current_progress(args.title)[0]

with open(args.df, 'r') as data_file:
	bookPart = pickle.load(data_file)

book = BookSchedule(bookPart._stop_file_path, bookPart._start, bookPart._end)

book.update_schedule(args.page)

book.write_schedule_to_file(os.path.join(os.path.dirname(args.df), date.today().isoformat() + '.txt'), args.columns)

with open(args.df, 'w') as data_file:
	pickle.dump(book, data_file)
