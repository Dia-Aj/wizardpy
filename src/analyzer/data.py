regex = {
	'spacesep_defining': [
		'syntax',
		r'(\w+\s*=\s*\w+\n*){2,5}',

		'''
			x = 10
			y = 20
			z = 3
		fix to
			x, y, z = 10, 20, 3
		this works only on consecutive definitions.''',
	],

	'chained_comparison': [
		'syntax',
		r'(\w+)\s*(?P<OP1>[<=>]+)\s*(\w+)\s*and\s*(\w)+\s*(?P<OP2>[<=>]+)\s*(\w)+',
		'''
			if(y >= z and x<=z):
		fix to
			if(y >= z >= x): '''
	],

	'repeated_variable_or_comparsion': [
		'conditional',
		r'(\w+\s*==\s*[\'\"]?[A-Za-z0-9\.]+[\'\"]?\s*(or)?\s*)+',
		'''
			if(x == 1 or x == 2 or x == 3):
		fix to
			if(x in (1,2,3)):

		'''
	],
	

}