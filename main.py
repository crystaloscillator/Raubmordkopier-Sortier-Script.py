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
from subprocess import CalledProcessError, check_call, DEVNULL, check_output, STDOUT
from os.path import expanduser

download_dir = expanduser("/data/Downloads/")
ffmpeg = "ffmpeg"
mkvinfo = "mkvinfo"
mkvmerge = "mkvmerge"
output_folder = expanduser("/data/Serien/")
dl_video_folder = expanduser("/data/Filme_input/sort_series.py/")
other_files_dir = expanduser("/data/Serien_input/other files/")
move_other_files = True
too_less_numbers = expanduser("/data/Serien_input/too less numbers/")
too_many_numbers = expanduser("/data/Serien_input/too many numbers/")
series_unknown = expanduser("/data/Serien_input/series unknown/")
no_exact_match = expanduser("/data/Serien_input/no exact match/")
tmp_folder = expanduser("/tmp/")

conversation_dict = {} #Search-strings
conversation_dict2 = {} #Title
conversation_dict3 = {} #Film
conversation_dict["battlestar"] = 0
conversation_dict["battelstar"] = 0
conversation_dict["battlestard"] = 0
conversation_dict["galactica"] = 0
conversation_dict["bsg"] = 0
conversation_dict["bg"] = 0
conversation_dict2[0] = "Battlestar Galactica"
conversation_dict3[0] = "film"
conversation_dict["dex"] = 1
conversation_dict["dexter"] = 1
conversation_dict["dextdvd"] = 1
conversation_dict2[1] = "Dexter"
conversation_dict3[1] = "film"
conversation_dict["vd"] = 2
conversation_dict["tvd"] = 2
conversation_dict["vampire"] = 2
conversation_dict["diaries"] = 2
conversation_dict["vampdiar"] = 2
conversation_dict2[2] = "Vampire Diaries, The"
conversation_dict3[2] = "film"
conversation_dict["moonlight"] = 3
conversation_dict2[3] = "Moonlight"
conversation_dict3[3] = "film"
conversation_dict["adad"] = 4
conversation_dict["itgad"] = 4
conversation_dict["americandad"] = 4
conversation_dict["americandadx"] = 4
conversation_dict["ad"] = 4
conversation_dict["dad"] = 4
conversation_dict["american"] = 4
conversation_dict2[4] = "American Dad"
conversation_dict3[4] = "animation"
conversation_dict["wire"] = 5
conversation_dict2[5] = "Wire, The"
conversation_dict3[5] = "film"
conversation_dict["fringe"] = 6
conversation_dict2[6] = "Fringe"
conversation_dict3[6] = "film"
conversation_dict["universe"] = 7
conversation_dict["sgu"] = 7
conversation_dict2[7] = "Stargate Universe"
conversation_dict3[7] = "film"
conversation_dict["mentalist"] = 8
conversation_dict["jane"] = 8
conversation_dict["thementalist"] = 8
conversation_dict2[8] = "Mentalist, The"
conversation_dict3[8] = "film"
conversation_dict["true"] = 9
conversation_dict["blood"] = 9
conversation_dict["tb"] = 9
conversation_dict["tblood"] = 9
conversation_dict["trueblood"] = 9
conversation_dict["truebloodxvid"] = 9
conversation_dict2[9] = "True Blood"
conversation_dict3[9] = "film"
conversation_dict["detektiv"] = 10
conversation_dict["conan"] = 10
conversation_dict2[10] = "Detektiv Conan"
conversation_dict3[10] = "animation"
conversation_dict["homer"] = 11
conversation_dict["simpsons"] = 11
conversation_dict2[11] = "Simpsons, The"
conversation_dict3[11] = "animation"
conversation_dict["fear"] = 12
conversation_dict["itself"] = 12
conversation_dict2[12] = "Fear Itself"
conversation_dict3[12] = "film"
conversation_dict["futu"] = 13
conversation_dict["futurama"] = 13
conversation_dict2[13] = "Futurama"
conversation_dict3[13] = "animation"
conversation_dict["numbers"] = 14
conversation_dict["numb3rs"] = 14
conversation_dict["numbrs"] = 14
conversation_dict2[14] = "Numb3rs"
conversation_dict3[14] = "film"
conversation_dict["band"] = 15
conversation_dict["brother"] = 15
conversation_dict2[15] = "Band of Brother"
conversation_dict3[15] = "film"
conversation_dict["house"] = 16
conversation_dict["hous"] = 16
conversation_dict["drh"] = 16
conversation_dict["drhouse"] = 16
conversation_dict2[16] = "Dr. House"
conversation_dict3[16] = "film"
conversation_dict["happy"] = 17
conversation_dict["tree"] = 17
conversation_dict2[17] = "Happy Tree Friends"
conversation_dict3[17] = "film"
conversation_dict["eureka"] = 18
conversation_dict["eur"] = 18
conversation_dict2[18] = "EUReKA"
conversation_dict3[18] = "film"
conversation_dict["men"] = 19
conversation_dict["twoandahalfmen"] = 19
conversation_dict2[19] = "Two and a Half Men"
conversation_dict3[19] = "film"
conversation_dict["bn"] = 20
conversation_dict["burn"] = 20
conversation_dict["burnnotice"] = 20
conversation_dict2[20] = "Burn Notice"
conversation_dict3[20] = "film"
conversation_dict["atlantis"] = 21
conversation_dict2[21] = "Stargate Atlantis"
conversation_dict3[21] = "film"
conversation_dict["sgeins"] = 22
conversation_dict["sg1"] = 22
conversation_dict2[22] = "Stargate SG1"
conversation_dict3[22] = "film"
conversation_dict["kino"] = 23
conversation_dict2[23] = "Stargate Universe - Kino"
conversation_dict3[23] = "film"
conversation_dict["family"] = 24
conversation_dict["famguy"] = 24
conversation_dict["fg"] = 24
conversation_dict["familyguy"] = 24
conversation_dict2[24] = "Family Guy"
conversation_dict3[24] = "animation"
conversation_dict["haven"] = 25
conversation_dict2[25] = "Haven"
conversation_dict3[25] = "film"
conversation_dict["unit"] = 26
conversation_dict["unitrp"] = 26
conversation_dict["tu"] = 26
conversation_dict2[26] = "Unit, The"
conversation_dict3[26] = "film"
conversation_dict["scrubs"] = 27
conversation_dict2[27] = "Scrubs"
conversation_dict3[27] = "film"
conversation_dict["chaos"] = 28
conversation_dict2[28] = "Chaos City"
conversation_dict3[28] = "film"
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
conversation_dict3[29] = "film"
conversation_dict["navicis"] = 30
conversation_dict["navycis"] = 30
conversation_dict["ncis"] = 30
conversation_dict["navy"] = 30
conversation_dict["cis"] = 30
conversation_dict2[30] = "Navy CIS"
conversation_dict3[30] = "film"
conversation_dict["tos"] = 31
conversation_dict2[31] = "Raumschiff Enterprise [tos]"
conversation_dict3[31] = "film"
conversation_dict["fallingskies"] = 32
conversation_dict["falling"] = 32
conversation_dict["skies"] = 32
conversation_dict2[32] = "Falling Skies"
conversation_dict3[32] = "film"
conversation_dict["aeon"] = 33
conversation_dict["flux"] = 33
conversation_dict2[33] = "Aeon Flux"
conversation_dict3[33] = "film"
conversation_dict["v"] = 34
conversation_dict2[34] = "V - Die Besucher"
conversation_dict3[34] = "film"
conversation_dict["hellsing"] = 35
conversation_dict2[35] = "Hellsing"
conversation_dict3[35] = "animation"
conversation_dict["spartacus"] = 36
conversation_dict["sparta"] = 36
conversation_dict2[36] = "Spartacus"
conversation_dict3[36] = "film"
conversation_dict["soul"] = 37
conversation_dict["eater"] = 37
conversation_dict2[37] = "Soul Eater"
conversation_dict3[37] = "film"
conversation_dict["stromberg"] = 38
conversation_dict2[38] = "Stromberg"
conversation_dict3[38] = "film"
conversation_dict["cowboy"] = 39
conversation_dict["bebop"] = 39
conversation_dict2[39] = "Cowboy Bebop"
conversation_dict3[39] = "animation"
conversation_dict["stv"] = 40
conversation_dict["voya"] = 40
conversation_dict2[40] = "Star Trek Voyager [stv]"
conversation_dict3[40] = "film"
conversation_dict["ent"] = 41
conversation_dict2[41] = "Star Trek Enterprise [ent]"
conversation_dict3[41] = "film"
conversation_dict["got"] = 42
conversation_dict["gamethrones"] = 42
conversation_dict["thrones"] = 42
conversation_dict2[42] = "Game of Thrones"
conversation_dict3[42] = "film"
conversation_dict["tng"] = 43
conversation_dict2[43] = "Star Trek The Next Generation [tng]"
conversation_dict3[43] = "film"
conversation_dict["continuum"] = 44
conversation_dict2[44] = "Continuum"
conversation_dict3[44] = "film"
conversation_dict["prisoner"] = 45
conversation_dict2[45] = "Prisoner, The"
conversation_dict3[45] = "film"
conversation_dict["mother"] = 46
conversation_dict["himym"] = 46
conversation_dict["swarley"] = 46
conversation_dict2[46] = "How I Met Your Mother"
conversation_dict3[46] = "film"
conversation_dict["anarchy"] = 47
conversation_dict["sons"] = 47
conversation_dict["sofsoa"] = 47
conversation_dict2[47] = "Sons Of Anarchy"
conversation_dict3[47] = "film"
conversation_dict["vik"] = 48
conversation_dict["viki"] = 48
conversation_dict2[48] = "Vikings"
conversation_dict3[48] = "film"
conversation_dict["breaking"] = 49
conversation_dict["breakingbad"] = 49
conversation_dict2[49] = "Breaking Bad"
conversation_dict3[49] = "film"
conversation_dict["upon"] = 50
conversation_dict["onceupon"] = 50
conversation_dict2[50] = "Once Upon a Time"
conversation_dict3[50] = "film"
conversation_dict["deadlike"] = 51
conversation_dict["deadlikeme"] = 51
conversation_dict["like"] = 51
conversation_dict["dlm"] = 51
conversation_dict["sgwt"] = 51
conversation_dict2[51] = "Dead Like Me"
conversation_dict3[51] = "film"
conversation_dict["ddvb"] = 52
conversation_dict2[52] = "Drachenreiter von Berk, Die"
conversation_dict3[52] = "animation"
conversation_dict["lostgirl"] = 53
conversation_dict2[53] = "Lost Girl"
conversation_dict3[53] = "film"
conversation_dict["arrow"] = 54
conversation_dict2[54] = "Arrow"
conversation_dict3[54] = "film"
conversation_dict["greysanatomy"] = 55
conversation_dict["anatomy"] = 55
conversation_dict["grey's"] = 55
conversation_dict2[55] = "Grey's Anatomy"
conversation_dict3[55] = "film"
conversation_dict["marvels"] = 56
conversation_dict["marvel's"] = 56
conversation_dict["agents"] = 56
conversation_dict["shield"] = 56
conversation_dict2[56] = "Marvel's Agents of S.H.I.E.L.D."
conversation_dict3[56] = "film"
conversation_dict["theamericans"] = 57
conversation_dict2[57] = "Americans, The"
conversation_dict3[57] = "film"
conversation_dict["sleepyhollow"] = 58
conversation_dict["sleepy"] = 58
conversation_dict2[58] = "Sleepy Hollow"
conversation_dict3[58] = "film"
conversation_dict["person"] = 59
conversation_dict["interest"] = 59
conversation_dict["poi"] = 59
conversation_dict2[59] = "Person of Interest"
conversation_dict3[59] = "film"
conversation_dict["firefly"] = 60
conversation_dict2[60] = "Firefly"
conversation_dict3[60] = "film"
conversation_dict["wheels"] = 61
conversation_dict["hell"] = 61
conversation_dict["hellonwheels"] = 61
conversation_dict2[61] = "Hell on Wheels"
conversation_dict3[61] = "film"
conversation_dict["exodus"] = 62
conversation_dict2[62] = "Exodus Erde"
conversation_dict3[62] = "film"
conversation_dict["berk"] = 63
conversation_dict["drachenreiter"] = 63
conversation_dict2[63] = "Drachenreiter von Berk, Die"
conversation_dict3[63] = "animation"
conversation_dict["walking"] = 64
conversation_dict["twd"] = 64
conversation_dict["thewalkingdead"] = 64
conversation_dict2[64] = "Walking Dead, The"
conversation_dict3[64] = "film"
conversation_dict["being"] = 65
conversation_dict["human"] = 65
conversation_dict["behu"] = 65
conversation_dict2[65] = "Being Human"
conversation_dict3[65] = "film"
conversation_dict["twobrokegirls"] = 66
conversation_dict["broke"] = 66
conversation_dict2[66] = "Two Broke Girls"
conversation_dict3[66] = "film"
conversation_dict["abenobashi"] = 67
conversation_dict["mahou"] = 67
conversation_dict["shoutengai"] = 67
conversation_dict2[67] = "Abenobashi Mahou Shoutengai"
conversation_dict3[67] = "animation"
conversation_dict["basilisk"] = 68
conversation_dict2[68] = "Basilisk"
conversation_dict3[68] = "animation"
conversation_dict["bones"] = 69
conversation_dict2[69] = "Bones"
conversation_dict3[69] = "film"
conversation_dict["crowd"] = 70
conversation_dict2[70] = "IT Crowd, The"
conversation_dict3[70] = "film"
conversation_dict["castle"] = 71
conversation_dict2[71] = "Castle"
conversation_dict3[71] = "film"
conversation_dict["lie"] = 72
conversation_dict2[72] = "Lie to Me"
conversation_dict3[72] = "film"
conversation_dict["sailor"] = 73
conversation_dict2[73] = "Sailor Moon"
conversation_dict3[73] = "animation"
conversation_dict["supernatural"] = 74
conversation_dict2[74] = "Supernatural"
conversation_dict3[74] = "film"
conversation_dict["followings"] = 75
conversation_dict["following"] = 75
conversation_dict2[75] = "Following, The"
conversation_dict3[75] = "film"
conversation_dict["americans"] = 76
conversation_dict2[76] = "Americans, The"
conversation_dict3[76] = "film"
conversation_dict["blackadder"] = 77
conversation_dict["adder"] = 77
conversation_dict2[77] = "Blackadder"
conversation_dict3[77] = "film"
conversation_dict["birmingham"] = 78
conversation_dict["blinders"] = 78
conversation_dict["peaky"] = 78
conversation_dict["peakyblinders"] = 78
conversation_dict2[78] = "Peaky Blinders - Gangs of Birmingham"
conversation_dict3[78] = "film"
conversation_dict["pinky"] = 79
conversation_dict2[79] = "Pinky und der Brain"
conversation_dict3[79] = "film"
conversation_dict["juw"] = 80
conversation_dict["jeeves"] = 80
conversation_dict["wooster"] = 80
conversation_dict2[80] = "Jeeves and Wooster"
conversation_dict3[80] = "film"
conversation_dict["lost"] = 81
conversation_dict2[81] = "Lost"
conversation_dict3[81] = "film"

