regex = {
	'space-sep_defining': [
		'syntax',
		r'(\w+\s*=\s*\w+\n*)+',
		'''
		this regex find variables defined on the following form:-
			x = 10
			y = 20
			z = 3
		And fix it to
			x, y, z = 10, 20, 3

		this works only on consecutive definitions.
		''',
	],
}