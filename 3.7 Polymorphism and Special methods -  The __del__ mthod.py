'''
A Class Finalizer

The garbage collector destroys objects that are no longer referenced anywhere

->hook into that lifecycle event

->use the __del__method

The __del__method will get called right before the object is destroyed by the GC

->so the GC determines when this method is called

->__del__is sometimes called the class finalizer

(sometimes called the destructor, but not entirely accurate, since 
GC destroys the object) ©2019 MathByte Academy

================================================================================================
When does __del__get called?

->that's the basic issue with the __del__method
->we do not control when it will get called!

called only when all references to the object are gone

->have to be extremely careful with our code

->easy to inadvertently create additional references, or circular references
================================================================================================

Additional Issues

If __del__contains references to global variables, or other objects

->those objects may be gone by the time __del__is called

If an exception occurs in the __del__method
->exception is not raised – it is silenced
->exception description is sent to stderr
->main program will not be aware something went wrong during finalization

->prefer using context managers to clean up resources

->personally I do not use __del__

'''

# =============================================================================
# The __del__ Method
# The __del__ method as we discussed in the lecture is called right before the object is about to be garbage collected. This is sometimes called the finalizer. It is sometimes referred to as the destructor, but that's not really accurate since that method does not destroy the object - that's the GC's responsibility - __del__ just gets called prior to the GC destroying the object.
# 
# Although this method can be useful in some circumstances we need to be aware of some pitfalls:
# 
# Using the del keyword does not call __del__ directly - it just removes the symbol for wehatever namespace it is being deleted from and reduces the reference count by 1.
# The __del__ method is not called until the object is about to be destroyed - so using del obj decreases the ref count by 1, but if something else is referencing that object then __del__ is not called.
# Unhandled exceptions that occur in the __del__ method are essentially ignored, and the exceptions are written to sys.stderr.
# It's actually pretty easy to have unwitting references to an object.
# 
# Let's first write a small helper function to calculate the reference count for an object using it's memory address (which only works correctly if the object actually exists):
# =============================================================================

import ctypes
​
def ref_count(address):
    return ctypes.c_long.from_address(address).value
#Now let's write a class that implements the __del__ method:

class Person:
    def __init__(self, name):
        self.name = name
        
    def __repr__(self):
        return f'Person({self.name})'
    
    def __del__(self):
        print(f'__del__ called for {self}...')
#Let's first see how the __del__ gets called when we create then remove a reference to an instance in our global scope:

p = Person('Alex')
#We can now remove that reference from the symbol p to the instance either by using del p or even just setting p to None:

p = None
#__del__ called for Person(Alex)...
#As you can see the __del__ was called.

#It works the same way with the del statement:

p = Person('Alex')
del p
#__del__ called for Person(Alex)...
#Now let's see how we might create an unwitting extra reference to the object.

#Let's implement a method that is going to create an exception:

class Person:
    def __init__(self, name):
        self.name = name
    
    def gen_ex(self):
        raise ValueError('Something went bump...')
        
    def __repr__(self):
        return f'Person({self.name})'
    
    def __del__(self):
        print(f'__del__ called for {self}...')
p = Person('Alex')
#At this point we have one reference to the object, the reference held by p:

p_id = id(p)
ref_count(p_id)
#1
#Now let's make that exception happen and store the exception in a variable:

try:
    p.gen_ex()
except ValueError as ex:
    error = ex
    print(ex)
#Something went bump...
ref_count(p_id)
#2
#As you can see our reference count is now 2. Why?

#Let's look at the error variable:

dir(error)
'''
['__cause__',
 '__class__',
 '__context__',
 '__delattr__',
 '__dict__',
 '__dir__',
 '__doc__',
 '__eq__',
 '__format__',
 '__ge__',
 '__getattribute__',
 '__gt__',
 '__hash__',
 '__init__',
 '__init_subclass__',
 '__le__',
 '__lt__',
 '__ne__',
 '__new__',
 '__reduce__',
 '__reduce_ex__',
 '__repr__',
 '__setattr__',
 '__setstate__',
 '__sizeof__',
 '__str__',
 '__subclasshook__',
 '__suppress_context__',
 '__traceback__',
 'args',
 'with_traceback']
dir(error.__traceback__)
['tb_frame', 'tb_lasti', 'tb_lineno', 'tb_next']
dir(error.__traceback__.tb_frame)
['__class__',
 '__delattr__',
 '__dir__',
 '__doc__',
 '__eq__',
 '__format__',
 '__ge__',
 '__getattribute__',
 '__gt__',
 '__hash__',
 '__init__',
 '__init_subclass__',
 '__le__',
 '__lt__',
 '__ne__',
 '__new__',
 '__reduce__',
 '__reduce_ex__',
 '__repr__',
 '__setattr__',
 '__sizeof__',
 '__str__',
 '__subclasshook__',
 'clear',
 'f_back',
 'f_builtins',
 'f_code',
 'f_globals',
 'f_lasti',
 'f_lineno',
 'f_locals',
 'f_trace']
'''
for key, value in error.__traceback__.tb_frame.f_locals.copy().items():
    if isinstance(value, Person):
        print(key, value, id(value), id(key))