remove_strings = ["dxvid", "xvid", "staffel", "episode", "the", "german", "ger", "intro", "ep", "avi", "divx", "flv", "ogm", "ac3", "0W4", "x264", "X264", "p0w4", "Prim3time", "1980", "1981", "1982", "1983", "1984", "1985", "1986", "1987", "1988", "1989", "1990", "1991", "1992", "1993", "1994", "1995", "1996", "1997", "1998", "1999", "2000", "2001", "2002", "2003", "2004", "2005", "2006", "2007", "2008", "2009", "2010", "2011", "2012", "2013", "2014", "1080p", "720p"]
seperators = ["_", " ", ".", "-", ",", "(", ")", "[", "]"]

try:
	os.chdir(download_dir)
except FileNotFoundError:
	print("Error: Download-directory not found")
	exit(1)

def ensure_dir(f):
    d = os.path.dirname(f)
    if not os.path.exists(d):
        os.makedirs(d)

def FixString(str):
	out = str
	for rem_str in remove_strings:
		if out.startswith(rem_str):
			out = out[-len(rem_str)-1:]
		if out.endswith(rem_str):
			out = out[:len(out)-len(rem_str)]
	return out

def checkMKV(sMkvInfo_txt):
	found = 0
	for line in sMkvInfo_txt.split("\n"):
		if line.startswith("|  + Codec-ID:") and "A_VORBIS" in line:
			found+=1
		if line.startswith("|   + Abtastrate:") and "32000" in line:
			found+=1
	if (found % 2) == 0 and found != 0:
		return 0
	return 1
	
