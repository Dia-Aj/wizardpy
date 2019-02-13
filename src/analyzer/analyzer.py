from expression import exp
from data import regex # EXPRESSIONS DIRECTORY
import sys

data = regex

class Regex:
	'''Holds all the regular expression inside data.py file
	   and find all the matches with the passed code then
	   passes each match to the optimizer individually'''

	#reads the regular expressions from data.py and 
	#create object for each regex
	_data = [
		exp(re, data[re][0], data[re][1], data[re][2])
		for re in data
	]
	_numberOfRegex = len(_data) #Count the overall number of the regular expressions

	def __repr__(self):
		return f'{Regex.__name__}(name, pattern = None, type = None, description = None)'

	def __len__(self):
		return Regex._numberOfRegex

	@staticmethod
	def find_matches(self, string):
		pass 


if __name__ == '__main__':
	sys.exit()

