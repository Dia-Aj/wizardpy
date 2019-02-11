import sys
import argparse
import os

TYPE_ERROR_MESSAGE = ':expected python type file\nEnter __name__ -h for more information'

def raise_error(error):
	print(f'error:{error}')

def checkType(file):
	if(not file[-3:] == '.py'):
		raise_error(TYPE_ERROR_MESSAGE)
		sys.exit()

def parse():
	parser = argparse.ArgumentParser()
	parser.add_argument('FILENAME', type = str, 
						help = 'python file name')
	parser.add_argument('-P', '--filepath', type = str, 
						help = 'path to the file directory.\
						Default is the current directory', 
						default = os.getcwd())
	
	args = parser.parse_args()

	return (args.filepath, args.FILENAME)

def run():

	(file_path, file_name) = parse()
	
	checkType(file_name)
	

if __name__ == '__main__':
	sys.exit()