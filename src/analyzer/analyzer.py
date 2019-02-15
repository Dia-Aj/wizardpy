from analyzer.expression import exp
from analyzer.data import regex
from optimizer.optimizer import code_optimizer
import sys
import re

data = regex
ERR_RE_MSG = 'Error: invalid regular expression'

class Regex:
	
	'''Holds all the regular expression inside data.py file
	   and find all the matches with the passed code then
	   passes each match to the optimizer individually'''

	#reads the regular expressions from data.py and 
	#create object for each regex
	_data = [
		exp(re, data[re][0], data[re][1], data[re][2])
		for re in data
	] #exp(name, type, pattern, description)
	_numberOfRegex = len(_data) #Count the overall number of the regular expressions

	def __len__(self):
		return Regex._numberOfRegex

	@staticmethod
	def read_code(file):
		with open(file) as f:
			content = file.read()

		return content

	@staticmethod
	def compile_regex(regex):
		try:
			pattern = re.compile(regex.pattern)
		except:
			print(f'{ERR_RE_MSG}\nName:{regex.name}\nType:{regex.type}')
		else:
			return pattern

	@staticmethod
	def find_matches(pattern, code):
		matches = pattern.finditer(code)
		code_optimizer.optimize(matches, code)

	@staticmethod
	def check_data(code_file):
		code = read_code(code_file)
		for regex in _data:
			pattern = compile_regex(regex)
			if(not pattern.search(code)):
				continue

			find_matches(pattern, code)


if __name__ == '__main__':
	sys.exit()
