#!/usr/bin/env python

from cx_Freeze import setup, Executable
setup(  name = "Ldraw bulk parser",
		version = "0.1",
		description = "Ldraw parts color batch replacement utility",
		author='Oren Titane',
		url='http://github.com/Genome36/LDraw-Bulk_Parser',
		executables = [Executable("LDraw_bulk_parser.py")],
		includes = ["pygtk","gdk","os","time", "urllib2", "icon.png"]
		)
