#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#KNOWN BUGS
#'v-0106.avi' to 'V - Die Besucher 0x010.mkv'
#   Remuxing with ffmpeg
#     Done.
#   Remuxing with mkvmerge
#     Done.
#
#
#

import os
import shutil
from time import sleep
from os.path import isfile
import subprocess

download_dir = "~/Downloads"
ffmpeg = "ffmpeg"+" "
output_folder = "~/Serien/"
dl_video_folder = "~/Filme/"
other_files_dir = "~/Downloads/other files/"
move_other_files = True
too_less_numbers = "~/Downloads/too less numbers/"
too_many_numbers = "~/Downloads/too many numbers/"
series_unknown = "~/Downloads/series unknown/"

conversation_dict = {}
conversation_dict2 = {}
conversation_dict["battlestar"] = 0
conversation_dict["battelstar"] = 0
conversation_dict["battlestard"] = 0
conversation_dict["galactica"] = 0
conversation_dict["bsg"] = 0
conversation_dict["bg"] = 0
conversation_dict2[0] = "Battlestar Galactica"
conversation_dict["dex"] = 1
conversation_dict["dexter"] = 1
conversation_dict2[1] = "Dexter"
conversation_dict["vd"] = 2
conversation_dict["tvd"] = 2
conversation_dict["vampire"] = 2
conversation_dict["diaries"] = 2
conversation_dict["vampdiar"] = 2
conversation_dict2[2] = "Vampire Diaries, The"
conversation_dict["moonlight"] = 3
conversation_dict2[3] = "Moonlight"
conversation_dict["adad"] = 4
conversation_dict["itgad"] = 4
conversation_dict["americandad"] = 4
conversation_dict["americandadx"] = 4
conversation_dict["ad"] = 4
conversation_dict["dad"] = 4
conversation_dict["american"] = 4
conversation_dict2[4] = "American Dad"
conversation_dict["wire"] = 5
conversation_dict2[5] = "Wire, The"
conversation_dict["fringe"] = 6
conversation_dict2[6] = "Fringe"
conversation_dict["universe"] = 7
conversation_dict["sgu"] = 7
conversation_dict2[7] = "Stargate Universe"
conversation_dict["mentalist"] = 8
conversation_dict["jane"] = 8
conversation_dict2[8] = "Mentalist, The"
conversation_dict["true"] = 9
conversation_dict["blood"] = 9
conversation_dict["tb"] = 9
conversation_dict["tblood"] = 9
conversation_dict["trueblood"] = 9
conversation_dict["truebloodxvid"] = 9
conversation_dict2[9] = "True Blood"
conversation_dict["detektiv"] = 10
conversation_dict["conan"] = 10
conversation_dict2[10] = "Detektiv Conan"
conversation_dict["homer"] = 11
conversation_dict["simpsons"] = 11
conversation_dict2[11] = "Simpsons, The"
conversation_dict["fear"] = 12
conversation_dict["itself"] = 12
conversation_dict2[12] = "Fear Itself"
conversation_dict["futu"] = 13
conversation_dict["futurama"] = 13
conversation_dict2[13] = "Futurama"
conversation_dict["numbers"] = 14
conversation_dict["numb3rs"] = 14
conversation_dict["numbrs"] = 14
conversation_dict2[14] = "Numb3rs"
conversation_dict["band"] = 15
conversation_dict["brother"] = 15
conversation_dict2[15] = "Band of Brother"
conversation_dict["house"] = 16
conversation_dict["hous"] = 16
conversation_dict["drh"] = 16
conversation_dict["drhouse"] = 16
conversation_dict2[16] = "Dr. House"
conversation_dict["happy"] = 17
conversation_dict["tree"] = 17
conversation_dict2[17] = "Happy Tree Friends"
conversation_dict["eureka"] = 18
conversation_dict["eur"] = 18
conversation_dict2[18] = "EUReKA"
conversation_dict["men"] = 19
conversation_dict["twoandahalfmen"] = 19
conversation_dict2[19] = "Two and a Half Men"
conversation_dict["bn"] = 20
conversation_dict["burn"] = 20
conversation_dict["burnnotice"] = 20
conversation_dict2[20] = "Burn Notice"
conversation_dict["atlantis"] = 21
conversation_dict2[21] = "Stargate Atlantis"
conversation_dict["sgeins"] = 22
conversation_dict2[22] = "Stargate SG1"
conversation_dict["kino"] = 23
conversation_dict2[23] = "Stargate Universe - Kino"
conversation_dict["unit"] = 26
conversation_dict["unitrp"] = 26
conversation_dict["tu"] = 26
conversation_dict2[26] = "Unit, The"
conversation_dict["haven"] = 25
conversation_dict2[25] = "Haven"
conversation_dict["family"] = 24
conversation_dict["famguy"] = 24
conversation_dict["fg"] = 24
conversation_dict["familyguy"] = 24
conversation_dict2[24] = "Family Guy"
conversation_dict["scrubs"] = 27
conversation_dict2[27] = "Scrubs"
conversation_dict["chaos"] = 28
conversation_dict2[28] = "Chaos City"
conversation_dict["bigbangtheory"] = 29
conversation_dict["bumm"] = 29
conversation_dict["tbbt"] = 29
conversation_dict["theory"] = 29
conversation_dict["nerdgeekshow"] = 29
conversation_dict["theory"] = 29
conversation_dict["big"] = 29
conversation_dict["bang"] = 29
conversation_dict["tbbt"] = 29
conversation_dict2[29] = "Big Bang Theory, The"
conversation_dict["navicis"] = 30
conversation_dict["navycis"] = 30
conversation_dict["ncis"] = 30
conversation_dict["navy"] = 30
conversation_dict["cis"] = 30
conversation_dict2[30] = "Navy CIS"
conversation_dict["tos"] = 31
conversation_dict2[31] = "Raumschiff Enterprise"
conversation_dict["fallingskies"] = 32
conversation_dict["falling"] = 32
conversation_dict["skies"] = 32
conversation_dict2[32] = "Falling Skies"
conversation_dict["aeon"] = 33
conversation_dict["flux"] = 33
conversation_dict2[33] = "Aeon Flux"
conversation_dict["v"] = 34
conversation_dict2[34] = "V - Die Besucher"
conversation_dict["hellsing"] = 35
conversation_dict2[35] = "Hellsing"
conversation_dict["spartacus"] = 36
conversation_dict["sparta"] = 36
conversation_dict2[36] = "Spartacus"
conversation_dict["soul"] = 37
conversation_dict["eater"] = 37
conversation_dict2[37] = "Soul Eater"
conversation_dict["stromberg"] = 38
conversation_dict2[38] = "Stromberg"
conversation_dict["cowboy"] = 39
conversation_dict["bebop"] = 39
conversation_dict2[39] = "Cowboy Bebop"
conversation_dict["stv"] = 40
conversation_dict["voya"] = 40
conversation_dict2[40] = "Star Trek Voyager"
conversation_dict["enterprise"] = 41
conversation_dict2[41] = "Star Trek Enterprise"
conversation_dict["got"] = 42
conversation_dict["gamethrones"] = 42
conversation_dict["thrones"] = 42
conversation_dict2[42] = "Game of Thrones"
conversation_dict["tng"] = 43
conversation_dict2[43] = "Star Trek The Next Generation"
conversation_dict["continuum"] = 44
conversation_dict2[44] = "Continuum"
conversation_dict["prisoner"] = 45
conversation_dict2[45] = "Prisoner, The"
conversation_dict["mother"] = 46
conversation_dict["himym"] = 46
conversation_dict["swarley"] = 46
conversation_dict2[46] = "How I Met Your Mother"
conversation_dict["anarchy"] = 47
conversation_dict["sons"] = 47
conversation_dict["sofsoa"] = 47
conversation_dict2[47] = "Sons Of Anarchy"
conversation_dict["vik"] = 48
conversation_dict["viki"] = 48
conversation_dict2[48] = "Vikings"
conversation_dict["breaking"] = 49
conversation_dict["breakingbad"] = 49
conversation_dict2[49] = "Breaking Bad"
conversation_dict["upon"] = 50
conversation_dict2[50] = "Once Upon a Time"
conversation_dict["dead"] = 51
conversation_dict2[51] = "Dead Like Me"

