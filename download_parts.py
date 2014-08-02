#!/usr/bin/python2
import json
from os import walk
from os.path import isfile, join
from urllib2 import urlopen
from sys import argv

def download_dat(partid):
	try:
		if isfile("/home/oren/Pictures/legoparts/dat/%s.dat" % (partid)):
			print "part %s data already downloaded" % (partid)
		else:
			data = urlopen("http://www.ldraw.org/library/official/parts/%s.dat" % (partid)).read()
			with open("/home/oren/Pictures/legoparts/dat/%s.dat" % (partid), "w") as file:
				file.write(data)
			print "part %s data is downloading" % (partid)
	except:
		print "part %s data does not exist (no such part id)" % (partid)

def download_img(partid):
	try:
		if isfile("/home/oren/Pictures/legoparts/img/%s.png" % (partid)):
			print "part %s image already downloaded" % (partid)
		else:
			data = urlopen("http://www.ldraw.org/library/official/images/parts/%s.png" % (partid)).read()
			with open("/home/oren/Pictures/legoparts/img/%s.png" % (partid), "w") as file:
				file.write(data)
			print "part %s image is downloading" % (partid)
	except:
		print "part %s image does not exist (no such part id)" % (partid)

def download():
	files_list = []
	files_paths = []
	dict = []
	for path, dirs, files in walk(argv[1]):
		for fileName in files:
			if ".dat" in fileName:
				files_list.append(fileName)
				files_paths.append(join(path, fileName))
				print len(files_list)
				print "added", fileName

	for file in files_list:
		download_img(file.replace(".dat", ""))
		files_list.pop(files_list.index(file))
		print len(files_list), "files left"

#	for file in files_paths:
#		with open(file, "r") as data:
#			content = data.readlines()
#			dict.append({"name":(content[0].replace(content[0][:2], "")), "code":(content[1].replace("0 Name: ", "").replace(".dat", ""))})
#	with open("/run/media/oren/Rikuto/python scripts/build/raw/parts.json", "w") as newdictfile:
#		json.dump(dict, newdictfile, indent=4)

if __name__ == "__main__":
	download()
