from collections import namedtuple

testTuple = namedtuple('Test', ['passed_code', 'expected_code'])

tests = {
	testTuple('foo = 10\n'\
		'fun = 20\n'\
		'bar = 30\n'\
		'baz = 40\n',

	 'foo, fun, bar, baz = ' \
	 				'10, 20, 30, 40'
	 				),

	testTuple('a = 10\n'\
			  'b = 20\n'\
			  'c = 30\n\n'\
			  'for i in range(1,5):\n'\
			  '\tprint(i)\n\n'\
			  'a, b, c = 1, 2, 3\n\n'\
			  'a = 1\n'\
			  'b = 2\n'\
			  'c = 3',

			  'a, b, c = 10, 20, 30\n\n'\
			  'for i in range(1,5):\n'\
			  '\tprint(i)\n\n'\
			  'a, b, c = 1, 2, 3\n\n'
			  'a, b, c = 1, 2, 3'
		)
}