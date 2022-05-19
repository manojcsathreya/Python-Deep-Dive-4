'''
__str__vs __repr__
->both used for creating a string representation of an object
->typically __repr__is used by developers
    ->try to make it so that the string could be used to recreated the object
    ->otherwise make it as descriptive as possible
    ->useful for debugging
    ->called when using the repr()function

->__str__is used by str()and print()functions, as well as various formatting functions
->typically used for display purposes to end user, logging, etc
->if __str__is not implemented, Python will look for __repr__instead
->if neither is implemented and since all objects inherit from 
Object, will use __repr__defined there instead
->we'll come back to this after we discuss inheritance
'''
#__str__ and __repr__
#Let's see how this works by first implementing the __repr__ method:

class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age
        
    def __repr__(self):
        print('__repr__ called')
        return f"Person(name='{self.name}, age={self.age}')"
p = Person('Python', 30)
#Here's how Jupyter shows us the string representation for the object p:

p
#__repr__ called
#Person(name='Python, age=30')
#Here's what it looks like when we use the print function:

print(p)
#__repr__ called
#Person(name='Python, age=30')
#Here's what happens if we call the repr function:

repr(p)
# =============================================================================
# __repr__ called
# "Person(name='Python, age=30')"
# And here's what happens when we call the str function:
# =============================================================================

str(p)
# =============================================================================
# __repr__ called
# "Person(name='Python, age=30')"
# As you can see, in all cases, our __repr__ method was called.
# 
# Now, let's implement a __str__ method:
# 
# =============================================================================
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age
        
    def __repr__(self):
        print('__repr__ called')
        return f"Person(name='{self.name}, age=self.age')"
    
    def __str__(self):
        print('__str__ called')
        return self.name
p = Person('Python', 30)
#And let's try out each of the ways to get a string representation for p:

p
# =============================================================================
# __repr__ called
# Person(name='Python, age=self.age')
# So, same as before - uses the __repr__ method.
# =============================================================================

print(p)
# =============================================================================
# __str__ called
# Python
# As you can see, print will try to use __str__ if present, otherwise it will fall back to using __repr__.
# =============================================================================

str(p)
# =============================================================================
# __str__ called
# 'Python'
# As expected, str() will try to use the __str__ method first.
# =============================================================================

repr(p)
# =============================================================================
# __repr__ called
# "Person(name='Python, age=self.age')"
# Whereas the repr() method will use the __repr__ method directly.
# 
# What happens if we define a __str__ method, but not __repr__ method.
# 
# We'll look at inheritance later, but for now think of it as Python providing "defaults" for those methods when they are not present.
# 
# Let's first see how it works if we do not have either of those methods for two different classes:
# =============================================================================

class Person:
    pass
​
class Point:
    pass
person = Person()
point = Point()
# =============================================================================
# repr(person), repr(point)
# ('<__main__.Person object at 0x7fbfe954b860>',
#  '<__main__.Point object at 0x7fbfe954b9e8>')
# As we can see, Python provides a default representation for objects that contains the class name, and the instance memory address.
# 
# If we use str() instead, we get the same result:
# 
# =============================================================================
str(person), str(point)
# =============================================================================
# ('<__main__.Person object at 0x7fbfe954b860>',
#  '<__main__.Point object at 0x7fbfe954b9e8>')
# Now let's go back to our original Person class and remove the __repr__ method:
# =============================================================================

class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age
    
    def __str__(self):
        print('__str__ called')
        return self.name
p = Person('Python', 30)
p
#<__main__.Person at 0x7fbfe9569e48>
repr(p)
#'<__main__.Person object at 0x7fbfe9569e48>'
#Since we do not have a __repr__ method, Python uses the "default" - it does not use our custom __str__ method!

#But if we use print() or str():

print(p)
# =============================================================================
# __str__ called
# Python
# =============================================================================
str(p)
# =============================================================================
# __str__ called
# 'Python'
# Lastly, various formatting functions will also prefer using the __str__ method when available. Lert's first go back to our Person class that implements both:
# =============================================================================

class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age
        
    def __repr__(self):
        print('__repr__ called')
        return f"Person(name='{self.name}, age=self.age')"
    
    def __str__(self):
        print('__str__ called')
        return self.name
p = Person('Python', 30)
f'The person is {p}'
#__str__ called
#'The person is Python'
'The person is {}'.format(p)
#__str__ called
#'The person is Python'
'The person is %s' % p
#__str__ called
#'The person is Python'
