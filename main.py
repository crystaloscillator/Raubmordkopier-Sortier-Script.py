#!/usr/bin/env python
# -*- coding: utf-8 -*-

## known bugs ##
# FIXME: 'v-0106.avi' to 'V - Die Besucher 0x010.mkv'

## open todos ##

# FIXME renumber the exits

import os
import shutil
from os.path import abspath, expanduser, isfile
from subprocess import CalledProcessError, DEVNULL, STDOUT, check_call, check_output
from time import sleep
from collections import namedtuple
from re import findall


def expand_and_ensure_path(rel_path: str) -> str:
	val = abspath(expanduser(rel_path))
	ensure_dir(val)
	return val

def ensure_dir(f: str) -> None:
	d = os.path.dirname(f)
	if not os.path.exists(d):
		os.makedirs(d)


def validate_mkv(filepath):
	MkvInfo_output = check_output([mkvinfo, filepath], stderr=STDOUT, universal_newlines=True)
	for line in MkvInfo_output.split("\n"):
		if line.startswith("|  + Codec-ID:") and "A_OPUS" in line:
			return 1
	return 0


def

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
		preprocessor = namedtuple('preprocessor', 'search replace')
		preprocessor.search = search
		preprocessor.replace = replace
		self.__preprocessor.append(preprocessor)
	
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
							search, replace = line.rstrip('\n').split(';')
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
	
	def valid_file(self, filename: str) -> tulple:
		"""
		:param filename: takes a filename
		:return: returns if the files is valid for processing
		"""
		if not type(filename) is str:
			return (False, False)
		
		if len(filename) < 5:
			return (False, False)
		if len(filename) >= 11:
			if filename[-11:].lower() == ".crdownload":
				return (False, False)
			elif filename[-11:].lower() == "desktop.ini":
				return (False, False)
		
		# ignore files like xxx.rar.001
		try:
			int(filename[-3:])
			return (False, False)
		except:
			pass
		
		if filename[-4:].lower() in (".avi", ".ogm", ".mp4", ".flv"):
			return (True, False)
		if filename[-4:].lower() == ".mkv":
			return (True, True)
		elif filename[-5:].lower() in (".divx", ".webm"):
			return (True, False)
		elif filename[-5:].lower() in (".part", ".rar_"):
			return (False, False)
		elif filename[-6:].lower() in ("_crash", "_ffmpg"):  # skip silently
			return (False, False)
		elif filename[-4:].lower() in (".rar", ".old", ".zip"):  # skip silently
			return (False, False)
		elif filename[-3:].lower() == ".7z":  # skip silently
			return (False, False)
		return (False, False)  # is a non-detectable filetype or a folder
	
	def preprocessor(self, filename: str) -> str:
		"""
		:param filename: input filename
		:return: returns preprocessed filename
		"""
		for preprocessor in self.__preprocessor:
			filename = filename.replace(preprocessor.search, preprocessor.replace)
		return filename
	
	def detect_series(self, filename: str, debug=False) -> int:
		"""
		:param filename: takes a string as input
		:param debug: if true, we print a verbose output of the detection
		:return: returns the number of the series according to the database keywords
		"""
		next_word = ""
		words = []
		for char in filename:
			if char in self.__seperator:
				if len(next_word) != 0:
					words.append(next_word)
					next_word = ""
			else:
				next_word += char
		
		found = []
		for word in words:
			if debug:
				print("Searching for words:")
				print("    " + word, end=' ')
			try:
				found.append(self.__db_keywords[word.lower()])
				if debug:
					print(" << found in database, Series no %i" % found[-1])
			except KeyError:
				print()
		
		# distinct list
		found = list(set(found))
		
		if len(found) == 1:
			return found[0]
		elif 1 < len(found):
			raise IndexError
		else:
			return -1
	
	def detect_season_episode(self, filename: str) -> tuple:
		"""
		runs a season + episode detection over a given filename
		:param filename: takes a preprocessed filename
		:return: returns a tuple: (season, episode)
		"""
		season, episode = 0, 0
		
		# old stuff
		integers = [0, 0, 0, 0]
		lastCharWasInt = False
		counter = 0
		hundersOfEpisodes = False
		# other old stuff
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
		# end of old stuff
		
		numbers = findall(r'\d+', filename)
		
		if len(numbers) == 2:
			season = numbers[0]
			episode = numbers[1]
			if 1 <= len(season) <= 2 and 1 <= len(episode) <= 2:
				return season, episode
			raise IndexError("invalid length for episode/season numbers")
			
		
		if counter > 4:
			try:
				print("Info: Too many numbers in filename, moving file '" + str(file) + "' to 'too many numbers'")
				move_file(filepath, too_many_numbers, input_filename)
			except:
				pass
			continue
		
		elif counter == 0:
			try:
				print("Info: No episode/season found, moving file '" + str(file) + "' to 'Filme'")
				move_file(filepath, dl_video_folder, input_filename)
			except:
				pass
			continue
		
		elif counter == 1:
			try:
				print("Info: Too less numbers in filename, moving file '" + str(file) + "' to 'too less numbers'")
				move_file(filepath, too_less_numbers, input_filename)
			except:
				pass
			continue
		
		elif counter == 2:
			integers[2] = integers[0]
			integers[3] = integers[1]
			integers[0] = 0
			integers[1] = 0
			hundersOfEpisodes = True
		
		if hundersOfEpisodes:
			new_filename[3] = "x"
			new_filename[4] = str(integers[1])
			new_filename[5] = str(integers[2])
			new_filename[6] = str(integers[3])
		
		else:
			new_filename[2] = str(integers[0])
			new_filename[3] = str(integers[1])
			new_filename[5] = str(integers[2])
			new_filename[6] = str(integers[3])
		
		return (season, episode)


