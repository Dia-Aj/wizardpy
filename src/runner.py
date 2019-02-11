import sys
import argparse
import os

def raise_error(error):
	print(f'error:{error}')

def checkType(file):
	return file[-3:] == 'py'

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
	
	if(not checkType(file_name)):
		raise_error(':expected python type file\nEnter __name__ -h for more information')
		sys.exit()


if __name__ == '__main__':
	sys.exit()