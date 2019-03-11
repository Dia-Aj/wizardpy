from testcases import tests 
import unittest
import os
import sys
path = os.path.split(sys.argv[0])[0]
sys.path.append(
			'\\'.join(path.split('\\')[:-2]))

from analyzer.analyzer import Regex

class testRegex(unittest.TestCase):
	def test_snippet(self):
		for test in tests:
			Regex.check_regex(test.passed_code)

			with open('optimizedCode.py', 'r') as file:
				output = file.read()
			
			try:
				self.assertIn(test.expected_code, output)
			except AssertionError:
				print(f'error expected:\n{test.expected_code}'\
					f'\nbut found:\n{output}')

if __name__ == '__main__':
	unittest.main()





