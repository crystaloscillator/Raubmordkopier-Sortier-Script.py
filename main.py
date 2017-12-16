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

### Setting ###





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
	
	def set_dir(self, path: str) -> None:
		self.__path = path
	
	def get_file(self) -> str:
		"""pop a file from the last dir reading"""
	
	def read_dir(self) -> bool:
		if self.__path is None:
			return False
		expand_and_ensure_path(self.__path)
		try:
			os.chdir(self.__path)
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
	
	# Load db file
	# check for only 3 items
	# check second item for in ['animation', 'grain', 'film']
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
	
	print("done.")
	
	exit(0)

### FIXME: old version ###

try:
	os.chdir(input_path)
except FileNotFoundError:
	print("Error: Download-directory not found")
	exit(1)


def FixString(str: str) -> str:
	out = str
	for rem_str in remove_strings:
		if out.startswith(rem_str):
			out = out[-len(rem_str) - 1:]
		if out.endswith(rem_str):
			out = out[:len(out) - len(rem_str)]
	return out


def checkMKV(MkvInfo_txt: str) -> int:
	found = 0
	for line in MkvInfo_txt.split("\n"):
		if line.startswith("|  + Codec-ID:") and "A_VORBIS" in line:
			found += 1
		if line.startswith("|   + Abtastrate:") and "32000" in line:
			found += 1
	if (found % 2) == 0 and found != 0:
		return 0
	return 1


def ffmpegConvertIt(bMKV: bool, sInputFile: str, sTitle: str, sTune: str) -> list:
	# bMKV        - sets true to mkvinfo it, do not transcode if already transcoded
	# sInputFile  - Input filename
	# sTune       - Film or Animation Seriestype
	# sTitle      - The Title of the Series -> Output Filename + .mkv
	needTranscode = 0
	tmpFilename = sInputFile + "_ffmpg"
	outputPath = tmp_folder + sTitle + ".mkv"
	MuxToMkv = False
	try:
		shutil.move(sInputFile, tmpFilename)
	except:
		print("Error: Renaming " + sInputFile + " to " + tmpFilename + " failed")
		return [999, tmpFilename, "", MuxToMkv]
	
	cmd1 = [ffmpeg, "-i", tmpFilename, "-y", "-vcodec", "libx264", "-crf", "24", "-preset", "slow", "-tune", sTune, \
	        "-movflags", "+faststart", "-acodec", "libvorbis", "-qscale:a", "0", "-ar", "32000", "-scodec", "copy",
	        "-f", "matroska", \
	        "-metadata", 'title="' + sTitle + '"', outputPath]
	cmd2 = [ffmpeg, "-i", tmpFilename, "-y", "-vcodec", "copy", "-acodec", "copy", "-scodec", "copy", "-metadata",
	        'title="' + sTitle + '"', "-f", "matroska", outputPath]
	cmd3 = [mkvmerge, "-q", "--title", sTitle, "--default-language", "de", "-B", "-T", "--no-chapters", "-M",
	        "--no-global-tags", "--priority", "lower", tmpFilename, "-o", outputPath]
	
	if bMKV:
		print("Debug: This is an mkv, running mkvinfo...")
		try:
			needTranscode = checkMKV(check_output([mkvinfo, tmpFilename], stderr=STDOUT, universal_newlines=True))
		except CalledProcessError:
			return [998, tmpFilename, "", MuxToMkv]
	else:  # going to mkv it first
		MuxToMkv = True
	
	if needTranscode:
		cmd = cmd1
		print("   Transcoding A/V-Data with ffmpeg, this might take some while...")
	elif MuxToMkv:
		cmd = cmd2
		cmd[-1] = sInputFile + ".mkv"
		print("   Remuxing with ffmpeg to mkv to input-folder")
	else:
		print("   Remuxing with ffmpeg to mkv")
		cmd = cmd2
	errorcode = -1
	crashed = 0
	try:
		check_call(cmd, stdout=DEVNULL, stderr=DEVNULL)
	except CalledProcessError as e:
		crashed = 1
		errorcode = e.returncode
		if needTranscode:
			print("Error: While doing FFMPEG-Transcoding, return code: '" + str(e.returncode) + "'")
		else:
			print(
					"Error: While doing FFMPEG-Copy, return code: '" + str(
							e.returncode) + "', try to remux with mkvmerge")
	if not needTranscode and crashed:
		cmd = cmd3
		try:
			check_call(cmd, stdout=DEVNULL, stderr=DEVNULL)
			print("Debug: Successfully remuxed to mkv with mkvmerge")
			crashed = 0
		except CalledProcessError as e:
			errorcode = e.returncode
			print("Error: While doing mkvmerge-Copy, return code: '" + str(e.returncode) + "'")
	
	if crashed:
		return [errorcode, tmpFilename, "", MuxToMkv]
	else:
		return [0, tmpFilename, outputPath, MuxToMkv]


