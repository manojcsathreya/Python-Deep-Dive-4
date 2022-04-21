'''
INITIALIZING CLASS INSTANCES


When we instantiate a class, by default Python does two separate things:
->creates a new instance of the class
->initializes the namespace of the class

class MyClass:
    language = 'Python' 
    

obj = MyClass() 
obj.__dict__ # {}

We can provide a custom initializer method that Python will use instead of its own:
class MyClass:
    language = 'Python'
    def __init__(obj, version):
        obj.version = version

notice that __init__is defined to work as a bound instance method
---------------------------------------------------------------------------------------
Deconstructing  this…
class MyClass:
    language = 'Python'
def __init__(obj, version): <USING self IS A convention)>
    obj.version = version

language is a class attribute -in class namespace
__init__is a class attribute -in class namespace(as a function)

when we call MyClass('3.7')
-Python creates a new instance of the object with an empty namespace
-if we have defined an __init__function in the class
-it calls obj.__init__('3.7') àbound method à MyClass.__init__(obj, '3.7')
-our function runs and adds versionto obj's namespace
-versionis an instance attribute
obj.__dict__ - {'version': '3.7'} 
a standard convention is to use an argument named self
--------------------------------------------------------------------------------------
Important!

By the time __init__is called
Python has already created the object and a namespace for it (like a __dict__in most cases)
then __init__is called as a method bound to the newly created instance

We can actually also specify a custom function to create the object

__new__

we'll come back to this later

But __init__is not creating the object, it is only running some code after the 
instance has been created
-----------------------------------------------------------------------------------------

'''
'''
When we create a new instance of a class two separate things are happening:

The object instance is created
The object instance is then further initialized
We can "intercept" both the creating and initialization phases, by using special methods __new__ and __init__.

We'll come back to __new__ later. For now we'll focus on __init__.

What's important to remember, is that __init__ is an instance method. By the time __init__ is called, the new object has already been created, and our __init__ function defined in the class is now treated like a method bound to the instance.
'''
class Person:
    def __init__(self):
        print(f'Initializing a new Person object: {self}')
        
p = Person()
#Initializing a new Person object: <__main__.Person object at 0x7f80a022b0f0>

hex(id(p))#'0x7f80a022b0f0'
#Because __init__ is an instance method, we have access to the object (instance) state within the method, so we can use it to manipulate the object state:

class Person:
    def __init__(self, name):
        self.name = name
p = Person('Eric')
p.__dict__ #{'name': 'Eric'}
#What actually happens is that after the new instance has been created, Python sees and automatically calls <instance>.__init__(self, *args, **kwargs)

#So this is no different that if we had done it this way:

class Person:
    def initialize(self, name):
        self.name = name
p = Person()
p.__dict__
#{}
p.initialize('Eric')
p.__dict__
#{'name': 'Eric'}
#But by using the __init__ method both these things are done automatically for us.

#Just remember that by the time __init__ is called, the instance has already been created, and __init__ is an instance method.
