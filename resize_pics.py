#!/usr/bin/python2
import os
from PIL import Image
import time

def resize(self, path, fileName, ext, heightsize, folder):
	if os.path.exists(os.path.join(path.replace(path[-4:], ""), folder)):
		print "found folder", folder
	else:
		print "creating directory", folder, "in", path.replace(path[-4:], "")
		os.mkdir(os.path.join(path.replace(path[-4:], ""), folder))
	try:
		filePath = os.path.join(path, fileName)
		im = Image.open(filePath)
		w, h  = im.size
		if h > heightsize and w > heightsize:
			print int(w*(((heightsize*100.0)/w)/100)), int(h*(((heightsize*100.0)/h)/100))
			newIm = im.resize((int(w*(((heightsize*100.0)/w)/100)), int(h*(((heightsize*100.0)/h)/100))))
		#	newfileName = path.replace(path[-4:], "")+folder+"/"+fileName.replace(fileName[-4:], " ")+str(int(w*resizeFactor))+"x"+str(int(h*resizeFactor))+ext
			newfileName = path.replace(path[-4:], "")+folder+"/"+fileName
			print "saving as", newfileName
			newIm.save(newfileName)
			time.sleep(1)
	except Exception as error:
		print error

def find(imageFolder):
	imgExts = [".png", ".bmp", ".jpg"]
	for path, dirs, files in os.walk(imageFolder):
		for fileName in files:
			print "found", fileName
			ext = fileName[-4:].lower()
			if ext not in imgExts:
				continue

			resize(path, fileName, ext, 200, "128")

#if __name__ == "__main__":
#	texture_resize()

