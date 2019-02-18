import sys

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
		 fixed_code = functions[regex_name](matches, code)
		 return fixed_code

	@log_function
	def function(self):
		pass

	def sub_code(self, new_string):
		pass


if __name__ == '__main__':
	sys.exit()