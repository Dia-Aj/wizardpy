import sys
import re

functions = {}

"""Log each function into functions dictionary.
   the rationale behind this is to map harmful 
   codes into the fixing function by regex name """
def log_function(function):
	functions.setdefault(function.__name__, function)

class code_optimizer:
	"""takes the passed harmfull code and returns
	   the idiomatic code"""

	@staticmethod
	def optimize(matches, regex_name, code):
		 new_code = functions['fix_'+regex_name](code_optimizer, matches, code)
		 return new_code

	@log_function
	def fix_spacesep_defining(self, matches, code):
		harmful = [match.group(0) for match in matches]
		groups = [a.split() for a in harmful]

		for group in groups:
			string, numeric = group[0], group[2]
			for i, j in enumerate(group):
				if(i < 3 or j == '='): continue
				if(group[i-1] == '='):
					numeric += f', {j}'
				else:
					string += f', {j}'
			
			fix = f'{string} = {numeric}\n\n'
			code = re.sub(harmful[groups.index(group)], fix, code)

		return code

	def sub_code(self, new_string):
		pass


if __name__ == '__main__':
	sys.exit()