from expression import exp
from data import regex # EXPRESSIONS DIRECTORY
import sys

data = regex

class Regex:
	
	_data = [
		exp(re, data[re][0], data[re][1], data[re][2])
		for re in data
	] # holds all patterns
	_numberOfRegex = len(_data) #Count the overall number of the regular expressions

	def __repr__(self):
		return f'{Regex.__name__}(name, pattern = None, type = None, description = None)'

	def __len__(self):
		return Regex._numberOfRegex

	@staticmethod
	def find_matches(self, string):
		pass 


def main():
	pass

if __name__ == '__main__':
	main()