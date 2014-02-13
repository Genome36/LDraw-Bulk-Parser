#!/usr/bin/python
import pygtk, gtk
import os
from time import sleep
from urllib2 import urlopen

class parser: # mpd not finished!
	def insert_text(self, text):
		self.console_textview.get_buffer().insert(self.console_textview.get_buffer().get_end_iter(),  "\n" + str(text))
		adj = self.console.get_vadjustment()
		adj.set_value(adj.upper - adj.page_size)

	def progress(self, total):
		self.progressbar.show()
	#	while True:
		self.progressbar.set_fraction(int(1/len(total)))
		self.progressbar.set_text("Parsing files")
		if self.progressbar.get_fraction == 1:
			self.progressbar.hide()
			self.progressbar.set_fraction(0)
			#	break
			#while gtk.events_pending():
			#	gtk.main_iteration()

	def write(self, path, filename, index, content):
		try:
			new_file =  open(os.path.join(path, filename), "w+")
			for i in range(len(content)):
				new_file.write(content[i])
			new_file.close()

		except Exception as error:
			self.insert_text(error)
			print error

	def replace_colors(self, path, filename):
		try:
			with open(os.path.join(path, filename), "r") as file:
				content= file.readlines()
				for line in content:
					if line.startswith("1 %s" % (self.color_old)):
						self.index = content.index(line)
						if line[3] == " ":
							new_line = line.replace(line[:3], "1 %s" % (self.color_new))
						else:
							new_line = line.replace(line[:4], "1 %s" % (self.color_new))
						content[self.index] = new_line
						self.insert_text("replacing %s \rwith %s \r in %s \n" % (line, new_line, filename))
						print "\n", "replacing", line, "with", new_line, "in", filename, "\n"

				#	while gtk.events_pending():
				#		gtk.main_iteration()

				self.write(path, filename, self.index, content)

		except Exception as error:
			self.insert_text(error)
			print error

	def replace(self, path, filename):
		try:
			with open(os.path.join(path, filename), "r") as file:
				content = file.readlines()
				for line in content:
					for part in self.parts:
						if part+".dat" in line:
							self.index = content.index(line)
							if line[3] == " ":
								new_line = line.replace(line[:3], "1 %s" % (self.color_new))
							else:
								new_line = line.replace(line[:4], "1 %s" % (self.color_new))
							content[self.index] = new_line
							self.insert_text("replacing %s \rwith %s \r in %s \n" % (line, new_line, filename))
							print "\n", "replacing", line, "with", new_line, "in", filename, "\n"

					#	while gtk.events_pending():
					#		gtk.main_iteration()

				self.write(path, filename, self.index, content)

		except Exception as error:
			self.insert_text(error)
			print error

	def replace_mpd(self, path, filename):
		try:
			with open(os.path.join(path, filename), "r") as file:
				sections = file.read().split("0 FILE")
				sections_lenth = len(sections)
				for i in sections_lenth:
					sections[i] = "0 FILE"+sections[1]
				for i in range(sections_lenth):
					text+sections[i]

				content = text.readlines()
				for line in content:
					for part in self.parts:
						if part+".dat" in line:
							self.index = content.index(line)
							new_line = line.replace(line[:4], "1 %s" % (self.color_new))
							content[self.index] = new_line
							self.insert_text("replacing %s \rwith %s \r in %s \n" % (line, new_line, filename))
							print "\n", "replacing", line, "with", new_line, "in", filename, "\n"

					#	while gtk.events_pending():
					#		gtk.main_iteration()

				self.write(path, filename, self.index, content)

		except Exception as error:
			self.insert_text(error)
			print error

	def parser(self, path, fileName):
		ext = [".ldr", ".mpd" ]
		if fileName[-4:] not in ext:
			pass
		else:
			if fileName[-4:] in ext and self.extension == "both":
				self.insert_text("Found %s" % (fileName))
				print "Found", fileName
				if self.color_option == "part":
					self.replace(path, fileName)
				else:
					self.replace_colors(path, fileName)

			if fileName[-4:] == ".ldr" and self.extension == "ldr":
				self.insert_text("Found %s" % (fileName))
				print "Found", fileName
				if self.color_option == "part":
					self.replace(path, fileName)
				else:
					self.replace_colors(path, fileName)

			if fileName[-4:] == ".mpd" and self.extension == "mpd":
				self.insert_text("Found %s" % (fileName))
				print "Found", fileName
				if self.color_option == "part":
					self.replace_mpd(path, fileName)
				else:
					self.replace_colors(path, fileName)

		#	sleep(0.125)

	def find_files(self, widget, data=None):
		key_words_get = self.key_words_entry.get_text()
		if key_words_get != "":
			if ", " in key_words_get:
				self.key_words = key_words_get.split(", ")
			else:
				self.key_words = [key_words_get]

		self.extension = self.ext_type_combo.entry.get_text()
		#self.body_part = raw_input('.mpd section name as body part seperaw_input("'color' for replacing color integer with another color integer\n'part' for replacing given part(s) color(s) with a color: ").lower()

		parts_id_get = self.parts_id_entry.get_text()
		if parts_id_get != "":
			if ", " in parts_id_get:
				self.parts = parts_id_get.split(", ")
			else:
				self.parts = [parts_id_get]

		self.color_option = self.parsing_type_combo.entry.get_text()
		if self.old_color_entry.get_text() != "":
			self.color_old = int(self.old_color_entry.get_text())
		if self.new_color_entry.get_text() != "":
			self.color_new = int(self.new_color_entry.get_text())

		try:
			self.parse_button.set_sensitive(False)
			for path, dirs, files in os.walk(self.system_path):
				files_list = files
				for fileName in files:
					if self.key_words not in ("", None):
						for key in self.key_words:
							if key in fileName:
								self.parser(path, fileName)
					else:
						self.parser(path, fileName)
					self.progress(files_list.pop(files_list.index(fileName)))
					while gtk.events_pending():
						gtk.main_iteration()
			self.parse_button.set_sensitive(True)
		except Exception as error:
			self.insert_text(error)
			print error

	def required_fields(self, widget, data=None):
		if self.parsing_type_combo.entry.get_text() == "part":
			self.parts_id_entry.set_sensitive(True)
			self.old_color_entry.set_sensitive(False)
			if self.system_path != "" and self.parts_id_entry.get_text() != "" and self.new_color_entry.get_text() != "":
				self.parse_button.set_sensitive(True)
			else:
				self.parse_button.set_sensitive(False)

		elif self.parsing_type_combo.entry.get_text() == "color":
			self.parts_id_entry.set_sensitive(False)
			self.old_color_entry.set_sensitive(True)
			if self.system_path != "" and self.old_color_entry.get_text() != "" and self.new_color_entry.get_text() != "":
				self.parse_button.set_sensitive(True)
			else:
				self.parse_button.set_sensitive(False)

	def folderchooser(self, widget, title):
		self.fc = gtk.FileChooserDialog(title, self.window, gtk.FILE_CHOOSER_ACTION_SELECT_FOLDER, (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_OPEN, gtk.RESPONSE_OK))
		self.fc.run()
		self.system_path = self.fc.get_filename()
		self.insert_text("You chose: %s" % (self.fc.get_filename()))
		print self.fc.get_filename()
		self.fc.destroy()
		self.required_fields(None)

	def about(self, widget, data=None):
		self.about = gtk.AboutDialog()
		self.about.set_size_request(475, 275)
		self.about.set_name("Oren Titane")
		self.about.set_program_name("Ldraw bulk parser")
		self.about.set_version("0.1.0")
		self.about.set_copyright("(C) Oren Titane")
	#	self.about.set_comments("coments")
		try:
			self.about.set_license(urlopen("https://raw.github.com/Genome36/LDraw-Bulk-Parser/master/EULA.license").read())
		except:
			self.about.set_license("License unavailable at this current moment.\nPlease verify internet connection or restart utility.")
		self.about.set_wrap_license(True)
		self.about.set_website("https://github.com/Genome36/Ldraw-Bulk-Parser")
	#	self.about.set_website_label("")
		self.about.set_authors(("Oren Titane - (Genome36)", ""))
		self.about.set_documenters(("Oren Titane - (Genome36)", ""))
		self.about.set_artists(("Oren Titane - (Genome36)", ""))
		self.about.set_translator_credits("Oren Titane - (Genome36)")
		self.logo2 = gtk.gdk.pixbuf_new_from_file(r"icon.png")
		self.about.set_logo(self.logo2)
	#	self.about.set_logo_icon_name("")
		self.about.show_all()
		self.about.run()
		self.about.destroy()

	def destroy(self, widget, data=None):
		gtk.main_quit()
		exit()

	def main(self):
		gtk.main()

	def __init__(self):
		self.system_path = ""
		self.key_words = ""
		self.extension = ""
		#self.body_part = ""
		self.parts = []
		self.color_old = ""
		self.color_new = ""
		self.index = None
		self.files_list = []

		'''MAIN WINDOW'''
		self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
		self.window.set_position(gtk.WIN_POS_CENTER)
		self.window.set_title("Ldraw bulk parser")
		self.window.set_size_request(700, 380)
		self.window.set_border_width(0)
		self.window.connect("destroy", self.destroy)

		self.global_vbox = gtk.VBox()
		self.window.add(self.global_vbox)

		self.global_hbox = gtk.HBox()
		self.global_vbox.pack_start(self.global_hbox, True, True)

		self.right_panel_frame = gtk.Frame()
		self.global_hbox.pack_start(self.right_panel_frame, False, False)

		self.right_panel_vbox = gtk.VBox()
		self.right_panel_frame.add(self.right_panel_vbox)

		self.about_button = gtk.Button()
		self.about_button.connect("clicked", self.about, None)
		self.right_panel_vbox.pack_start(self.about_button, True, True)

		self.logo = gtk.Image()
		self.logo.set_from_file(r"icon.png")
		self.about_button.add(self.logo)

		'''WINDOW PANE'''
		self.open_folder = gtk.Button("Open folder")
		self.open_folder.set_tooltip_text("Open folder to parse")
		self.open_folder.connect("clicked", self.folderchooser, "Choose folder to parse")
		self.right_panel_vbox.pack_start(self.open_folder, False, False)

		self.parsing_options_hbox = gtk.HBox()
		self.right_panel_vbox.pack_start(self.parsing_options_hbox, False, False)

		self.parsing_labels_vbox = gtk.VBox()
		self.parsing_options_hbox.pack_start(self.parsing_labels_vbox, False, False)

		self.key_words_label = gtk.Label("Key words")
		self.parsing_labels_vbox.pack_start(self.key_words_label, True, True)

		self.ext_type_combo_label = gtk.Label("Extensions")
		self.parsing_labels_vbox.pack_start(self.ext_type_combo_label, True, True)

		self.parsing_type_combo_label = gtk.Label("Parsing type")
		self.parsing_labels_vbox.pack_start(self.parsing_type_combo_label, True, True)

		self.parts_id_label = gtk.Label("Parts id(s)")
		self.parsing_labels_vbox.pack_start(self.parts_id_label, True, True)

		self.old_color_label = gtk.Label("Old color")
		self.parsing_labels_vbox.pack_start(self.old_color_label, True, True)

		self.new_color_label = gtk.Label("New color")
		self.parsing_labels_vbox.pack_start(self.new_color_label, True, True)

		self.parsing_entries_vbox = gtk.VBox()
		self.parsing_options_hbox.pack_start(self.parsing_entries_vbox, False, False)

		self.key_words_entry = gtk.Entry()
		self.key_words_entry.set_tooltip_text('specify "key words" to look for in filenames\nseperated by a comma and a space (", ")\nCAUTION: key words are case sensitive')
		self.parsing_entries_vbox.pack_start(self.key_words_entry, True, True)

		self.ext_type_combo = gtk.Combo()
		self.ext_type_combo.entry.set_editable(False)
		self.ext_type_combo.set_tooltip_text("Extensions")
		self.ext_type_combo.set_popdown_strings(["both", "ldr", "mpd"])
		self.parsing_entries_vbox.pack_start(self.ext_type_combo, True, True)

		self.parsing_type_combo = gtk.Combo()
		self.parsing_type_combo.entry.set_editable(False)
		self.parsing_type_combo.set_tooltip_text("Parse part(s) old color with new color / old color with new color")
		self.parsing_type_combo.set_popdown_strings(["part", "color"])
		self.parsing_entries_vbox.pack_start(self.parsing_type_combo, True, True)

		self.parts_id_entry = gtk.Entry()
		self.parts_id_entry.set_tooltip_text('Part(s) id seperated by a comma and a space (", ")\nCAUTION: key word(s) are case sensitive.')
		self.parsing_entries_vbox.pack_start(self.parts_id_entry, True, True)

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

		self.console_vbox = gtk.VBox()
		self.parsing_options_hbox.pack_start(self.console_vbox, True, True)

		self.console = gtk.ScrolledWindow()
		self.console_textview = gtk.TextView()
		self.console_textview.set_editable(False)
		self.console_textview.set_wrap_mode(gtk.WRAP_WORD)
		self.console_textbuffer = self.console_textview.get_buffer()
		self.console.add(self.console_textview)
		self.global_hbox.pack_start(self.console, True, True)

		'''PROGRESS BAR IF PARSING FILES'''
		self.progressbar = gtk.ProgressBar(adjustment=None)
		self.progressbar.set_orientation(gtk.PROGRESS_LEFT_TO_RIGHT)
		self.global_vbox.pack_start(self.progressbar, False, True)

		'''VISIBILITIES AT STARTUP'''
		self.window.show_all()

		self.insert_text("Welcome to the ldraw parts color batch replacement utility\n")
		print "Welcome to the ldraw parts color batch replacement utility"

		self.progressbar.hide()

		self.parse_button.set_sensitive(False)
		self.ext_type_combo.entry.connect("event", self.required_fields)
		self.parsing_type_combo.entry.connect("event", self.required_fields)
		self.parts_id_entry.connect("event", self.required_fields)
		self.old_color_entry.connect("event", self.required_fields)
		self.new_color_entry.connect("event", self.required_fields)
		self.required_fields(None)

if __name__ == "__main__":
	utility = parser()
	utility.main()
