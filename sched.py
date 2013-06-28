from HTMLParser import HTMLParser
import urllib2
from string import ascii_letters
from datetime import *
import math
import os
import pickle
import sys

PROFILE_URL = 'http://www.goodreads.com/user/show/5917703-alex'

class BookStatFinder(HTMLParser):
    validBook = False
    current_title = ""
    desired_book = ""
    current_page = 0
    max_page = 0
    
    def set_book(self, title):
        self.desired_book = title.lower()
            
    def handle_starttag(self, tag, attrs):
        if (tag == 'a') and (('class', 'bookTitle') in attrs):
            self.validBook = True
            
    def handle_data(self, data):
        if data.find('page ') != -1 \
            and data.find('is on') == -1 \
            and self.current_title.find(self.desired_book) != -1:
                self.parse_progress(data)
        if self.validBook == True:
            self.current_title = data.lower()
            self.validBook = False

    def parse_progress(self, string):
        string = string.strip('()')
        string_els = string.split(' ')
        self.current_page = int(string_els[1])
        self.max_page = int(string_els[3])


class BookSchedule:

	_stop_points = []
	_stop_dict = {}
	_pages = 0
	_pages_per_day = 0
	schedule = []

	def __init__(self, break_file_loc, start = date.today(), end = date.today(), days = 0):
		if start == end and days == 0:
			raise Exception("Please supply time range information")
		elif start > end:
			raise Exception("Start date must be before end date")
		elif start == end:
			self._start = start
			self._end = self._start + timedelta(days=(days-1))
			self._days = days
		else:
			self._start = start
			self._end = end
			self._days = (self._end - self._start).days + 1
		self._stop_file_path = break_file_loc
		self.__read_stop_points()
		self._pages = self._stop_points[-1]
		self._pages_per_day = int(math.ceil(float(self._pages) / self._days))
		self.__make_dict()
		self.__make_schedule()

	def __read_stop_points(self):
		if self._stop_points == []:
			with open(self._stop_file_path) as f:
				for line in f:
					line.strip('\n')
					self._stop_points.append(int(line))

	def __make_dict(self):
		for page in range(self._pages, 0, -1):
			if self._stop_points.count(page) == 1:
				self._stop_dict[page] = page
				next_stop = page
			else:
				self._stop_dict[page] = next_stop

	def __make_schedule(self, current_page = -1, dateIn = date(1, 1, 1)):
		self.schedule = []
		if current_page == -1:
			current_page = self._pages_per_day  
		if dateIn == date(1, 1, 1):
			dateIn = self._start
		while current_page < self._pages:
			current_page = self._stop_dict[current_page]
			self.schedule.append((dateIn, current_page))
			dateIn += timedelta(days=1)
			if current_page != self._pages:
				current_page += self._pages_per_day
			if current_page >= self._pages:
				self.schedule.append((dateIn, self._pages))

	def print_schedule(self):
		for pair in self.schedule:
			print "Date: {} \t\t Page {}".format(pair[0].strftime('%b %d'), pair[1])
						
	def write_schedule_to_file(self, filename, cols=1):
		with open(filename, 'w') as out:
			for i in range(cols):
				out.write("|{:13} | {:4} | ".format(" Date", "Page"))
			out.write("\n")
			for i in range(cols):
				out.write("+{:-<14}+{:-<6}+ ".format('',''))
			out.write("\n")
			rows = int(math.ceil(float(len(self.schedule)) / cols))
			for i in range(rows):
				for j in range(cols):
					index = j*rows + i
					if index < len(self.schedule):
						pair = self.schedule[index]
						out.write("|{:13} | {:4} | ".format(pair[0].strftime(' %B %d'), pair[1]))
				out.write("\n")
	
	def pickle_to_file(self, filename):
		out_file = open(filename, 'w')
		pickle.dump(self, out_file)
		out_file.close()

	def update_schedule(self, current_page, date=date.today()):
		self.__make_schedule(current_page, date)
    

def get_current_progress(title):
	html_string = urllib2.urlopen(PROFILE_URL).read()
	
	search = BookStatFinder()
	search.set_book(title)
	search.feed(html_string)
	return (search.current_page, search.max_page)
