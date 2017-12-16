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
	
	def get_file(self) -> str:
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
	def set_db_path(self, path: str) -> None:
		self._db_path = path
	
	def set_preprocessor_path(self, path: str) -> None:
		self.__preprocessor_path = path
	
	def set_seperator_path(self, path: str) -> None:
		self.__seperator_path = path
	
	def __init__(self):
		self.__db_path = './series.db'
		self.__preprocessor_path = './preprocessor.list'
		self.__seperator_path = './seperator.list'
	
	def __init_db(self) -> None:
		self.__db_keywords = { }
		self.__db_tunings = { }
		self.__db_names = { }
	
	def __init_preprocessor(self) -> None:
		self.__preprocessor = []
		self.__preprocessor_searches = set()
	
	def __init_seperator(self) -> None:
		self.__seperator = []
	
	def __import_db_line(self, line_number: int, name: str, tuning: str, keywords: str) -> None:
		for keyword in keywords.split(','):
			if keyword in self.__db_keywords:
				print("Database inconsistent, line %i and line %i contain the same keyword '%s', abort loading"
				      % (self.__db_keywords[keyword], line, keyword))
				exit(111)
			if tuning not in ('animation', 'grain', 'film'):
				print("unsupported tuning found in line %i: '%s', abort loading" % (line_number, tuning))
				exit(100)
			self.__db_keywords[keyword] = line_number
			self.__db_names[line_number] = name
			self.__db_tunings[line_number] = tuning
	
	def __import_preprocessor_line(self, line_number: int, search: str, replace: str) -> None
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
	
	# check second item for in
	# check third items for beeing all lowercase, else print a warning
	# check for search string collisions
	# check for series names collisions
	# lasse einen Test laufen, ob ein eintrag in der DB reversibel ist, sprich nach dem Umbennenen wird mit hilfe der
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
	
	first_time__in_loop = 1
	while True:
		file = dir_reader.get_file()
		if file is None:
			print("Working queue is empty - wait 5 seconds before re-reading this directory")
			sleep(5)
			dir_reader.refresh()
			continue
		
	
	exit(0)
