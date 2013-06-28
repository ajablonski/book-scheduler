from sched import *
import sys
import pickle
import argparse

STOP_DEFAULT_NAME = '\stop.dat'
OUTPUT_DEFAULT_NAME = 'a.out'
		
parser = argparse.ArgumentParser('Create new schedule for book')

def slash_date(str):
	return datetime.strptime(str, "%m/%d/%Y").date()

parser.add_argument('-s', '--start', default=date.today(), type=slash_date,
	help = 'Start date, MM/DD/YY')
parser.add_argument('-e', '--end', required=True, type=slash_date,
	help = 'End date, MM/DD/YY')
parser.add_argument('-t', '--title',
	help = 'Title of book')
parser.add_argument('-o', '--output-file', type=os.path.normpath, default=OUTPUT_DEFAULT_NAME,
	help = 'Output file name')
parser.add_argument('-d', '--output-dir', default=os.getcwd() + '\\',
	help = 'Output file dir')
parser.add_argument('-p', '--stop-file', type=os.path.normpath, default=STOP_DEFAULT_NAME, required=True,
	help = 'Stop file location')
parser.add_argument('-c', '--columns', type=int, default=1,
	help = 'Columns')

args = parser.parse_args(sys.argv[1:])
book = BookSchedule(args.stop_file, args.start, args.end)
book.pickle_to_file(args.output_dir + 'pickle.dat')
book.write_schedule_to_file(args.output_file, args.columns)
