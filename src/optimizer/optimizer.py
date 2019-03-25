import sys
import re
from collections import defaultdict

functions = {}

def log_function(function):

	""" Log each function into functions dictionary. """
	functions.setdefault(function.__name__, function)

def flip(op):
	flipped_ops = {'>':'<', '<': '>', '>=' : '<=', '<=' : '>='}
	return flipped_ops[op]

def operators_is_equal(op1, op2):
	return op1 == op2

def fix_equal_operators(op, mid_var, left_value, right_value):
	if(op == '>'):
		fix = f'{mid_var} > {max(left_value, right_value)}'
	elif(op == '<'):
		fix = f'{mid_var} < {min(left_value, right_value)}'

	return fix


class code_optimizer:
	"""takes the passed harmfull code and returns
	   the idiomatic code"""

	@staticmethod
	def optimize(matches, regex_name, code):
		 new_code = functions['fix_'+regex_name](code_optimizer, matches, code)
		 return new_code

	@log_function
	def fix_spacesep_defining(self, matches, code):
		"""
		This method is to fix the multiple lines variables definition
		 e.g. x = 1
		 	  y = 2
		 change to: x, y = 1, 2 """

		#store the matches with thier spans
		harmful = [
			#the span is stored to figure out if the block of 
			#consecutive variables have ended.
			(match.group(0), match.span())
			for match in matches
		]

		#separate the variables name and value from each others 
		groups = [a[0].split() for a in harmful]
		for i, group in enumerate(groups):
			leftmost, rightmost = group[0], group[2]
			for i, j in enumerate(group):
				if(i < 3 or j == '='): continue
				#if the current item preceded by '=' then its a value
				#otherwise its a variable name
				if(group[i-1] == '='): 
					rightmost += f', {j}'
				else:
					leftmost += f', {j}'
			
			fix = f'{leftmost} = {rightmost}\n'

			ind = groups.index(group)
			#add a newline if the current declariton block has ended
			if(ind < len(harmful)-1 and 
						harmful[ind][1][1] != harmful[ind+1][1][0]):
				fix+='\n'
			
			#substitute the harmful code 
			code = self.sub_code(harmful[ind][0], fix, code)

		return code

	@log_function
	def fix_chained_comparison(self, matches, code):
		"""
			Substitutes 'and' with chained comparison in values
			comparing
			e.g. if(y >= z and x<=z)
			change to: if(y >= z >= x) """

		for match in matches:
			op1, op2 = match.group('OP1'), match.group('OP2')

			if(match.group(1) == match.group(4)):
				(left, mid, right) = (match.group(3), 
											match.group(1), match.group(6))
				"""
				z *<=* y and z >= x
				*<=* must be flipped to *>=* in order to make the 
				resulting expression valid 
				---> y *>=* z >= x

				same concept for the other cases 

				"""
				if(operators_is_equal(op1, op2)):
					code = self.sub_code(match.group(0), 
						          fix_equal_operators(op1, mid, left, right), code)
					continue

				op1 = flip(op1)

			elif(match.group(1) == match.group(6)):
				(left, mid, right) = (match.group(3), 
											match.group(1), match.group(4))
				# z *<=* y and x *<=* z
				# y *>=* z *>=* x
				if(operators_is_equal(op1, op2)):
					code = self.sub_code(match.group(0), 
						          fix_equal_operators(op1, mid, left, right), code)
					continue

				(op1, op2) = (flip(op1), flip(op2))

			elif(match.group(3) == match.group(4)):
				(left, mid, right) = (match.group(1), 
											match.group(3), match.group(6))

				if(operators_is_equal(op1, op2)):
					code = self.sub_code(match.group(0), 
						          fix_equal_operators(op1, mid, left, right), code)
					continue

				#no flipping required

			elif(match.group(3) == match.group(6)):
				(left, mid, right) = (match.group(1), 
											match.group(3), match.group(4))
				# y >= z and x *<=* z
				# y >= z *>=* x
				if(operators_is_equal(op1, op2)):
					code = self.sub_code(match.group(0), 
						          fix_equal_operators(op1, mid, left, right), code)
					continue

				op2 = flip(op2)
			
			else:
				continue
				
			fix = f'{left} {op1} {mid} {op2} {right}'
			code = self.sub_code(match.group(0), fix, code)

		return code


	@log_function
	def fix_repeated_variable_or_comparsion(self, matches, code):
		for match in matches:
			offset = match.group(0).split(' or ')
			result = defaultdict(list)
			for d in offset:
				(name, value) = (d.split('=='))
				result[name].append(value)
	
			fix = ''
			for name in result:
				if(fix != ''): fix+=' or '
				fix+=f"{name}in ({','.join(list(set(result[name])))})"

			code = self.sub_code(match.group(0), fix, code)

		return code

	@staticmethod
	def sub_code(harmful_match, match_fix, code):
		code = re.sub(harmful_match, match_fix, code)
		return code


if __name__ == '__main__':
	sys.exit()