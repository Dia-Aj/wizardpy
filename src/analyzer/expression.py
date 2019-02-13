
from dataclasses import dataclass
import sys

@dataclass
class exp:
	'''to encapsulate each regex details
	   which would make it easier to track
	   errors'''

	#regex name
	name : str 
	
	#regex catagory
	type : str 

	'''an example code (as string) 
	   for the corresponding regex'''
	description : str   

	#the regex patteren
	pattern : repr 

	def __init__(self, name, type, pattern, description = None):
		self.name = name
		self.type = type
		self.description = description
		self.pattern = pattern

if __name__ == '__main__':
	sys.exit()