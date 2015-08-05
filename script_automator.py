#!/usr/bin/python

######################################################################
# Created on 4 August 2015
#
# Option 1
# A simple script that automates the process of writing
# information to the top bit of a file or script. When run the script adds
# a title, a shebang, an author, script or file information, time it was
# created to the top of the file. 
#
# Option 2
# The script when run with the option
# python createInfo.py -f <filepath> -c can also add the same information 
# in option 1 to an existing script. It does so without altering the data 
# that already exists within that script.
# 
########################################################################

import time
import optparse
import os

class Time(object):
	"""The current date and time"""

	def get_date(self, format='%d/%m/%Y'):
		"""returns the current date"""
		return time.strftime(format)

	def get_time(self):
		"""returns the current date"""
		return time.strftime("%X")

class Description(object):
	"""The description of the script"""

	def get_author(self, author='Egbie Anderson'):
		"""return the author name"""
		return author

	def get_script_description(self, message):
		"""Get a description for the file"""
		text = []

		if len(message) < 80:
			return False, message

		while len(message) > 85:
			text.append(message[:80])
			message = message[80:]
		text.append(message[0:])

		return True, text
		
class Format(object):
	"""A simple class creates the format for the page"""

	def get_border(self, num):
		return "#" * num
		
class InputOutput(Format):
	"""Allows the user to input data to a text file"""

	def __init__(self, file_name, loc):
		
		self._file_location = os.path.join(loc, file_name)      # createe a file path
		self._create_file(self._file_location)                  # create a file at that location
		self._add_string('#!/usr/bin/python')                   # add a shebang to the top of the file
		self._add_string('\n')
		self._add_string(self.get_border(80))			   # add a border to the top of that page

	def load(self, file_name):
		"""load an existing file"""
		with open(file_name) as f:
			my_file = f.read()
		return my_file

	def write(self, new_file, old_file):

		with open(new_file, "a") as f:
			f.write(old_file)

	def _create_file(self, file_name):
		"""Create an empty file"""

		f = open(file_name, "w")
		f.close()

	def _add_string(self, string):
		"""append text to a file"""
		f = open(self._file_location, "a")
		f.write(str(string))
		f.write('\n')
		f.close()

	def get_user_input(self):
		"""Get input from the user"""

		title, script_description, version = False, False, False

		while True:

			print
			if not title:
				title = raw_input("[+] Enter name of the script : ")
			if not script_description:
				script_description = raw_input("[+] Enter the description for the script : ")
			if not version:
				version = raw_input("[+] Enter the version number : ")
			if title and script_description and version:
				break

		return title, script_description, version
			
def create_template(user_obj):
	"""creates the information heading for the file"""

	info = Description()
	time = Time()
	border = Format()
	title, description, version = user_obj.get_user_input()
	user_obj._add_string(border.get_border(1))

	time_str = "{} Created on the {} at {} hrs".format(border.get_border(1), time.get_date(), time.get_time())
	author   = "{} Created by : {} ".format(border.get_border(1), info.get_author())
	script_name = "{} Name of the script : {} ".format(border.get_border(1), title)
	ver = "{} This is version : {} ".format(border.get_border(1), version)
	val, script_description = info.get_script_description(description)

	user_obj._add_string(time_str)
	user_obj._add_string(script_name)
	user_obj._add_string(author)
	user_obj._add_string(ver)
	user_obj._add_string(border.get_border(1))
	user_obj._add_string(border.get_border(1))
	user_obj._add_string("{} File description ".format(border.get_border(1)))
	user_obj._add_string(border.get_border(1))

	if not val:
		user_obj._add_string("{} {}".format(border.get_border(1), script_description))

	else:
		for text in script_description:
			user_obj._add_string("{} {}".format(border.get_border(1), text))

	user_obj._add_string(border.get_border(1))
	user_obj._add_string(border.get_border(80))


def main():

	parser = optparse.OptionParser("usage -f <filename> -l <dir location> or -f <file_path> -c" )
	parser.add_option('-f', '--filename', dest="filename", type=str, help="Enter the name of a file")
	parser.add_option('-l', '--location', dest="location", type=str, help="Enter location")
	parser.add_option('-a', '--add', action="store_true", dest="add", default=False, 
		                      help="edit existing file")
	options, args = parser.parse_args()

	# adds information to a new file.
	if (options.filename and options.location): 
		if not os.path.exists(options.location) and not os.path.isdir(options.location):
			print "[+] The location for the file is not valid. Enter a valid file location"
			exit(0)

		user = InputOutput(options.filename, options.location)
		create_template(user) # create the template

	# Enables information to be added to the top of a file or script that already
	# has information without overiding the information that already exists in the file.
	elif not options.location and options.filename and options.add:
		if os.path.exists(options.filename):

			file_path = os.path.dirname(options.filename)
			user = InputOutput("log.txt", file_path)
			
			old_file = user.load(options.filename)
			user = InputOutput(options.filename, file_path)
			create_template(user)
			user._add_string('\n')
			user._add_string(old_file)
	else:
		print """
			Script usage:

			option 1 for new files
			python createInfo.py -f <filename> -l <location for new file>

			option 2
			python createInfo.py -f <file path> -c
		"""

if __name__ == "__main__":
	main()

