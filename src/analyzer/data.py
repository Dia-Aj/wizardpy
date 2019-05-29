regex = {
	'spacesep_defining': [
		'syntax',
		r'''
		(\s*(?P<variable>\w+)\s*=\s*["']?(?P<value>\w+)["']?\s*){2,5} #matches sequence of variable = value
		''',

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
		r'''
		(?P<statment>for\s+												# for
		(?P<var_name>\w+)\s+in\s+range[(]{1}len[(]{1}					# var_name in range(len(
		(?P<container_name>\w+)[)]{2}:)									# container_name)):
		(?P<body>(\n\t.*)+)												#body loop
		''',
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
	    r'''  
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
		r'''
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
		r'''
		(?<!el)if\s*[(]?\s*(?P<condition>.+)\s*[)]?\s*:\s*         	 	#condition statment,
                                                                    	#(?<!el) -> negative look behind to avoid matching elif
        (?P<variable_name>\w+)\s*=\s*(?P<variable_value1>.+)\s*     	#value for first condition
        else\s*:\s*                                                    
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

	'list_joining':[
		'syntax',
		r'''
			(\s*(\w+)\s*=.+\s*)?
			for\s*(?P<element>\w+)\s*in\s*(?P<container>\w+)\s*:\s*                             # matches for element in container
            (if\s*[(]?\s*(?P<condition>.+)\s*[)]?\s*:\s*)?                                      # matches if statment if it exists

            (# match two forms of concatination     
            	( (?P<variable_f1>\w+)\s*[+]=\s*(?P<value_f1>\w+)\s* )|                         # matches form one: variable += element
            	( (?P<variable_f2>\w+)\s*=\s*(?P=variable_f2)\s*[+]\s*(?P<value_f2>\w+)\s* )    # matches form two: variable = variable + element
            )
		''',
		'''
		for element in container:
    		result += element
    	fix to
    		result = ''.join(container)

    	for element in result_list:
    		if condition:
        		result = result + element
        fix to
        	result = ''.join([i if condition for i in container])
		'''

	],

}