remove_strings = ["dxvid", "xvid", "staffel", "episode", "the", "german", "ger", "intro", "ep", "avi", "divx", "flv", "ogm", "ac3", "0W4", "x264", "p0w4", "Prim3time", "1980", "1981", "1982", "1983", "1984", "1985", "1986", "1987", "1988", "1989", "1990", "1991", "1992", "1993", "1994", "1995", "1996", "1997", "1998", "1999", "2000", "2001", "2002", "2003", "2004", "2005", "2006", "2007", "2008", "2009", "2010", "2011", "2012", "2013", "2014", "1080p", "720p"]
seperators = ["_", " ", ".", "-", ","]
try:
	os.chdir(download_dir)
except FileNotFoundError:
	print("Error: Download-Directory not found")
	exit(1)

def FixString(str):
	out = str
	for rem_str in remove_strings:
		if out.startswith(rem_str):
			out = out[-len(rem_str)-1:]
		if out.endswith(rem_str):
			out = out[:len(out)-len(rem_str)]
	return out
	
def mkvIt(new_filename_, file):
	return os.system('mkvmerge -q -o "'+output_folder+new_filename_+'" --title "'+new_filename_[:-4]+'" --default-language de -B -T --no-chapters -M --no-global-tags --priority lower "'+file+'"')
	