first_time_loop = 1
while True:
	
	if first_time_loop == 1:
		first_time_loop = 2
		print("Initialisation finished, loading directory...")
	
	if first_time_loop == 2:
		first_time_loop = False
		print("Working queue was completed - wait 5 seconds before re-reading this directory")
	
	elif elements_done:
		print("Working queue is empty - wait 5 seconds before re-reading this directory")
	
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
	
	# print("read download directory")
	files = os.listdir(os.getcwd())
	# print("got "+str(len(files))+" files")
	
	for file in files:
		bIsAnMkvInputFile = False
		# print("Filename: '"+str(file)+"'...")
		new_filename = ["dummyname", " ", "0", "0", "x", "0", "0", ".", "ext"]
		skip_file = False
		if len(file) < 5:
			continue
		elif len(file) >= 11:
			if file[-11:].lower() == ".crdownload":  # skip silently
				continue
			elif file[-11:].lower() == "desktop.ini":  # skip silently
				continue
		
		# ignore files like xxx.rar.001
		try:
			temp_int = int(file[-3:])
		except:
			temp_int = -1
		
		if file[-4:].lower() == ".avi":
			new_filename[8] = "avi"
		elif file[-5:].lower() == ".divx":
			new_filename[8] = "avi"
		elif file[-4:].lower() == ".ogm":
			new_filename[8] = "ogm"
		elif file[-4:].lower() == ".mkv":
			bIsAnMkvInputFile = True
			new_filename[8] = "mkv"
		elif file[-4:].lower() == ".mp4":
			new_filename[8] = "mp4"
		elif file[-4:].lower() == ".flv":
			new_filename[8] = "flv"
		elif file[-5:].lower() == ".part":  # skip silently
			continue
		elif file[-6:].lower() == "_crash":  # skip silently
			continue
		elif file[-6:].lower() == "_ffmpg":  # skip silently
			continue
		elif file[-5:].lower() == ".rar_":  # skip silently
			continue
		elif file[-4:].lower() == ".rar":  # skip silently
			continue
		elif file[-3:].lower() == ".7z":  # skip silently
			continue
		elif temp_int != -1:  # skip silently
			continue
		elif file[-4:].lower() == ".old":  # skip silently
			continue
		elif file[-3] == ".":
			skip_file = True
		elif file[-4] == ".":
			skip_file = True
		elif file[-5] == ".":
			skip_file = True
		elif isfile(file):
			print("Warning: no filetype detected, use AVI - should not happen!")
			new_filename[8] = "avi"
		else:  # folder
			continue
		
		elements_done = True
		
		if skip_file:
			if move_other_files:
				try:
					print("Info: No usable file-extension found, moving file '" + str(file) + "' to 'other files'")
					ensure_dir(other_files_dir + file)
					shutil.move(file, other_files_dir + file)
				except:
					print("Error: Can't move file '" + str(file) + "'")
					pass
			continue
		
		# seperate strings
		next_word = ""
		words = []
		fn = file.replace("S0", ".")  # import replaces here
		for char in fn:
			if char in seperators:
				if len(next_word) != 0:
					if next_word in remove_strings:
						next_word = ""
						continue
					words.append(FixString(next_word))
					next_word = ""
			else:
				next_word += char
		
		# get episode and season	exp-dexterxvid-s02e01.avi
		integers = [0, 0, 0, 0]
		lastCharWasInt = False
		counter = 0
		hundersOfEpisodes = False
		
		fn = file.replace("numb3rs", "numbers")  # import replaces2
		for char in fn:
			try:
				tmpint = int(char)
				if counter == 0:
					integers[0] = tmpint
				elif counter == 1 and lastCharWasInt:
					integers[1] = tmpint
				elif counter == 1 and not lastCharWasInt:  # we have 0x00
					integers[1] = integers[0]
					integers[0] = 0
					integers[2] = tmpint
					counter += 1
				elif counter == 2 and lastCharWasInt:  # we have --x000
					integers[3] = tmpint
					integers[2] = integers[1]
					integers[1] = integers[0]
					integers[0] = 0
					hundersOfEpisodes = True
				elif counter == 2 and not lastCharWasInt:
					integers[2] = tmpint
				elif counter == 3 and lastCharWasInt and not hundersOfEpisodes:
					integers[3] = tmpint
				elif counter == 3 and lastCharWasInt and HundersOfEpisodes:
					integers[0] = integers[1]
					integers[1] = integers[2]
					integers[2] = integers[3]
					integers[3] = tmpint
					hundersOfEpisodes = False
				
				lastCharWasInt = True
				counter += 1
			except:
				lastCharWasInt = False
		
		if counter > 4:
			try:
				print("Info: Too many numbers in filename, moving file '" + str(file) + "' to 'too many numbers'")
				ensure_dir(too_many_numbers + file)
				shutil.move(file, too_many_numbers + file)
			except:
				pass
			continue
		
		elif counter == 0:
			try:
				print("Info: No episode/season found, moving file '" + str(file) + "' to 'Filme'")
				ensure_dir(dl_video_folder + file)
				shutil.move(file, dl_video_folder + file)
			except:
				pass
			continue
		
		elif counter == 1:
			try:
				print("Info: Too less numbers in filename, moving file '" + str(file) + "' to 'too less numbers'")
				ensure_dir(too_less_numbers + file)
				shutil.move(file, too_less_numbers + file)
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
		
		found = []
		for word in words:
			try:
				found.append(str2no_lookup[word.lower()])
			except KeyError:
				pass
		
		# distinct list
		found = list(set(found))
		
		if 1 == len(found):
			new_filename[0] = no2title_lookup[found[0]]
			try:
				TuneProfile = no2tuning_lookup[str2no_lookup[word.lower()]]
			except KeyError:
				pass
		elif 1 < len(found):
			print("Info: No exact match found: " + str(found) + ", moving file '" + str(file) + "' to no exact match")
			try:
				ensure_dir(no_exact_match + file)
				shutil.move(file, no_exact_match + file)
			except:
				pass
			continue
		else:
			print("Info: Series unknown, moving file '" + str(file) + "' to series unknown")
			try:
				ensure_dir(series_unknown + file)
				shutil.move(file, series_unknown + file)
			except:
				pass
			continue
		
		# mkv it
		new_filename[-1] = "mkv"
		
		FileTitle = ""
		for string in new_filename[0:-2]:
			FileTitle += string
		
		print("'" + str(file) + "' to '" + str(FileTitle + ".mkv") + "'")
		
		ffmpeg_return = ffmpegConvertIt(bIsAnMkvInputFile, file, FileTitle, TuneProfile)
		
		input_file = ffmpeg_return[1]
		tmp_file = ffmpeg_return[2]
		JustMkvIt = ffmpeg_return[3]
		
		if ffmpeg_return[0] == 0:
			print("     Done.")
			if not JustMkvIt:
				print("   Moving file from temp-location to series-folder...")
				
				output_folder_ = output_folder + str(new_filename[0]) + '/' + str(new_filename[0]) + ' S' + str(
						new_filename[2]) + str(new_filename[3]) + '/'
				output_file = output_folder_ + FileTitle + ".mkv"
				
				# test if file already exists:
				if isfile(output_file):
					print("Warning: Output File Exists '" + output_file + "'")
					for tmp_int in range(2, 100):
						test_filename = output_folder_ + FileTitle + "_" + str(tmp_int) + ".mkv"
						if isfile(test_filename):
							print("Warning: Output File Exists '" + test_filename + "'")
						else:
							output_file = test_filename
							break
				# moving file, deleting input
				try:
					ensure_dir(output_file)
					shutil.move(tmp_file, output_file)
					print("     Done.")
				except:
					try:
						os.remove(output_file)
					except:
						pass
					print(
							"Error: can't move file '" + tmp_file + "' to output location '" + output_file + "', "
							                                                                                 "leaving "
							                                                                                 "it on "
							                                                                                 "temp-location")
					continue
			try:
				print("   Removing input-file...")
				os.remove(input_file)
				print("     Done.")
			except:
				print("Error: can't delete inputfile '" + str(input_file) + "' after reading with ffmpeg")
				continue
		elif ffmpeg_return[0] == 999:
			print("Warning: Removed from queue, retry on rescan")
		else:
			print("Error: process crashed on file '" + str(file) + "' with errorcode '" + str(ffmpeg_return[0]) + "'")
			try:
				shutil.move(input_file, file + "_crash")
			except:
				pass
	
	# print("Strg+C to cancel - sleeping for 5 sec")
	try:
		sleep(5)
	except KeyboardInterrupt:
		print("")
		exit(0)
