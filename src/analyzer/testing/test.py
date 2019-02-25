import unittest
import os
import sys
path = os.path.split(sys.argv[0])[0]
sys.path.append(
			'\\'.join(path.split('\\')[:-2]))


from analyzer.analyzer import Regex

passed_code = '''foo = 10
fun = 20
bar = 30
baz = 40'''

expected_code = '''foo, fun, bar, baz = 10, 20, 30, 40'''


class testRegex(unittest.TestCase):
	def test_spacesep_defining(self):
		Regex.check_regex(passed_code)

		with open('optimizedCode.py', 'r') as file:
			output = file.read()
			
		self.assertIn(expected_code, output)


if __name__ == '__main__':
	unittest.main()





