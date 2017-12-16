#!/usr/bin/env python
# -*- coding: utf-8 -*-

## known bugs ##
# FIXME: 'v-0106.avi' to 'V - Die Besucher 0x010.mkv'

## open todos ##

# FIXME renumber the exits

import os
from os.path import abspath, expanduser
from time import sleep


def expand_and_ensure_path(rel_path: str) -> str:
	val = abspath(expanduser(rel_path))
	ensure_dir(val)
	return val


def ensure_dir(f: str) -> None:
	d = os.path.dirname(f)
	if not os.path.exists(d):
		os.makedirs(d)


class directory_reader:
	def __init__(self, path=None):
		self.__path = path
		self.__files = None
	
	def set_dir(self, path: str) -> None:
		self.__path = path
	
	def pop_filename(self) -> str:
		"""pop a file from the last dir reading"""
		if self.__files is None or not len(self.__files):
			return None
		return self.__files.pop()
	
	def refresh(self) -> None:
		"""refresh the directory reading"""
		if self.__path is None:
			raise FileNotFoundError("No path specified!")
		expand_and_ensure_path(self.__path)
		try:
			self.__files = os.listdir(self.__path)
		except FileNotFoundError:
			raise FileNotFoundError("Could not read directory at path '%s', it doesn't exist" % self.__path)

