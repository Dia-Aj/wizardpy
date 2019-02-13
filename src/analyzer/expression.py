from dataclasses import dataclass
import sys

@dataclass
class exp:
	name : str
	type : str
	description : str
	pattern : repr

	def __init__(self, name, type, description, pattern):
		self.name = name
		self.type = type
		self.description = description
		self.pattern = pattern