def ffmpegConvertIt(file, file_, new_file):
	try:
		shutil.move(file, file_)
	except:
		print("rename "+file+" to "+file_+" failed")
		return 999
	#return os.system(ffmpeg+' -y -vcodec copy -acodec copy -scodec copy -i "'+file_+'" "'+new_file+'"')
	nulfp = open(os.devnull, "w")
	cmd = ffmpeg+' -i "'+file_+'" -y -vcodec copy -acodec copy -scodec copy  "'+new_file+'"'
	p = subprocess.Popen(cmd, stdout=None, stderr=nulfp.fileno())
	#win32process.SetPriorityClass(p, win32process.BELOW_NORMAL_PRIORITY_CLASS) #win32process.IDLE_PRIORITY_CLASS
	tmpint = p.wait()
	nulfp.close()
	return tmpint
	
first_time_loop = 1
while True:

	if first_time_loop == 1:
		first_time_loop = 2
		print("Initialisation finished, loading directory...")
		
	if first_time_loop == 2:
		first_time_loop = False
		print("Working queue was completed - waiting 5 sec before rescan directory")
		
	elif elements_done:
		print("Working queue is empty - waiting 5 sec before rescan directory")
		
	elements_done = False
	skip_file = False
	new_filename_ = ""
	counter = 0
	new_filename = []
	tmpint = 0
	next_word = ""
	words = []

	#print("read download directory")
	files = os.listdir(os.getcwd())
	#print("got "+str(len(files))+" files")

	for file in files:
		#print("Filename: '"+str(file)+"'...")
		new_filename = ["dummyname"," ","0","0","x","0","0",".","ext"]
		skip_file = False
		if len(file) < 5:
			continue
		elif len(file) >= 11:
			if file[-11:].lower() == ".crdownload": #skip silently
				continue
			elif file[-11:].lower() == "desktop.ini": #skip silently
				continue
		
		#ignore files like xxx.rar.001
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
			new_filename[8] = "mkv"
		elif file[-4:].lower() == ".mp4":
			new_filename[8] = "mp4"
		elif file[-4:].lower() == ".flv":
			new_filename[8] = "flv"
		elif file[-5:].lower() == ".part": #skip silently
			continue
		elif file[-6:].lower() == "_crash": #skip silently
			continue
		elif file[-6:].lower() == "_ffmpg": #skip silently
			continue
		elif file[-5:].lower() == ".rar_": #skip silently
			continue
		elif file[-4:].lower() == ".rar": #skip silently
			continue
		elif file[-3:].lower() == ".7z": #skip silently
			continue
		elif temp_int != -1: #skip silently
			continue
		elif file[-4:].lower() == ".old": #skip silently
			continue
		elif file[-3] == ".":
			skip_file = True
		elif file[-4] == ".":
			skip_file = True
		elif file[-5] == ".":
			skip_file = True
		elif isfile(file):
			print(" - no filetype detected, use AVI - should not happend!")
			new_filename[8] = "avi"
		else: #folder
			continue
			
		elements_done = True
		
		if skip_file:
			if move_other_files:
				try:
					print("moving file '"+str(file)+"' to 'other files'")
					shutil.move(file, other_files_dir+file)
				except:
					print("ERROR: Can't move file '"+str(file)+"'")
					pass
			continue
		
		print(" - working...")
		
		#seperate strings
		next_word = ""
		words = []
		fn = file.replace("S0", ".").replace("S1", ".").replace("S2", ".").replace("s0", ".").replace("s1", ".").replace("s2", ".").replace("numb3rs", "numbers").replace("Numb3rs", "numbers").replace("AC3", "").replace("sg1", "sgeins").replace("SG1", "sgeins").replace("crow_s", "scrubs").replace("SC_", "scrubs_").replace("crow-s", "scrubs_").replace("720p", " ").replace("x264", " ").replace("gtvg-fr", "fringe").replace("futu", "futurama ")
		fn = fn.replace("0", " ").replace("1", " ").replace("2", " ").replace("3", " ").replace("4", " ").replace("5", " ").replace("6", " ").replace("7", " ").replace("8", " ").replace("9", " ").replace("Teil.2", "_").replace("teil.2", "_").replace("Teil2", "_").replace("teil2", "_").replace("Teil.2", "_").replace("Teil.1", "_").replace("teil.1", "_").replace("Teil1", "_").replace("teil1", "_").replace("Teil.1", "_")
		for char in fn:
			if char in seperators:
				if len(next_word)!=0:
					if next_word in remove_strings:
						next_word = ""
						continue
					words.append( FixString(next_word) )
					next_word = ""
			else:
				next_word += char
		
		#get episode and season	exp-dexterxvid-s02e01.avi
		integers = [0, 0, 0, 0]
		lastCharWasInt = False
		counter = 0
		hundersOfEpisodes = False
		
		fn = file.replace("numb3rs", "numbers") \
		.replace("Numb3rs", "numbers") \
		.replace("AC3", "") \
		.replace("sg1", "sgeins") \
		.replace("SG1", "sgeins") \
		.replace("Episode 1.", "Episode 01.") \
		.replace("Episode 2.", "Episode 02.") \
		.replace("Episode 3.", "Episode 03.") \
		.replace("Episode 4.", "Episode 04.") \
		.replace("Episode 5.", "Episode 05.") \
		.replace("Episode 6.", "Episode 06.") \
		.replace("Episode 7.", "Episode 07.") \
		.replace("Episode 8.", "Episode 08.") \
		.replace("Episode 9.", "Episode 09.") \
		.replace("Season 1,", "Season 01,") \
		.replace("Season 2,", "Season 02,") \
		.replace("Season 3,", "Season 03,") \
		.replace("Season 4,", "Season 04,") \
		.replace("Season 5,", "Season 05,") \
		.replace("Season 6,", "Season 06,") \
		.replace("Season 7,", "Season 07,") \
		.replace("Season 8,", "Season 08,") \
		.replace("Season 9,", "Season 09,") \
		.replace("Dexter.5", "Dexter.05x") \
		.replace("Dexter.5", "Dexter.05") \
		.replace("dexter5", "Dexter.05") \
		.replace("Dexter.6", "Dexter.06x") \
		.replace("Dexter.6", "Dexter.06") \
		.replace("Dexter.7", "Dexter.07x") \
		.replace("Dexter.7", "Dexter.07") \
		.replace("dexter7", "Dexter.07") \
		.replace("dexter7", "Dexter.07") \
		.replace("homer20", "homer 20x") \
		.replace("homer21", "homer 21x") \
		.replace("homer22", "homer 22x") \
		.replace("homer23", "homer 23x") \
		.replace("homer24", "homer 24x") \
		.replace("homer25", "homer 25x") \
		.replace("homer26", "homer 26x") \
		.replace("homer27", "homer 27x") \
		.replace("720p", " ") \
		.replace("x264", " ") \
		.replace("P0W4", " ") \
		.replace("GhostUp10", " ") \
		.replace("Prim3time", " ") \
		.replace("1980", " ") \
		.replace("1981", " ") \
		.replace("1982", " ") \
		.replace("1983", " ") \
		.replace("1984", " ") \
		.replace("1985", " ") \
		.replace("1986", " ") \
		.replace("1987", " ") \
		.replace("1988", " ") \
		.replace("1989", " ") \
		.replace("1990", " ") \
		.replace("1991", " ") \
		.replace("1992", " ") \
		.replace("1993", " ") \
		.replace("1994", " ") \
		.replace("1995", " ") \
		.replace("1996", " ") \
		.replace("1997", " ") \
		.replace("1998", " ") \
		.replace("1999", " ") \
		.replace("2000", " ") \
		.replace("2001", " ") \
		.replace("2002", " ") \
		.replace("2003", " ") \
		.replace("2004", " ") \
		.replace("2005", " ") \
		.replace("2006", " ") \
		.replace("2007", " ") \
		.replace("2008", " ") \
		.replace("2009", " ") \
		.replace("2010", " ") \
		.replace("2011", " ") \
		.replace("2012", " ") \
		.replace("Teil.2", "_") \
		.replace("teil.2", "_") \
		.replace("Teil2", "_") \
		.replace("teil2", "_") \
		.replace("Teil.2", "_") \
		.replace("Teil.1", "_") \
		.replace("teil.1", "_") \
		.replace("Teil1", "_") \
		.replace("teil1", "_") \
		.replace("Teil.1", "_") \
		.replace("c0nFuSed", "confused") \
		.replace(".mp4", ".mpv") \
		.replace("stream2", "stream zwei") \
		.replace("720i", "_") \
		.replace("720p", "_") \
		.replace("720", "_") \
		.replace("1080i", "_") \
		.replace("1080p", "_") \
		.replace("1080", "_") \
		.replace("R5", "_") \
		.replace("stream.4.kinox", "_") \
		.replace("sofsoa1", "sofsoa01 ") \
		.replace("sofsoa2", "sofsoa02 ") \
		.replace("sofsoa3", "sofsoa03 ") \
		.replace("gu10", " ") \
		.replace("S1 S01E", "01") \
		.replace("S1 S02E", "02") \
		.replace("S1 S03E", "03") \
		.replace("3D", "_")
		for char in fn:
			try:
				tmpint = int(char)
				if counter == 0:
					integers[0] = tmpint
				elif counter == 1 and lastCharWasInt:
					integers[1] = tmpint
				elif counter == 1 and not lastCharWasInt: #we have 0x00
					integers[1] = integers[0]
					integers[0] = 0
					integers[2] = tmpint
					counter += 1
				elif counter == 2 and lastCharWasInt: #we have --x000
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
				print("too many numbers in filename, moving file '"+str(file)+"' to 'too many numbers'")
				shutil.move(file, too_many_numbers+file)	
			except:
				pass
			continue
		
		elif counter == 0:
			try:
				print("error while parsing episode/season, moving file '"+str(file)+"' to 'Filme'")
				shutil.move(file, dl_video_folder+file)
			except:
				pass
			continue
			
		elif counter == 1:
			try:
				print("too less numbers in filename, moving file '"+str(file)+"' to 'too less numbers'")
				shutil.move(file, too_less_numbers+file)
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
			
		found = False
		for word in words:
			if word.lower() in conversation_dict:
				new_filename[0] = conversation_dict2[conversation_dict[word.lower()]]
				found = True
				break
		if not found:
			try:
				print("Series unknown, moving file '"+str(file)+"' to series unknown")
				shutil.move(file, series_unknown+file)
			except:
				pass
			continue
		
		#mkv it
		new_filename[-1] = "mkv"
		
		new_filename_ = ""
		for string in new_filename:
			new_filename_ += string
		
		tmp_int = 2
		if isfile(output_folder+new_filename_):
			print("WARNING: Output File Exists '"+str(new_filename_)+"'")
			while tmp_int < 100:
				new_filename_tmp = new_filename_[:-4]+"_"+str(tmp_int)+new_filename_[-4:]
				if isfile(output_folder+new_filename_tmp):
					print("WARNING: Output File Exists '"+str(new_filename_)+"'")
					tmp_int+=1
				else:
					new_filename_ = new_filename_tmp
					break
		print("'"+str(file)+"' to '"+str(new_filename_)+"'")
		
		new_file = file+".avi"
		print("   Remuxing with ffmpeg")
		
		tmp_file = file+"_ffmpg"
		
		returnvalue = ffmpegConvertIt(file, tmp_file, new_file)
		
		if returnvalue == 0:
			print("     Done.")
			try:
				os.remove(tmp_file)
			except:
				print("can't delete inputfile '"+str(tmp_file)+"' after remuxing with ffmpeg")
				continue
			
			file = new_file
			
			print("   Remuxing with mkvmerge")
			
			if mkvIt(new_filename_, file) == 0:
				print("     Done.")
				try:
					os.remove(file)
				except:
					try:
						shutil.move(file, new_filename_+".old")
					except:
						print("can't delete or move inputfile after remuxing '"+str(file)+"'")
			else:
				print("mkvmerge crashed on file '"+str(file)+"'")
				try:
					shutil.move(file, file+"_crash")
				except:
					pass
		elif returnvalue == 999:
			print("removed from queue, retry on rescan")
		else:
			print("ffmpeg crashed on file '"+str(file)+"'")
			try:
				shutil.move(file, file+"_crash")
			except:
				pass

		
	#print("Strg+C to cancel - sleeping for 5 sec")
	sleep(5)
