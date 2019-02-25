import unittest
import os
import sys
path = os.path.split(sys.argv[0])[0]
sys.path.append(
			'\\'.join(path.split('\\')[:-2]))


from analyzer.analyzer import Regex

