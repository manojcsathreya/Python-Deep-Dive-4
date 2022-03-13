'''
What is an object?

a container

contains data           ->state     ->attributes
contains functionality  ->behavior  ->methods


my_car
brand = Ferrari  
model = 599XX     --- state
year = 2010

accelerate
brake             --- behavior
steer



dot notation
Retriving
my_car.brand ->Ferrari
my_car.purchase_price = 1_600_000

Setting
my_car.accelerate(10)
my_car.steer(-15)

------------------------------------------------------------------------------------
Creating objects
How do we create the "container"?
How do we define and set state?
How do we define and implement behavior?

Many languages use a class-based approach -> C++, Java, Python, etc

A class is like a template used to create objects
-> also called a type
-> objects created from that class are called instances of that class or type

------------------------------------------------------------------------------------
Classes
Classes are themselves objects
They have attributes (state)
àe.g. class name (or type name)

They have behavior
àe.g. how to create an instance of the class

if a class is an object, and objects are created from classes, how are classes created?

Python àclasses are created from the typemetaclass


------------------------------------------------------------------------------------

Instances
Classes have behavior ->they are callable       MyClass()
                      ->this returns an instance of the class
                      ->often called objects, differentiating from class
                      (even though a class is technically an object as well)

Instances are created from classes
    their type is the class they were created from

if MyClassis a class in Python and my_obj is an instance of that class my_obj = MyClass()

type(my_obj) -> MyClass  this is an object (classes are objects)

isinstance(my_obj, MyClass) -> True


------------------------------------------------------------------------------------

Creating Classes
use the classkeyword
class MyClass:
    pass

->Python creates an object
->called MyClass
->of type type
->automatically provides us certain attributes (state) and methods (behavior)

MyClass.__name__ -> 'MyClass'  string  (state)

MyClass() -> returns an instance of MyClass (behavior)

type(MyClass) -> type
isinstance(MyClass, type) -> True 
'''

### Objects and Classes

#A class is a type of object. In Python we create classes using the `class` keyword.

class Person:
    pass

#Now this class doesn't do much, but it is an object of type `type` (which is itself an object).

type(Person) #type

type(type) #type

#Classes have "built-in" attributes, even though we did not specifically add any to the class ourselves.

#For example, they have a name:

Person.__name__ #'Person'

#They are also callables, and calling a class results in the creation and return of a new **instance** of that class:

p = Person()

#Now the type of the object is the class used to build that object:

type(p) #__main__.Person

#These instances also have "built_in" properties, which we will cover throughout this course.

#For example, they have a `__class__` property that tells us which class was used to create the instance:

p.__class__ #__main__.Person

#As you can see that returns the class object used to instantiate `p`.

#In fact:

type(p) is p.__class__ #True

#We can also use `isinstance` to test if an object is an instance of a particular class - now this gets a bit more complicated when we use inheritance, but right now we're not, so it's quite straightforward:

isinstance(p, Person) #True

isinstance(p, str) #False

#We can even use `isinstance` with our class, since we know it's type is `type`:

isinstance(Person, type) #Type

#`type` is like the most generic kind of **class** object - we'll come back to this when discussing meta programming.

#We really need inheritance to understand how this works, but every class **is** a `type` object (it inherits all the properties of `type`).

#For now let's just see what functionality `type` has:

help(type)

'''
Help on class type in module builtins:

class type(object)
 |  type(object_or_name, bases, dict)
 |  type(object) -> the object's type
 |  type(name, bases, dict) -> a new type
 |  
 |  Methods defined here:
 |  
 |  __call__(self, /, *args, **kwargs)
 |      Call self as a function.
 |  
 |  __delattr__(self, name, /)
 |      Implement delattr(self, name).
 |  
 |  __dir__(self, /)
 |      Specialized __dir__ implementation for types.
 |  
 |  __getattribute__(self, name, /)
 |      Return getattr(self, name).
 |  
 |  __init__(self, /, *args, **kwargs)
 |      Initialize self.  See help(type(self)) for accurate signature.
 |  
 |  __instancecheck__(self, instance, /)
 |      Check if an object is an instance.
 |  
 |  __repr__(self, /)
 |      Return repr(self).
 |  
 |  __setattr__(self, name, value, /)
 |      Implement setattr(self, name, value).
 |  
 |  __sizeof__(self, /)
 |      Return memory consumption of the type object.
 |  
 |  __subclasscheck__(self, subclass, /)
 |      Check if a class is a subclass.
 |  
 |  __subclasses__(self, /)
 |      Return a list of immediate subclasses.
 |  
 |  mro(self, /)
 |      Return a type's method resolution order.
 |  
 |  ----------------------------------------------------------------------
 |  Class methods defined here:
 |  
 |  __prepare__(...)
 |      __prepare__() -> dict
 |      used to create the namespace for the class statement
 |  
 |  ----------------------------------------------------------------------
 |  Static methods defined here:
 |  
 |  __new__(*args, **kwargs)
 |      Create and return a new object.  See help(type) for accurate signature.
 |  
 |  ----------------------------------------------------------------------
 |  Data descriptors defined here:
 |  
 |  __abstractmethods__
 |  
 |  __dict__
 |  
 |  __text_signature__
 |  
 |  ----------------------------------------------------------------------
 |  Data and other attributes defined here:
 |  
 |  __base__ = <class 'object'>
 |      The base class of the class hierarchy.
 |      
 |      When called, it accepts no arguments and returns a new featureless
 |      instance that has no instance attributes and cannot be given any.
 |  
 |  __bases__ = (<class 'object'>,)
 |  
 |  __basicsize__ = 880
 |  
 |  __dictoffset__ = 264
 |  
 |  __flags__ = 2148291584
 |  
 |  __itemsize__ = 40
 |  
 |  __mro__ = (<class 'type'>, <class 'object'>)
 |  
 |  __weakrefoffset__ = 368
'''

#As you can see it has a `__call__` method (that's how our class becomes callable), and a bunch of other attributes and methods that we'll see throughout this course.

#Our class objects also have these properties, because they inherit from the `type` object.

#And in fact, `type` is an instance of itself - that's kind of weird, and not the case for our own classes:

isinstance(type, type)  #true

isinstance(Person, Person) #False