def ffmpegConvertIt(bMKV, sInputFile, sTitle, sTune): 
	# bMKV        - sets true to mkvinfo it, do not transcode if already transcoded
	# sInputFile  - Input filename
	# sTune       - Film or Animation Seriestype
	# sTitle      - The Title of the Series -> Output Filename + .mkv
	needTranscode = 0
	tmpFilename = sInputFile + "_ffmpg"
	outputPath = tmp_folder+sTitle+".mkv"
	MuxToMkv = False
	try:
		shutil.move(sInputFile, tmpFilename)
	except:
		print("Error: Renaming "+sInputFile+" to "+tmpFilename+" failed")
		return [999, tmpFilename, "", MuxToMkv]
	
	cmd1 = [ffmpeg, "-i", tmpFilename, "-y", "-vcodec", "libx264", "-crf", "24", "-preset", "slow", "-tune", sTune, \
			"-movflags", "+faststart", "-acodec", "libvorbis", "-qscale:a", "0", "-ar", "32000", "-scodec", "copy", "-f", "matroska", \
			"-metadata", 'title="'+sTitle+'"', outputPath]
	cmd2 = [ffmpeg,"-i",tmpFilename, "-y","-vcodec", "copy","-acodec","copy", "-scodec", "copy", "-metadata", 'title="'+sTitle+'"', "-f", "matroska", outputPath]
	cmd3 = [mkvmerge, "-q", "--title", sTitle, "--default-language", "de", "-B", "-T", "--no-chapters", "-M", "--no-global-tags", "--priority", "lower", tmpFilename, "-o", outputPath]
	
	if bMKV:
		print("Debug: This is an mkv, running mkvinfo...")
		try:
			needTranscode = checkMKV(check_output([mkvinfo, tmpFilename], stderr=STDOUT, universal_newlines=True))
		except CalledProcessError:
			return [998, tmpFilename, "", MuxToMkv]
	else: #going to mkv it first
		MuxToMkv = True
		
	if needTranscode:
		cmd = cmd1
		print("   Transcoding A/V-Data with ffmpeg, this might take some while...")
	elif MuxToMkv:
		cmd = cmd2
		cmd[-1] = sInputFile+".mkv"
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
			print("Error: While doing FFMPEG-Transcoding, return code: '"+str(e.returncode)+"'")
		else:
			print("Error: While doing FFMPEG-Copy, return code: '"+str(e.returncode)+"', try to remux with mkvmerge")
	if not needTranscode and crashed:
		cmd = cmd3
		try:
			check_call(cmd, stdout=DEVNULL, stderr=DEVNULL)
			print("Debug: Successfully remuxed to mkv with mkvmerge")
			crashed = 0
		except CalledProcessError as e:
			errorcode = e.returncode
			print("Error: While doing mkvmerge-Copy, return code: '"+str(e.returncode)+"'")
			
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

	#print("read download directory")
	files = os.listdir(os.getcwd())
	#print("got "+str(len(files))+" files")

	for file in files:
		bIsAnMkvInputFile = False
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
			bIsAnMkvInputFile = True
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
			print("Warning: no filetype detected, use AVI - should not happen!")
			new_filename[8] = "avi"
		else: #folder
			continue
			
		elements_done = True
		
		if skip_file:
			if move_other_files:
				try:
					print("Info: No usable file-extension found, moving file '"+str(file)+"' to 'other files'")
					ensure_dir(other_files_dir+file)
					shutil.move(file, other_files_dir+file)
				except:
					print("Error: Can't move file '"+str(file)+"'")
					pass
			continue
		
		#seperate strings
		next_word = ""
		words = []
		fn = file.replace("S0", ".").replace("S1", ".").replace("S2", ".").replace("s0", ".").replace("s1", ".").replace("s2", ".").replace("numb3rs", "numbers").replace("Numb3rs", "numbers").replace("AC3", "").replace("sg1", "sgeins").replace("SG1", "sgeins").replace("crow_s", "scrubs").replace("SC_", "scrubs_").replace("crow-s", "scrubs_").replace("720p", " ").replace("x264", " ").replace("gtvg-fr", "fringe").replace("futu", "futurama ").replace("lost.girl", "lostgirl").replace("gu10conti2", "continuum 02x").replace("gu10conti3", "continuum 03x").replace("gu10conti1", "continuum 01x").replace("gu10conti4", "continuum 04x").replace("-2brokegirls-", "-twobrokegirls-")
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
		.replace("G.o.T.", "gamethrones") \
		.replace("-101.", "-01_01.") \
		.replace("-102.", "-01_02.") \
		.replace("-103.", "-01_03.") \
		.replace("-104.", "-01_04.") \
		.replace("-105.", "-01_05.") \
		.replace("-106.", "-01_06.") \
		.replace("-107.", "-01_07.") \
		.replace("-108.", "-01_08.") \
		.replace("-109.", "-01_09.") \
		.replace("-110.", "-01_10.") \
		.replace("-111.", "-01_11.") \
		.replace("-112.", "-01_12.") \
		.replace("-113.", "-01_13.") \
		.replace("-114.", "-01_14.") \
		.replace("-115.", "-01_15.") \
		.replace("-116.", "-01_16.") \
		.replace("-117.", "-01_17.") \
		.replace("-118.", "-01_18.") \
		.replace("-119.", "-01_19.") \
		.replace("-120.", "-01_20.") \
		.replace("-121.", "-01_21.") \
		.replace("-122.", "-01_22.") \
		.replace("-123.", "-01_23.") \
		.replace("-124.", "-01_24.") \
		.replace("-125.", "-01_25.") \
		.replace("-126.", "-01_26.") \
		.replace("-127.", "-01_27.") \
		.replace("-128.", "-01_28.") \
		.replace("-129.", "-01_29.") \
		.replace("-130.", "-01_30.") \
		.replace("-201.", "-02_01.") \
		.replace("-202.", "-02_02.") \
		.replace("-203.", "-02_03.") \
		.replace("-204.", "-02_04.") \
		.replace("-205.", "-02_05.") \
		.replace("-206.", "-02_06.") \
		.replace("-207.", "-02_07.") \
		.replace("-208.", "-02_08.") \
		.replace("-209.", "-02_09.") \
		.replace("-210.", "-02_10.") \
		.replace("-211.", "-02_11.") \
		.replace("-212.", "-02_12.") \
		.replace("-213.", "-02_13.") \
		.replace("-214.", "-02_14.") \
		.replace("-215.", "-02_15.") \
		.replace("-216.", "-02_16.") \
		.replace("-217.", "-02_17.") \
		.replace("-218.", "-02_18.") \
		.replace("-219.", "-02_19.") \
		.replace("-220.", "-02_20.") \
		.replace("-221.", "-02_21.") \
		.replace("-222.", "-02_22.") \
		.replace("-223.", "-02_23.") \
		.replace("-224.", "-02_24.") \
		.replace("-225.", "-02_25.") \
		.replace("-226.", "-02_26.") \
		.replace("-227.", "-02_27.") \
		.replace("-228.", "-02_28.") \
		.replace("-229.", "-02_29.") \
		.replace("-230.", "-02_30.") \
		.replace("-301.", "-03_01.") \
		.replace("-302.", "-03_02.") \
		.replace("-303.", "-03_03.") \
		.replace("-304.", "-03_04.") \
		.replace("-305.", "-03_05.") \
		.replace("-306.", "-03_06.") \
		.replace("-307.", "-03_07.") \
		.replace("-308.", "-03_08.") \
		.replace("-309.", "-03_09.") \
		.replace("-310.", "-03_10.") \
		.replace("-311.", "-03_11.") \
		.replace("-312.", "-03_12.") \
		.replace("-313.", "-03_13.") \
		.replace("-314.", "-03_14.") \
		.replace("-315.", "-03_15.") \
		.replace("-316.", "-03_16.") \
		.replace("-317.", "-03_17.") \
		.replace("-318.", "-03_18.") \
		.replace("-319.", "-03_19.") \
		.replace("-320.", "-03_20.") \
		.replace("-321.", "-03_21.") \
		.replace("-322.", "-03_22.") \
		.replace("-323.", "-03_23.") \
		.replace("-324.", "-03_24.") \
		.replace("-325.", "-03_25.") \
		.replace("-326.", "-03_26.") \
		.replace("-327.", "-03_27.") \
		.replace("-328.", "-03_28.") \
		.replace("-329.", "-03_29.") \
		.replace("-330.", "-03_30.") \
		.replace("-401.", "-04_01.") \
		.replace("-402.", "-04_02.") \
		.replace("-403.", "-04_03.") \
		.replace("-404.", "-04_04.") \
		.replace("-405.", "-04_05.") \
		.replace("-406.", "-04_06.") \
		.replace("-407.", "-04_07.") \
		.replace("-408.", "-04_08.") \
		.replace("-409.", "-04_09.") \
		.replace("-410.", "-04_10.") \
		.replace("-411.", "-04_11.") \
		.replace("-412.", "-04_12.") \
		.replace("-413.", "-04_13.") \
		.replace("-414.", "-04_14.") \
		.replace("-415.", "-04_15.") \
		.replace("-416.", "-04_16.") \
		.replace("-417.", "-04_17.") \
		.replace("-418.", "-04_18.") \
		.replace("-419.", "-04_19.") \
		.replace("-420.", "-04_20.") \
		.replace("-421.", "-04_21.") \
		.replace("-422.", "-04_22.") \
		.replace("-423.", "-04_23.") \
		.replace("-424.", "-04_24.") \
		.replace("-425.", "-04_25.") \
		.replace("-426.", "-04_26.") \
		.replace("-427.", "-04_27.") \
		.replace("-428.", "-04_28.") \
		.replace("-429.", "-04_29.") \
		.replace("-430.", "-04_30.") \
		.replace("-501.", "-05_01.") \
		.replace("-502.", "-05_02.") \
		.replace("-503.", "-05_03.") \
		.replace("-504.", "-05_04.") \
		.replace("-505.", "-05_05.") \
		.replace("-506.", "-05_06.") \
		.replace("-507.", "-05_07.") \
		.replace("-508.", "-05_08.") \
		.replace("-509.", "-05_09.") \
		.replace("-510.", "-05_10.") \
		.replace("-511.", "-05_11.") \
		.replace("-512.", "-05_12.") \
		.replace("-513.", "-05_13.") \
		.replace("-514.", "-05_14.") \
		.replace("-515.", "-05_15.") \
		.replace("-516.", "-05_16.") \
		.replace("-517.", "-05_17.") \
		.replace("-518.", "-05_18.") \
		.replace("-519.", "-05_19.") \
		.replace("-520.", "-05_20.") \
		.replace("-521.", "-05_21.") \
		.replace("-522.", "-05_22.") \
		.replace("-523.", "-05_23.") \
		.replace("-524.", "-05_24.") \
		.replace("-525.", "-05_25.") \
		.replace("-526.", "-05_26.") \
		.replace("-527.", "-05_27.") \
		.replace("-528.", "-05_28.") \
		.replace("-529.", "-05_29.") \
		.replace("-530.", "-05_30.") \
		.replace("-601.", "-06_01.") \
		.replace("-602.", "-06_02.") \
		.replace("-603.", "-06_03.") \
		.replace("-604.", "-06_04.") \
		.replace("-605.", "-06_05.") \
		.replace("-606.", "-06_06.") \
		.replace("-607.", "-06_07.") \
		.replace("-608.", "-06_08.") \
		.replace("-609.", "-06_09.") \
		.replace("-610.", "-06_10.") \
		.replace("-611.", "-06_11.") \
		.replace("-612.", "-06_12.") \
		.replace("-613.", "-06_13.") \
		.replace("-614.", "-06_14.") \
		.replace("-615.", "-06_15.") \
		.replace("-616.", "-06_16.") \
		.replace("-617.", "-06_17.") \
		.replace("-618.", "-06_18.") \
		.replace("-619.", "-06_19.") \
		.replace("-620.", "-06_20.") \
		.replace("-621.", "-06_21.") \
		.replace("-622.", "-06_22.") \
		.replace("-623.", "-06_23.") \
		.replace("-624.", "-06_24.") \
		.replace("-625.", "-06_25.") \
		.replace("-626.", "-06_26.") \
		.replace("-627.", "-06_27.") \
		.replace("-628.", "-06_28.") \
		.replace("-629.", "-06_29.") \
		.replace("-630.", "-06_30.") \
		.replace("-701.", "-07_01.") \
		.replace("-702.", "-07_02.") \
		.replace("-703.", "-07_03.") \
		.replace("-704.", "-07_04.") \
		.replace("-705.", "-07_05.") \
		.replace("-706.", "-07_06.") \
		.replace("-707.", "-07_07.") \
		.replace("-708.", "-07_08.") \
		.replace("-709.", "-07_09.") \
		.replace("-710.", "-07_10.") \
		.replace("-711.", "-07_11.") \
		.replace("-712.", "-07_12.") \
		.replace("-713.", "-07_13.") \
		.replace("-714.", "-07_14.") \
		.replace("-715.", "-07_15.") \
		.replace("-716.", "-07_16.") \
		.replace("-717.", "-07_17.") \
		.replace("-718.", "-07_18.") \
		.replace("-719.", "-07_19.") \
		.replace("-720.", "-07_20.") \
		.replace("-721.", "-07_21.") \
		.replace("-722.", "-07_22.") \
		.replace("-723.", "-07_23.") \
		.replace("-724.", "-07_24.") \
		.replace("-725.", "-07_25.") \
		.replace("-726.", "-07_26.") \
		.replace("-727.", "-07_27.") \
		.replace("-728.", "-07_28.") \
		.replace("-729.", "-07_29.") \
		.replace("-730.", "-07_30.") \
		.replace("-801.", "-08_01.") \
		.replace("-802.", "-08_02.") \
		.replace("-803.", "-08_03.") \
		.replace("-804.", "-08_04.") \
		.replace("-805.", "-08_05.") \
		.replace("-806.", "-08_06.") \
		.replace("-807.", "-08_07.") \
		.replace("-808.", "-08_08.") \
		.replace("-809.", "-08_09.") \
		.replace("-810.", "-08_10.") \
		.replace("-811.", "-08_11.") \
		.replace("-812.", "-08_12.") \
		.replace("-813.", "-08_13.") \
		.replace("-814.", "-08_14.") \
		.replace("-815.", "-08_15.") \
		.replace("-816.", "-08_16.") \
		.replace("-817.", "-08_17.") \
		.replace("-818.", "-08_18.") \
		.replace("-819.", "-08_19.") \
		.replace("-820.", "-08_20.") \
		.replace("-821.", "-08_21.") \
		.replace("-822.", "-08_22.") \
		.replace("-823.", "-08_23.") \
		.replace("-824.", "-08_24.") \
		.replace("-825.", "-08_25.") \
		.replace("-826.", "-08_26.") \
		.replace("-827.", "-08_27.") \
		.replace("-828.", "-08_28.") \
		.replace("-829.", "-08_29.") \
		.replace("-830.", "-08_30.") \
		.replace("-901.", "-09_01.") \
		.replace("-902.", "-09_02.") \
		.replace("-903.", "-09_03.") \
		.replace("-904.", "-09_04.") \
		.replace("-905.", "-09_05.") \
		.replace("-906.", "-09_06.") \
		.replace("-907.", "-09_07.") \
		.replace("-908.", "-09_08.") \
		.replace("-909.", "-09_09.") \
		.replace("-910.", "-09_10.") \
		.replace("-911.", "-09_11.") \
		.replace("-912.", "-09_12.") \
		.replace("-913.", "-09_13.") \
		.replace("-914.", "-09_14.") \
		.replace("-915.", "-09_15.") \
		.replace("-916.", "-09_16.") \
		.replace("-917.", "-09_17.") \
		.replace("-918.", "-09_18.") \
		.replace("-919.", "-09_19.") \
		.replace("-920.", "-09_20.") \
		.replace("-921.", "-09_21.") \
		.replace("-922.", "-09_22.") \
		.replace("-923.", "-09_23.") \
		.replace("-924.", "-09_24.") \
		.replace("-925.", "-09_25.") \
		.replace("-926.", "-09_26.") \
		.replace("-927.", "-09_27.") \
		.replace("-928.", "-09_28.") \
		.replace("-929.", "-09_29.") \
		.replace("-930.", "-09_30.") \
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
		.replace("-2brokegirls-", "-twobrokegirls-") \
		.replace("720p", " ") \
		.replace("x264", " ") \
		.replace("X264", " ") \
		.replace("x265", " ") \
		.replace("X265", " ") \
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
		.replace("480p", "_") \
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
		.replace("3D", "_") \
		.replace(".108-pretail.", ".")
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
				print("Info: Too many numbers in filename, moving file '"+str(file)+"' to 'too many numbers'")
				ensure_dir(too_many_numbers+file)
				shutil.move(file, too_many_numbers+file)	
			except:
				pass
			continue
		
		elif counter == 0:
			try:
				print("Info: No episode/season found, moving file '"+str(file)+"' to 'Filme'")
				ensure_dir(dl_video_folder+file)
				shutil.move(file, dl_video_folder+file)
			except:
				pass
			continue
			
		elif counter == 1:
			try:
				print("Info: Too less numbers in filename, moving file '"+str(file)+"' to 'too less numbers'")
				ensure_dir(too_less_numbers+file)
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
			
		found = []
		for word in words:
			try:
				found.append(conversation_dict[word.lower()])
			except KeyError:
				pass
		
		#distinct list
		found = list(set(found))
		
		if 1 == len(found):
			new_filename[0] = conversation_dict2[found[0]]
			try:
				TuneProfile = conversation_dict3[conversation_dict[word.lower()]]
			except KeyError:
				pass
		elif 1 < len(found):
			print("Info: No exact match found: "+str(found)+", moving file '"+str(file)+"' to no exact match")
			try:
				ensure_dir(no_exact_match+file)
				shutil.move(file, no_exact_match+file)
			except:
				pass
			continue
		else:
			print("Info: Series unknown, moving file '"+str(file)+"' to series unknown")
			try:
				ensure_dir(series_unknown+file)
				shutil.move(file, series_unknown+file)
			except:
				pass
			continue
		
		#mkv it
		new_filename[-1] = "mkv"
		
		FileTitle = ""
		for string in new_filename[0:-2]:
			FileTitle += string
			
		print("'"+str(file)+"' to '"+str(FileTitle+".mkv")+"'")
		
		ffmpeg_return = ffmpegConvertIt(bIsAnMkvInputFile, file, FileTitle, TuneProfile)
		
		input_file=ffmpeg_return[1]
		tmp_file=ffmpeg_return[2]
		JustMkvIt = ffmpeg_return[3]
		
		if ffmpeg_return[0] == 0:
			print("     Done.")
			if not JustMkvIt:
				print("   Moving file from temp-location to series-folder...")
				
				output_folder_ = output_folder+str(new_filename[0])+'/'+str(new_filename[0])+' S'+str(new_filename[2])+str(new_filename[3])+'/'
				output_file=output_folder_+FileTitle+".mkv"
				
				#test if file already exists:
				if isfile(output_file):
					print("Warning: Output File Exists '"+output_file+"'")
					for tmp_int in range(2,100):
						test_filename=output_folder_+FileTitle+"_"+str(tmp_int)+".mkv"
						if isfile(test_filename):
							print("Warning: Output File Exists '"+test_filename+"'")
						else:
							output_file = test_filename
							break	
				#moving file, deleting input	
				try:
					ensure_dir(output_file)
					shutil.move(tmp_file, output_file)
					print("     Done.")
				except:
					try:
						os.remove(output_file)
					except:
						pass
					print("Error: can't move file '"+tmp_file+"' to output location '"+output_file+"', leaving it on temp-location")
					continue
			try:
				print("   Removing input-file...")
				os.remove(input_file)
				print("     Done.")
			except:
				print("Error: can't delete inputfile '"+str(input_file)+"' after reading with ffmpeg")
				continue
		elif ffmpeg_return[0] == 999:
			print("Warning: Removed from queue, retry on rescan")
		else:
			print("Error: process crashed on file '"+str(file)+"' with errorcode '"+str(ffmpeg_return[0])+"'")
			try:
				shutil.move(input_file, file+"_crash")
			except:
				pass
		
	#print("Strg+C to cancel - sleeping for 5 sec")
	try:
		sleep(5)
	except KeyboardInterrupt:
		print("")
		exit(0)
