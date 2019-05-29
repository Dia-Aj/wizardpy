x = 10
y = 20
z = 30
name = 'John'

if(x > 200): pass

elif(100 < x and x < 200 and 300 < y and y < 800):
	pass

if(x == 1 or x == 2 or y == 10 or y == 3): print("yes")

if(name == 'John'): print(name)

my_container = ['Larry', 'Moe', 'Curly']
for i in range(len(my_container)):
	print(i, my_container[i])
	my_container[i] = 10
	my_container[i] *= 20

print(my_container)

x = '10'
y = '20'
z = '30'
a = '40'


container = [2]
for i in range(10):
	if(i > 5 and i%3 == 0):
		container.append(i)

container = []
for i in range(20):
	if(i%2 == 0 and i > 5):
		container.append(i)

band = "The beatles"
print("My favorite band is " + band)

name = "John"
age = 24
hobby = "programming"

print("Hello, my name is " + name + " I'm " + age + " years old. My hobby is " + hobby)

if condition:
    string = value1
else:
    string = value2


contianer = ['A', 'B', 'C']
result = ''
for element in container:
    result += element

for element in result_list:
    if condition:
        result = result + element