def move_file(source: str, destination: str, filename: str) -> None:
	ensure_dir(destination + filename)
	shutil.move(source, destination + filename)


if __name__ == "__main__":
	input_path = "~/downloads/"
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
	
	while True:  #one loop per file
		# init vars
		valid_file, filetype_mkv = False, False
		output_filename = namedtuple('episode', 'name season episode file_extention tuning')
		
		#pop a filename from reader or reread directory
		input_filename = dir_reader.pop_filename()
		if file is None:
			print("Working queue is empty - wait 5 seconds before re-reading this directory")
			sleep(5)
			dir_reader.refresh()
			continue
		
		# validate file-extentions #FIXME: we need more magic here!
		valid_file, filetype_mkv = db.valid_file(input_path)
		filepath = input_path + '/' + input_filename
		if not valid_file:
			if isfile(filepath):  # make sure this isn't a directory
				try:
					print("Info: No usable file-extension found, moving file '%s' to 'other files'" % input_filename)
					move_file(filepath, other_files_dir, input_filename)
				except:
					print("Error: Can't move file '%s'" % input_filename)
				pass
			continue
		
		try:
			input_filename_preprocessed = db.preprocessor(input_filename)
			series_number = db.detect_series(input_filename_preprocessed)
			if series_number == -1:
				print("Info: Series unknown, moving file '%s' to series unknown" % str(input_filename))
				try:
					move_file(filepath, series_unknown, input_filename)
				except:
					print("Error: Can't move file '%s'" % input_filename)
				continue
			output_filename.name = db.get_name(series_number)  # FIXME method missing
			output_filename.tuning = db.get_tuning(series_number)  # FIXME method missing
			output_filename.season, output_filename.episode = db.detect_season_episode(input_filename_preprocessed)
		
		except IndexError as e:
			print("Info: No exact match found: %s, moving file '%s' to no exact match" % (str(found), input_filename))
			try:
				move_file(filepath, no_exact_match, input_filename)
			except:
				print("Error: Can't move file '%s'" % input_filename)
			continue
		
		
		# FIXME: Old stuff - really needed?
		bIsAnMkvInputFile = False
		skip_file = False
		
		
	
	exit(0)
