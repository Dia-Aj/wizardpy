import sys
import argparse
import os

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
	print(file_path, file_name)

if __name__ == '__main__':
	sys.exit()