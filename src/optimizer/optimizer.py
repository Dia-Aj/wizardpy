import sys
import re

functions = {}

"""Log each function into functions dictionary.
   the rationale behind this is to map harmful 
   codes into the fixing function by regex name """
def log_function(function):
	functions.setdefault(function.__name__, function)

def flip(op):
	flipped_ops = {'>':'<', '<': '>', '>=' : '<=', '<=' : '>='}
	return flipped_ops[op]

class code_optimizer:
	"""takes the passed harmfull code and returns
	   the idiomatic code"""

	@staticmethod
	def optimize(matches, regex_name, code):
		 new_code = functions['fix_'+regex_name](code_optimizer, matches, code)
		 return new_code

	@log_function
	def fix_spacesep_defining(self, matches, code):
		harmful = [
			(match.group(0), match.span())
			for match in matches
		]
		groups = [a[0].split() for a in harmful]
		
		for i, group in enumerate(groups):
			string, numeric = group[0], group[2]
			for i, j in enumerate(group):
				if(i < 3 or j == '='): continue
				if(group[i-1] == '='):
					numeric += f', {j}'
				else:
					string += f', {j}'
			
			fix = f'{string} = {numeric}\n'

			ind = groups.index(group)
			if(ind < len(harmful)-1 and 
						harmful[ind][1][1] != harmful[ind+1][1][0]):
				fix+='\n'
			
			code = re.sub(harmful[ind][0], fix, code)

		return code

	@log_function
	def fix_chained_comparison(self, matches, code):

		for match in matches:

			op1, op2 = match.group('OP1'), match.group('OP2')
			if(match.group(1) == match.group(4)):
				(left, mid, right) = (match.group(3), 
											match.group(1), match.group(6))
				op1 = flip(op1)

			elif(match.group(1) == match.group(6)):
				(left, mid, right) = (match.group(3), 
											match.group(1), match.group(4))
				(op1, op2) = (flip(op1), flip(op2))

			elif(match.group(3) == match.group(4)):
				(left, mid, right) = (match.group(1), 
											match.group(3), match.group(6))

			elif(match.group(3) == match.group(6)):
				(left, mid, right) = (match.group(1), 
											match.group(3), match.group(4))
				op2 = flip(op2)
			
			else:
				continue
				
			fix = f'{left} {op1} {mid} {op2} {right}'
			code = re.sub(match.group(0), fix, code)

		return code

	def sub_code(self, new_string):
		pass


if __name__ == '__main__':
	sys.exit()