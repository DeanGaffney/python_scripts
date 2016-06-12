#using lambda as a one line function
def epic(c,s):
	oneLineFunc = lambda c, s: c+s
	print oneLineFunc(c,s)

epic(4,2)

#using lambda to square a number
square = lambda x : x*x
print square(99)

#sum of RGB usng lambda
sumRGB = lambda r,g,b: r+g+b
print sumRGB(100,100,100)

#remove duplicates
#takes in elements and turns them into a set.
remove_duplicates = lambda iterable : set(iterable)
print remove_duplicates("roooot")
print remove_duplicates([1,1,1,1,1,2,3,4])

#convert a list to integers.
convert_list_to_int = lambda iterable: map(int,iterable)
print convert_list_to_int(["123","34567","21"])

#keep even numbers
is_even = lambda number: number % 2 == 0
evens_list = lambda lst: filter(is_even,lst)
print(evens_list(range(5)))

#zip,map and lambda functions
a = [1,2,3,4,5]
b = [2,2,9,0,9]

#zip combines to same length lists into pairs
result = zip(a,b)
print result

#get biggest number of the two lists using all functions
biggest_of_lists = map(lambda pair : max(pair),zip(a,b))
print biggest_of_lists

#map,reduce,filter,list comprehensions
a = range(1,21)
#make a new list by mapping a lambda function onto exisitng list.
b = map(lambda double_item: double_item * 2,a)
evens = filter(lambda number : number % 2 == 0,b)
print evens

#list comprehensions,another way to double all items
c = [x*2 for x in a]
print 'I am C'
print c

#make even number list using list comprehensions.
c = [x for x in a if x % 2 == 0]
print 'I am even C'
print c