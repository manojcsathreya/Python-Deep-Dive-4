'''
Classes are Callable

When we create a class using the classkeyword
Python automatically adds behaviors to the class in particular:
->it adds something to make the class callable
->the return value of that callable is an object
->the type of that object is the class object

we say the object is an instance of 
the class

my_obj = MyClass()

type(my_obj) -> MyClass
isinstance(my_obj, MyClass) ->True

also called class instantiation or instantiating the class
-----------------------------------------------------------------------------
Instantiating Classes
When we call a class, a class instance object is created

This class instance object has its own namespace
->distinct from the namespace of the class that was used to create the object

This object has some attributes Python automatically implements for us:

->__class__tells us which class was used to instantiate the object

->__dict__is the object's local namespace

->prefer using type(obj)instead of obj.__class__
'''

### Classes are Callable

#As we saw earlier, one of the things Python does for us when we create a class is to make it callable.

#Calling a class creates a new instance of the class - an object of that particular type.

class Program:
    language = 'Python'
    
    def say_hello():
        print(f'Hello from {Program.language}!')

p = Program()

type(p) #__main__.Program

isinstance(p, Program) #True

#These instances have their own namespace, and their own `__dict__` that is distinct from the class `__dict__`:

p.__dict__ #{}

Program.__dict__

'''
mappingproxy({'__module__': '__main__',
              'language': 'Python',
              'say_hello': <function __main__.Program.say_hello()>,
              '__dict__': <attribute '__dict__' of 'Program' objects>,
              '__weakref__': <attribute '__weakref__' of 'Program' objects>,
              '__doc__': None})
'''

#Instances also have attributes that may not be visible in their `__dict__` (they are being stored elsewhere, as we'll examine later):

p.__class__ #__main__.Program

#Although we can use `__class__` we can also use `type`:

type(p) is p.__class__ #__main__.Program

#Generally we use `type` instead of using `__class__` just like we usually use `len()` instead of accessing `__len__`.

#Why? Well, one reason is that people can mess around with the `__class__` attribute:

class MyClass:
    pass

m = MyClass()

type(m), m.__class__ #(__main__.MyClass, __main__.MyClass)

But look at what happens here:

class MyClass:
    __class__ = str

m = MyClass()

type(m), m.__class__ #(__main__.MyClass, str)

So as you can see, `type` wasn't fooled!


