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
		r'(\w+)\s*(?P<OP1>[<=>]+)\s*(\w+)\s*and\s*(\w)+\s*(?P<OP2>[<=>]+)\s*(\w+)',
		'''
			if(y >= z and x<=z):
		fix to
			if(y >= z >= x): '''
	],

	'inline_if_statement': [
		'format',
		r'(if?.+):(.+[^\n])',
		'''
			if(name == 'John'): print(name)
		fix to
			if(name == 'John'):
				print(name)
		'''
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

	'naive_index_loop': [
		'syntax',
		r'(?P<statment>for\s+(?P<var_name>\w+)\s+in\s+range[(]{1}len[(]{1}'\
								r'(?P<container_name>\w+)[)]{2}:)(?P<body>(\n\t.*)+)',
		'''
			my_container = ['Larry', 'Moe', 'Curly']

			for i in range(len(my_container)):
				print(f'{i}: {my_container[i]}')
		fix to
			for i, element in enumerate(my_container):
    			print(f'{i}: {element}')
		'''
	],

}