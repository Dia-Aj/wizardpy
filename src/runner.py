from analyzer.analyzer import run
import sys
import argparse
import os

TYPE_ERROR_MESSAGE = ':expected python type file\nEnter __name__ -h for more information'

def raise_error(error):
	print(f'error:{error}') #format error message

def check_type(file):
	""" to ensure the passed file type isn't
		anything other than python type. Otherwise, 
		it stops the programme from executing. """

	if(not file[-3:] == '.py'):
		raise_error(TYPE_ERROR_MESSAGE)
		sys.exit()

def check_path(path):
	""" checks if the passed file path is
		valid. Otherwise, it stops the programme 
		from executing. """

	if(path != os.getcwd()):
		try:
			os.chdir(path)
		except FileNotFoundError as err:
			raise_error(err)
			sys.exit()

def check_code(file):
	""" to see if the passed python file is
	    executing properly. Otherwise, it stops 
	    the programme. """

	if(os.system(f'python -m py_compile {file}')): #returns true when the the code has error
		sys.exit()

def parse():
	""" returns the entered file path and file name
		from the command line """

	parser = argparse.ArgumentParser()
	parser.add_argument('FILENAME', type = str, 
						help = 'python file name') #essential argument

	""" optional argument if the file
	 	is in the current directory (default 
	 	value equals current directory)"""

	parser.add_argument('-P', '--filepath', type = str, 
						help = 'path to the file directory.\
						Default is the current directory', 
						default = os.getcwd()) 
	
	args = parser.parse_args()

	return (args.filepath, args.FILENAME)

def run():

	(file_path, file_name) = parse()
	
	""" three required phases to check code validity 
	    before running the analyzer """
	check_type(file_name) 
	check_path(file_path)
	check_code(file_name)

	run(file_name)


if __name__ == '__main__':
	sys.exit() 