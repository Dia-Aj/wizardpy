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
			op1, op2 = map(str.strip, 
					(match.group('OP1'), match.group('OP2')) )

			if(match.group(1) == match.group(4)):
				(left, mid, right) = map(str.strip, 
							(match.group(3), match.group(1), match.group(6)) )

				"""If both operators are equal, then it takes only the min/max value
				   depending on the operator."""
				if(operators_is_equal(op1, op2)):
					code = self.sub_code(match.group(0), 
								  fix_equal_operators(op1, mid, left, right), code)
					continue

				"""
				z *<=* y and z >= x
				*<=* must be flipped to *>=* in order to make the 
				resulting expression valid 
				---> y *>=* z >= x

				same concept for the other cases 

				"""
				op1 = flip(op1)

			elif(match.group(1) == match.group(6)):
				(left, mid, right) = map(str.strip, 
							(match.group(3),match.group(1), match.group(4)) )
				# z *<=* y and x *<=* z
				# y *>=* z *>=* x

				if(operators_is_equal(op1, op2)):
					code = self.sub_code(match.group(0), 
								  fix_equal_operators(op1, mid, left, right), code)
					continue

				(op1, op2) = (flip(op1), flip(op2))

			elif(match.group(3) == match.group(4)):
				(left, mid, right) = map(str.strip,
							(match.group(1), match.group(3), match.group(6)) )

				if(operators_is_equal(op1, op2)):
					code = self.sub_code(match.group(0), 
								  fix_equal_operators(op1, mid, left, right), code)
					continue

				#no flipping required

			elif(match.group(3) == match.group(6)):
				(left, mid, right) = map(str.strip, 
							(match.group(1), match.group(3), match.group(4)))
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
		"""Substitute long or '==' comparsion for the same variable with 
		  'in' operator and parenthesis. """
		for match in matches:
			offset = match.group(0).split(' or ')

			#Create a list for each variable, if the statement contains multiple
			#variables and repeated comparsion 
			result = defaultdict(list)

			#Split each comparsion from '==' operator
			for comp in offset:
				(name, value) = map(str.strip, (comp.split('==')) )
				result[name].append(value)
	
			fix = ''

			#fix the comparsion for each key in the dictionary individually
			for name in result:
				if(fix != ''): fix+=' or '
				fix+=f"{name} in ({','.join(list(set(result[name])))})"

			code = self.sub_code(match.group(0), fix, code)

		return code

	@log_function
	def fix_inline_if_statement(self, matches, code):
		"""Reformat inline if statement"""

		for match in matches:
			#seperate between the if condition and the body with
			#new-line and a single TAB
			fix = f'{match.group(1)}:\n\t{match.group(2)}'

			code = self.sub_code(match.group(0), fix, code)

		return code

	@log_function
	def fix_naive_index_loop(self, matches, code):
		""" Fixes naive range(len(arr)) for loop to enumerate"""        
		for match in matches:
			(fix, var, container,
					body, statment) = ( match.group(0),
										match.group("var_name"),
										match.group("container_name"), 
										match.group("body"),
										match.group("statment")
			)
			#'element' is a random name given for the array elements
			#reformat the condition statment.
			fix_statment = f'for {var}, element in enumerate({container}):'

			#replace each naive call by indices with 'element' variable
			fix_body = body.replace(f'{container}[{var}]', 'element')
			fix = fix.replace(statment, fix_statment)
			fix = fix.replace(body, fix_body)

			code = self.sub_code(match.group(0), fix, code)

		return code

	@log_function
	def fix_naive_container_loop(self, matches, code):
		for match in matches:
			offset = lambda x: match.group(x)                        #shortcut function
			index = match.span()[0]
			pattern = re.compile(
				r"%s\s*=\s*(?P<Par>list\(.*\)|set\(.*\)|tuple\(.*\)|\(.*\)|\{.*\}|\[.*\]|\w+)+" % 
				offset("container"),re.VERBOSE
			)

			container = pattern.finditer(code, endpos = index)
			obj = list(container)[-1]
			index, container = obj.span(), obj.group('Par')
		
			(condition) = (f" {offset('condition').replace(':','')} " 
													 if offset("condition") else '')

			(opar, cpar) = (container[0], container[-1])
			fix = f"{opar}{offset('iterator')} "\
						f"for {offset('iterator')} in {offset('sequence')}{condition}{cpar}"
			if(container in ['[]', '()', '{}', 'tuple()', 'list()', 'set()']):
				fix = f"{offset('container')} = {fix}"

			else:
				fix = f"{offset('container')} = {container} + {fix}"

			code = code.replace(code[index[0]:index[1]], '')
			code = self.sub_code(offset(0), fix, code)

		return code

	@log_function
	def fix_strings_concat(self, matches, code):
		for match in matches:
			h_exp = match.group("expression")
			container = h_exp.split('+')
			container = [el.strip().replace(el.strip()[0], '') if el.strip()[0] in ('\"', "'")
				else "{leftpar}{var}{rightpar}".format(
					leftpar = '{', var = el.strip(), rightpar = '}')
				for el in container]

			fix = "print({}{}{})".format('f\"', ''.join(container), "\"")
			code = self.sub_code(match.group(0), fix, code)

		return code    

	@log_function
	def fix_inline_variable_assignment(self, matches, code):
		for match in matches:
			grp = lambda x: match.group(x)
			(variable, value1, value2, condition) = (
										grp('variable_name'), grp('variable_value1'),
										grp('variable_value2'), grp('condition'))

			fix = f'{variable} = {value1} if {condition} else {value2}'
			code = self.sub_code(match.group(0), fix, code)

		return code

	@staticmethod
	def sub_code(harmful_match, match_fix, code):
		code = code.replace(harmful_match, match_fix)
		return code


if __name__ == '__main__':
	sys.exit()