class series_database:
	"""
	loads and holds a database in memory, answer questions to filenames
	"""
	def set_db_path(self, path: str) -> None:
		"""
		:param path: ability to specify a absolut/relativ path the the db file
		:return: None
		"""
		self._db_path = path
	
	def set_preprocessor_path(self, path: str) -> None:
		"""
		:param path: ability to specify a absolut/relativ path the the preprocessor file
		:return: None
		"""
		self.__preprocessor_path = path
	
	def set_seperator_path(self, path: str) -> None:
		"""
		:param path: ability to specify a absolut/relativ path the the seperator file
		:return: None
		"""
		self.__seperator_path = path
	
	def __init__(self):
		"""
		set the default relativ paths for all three database files
		"""
		self.__db_path = './series.db'
		self.__preprocessor_path = './preprocessor.list'
		self.__seperator_path = './seperator.list'
	
	def __init_db(self) -> None:
		"""
		init the variables for the database file
		:return: None
		"""
		self.__db_keywords = { }
		self.__db_tunings = { }
		self.__db_names = { }
	
	def __init_preprocessor(self) -> None:
		"""
		init the variables for the preprocessor file
		:return: None
		"""
		self.__preprocessor = []
		self.__preprocessor_searches = set()
	
	def __init_seperator(self) -> None:
		"""
		init the variable for the seperator file
		:return: None
		"""
		self.__seperator = []
	
	def __import_db_line(self, line_number: int, name: str, tuning: str, keywords: str) -> None:
		"""
		:param line_number: current line number which is beeing read
		:param name: name of the database entry
		:param tuning: the specified tuning for the database entry
		:param keywords: all keywords which should identify a file to the database entry (need to be lowercase)
		:return: None
		"""
		if name in self.__db_names:
			print("database entry '%s' in line %i is a duplicate, abort loading" % (name, line_number))
			exit(101)
		self.__db_names[line_number] = name
		if tuning not in ('animation', 'grain', 'film'):
			print("unsupported tuning found in line %i: '%s', abort loading" % (line_number, tuning))
			exit(100)
		self.__db_tunings[line_number] = tuning
		for keyword in keywords.split(','):
			if keyword in self.__db_keywords:
				print("Database inconsistent, line %i and line %i contain the same keyword '%s', abort loading"
				      % (self.__db_keywords[keyword], line_number, keyword))
				exit(111)
			if keyword != lower(keyword):
				print(
					"keyword '%s' in line %i is not lowercase, case sensitive matching isn't supported, abort loading"
					% (
					keyword, line_number))
				exit(123)
			self.__db_keywords[keyword] = line_number
	
	# FIXME: lasse einen Test laufen, ob ein eintrag in der DB reversibel ist, sprich nach dem Umbennenen wird mit
	# FIXME: Hilfe der Keywords die Serie erneut gefunden.
	
	def __import_preprocessor_line(self, line_number: int, search: str, replace: str) -> None:
		"""
		:param line_number: which line of the db file we're currently reading
		:param search: what's the search-phrase?
		:param replace: what's the replace-phrase?
		:return: None
		"""
		try:
			if not len(search):
				raise ValueError("preprocessor file: line %i has an empty search string" % line_number)
			elif not len(replace):
				raise ValueError("preprocessor file: line %i has an empty replace string" % line_number)
			elif search in self.__preprocessor_searches:
				raise ValueError("preprocessor file: search string '%s' was already added before" % search)
		except ValueError as e:
			print("preprocessor file inconsistent at line %i, abort loading" % int(line_number))
			print(e.message)
			exit(100)
		self.__preprocessor_searches.add(search)
		self.__preprocessor.append(search, replace)
	
	def __load_file(self, file_type: str) -> None:
		"""
		:param file_type: get a string which db filetype should be (re)loaded
		:return: None
		"""
		if file_type == "database":
			path = self.__db_path
			self.__init_db()
		elif file_type == "preprocessor":
			path = self.__preprocessor_path
			self.__init_preprocessor()
		elif file_type == "seperator":
			path = self.__seperator_path
			self.__init_seperator()
		else:
			print("unable to complete series_database.__load_file with this type: '%s'" % str(path))
			exit(111)
		try:
			file = open(path, 'r')
		except ValueError as e:
			print("unable to open %s file at path '%s', exiting now" % (file_type, str(path))
			print(e)
			exit(111)
			
			try:
				for line_number, line in enumerate(file):
					try:
						if file_type == "database":
							name, tuning, keywords = line.split(';')
						elif file_type == "preprocessor":
							search, replace = line.split(';')
						elif file_type == "seperator":
							if not len(line) == 1:
								raise ValueError
							seperator = line
					
					except ValueError:
						print("%s file inconsistent at line %i, abort loading" % (file_type, int(line_number)))
						exit(111)
					if file_type == "database":
						self.__import_db_line(line_number, name, tuning, keywords)
					elif file_type == "preprocessor":
						self.__import_preprocessor_line(line_number, search, replace)
					elif file_type == "seperator":
						self.__import_seperator_line(line_number, seperator)
			file.close()
		except:
			print("something went wrong reading the %s file" % file_type)
			exit(120)
	
	def load_databases(self) -> None:
		self.__load_file("database")
		self.__load_file("preprocessor")
		self.__load_file("seperator")
	
	def valid_file(self, filename) -> bool:
		"""
		:param filename:
		:return:
		"""


if __name__ == "__main__":
	input_path = "~/Downloads/"
	output_folder = "~/series/"
	dl_video_folder = "~/movies/"
	other_files_dir = "~/stuff/"
	too_less_numbers = input_path + "too less numbers/"
	too_many_numbers = input_path + "too many numbers/"
	series_unknown = input_path + "series unknown/"
	no_exact_match = input_path + "/no exact match/"
	tmp_folder = "/tmp/"
	
	ffmpeg = "ffmpeg"
	mkvinfo = "mkvinfo"
	mkvmerge = "mkvmerge"
	
	### Setting end ###
	
	input_path = expanduser(input_path)
	
	output_folder = expanduser(output_folder)
	dl_video_folder = expanduser(dl_video_folder)
	other_files_dir = expanduser(other_files_dir)
	move_other_files = True
	too_less_numbers = expanduser(too_less_numbers)
	too_many_numbers = expanduser(too_many_numbers)
	series_unknown = expanduser(series_unknown)
	no_exact_match = expanduser(no_exact_match)
	tmp_folder = expanduser(tmp_folder)
	
	# FIXME: todo list #
	
	# Replaces und den Suchwörtern der Eintrag wieder richtig zugeordnet
	
	# remove_strings = #do an import here
	# seperator = #do an import here
	
	print("Initialisation finished, reading database...", end='')
	
	db = series_database()
	db.load_databases()
	
	print("done.")
	
	print("reading input directory...", end='')
	
	dir_reader = directory_reader(input_path)
	dir_reader.refresh()
	
	print("done.\n")
	
	# FIXME: Old stuff - really needed?
	elements_done = False
	skip_file = False
	new_filename_ = ""
	counter = 0
	new_filename = []
	tmpint = 0
	next_word = ""
	words = []
	bIsAnMkvInputFile = False
	TuneProfile = "film"
	first_time__in_loop = 1
	
	while True:
		file = dir_reader.pop_filename()
		if file is None:
			print("Working queue is empty - wait 5 seconds before re-reading this directory")
			sleep(5)
			dir_reader.refresh()
			continue
		
		# FIXME: Old stuff - really needed?
		bIsAnMkvInputFile = False
		new_filename = ["dummyname", " ", "0", "0", "x", "0", "0", ".", "ext"]
		skip_file = False
		
		
	
	exit(0)