p Person(Alex) 140665691193640 140665683500032
# =============================================================================
# As you can see the traceback contains a refererence to our object in it's dictionary - so we have a second reference to our object.
# 
# Let's check our reference count now, to make sure we did not inadvertently create even more references:
# =============================================================================

ref_count(p_id)
#2
#Now, even if we remove our reference to the object, we will still have something handing on to it, and the __del__ method will not get called:

del p
#See! __del__ was not called!

#But now let's get rid of that exception we stored:

del error
#__del__ called for Person(Alex)...
# =============================================================================
# And now, as you can see, we finally had the __del__ method called. (Note that depending on what you were doing in your notebook, you may not even see this call at all - which just means that something else is holding on to our object somewhere!)
# 
# For this reason it is rare for devs to use the __del__ method for critical things like closing a file, or closing committing a transaction in a database, etc - instead use a context manager, and avoid using the __del__ method.
# 
# Because you do not know when the __del__ method is going to get called (unless you know exactly how your code might be creating references to the object), you could also get into a situation where other objects (like global objects) referenced in the __del__ method will even still be around by the time __del__ is called (it would get called when the module is destroyed, such as at program shutdown).
# 
# The last point to make about __del__ is that any unhandled exceptions in the __del__ method are essentially ignored by Python (although their output is sent to sys.stderr).
# 
# Let's see this:
# =============================================================================

class Person:
    def __del__(self):
        raise ValueError('Something went bump...')
p = Person()
del p
# =============================================================================
# Exception ignored in: <bound method Person.__del__ of <__main__.Person object at 0x7fef381d8e48>>
# Traceback (most recent call last):
#   File "<ipython-input-19-6ed6e62e38b8>", line 3, in __del__
# ValueError: Something went bump...
# What we are seeing here is actually the stderr output, which Jupyter redirects into our notebook.
# =============================================================================

import sys
sys.stderr, sys.stdout
# =============================================================================
# (<ipykernel.iostream.OutStream at 0x7fef18b90978>,
#  <ipykernel.iostream.OutStream at 0x7fef18b903c8>)
# What I'm going to do here is redirect stderr to a file instead, using a context manager:
# =============================================================================

class ErrToFile:
    def __init__(self, fname):
        self._fname = fname
        self._current_stderr = sys.stderr
        
    def __enter__(self):
        self._file = open(self._fname, 'w')
        sys.stderr = self._file
        
    def __exit__(self, exc_type, exc_value, exc_tb):
        sys.stderr = self._current_stderr
        if self._file:
            self._file.close()
        return False
p = Person()
with ErrToFile('err.txt'):
    del p
#As you can see, no exception was generated and our code continues to run happily along.

#But let's examine the contents of that file:

with open('err.txt') as f:
    print(f.readlines())
#['Exception ignored in: <bound method Person.__del__ of <__main__.Person object at 0x7fef381cc9e8>>\n', 'Traceback (most recent call last):\n', '  File "<ipython-input-19-6ed6e62e38b8>", line 3, in __del__\n', 'ValueError: Something went bump...\n']
#So, as you can see the exception was silenced and the exception data was just sent to stderr.

#What this means is that you cannot trap exceptions that occur in the __del__ method (from outside the __del__ method to be exact):

p = Person()
​
try:
    del p
    print('p was deleted (succesfully)')
except ValueError as ex:
    print('Exception caught!')
else:
    print('No exception seen!')
# =============================================================================
# p was deleted (succesfully)
# No exception seen!
# Exception ignored in: <bound method Person.__del__ of <__main__.Person object at 0x7fef381ee898>>
# Traceback (most recent call last):
#   File "<ipython-input-19-6ed6e62e38b8>", line 3, in __del__
# ValueError: Something went bump...
# Now all this does not mean you should just altogether avoid using the __del__ method - you just need to be aware of its limitations, and be extra careful in your code with circular references or unintentional extra references to your objects. Things get even dicier when using multi-threading, but that's beyond the scope of this course!
# 
# Personally I never use __del__. Instead I use context managers to manage releasing resources such as files, sockets, database connections, etc.
# =============================================================================
