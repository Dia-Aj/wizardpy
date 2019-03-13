regex = {
	'spacesep_defining': [
		'syntax',
		r'(\w+\s*=\s*\w+\n*){2,5}',

		'''
		E.g.
			x = 10
			y = 20
			z = 3
		fixed it to
			x, y, z = 10, 20, 3
		this works only on consecutive definitions.''',
	],

	'chained_comparison': [
		'syntax',
		r'(\w+)\s*(?P<OP1>[<=>]+)\s*(\w+)\s*and\s*(\w)+\s*(?P<OP2>[<=>]+)\s*(\w)+',
		'''
		E.g.
			if(y >= z and x<=z)
		fixed to
			if(y >= z >= x) '''
	],

}