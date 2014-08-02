#!/usr/bin/python2
import pygtk, gtk, gobject, threading
import os, json
from time import sleep
from urllib2 import urlopen
from datetime import datetime
from sys import argv

class splashScreen():
	def __init__(self):
		'''MAIN WINDOW'''
		self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
		self.window.set_position(gtk.WIN_POS_CENTER_ALWAYS)
		self.window.set_title("Rikuto Launcher Splash")
		self.window.set_icon_from_file("images/icon.png")
		self.window.set_decorated(False)
		self.window.set_resizable(False)
		self.window.connect("destroy", self.destroy)

		self.global_vbox = gtk.VBox()
		self.window.add(self.global_vbox)

		'''SPLASH IMAGE'''
		self.splash_image = gtk.Image()
		self.splash_image.set_from_file("images/icon.png")
		self.global_vbox.pack_start(self.splash_image, False, True)

		'''VISIBILITIES AT STARTUP'''
		self.window.show_all()

	def destroy(self):
		gtk.main_quit()

class parser: # mpd not finished!
	def insert_text(self, text):
		self.console_textview.get_buffer().insert(self.console_textview.get_buffer().get_end_iter(), str(text) + "\n")
		adj = self.console.get_vadjustment()
		adj.set_value(adj.upper - adj.page_size)
		if "-debug" in argv:
			print text

	def progress(self, text, fraction=None):
		self.progressbar.show()
		self.progressbar.set_fraction(fraction)
		self.progressbar.set_text(text)
		if "-debug" in argv:
			print text
		if self.progressbar.get_fraction() == 1:
			self.progressbar.set_fraction(0)
			self.progressbar.hide()

	def write(self, filepath, content):
		try:
			if "-dry-run" not in argv:
				with open(filepath, "wt") as new_file:
					for i in range(len(content)):
						new_file.write(content[i])
			else:
				pass
		except Exception as error:
			self.insert_text(error)

	def replace_colors(self, filepath):
		try:
			with open(filepath, "r") as file:
				content = file.readlines()
				for line in content:
					sections = line.split(" ")
					new_line = ""
					self.index = content.index(line)
					if len(sections) >= 15 and sections[1] == self.old_color_entry.get_text():
						sections[1] = self.new_color_entry.get_text()
						for data in sections:
							new_line = " ".join((new_line, data))
						new_line = new_line[1:]
						content[self.index] = new_line
						self.insert_text("replacing %s \rwith %s \rin %s\n" % (line.replace("\n", ""), new_line.replace("\n", ""), filepath))
						self.write(filepath, content)
					else:
						pass
		except Exception as error:
			self.insert_text(error)

	def replace_parts(self, filepath): #needs a second part entry
		try:
			with open(filepath, "r") as file:
				content = file.readlines()
				for line in content:
					sections = line.split(" ")
					new_line = ""
					self.index = content.index(line)
					if len(sections) >= 15 and sections[14] == self.old_part_entry.get_text():
						sections[14] = self.new_color_entry.get_text()
						for data in sections:
							new_line = " ".join((new_line, data))
						new_line = new_line[1:]
						content[self.index] = new_line
						self.insert_text("replacing %s \rwith %s \rin %s\n" % (line.replace("\n", ""), new_line.replace("\n", ""), filepath))
						self.write(filepath, content)
					else:
						pass
		except Exception as error:
			self.insert_text(error)

	def replace(self, filepath): # old need to replace with new way to parse
		try:
			with open(filepath, "rt", "utf-8") as file:
				content = file.readlines()
				for line in content:
					for part in self.parts:
						if part != "" and " "+part+"." in line:
							self.index = content.index(line)
							if line[3] == " ":
								new_line = line.replace(line[:3], "1 %s" % (self.color_new))
							elif line[3] != " " and line[4] != " " and line[5] == " ":
								new_line = line.replace(line[:5], "1 %s" % (self.color_new))
							else:
								new_line = line.replace(line[:4], "1 %s" % (self.color_new))
							content[self.index] = new_line
							self.insert_text("replacing %s \rwith %s \r in %s" % (line, new_line, filename))
			self.write(filepath, self.index, content)
		except Exception as error:
			self.insert_text(error)

	def replace_mpd(self, filepath):
		print "mpd parser not yet implemented"
		pass

	def parser(self, filepath): #combo list changed
		ext = [".ldr", ".mpd" ]
		if filepath[-4:] not in ext:
			if "-debug" in argv:
				print "file extension: %s skipping file" % filepath[-4:]
			else:
				pass

			#"part -> part", "part color -> new color", "color -> color"
		else:
			if filepath[-4:] in ext and self.ext_type_combo.entry.get_text() == "both":
				self.insert_text("Found %s" % (filepath))
				if self.parsing_type_combo.entry.get_text() == "part -> part":
					self.replace_parts(filepath)
				elif self.parsing_type_combo.entry.get_text() == "part color -> new color":
					self.replace(filepath)
				elif self.parsing_type_combo.entry.get_text() == "color -> color":
					self.replace_colors(filepath)
				else:
					pass

			if filepath[-4:] == ".ldr" and self.ext_type_combo.entry.get_text() == "ldr":
				self.insert_text("Found %s" % (filepath))
				if self.parsing_type_combo.entry.get_text() == "part -> part":
					self.replace_parts(filepath)
				elif self.parsing_type_combo.entry.get_text() == "part color -> new color":
					self.replace(filepath)
				elif self.parsing_type_combo.entry.get_text() == "color -> color":
					self.replace_colors(filepath)
				else:
					pass

			# not yet implemented
			'''if filepath[-4:] == ".mpd" and self.ext_type_combo.entry.get_text() == "mpd":
				self.insert_text("Found %s" % (filepath))
				if self.parsing_type_combo.entry.get_text() == "part -> part":
					self.replace_parts(filepath)
				elif self.parsing_type_combo.entry.get_text() == "part color -> new color":
					self.replace(filepath)
				elif self.parsing_type_combo.entry.get_text() == "color -> color":
					self.replace_colors(filepath)
				else:
					pass'''

		#	sleep(0.125)

	def find_files(self, widget, data=None):
		self.key_words = self.key_words_entry.get_text()
		if self.key_words != "":
			if ", " in self.key_words:
				self.key_words = self.key_words.split(", ")
			else:
				self.key_words = [self.key_words, ""]

		#self.mpd_section = raw_input('.mpd section name as body part seperaw_input("'color' for replacing color integer with another color integer\n'part' for replacing given part(s) color(s) with a color: ").lower()

		self.parts = self.parts_id_entry.get_text()
		if self.parts != "":
			if ", " in self.parts:
				self.parts = self.parts.split(", ")
			else:
				self.parts = [self.parts, ""]

	#	try:
		self.parse_button.set_sensitive(False)
	#	self.progressbar.show()
	#	self.progressbar.set_text("Searching for files ...")

		for path, dirs, files in os.walk(self.system_path):
			for fileName in files:
				self.files_list.append(os.path.join(path, fileName))
	#			self.progressbar.set_text("Searching for files; Found %s file(s) ..." % (len(self.files_list)))
			while gtk.events_pending():
				gtk.main_iteration()

	#	self.progressbar.set_text("Starting files parsing ...")
	#	sleep(3)

		for filepath in self.files_list:
			if self.key_words not in ("", None):
				for key in self.key_words:
					if key in filepath and key != "":#problems
						self.parser(filepath)
	#					self.progress(self.files_list.pop(self.files_list.index(filepath)))
			else:
				self.parser(filepath)
	#			self.progress(self.files_list.pop(self.files_list.index(filepath)))
		self.parse_button.set_sensitive(True)
		self.files_list = []
	#	self.progressbar.hide()
	#	except Exception as error:
	#		self.insert_text(error)

	def required_fields(self, widget, data=None):
		'''self.key_words_label, self.ext_type_combo_label, self.parsing_type_combo_label, self.old_parts_id_label, self.new_part_id_label, self.old_color_label, self.new_color_label, self.key_words_entry, self.ext_type_combo, self.parsing_type_combo, self.old_parts_id_entry, self.new_part_id_entry, self.old_color_entry, self.new_color_entry, self.parse_button'''

		if self.parsing_type_combo.entry.get_text() == "part -> part":
			self.old_parts_id_entry.set_sensitive(True)
			self.new_part_id_entry.set_sensitive(True)
			self.old_color_entry.set_sensitive(False)
			self.new_color_entry.set_sensitive(False)
			if self.system_path != "" and self.old_parts_id_entry.get_text() != "" and self.new_part_id_entry.get_text() != "":
				self.parse_button.set_sensitive(True)
			else:
				self.parse_button.set_sensitive(False)

		elif self.parsing_type_combo.entry.get_text() == "color -> color":
			self.old_parts_id_entry.set_sensitive(False)
			self.new_part_id_entry.set_sensitive(False)
			self.old_color_entry.set_sensitive(True)
			self.new_color_entry.set_sensitive(True)
			if self.system_path != "" and self.old_color_entry.get_text() != "" and self.new_color_entry.get_text() != "":
				self.parse_button.set_sensitive(True)
			else:
				self.parse_button.set_sensitive(False)

		else:
			'''self.parsing_type_combo.entry.get_text() == "part color -> color":'''
			self.old_parts_id_entry.set_sensitive(True)
			self.new_part_id_entry.set_sensitive(False)
			self.old_color_entry.set_sensitive(False)
			self.new_color_entry.set_sensitive(True)
			if self.system_path != "" and self.old_parts_id_entry.get_text() != "" and self.new_color_entry.get_text() != "":
				self.parse_button.set_sensitive(True)
			else:
				self.parse_button.set_sensitive(False)

	def folderchooser(self, widget, data=None):
		self.fc = gtk.FileChooserDialog("Choose folder to parse", self.window, gtk.FILE_CHOOSER_ACTION_SELECT_FOLDER, (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_OPEN, gtk.RESPONSE_OK))
		self.fc.run()
		self.system_path = self.fc.get_filename()
		self.insert_text("You chose: %s" % (self.fc.get_filename()))
		self.fc.destroy()
		self.required_fields(None)

	def about(self, widget, data=None):
		self.about = gtk.AboutDialog()
		self.about.set_size_request(475, 275)
		self.about.set_name("Oren Titane")
		self.about.set_program_name("LDraw bulk parser")
		self.about.set_version("0.2.5")
		self.about.set_copyright("(C) Oren Titane 2013 - %s" % (str(datetime.now())[:4]))
	#	self.about.set_comments("coments")
		try:
			self.about.set_license(urlopen("https://raw.github.com/Genome36/LDraw-Bulk-Parser/master/EULA.license").read())
		except:
			self.about.set_license("License unavailable at this current moment.\nPlease verify internet connection or restart utility.")
		self.about.set_wrap_license(True)
		self.about.set_website("https://github.com/Genome36/LDraw-Bulk-Parser")
	#	self.about.set_website_label("")
		self.about.set_authors(("Oren Titane - (Genome36)", ""))
		self.about.set_documenters(("Oren Titane - (Genome36)", ""))
		self.about.set_artists(("Oren Titane - (Genome36)", ""))
		self.about.set_translator_credits("Oren Titane - (Genome36)")
		self.logo2 = gtk.gdk.pixbuf_new_from_file("images/icon.png")
		self.about.set_logo(self.logo2)
	#	self.about.set_logo_icon_name("")
		self.about.show_all()
		self.about.run()
		self.about.destroy()

	def popup_help(self, widget, data):
		self.description_window = gtk.Dialog(data[0], self.help_listing_window, gtk.MESSAGE_WARNING | gtk.DIALOG_DESTROY_WITH_PARENT, (gtk.STOCK_CLOSE, gtk.RESPONSE_CLOSE))
		self.description_window.set_position(gtk.WIN_POS_CENTER_ALWAYS)
		self.description_window.set_size_request(400, 300)

		self.description = gtk.ScrolledWindow()
		self.description.set_policy(gtk.POLICY_NEVER, gtk.POLICY_AUTOMATIC)
		self.description_textview = gtk.TextView()
		self.description_textview.set_editable(False)
		self.description_textview.set_wrap_mode(gtk.WRAP_WORD)
		self.description_textview.get_buffer().set_text(data[1])
		self.description.add(self.description_textview)
		self.description_window.vbox.pack_start(self.description, True, True)

		self.description_window.show_all()
		self.description_window.run()
		self.description_window.destroy()

	def set_tab_selection(self, widget, data=None):
		if "Old" in data[0].entry.get_text():
			data[1].set_text(str(data[3]))
		else:
			data[2].set_text(str(data[3]))

	def tab_search_filter(self, widget, event=None, data=None):
		#if data[] != None:
		for btn in data:
			btn.show()
			tooltip = btn.get_tooltip_text()
			#tooltip = str(tooltip).lower()
			searchbar = widget.get_text().lower()
			if searchbar not in tooltip and searchbar != "":
				btn.hide()

	def help(self, widget, data=None):
		try:
			def retreive():
				dict = json.load(urlopen("https://raw.github.com/Genome36/LDraw-Bulk-Parser/master/help.json"))
				for table_line in dict:
					btn = gtk.Button(table_line["title"])
					btn.set_size_request(-1, 30)
					btn.connect("clicked", self.popup_help, ((table_line["title"], table_line["content"])))
					self.help_list_vbox.pack_start(btn, False, True)

			def filter(widget, data=None):
				for btn in self.help_list_vbox:
					btn.show()
					tooltip = btn.get_label().lower()
					searchbar = widget.get_text().lower()
					if searchbar not in tooltip and searchbar != "":
						btn.hide()

			self.help_listing_window = gtk.Dialog("Help listing", None, gtk.MESSAGE_WARNING | gtk.DIALOG_DESTROY_WITH_PARENT, (gtk.STOCK_CLOSE, gtk.RESPONSE_CLOSE))
			self.help_listing_window.set_position(gtk.WIN_POS_CENTER)
			self.help_listing_window.set_size_request(600, 400)

			self.help_listing_searchbar = gtk.Entry()
			self.help_listing_searchbar.set_tooltip_text("Search for key words")
			self.help_listing_searchbar.connect("event", filter)
			self.help_listing_searchbar.set_alignment(0.5)
			self.help_listing_window.vbox.pack_start(self.help_listing_searchbar, False, False)

			self.help_list = gtk.ScrolledWindow()
			self.help_list.set_policy(gtk.POLICY_NEVER, gtk.POLICY_AUTOMATIC)
			self.help_list_vbox = gtk.VBox()
			self.help_list.add_with_viewport(self.help_list_vbox)
			self.help_listing_window.vbox.pack_start(self.help_list, True, True)

			retreive()

			self.help_listing_window.show_all()
			self.help_listing_window.run()
			self.help_listing_window.destroy()

		except Exception as error:
			self.insert_text("Help unavailable; an exception occurred, please verify inernet connection or restart application.")
			self.insert_text

	def part_viewer(self, widget, data=None):
		self.viewer = gtk.Dialog(data[0], None, gtk.MESSAGE_WARNING | gtk.DIALOG_DESTROY_WITH_PARENT, (gtk.STOCK_CLOSE, gtk.RESPONSE_CLOSE))
		self.viewer.set_position(gtk.WIN_POS_CENTER)
		self.viewer.set_size_request(600, 400)
		self.viewer.vbox.pack_start(gtk.Label(data[1]))
		img = gtk.Image()
		if os.path.isfile("images/parts/%s.png" % data[0]):
			img.set_from_file("images/parts/%s.png" % data[0])
			self.viewer.vbox.pack_start(img, True, True)
		else:
			img.set_from_file("images/?.png")
			self.viewer.vbox.pack_start(img, True, True)
		self.viewer.show_all()
		self.viewer.run()
		self.viewer.destroy()

	def parts_setter(self, name, code):
		alloc = self.parts_list.get_allocation()
		hbox = gtk.HBox()
		btn = gtk.Button(code)
		btn.set_tooltip_text("Name: %s\nCode: %s" % (name, code))
		btn.connect("clicked", self.set_tab_selection, ((self.parts_listing_old_new_combo, self.old_parts_id_entry, self.new_part_id_entry, code)))
		btn.set_relief(gtk.RELIEF_NONE)
		view = gtk.Button("View part image")
		view.connect("clicked", self.part_viewer, ((code, name)))
		view.set_size_request(alloc.width/3, -1)
		hbox.pack_start(btn, True, True)
		hbox.pack_start(view, False, True)
		self.parts_list_vbox.pack_start(hbox, False, True)
		#hbox.show_all()

		#print len(self.parts_list_vbox.get_children())

	def parts_threading(self):
		try:
			with open("parts.json", "r") as file:
				dict = json.load(file)
				total = int(len(dict))
				done = 0
				for item in dict:
					if done < total:
						done +=1
					gobject.idle_add(self.parts_setter, item["name"], item["code"])
					gobject.idle_add(self.progress, "loading part %s" % item["name"], float(done)/float(total))
					sleep(0.0005)
			#	self.parts_listing_searchbar.connect("event", self.tab_search_filter, (self.parts_hbox))
		except Exception as error:
			self.insert_text("Parts unavailable; an exception occurred, please verify integrity of the Parts.json file.")
			self.insert_text(error)

	def clear(self, widget, data=None):
		self.console_textbuffer.set_text("")

	def destroy(self, widget, data=None):
		gtk.main_quit()
		exit()

	def main(self):
		gtk.main()

	def __init__(self):
		self.system_path = ""
		self.key_words = ""
		self.extension = ""
	#	self.mpd_section = ""
		self.parts = []
	#	self.new_part = ""
		self.index = None
		self.files_list = []

		'''MAIN WINDOW'''
		self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
		self.window.set_position(gtk.WIN_POS_CENTER)
		self.window.set_title("LDraw bulk parser")
	#	self.window.set_icon_from_file("images/icon.png")
		self.window.set_size_request(850, 450)
		self.window.set_border_width(0)
		self.window.connect("destroy", self.destroy)

	#	self.tray = gtk.StatusIcon() # need more time to dive into it's settings and constructors
	#	self.tray.set_from_file("images/icon.png") # self.tray.set_blinking(True)

		self.global_vbox = gtk.VBox()
		self.window.add(self.global_vbox)

		'''MENU BAR'''
		self.menubar = gtk.MenuBar()
		self.global_vbox.pack_start(self.menubar, False, True)

		self.Actions_menuitem = gtk.MenuItem("Actions")
		self.menubar.append(self.Actions_menuitem)

		self.actions_menulist = gtk.Menu()
		self.Actions_menuitem.set_submenu(self.actions_menulist)

		self.open_menuitem = gtk.MenuItem("Open")
		self.open_menuitem.connect("activate", self.folderchooser)
		self.actions_menulist.append(self.open_menuitem)

		self.clear_menuitem = gtk.MenuItem("Clear")
		self.clear_menuitem.connect("activate", self.clear)
		self.actions_menulist.append(self.clear_menuitem)

		self.quit_menuitem = gtk.MenuItem("Quit")
		self.quit_menuitem.connect("activate", self.destroy)
		self.actions_menulist.append(self.quit_menuitem)

		self.help_menuitem = gtk.MenuItem("Help")
		self.menubar.append(self.help_menuitem)

		self.help_menulist = gtk.Menu()
		self.help_menuitem.set_submenu(self.help_menulist)

		self.about_menuitem = gtk.MenuItem("About")
		self.about_menuitem.connect("activate", self.about)
		self.help_menulist.append(self.about_menuitem)

		self.faq_menuitem = gtk.MenuItem("Help")
		self.faq_menuitem.connect("activate", self.help)
		self.help_menulist.append(self.faq_menuitem)

		self.global_hbox = gtk.HBox()
		self.global_vbox.pack_start(self.global_hbox, True, True)

		self.right_panel_frame = gtk.Frame()
		self.global_hbox.pack_start(self.right_panel_frame, False, False)

		self.right_panel_vbox = gtk.VBox()
		self.right_panel_frame.add(self.right_panel_vbox)

		self.about_button = gtk.Button()
		self.about_button.set_tooltip_text("About")
		self.about_button.connect("clicked", self.about, None)
		self.right_panel_vbox.pack_start(self.about_button, True, True)

		self.logo = gtk.Image()
		self.logo.set_from_file("images/icon.png")
		self.about_button.add(self.logo)

		'''WINDOW PANE'''
		self.open_folder = gtk.Button("Open folder")
		self.open_folder.set_tooltip_text("Open folder to parse")
		self.open_folder.connect("clicked", self.folderchooser)
		self.right_panel_vbox.pack_start(self.open_folder, False, False)

		self.parsing_options_hbox = gtk.HBox()
		self.right_panel_vbox.pack_start(self.parsing_options_hbox, False, False)

		self.parsing_labels_vbox = gtk.VBox()
		self.parsing_options_hbox.pack_start(self.parsing_labels_vbox, False, False)

		self.key_words_label = gtk.Label("Key word(s)")
		self.parsing_labels_vbox.pack_start(self.key_words_label, True, True)

		self.ext_type_combo_label = gtk.Label("Extensions")
		self.parsing_labels_vbox.pack_start(self.ext_type_combo_label, True, True)

		self.parsing_type_combo_label = gtk.Label("Parsing type")
		self.parsing_labels_vbox.pack_start(self.parsing_type_combo_label, True, True)

		self.old_parts_id_label = gtk.Label("Old parts id(s)")
		self.parsing_labels_vbox.pack_start(self.old_parts_id_label, True, True)

		self.new_part_id_label = gtk.Label("New part id")
		self.parsing_labels_vbox.pack_start(self.new_part_id_label, True, True)

		self.old_color_label = gtk.Label("Old color")
		self.parsing_labels_vbox.pack_start(self.old_color_label, True, True)

		self.new_color_label = gtk.Label("New color")
		self.parsing_labels_vbox.pack_start(self.new_color_label, True, True)

		self.parsing_entries_vbox = gtk.VBox()
		self.parsing_options_hbox.pack_start(self.parsing_entries_vbox, False, False)

		self.key_words_entry = gtk.Entry()
		self.key_words_entry.set_tooltip_text('specify "key word(s)" to look for in filenames\nseperated by a comma and a space (", ")\nCAUTION: key word(s) are case sensitive')
		self.parsing_entries_vbox.pack_start(self.key_words_entry, True, True)

		self.ext_type_combo = gtk.Combo()
		self.ext_type_combo.entry.set_editable(False)
		self.ext_type_combo.set_tooltip_text("Extensions")
		self.ext_type_combo.set_popdown_strings(["both", "ldr", "mpd"])
		self.parsing_entries_vbox.pack_start(self.ext_type_combo, True, True)

		self.parsing_type_combo = gtk.Combo()
		self.parsing_type_combo.entry.set_editable(False)
		self.parsing_type_combo.set_tooltip_text("Parse part(s) old color with new color / old color with new color")
		self.parsing_type_combo.set_popdown_strings(["part -> part", "part color -> new color", "color -> color"])
		self.parsing_entries_vbox.pack_start(self.parsing_type_combo, True, True)

		self.old_parts_id_entry = gtk.Entry()
		self.old_parts_id_entry.set_tooltip_text('Old part(s) id seperated by a comma and a space (", ")\nCAUTION: part id are case sensitive.')
		self.parsing_entries_vbox.pack_start(self.old_parts_id_entry, True, True)

		self.new_part_id_entry = gtk.Entry()
		self.new_part_id_entry.set_tooltip_text('New Part id\nCAUTION: part id is case sensitive.')
		self.parsing_entries_vbox.pack_start(self.new_part_id_entry, True, True)

		self.old_color_entry = gtk.Entry()
		self.old_color_entry.set_tooltip_text("Old color to replace (integer)")
		self.parsing_entries_vbox.pack_start(self.old_color_entry, True, True)

		self.new_color_entry = gtk.Entry()
		self.new_color_entry.set_tooltip_text("New color to replace with (integer)")
		self.parsing_entries_vbox.pack_start(self.new_color_entry, True, True)

		self.parse_button = gtk.Button("Parse")
		self.parse_button.connect("clicked", self.find_files, None)
		self.parse_button.set_tooltip_text("Parse")
		self.right_panel_vbox.pack_start(self.parse_button, False, True)

		def console_init():
			'''console'''
			self.console = gtk.ScrolledWindow()
			self.console.set_policy(gtk.POLICY_NEVER, gtk.POLICY_AUTOMATIC)
			self.console_textview = gtk.TextView()
			self.console_textview.set_editable(False)
			self.console_textview.set_wrap_mode(gtk.WRAP_WORD)
			self.console_textbuffer = self.console_textview.get_buffer()
			self.console.add(self.console_textview)
		#	self.global_hbox.pack_start(self.console, True, True)

		def parts_list_init():
			'''parts listing'''
			self.parts_vbox = gtk.VBox()

			self.parts_listing_searchbar = gtk.Entry()
			self.parts_listing_searchbar.set_tooltip_text("Search for key words")
			self.parts_listing_searchbar.set_alignment(0.5)
			self.parts_vbox.pack_start(self.parts_listing_searchbar, False, False)

			self.parts_options_hbox = gtk.HBox()
			self.parts_vbox.pack_start(self.parts_options_hbox, False, True)

			self.parts_listing_old_new_combo = gtk.Combo()
			self.parts_listing_old_new_combo.entry.set_editable(False)
			self.parts_listing_old_new_combo.set_popdown_strings(["Old part", "New part"])
			self.parts_options_hbox.pack_start(self.parts_listing_old_new_combo, False, True)

			self.parts_left_page_button = gtk.Button("<")
			self.parts_left_page_button.set_tooltip_text("Previous page")
		#	self.parts_left_page_button.connect("clicked", )
			self.parts_options_hbox.pack_start(self.parts_left_page_button, True, True)

			self.parts_page_numb_button = gtk.Label("0/0")
			self.parts_options_hbox.pack_start(self.parts_page_numb_button, True, True)

			self.parts_right_page_button = gtk.Button(">")
			self.parts_right_page_button.set_tooltip_text("Next page")
		#	self.parts_right_page_button.connect("clicked", )
			self.parts_options_hbox.pack_start(self.parts_right_page_button, True, True)

			self.parts_list = gtk.ScrolledWindow()
			self.parts_list.set_policy(gtk.POLICY_NEVER, gtk.POLICY_AUTOMATIC)
			self.parts_list_vbox = gtk.VBox()
			self.parts_list.add_with_viewport(self.parts_list_vbox)
			self.parts_vbox.pack_start(self.parts_list, True, True)

		def colors_list_init():
			self.colors_vbox = gtk.VBox()

			'''old colors listing'''
			self.colors_listing_searchbar = gtk.Entry()
			self.colors_listing_searchbar.set_tooltip_text("Search for key words")
			self.colors_listing_searchbar.set_alignment(0.5)
			self.colors_vbox.pack_start(self.colors_listing_searchbar, False, False)

			self.color_listing_old_new_combo = gtk.Combo()
			self.color_listing_old_new_combo.entry.set_editable(False)
			self.color_listing_old_new_combo.set_popdown_strings(["Old Color", "New color"])
			self.colors_vbox.pack_start(self.color_listing_old_new_combo, False, True)

			self.colors_list = gtk.ScrolledWindow()
			self.colors_list.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_NEVER)
			self.colors_hbox = gtk.HBox()
			self.colors_list.add_with_viewport(self.colors_hbox)
			self.colors_vbox.pack_start(self.colors_list, True, True)

			try:
				with open("colors.json", "r") as file:
					dict = json.load(file)
					for item in dict:
						btn = gtk.Button()
						btn.set_tooltip_text("Name: %s\nCode: %s\nType: %s" % (item["name"], item["code"], item["type"]))
						btn.connect("clicked", self.set_tab_selection, ((self.color_listing_old_new_combo, self.old_color_entry, self.new_color_entry, item["code"])))
						img = gtk.Image()
						img.set_from_file("images/colors/100/%s.png" % item["code"])
						btn.set_relief(gtk.RELIEF_NONE)
						btn.add(img)
						self.colors_hbox.pack_start(btn, True, True)
				self.colors_listing_searchbar.connect("event", self.tab_search_filter, (self.colors_list))
			except Exception as error:
				self.insert_text("Colors unavailable; an exception occurred, please verify integrity of the colors.json file.")
				self.insert_text(error)

		self.tabs = gtk.Notebook()
		self.tabs.set_show_border(True)
		self.tabs.set_scrollable(True)
		self.tabs.set_tab_pos(gtk.POS_RIGHT)#gtk.POS_LEFT, gtk.POS_RIGHT, gtk.POS_TOP, gtk.POS_BOTTOM
		console_init()
		self.tabs.append_page(self.console, gtk.Label("console"))
		parts_list_init()
		self.tabs.append_page(self.parts_vbox, gtk.Label("Parts"))
		colors_list_init()
		self.tabs.append_page(self.colors_vbox, gtk.Label("Colors"))
	#	self.tabs.set_tab_detachable(self.console, True)
		self.global_hbox.pack_start(self.tabs, True, True)

		'''PROGRESS BAR IF PARSING FILES'''
		self.progressbar = gtk.ProgressBar(adjustment=None)
		self.progressbar.set_orientation(gtk.PROGRESS_LEFT_TO_RIGHT)
		self.global_vbox.pack_start(self.progressbar, False, True)

		'''VISIBILITIES AT STARTUP'''
		self.window.show_all()
		self.insert_text("Welcome to the LDraw parts and color batch replacement utility")
		self.progressbar.hide()

		self.parse_button.set_sensitive(False)
		self.ext_type_combo.entry.connect("event", self.required_fields)
		self.parsing_type_combo.entry.connect("event", self.required_fields)
		self.old_parts_id_entry.connect("event", self.required_fields)
		self.new_part_id_entry.connect("event", self.required_fields)
		self.old_color_entry.connect("event", self.required_fields)
		self.new_color_entry.connect("event", self.required_fields)

		if not "-no-lib" in argv:
			gobject.threads_init()
			thread = threading.Thread(target=self.parts_threading)
			thread.setDaemon(True)
			thread.start()

if __name__ == "__main__":
	if "-help" in argv:
		print ""
		print " ", "-help    ", "\tPrint this help."
		print " ", "-debug   ", "\tPrint debug properties in terminal."
		print " ", "-no-lib  ", "\tDoes't load parts library on startup."
		print " ", "-dry-run ", "\tDoes't write changes to files."
		print ""
	else:
		utility = parser()
		utility.main()
