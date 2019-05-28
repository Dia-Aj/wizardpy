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

	'naive_container_loop':[
		'syntax',
	    '''  
        (?P<main_loop>for\s+                                             #for                
      	(?P<iterator>\w+)\s+in\s+                                        #iterator in
      	(?P<sequence>range(.+)|\(.+\)|\{.+\}|\[.+\]|\w+)):\s             #sequence
      	\s*(?P<condition>if\(.+\):)?\s*                                  #condition_statment(optional)
      	\s(?P<container>\w+)\.append(.+)                                 #container.append(...)
      	''',
      	''' 
      		container = [1, 2, 3]
      		for i in range(5):
      			if(i % 2 == 0):
      				container.append(i)
      	fix to
      		container = container + [i for i in range(5) if(i % 2 == 0)]

      	'''
	],

    'strings_concat':[
		'syntax', 
		'''
        print[(](?P<expression>(				 						#match sequence of string concatination 
			(
			  	(["]([^"].*)["] |         	 							#match double quotation string ("string")
             	[']([^'].*)[']) | 			 							#match single quotation string ('string')
             	\w+														#match a variable
             								 							
             )\s*[+]?\s*     				 
         )*)[)]
        ''',
		'''
		 	band = "The Beatles"
		 	print("My favorite band  is " + band)
		fix to
			print(f'My favorite band is {band}')
		'''
	],

	'inline_variable_assignment':[
		'syntax',
		'''
		(?<!el)if\s*[(]?\s*(?P<condition>.+)\s*[)]?\s*:\s*         	 	#condition statment,
                                                                    	#(?<!el) -> negative look behind to avoid matching elif
        (?P<variable_name>\w+)\s*=\s*(?P<variable_value1>.+)\s*     	#value for first condition
        else:\s*                                                    
        (?P=variable_name)\s*=\s*(?P<variable_value2>.+)\s*         	#value if the first condition isn't statisfied

		''',
		'''
		if condition:
			var = value1
		else:
			var = value2

		fix to
			var = value1 if condition else value2

		'''
	],

}