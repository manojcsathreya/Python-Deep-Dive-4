'''
CLASS ATTRIBUTES

Defining Attributes in Classes
class MyClass:
    language = 'Python'
    version = '3.6'

MyClassis a class -> it is an object (of type type)

in addition to whatever attributes Python automatically creates for us

e.g. __name__with a state of 'MyClass'

->it also has language and version attributes

with a state of 'Python'and '3.6'respectively
-------------------------------------------------------------------------------------
Retrieving Attribute Values from Objects

class MyClass:
    language = 'Python'
    version = '3.6'

->getattr function getattr(object_symbol, attribute_name, optional_default)

getattr(MyClass, 'language') -> 'Python'
getattr(MyClass, 'x') -> AttributeErrorexception
#if the attribute does not exist to return some value instead of exception
getattr(MyClass, 'x', 'N/A') -> 'N/A'

->dot notation (shorthand)
MyClass.language -> 'Python'
MyClass.x -> AttributeErrorexception
-------------------------------------------------------------------------------------
Setting Attribute Values in Objects
class MyClass:
    language = 'Python'
    version = '3.6'

->setattrfunction setattr(object_symbol, attribute_name, attribute_value)

setattr(MyClass, 'version', '3.7')
MyClass.version = '3.7'

this has modified the state of MyClass ->MyClasswas mutated

getattr(MyClass, 'version')
MyClass.version -> '3.7'
-------------------------------------------------------------------------------------
Setting Attribute Values in Objects
class MyClass:
    language = 'Python'
    version = '3.6'

What happens if we call setattr for an attribute we did not define in our class?

Python is a dynamic language ->can modify our classes at runtime (usually)
setattr(MyClass, 'x', 100)
or MyClass.x = 100
-> MyClassnow has a new attribute named x with a state of 100

getattr(MyClass, 'x')
MyClass.x -> 100
-------------------------------------------------------------------------------------
Where is the state stored?
->in a dictionary
class MyClass:
    language = 'Python'
    version = '3.6'

MyClass.__dict__

mappingproxy({'__module__': '__main__',
'language': 'Python',
'version': '3.6',
'__dict__': <attribute '__dict__' of 'MyClass' objects>,
'__weakref__': <attribute '__weakref__' of 'MyClass' objects>,
'__doc__': None})

->not directly mutable dictionary (but setattrcan)
->ensures keys are strings (helps speed things up for Python)

-------------------------------------------------------------------------------------
Mutating Attributes
We saw we can modify the sate or create a brand new attribute using setattror the dot notation
class MyClass:
    language = 'Python'
    version = '3.6'

MyClass.__dict__ -> mappingproxy({'language': 'Python',
'version': '3.6', …})

We can then mutate MyClass:
setattr(MyClass, 'x', 100) or MyClass.x = 100

And this is reflected in the namespace:
MyClass.__dict__ -> mappingproxy({'language': 'Python',
'version': '3.6', 
'x': 100, …})
-------------------------------------------------------------------------------------
Deleting Attributes

So if we can mutate the namespace at runtime by using setattr(or equivalent dot notation)

Can we remove an attribute at runtime?

Yes! (usually) -> delattr(obj_symbol, attribute_name)
or delkeyword

class MyClass:
    language = 'Python'
    version = '3.6'

MyClass.__dict__ -> mappingproxy({'language': 'Python',
'version': '3.6', …})

delattr(MyClass, 'version') or del MyClass.version

MyClass.__dict__ -> mappingproxy({'language': 'Python',
…})
->versionhas been removed from namespace
-------------------------------------------------------------------------------------
Accessing the Namespace Directly

As we saw the class namespace uses a dictionary, which we can request using the __dict__ 
attribute of the class
The __dict__attribute of a class returns a mappingproxyobject

Although this is not a dict, it is still a hash map (dictionary), so we can at least read access the 
class namespace directly – not common practice!!

class MyClass:
    language = 'Python'
    version = '3.6'

MyClass.language -> 'Python'
getattr(MyClass, 'language')
MyClass.__dict__['language']
Be careful with this – sometimes classes have attributes that don't show up in that dictionary!

(we'll come back to that later)
'''
#Class Attributes
#As we saw, when we create a class Python automatically builds-in properties and behaviors into our class object, like making it callable, and properties like __name__.

class Person:
    pass

Person.__name__ #'Person'

#__name__ is a class attribute. We can add our own class attributes easily this way:
    
class Program:
    language = 'Python'
    version = '3.6'
    
Program.__name__ #'Program'

Program.version #'3.6'

Program.language # 'Python'

#Here we used "dotted notation" to access the class attributes. In fact we can also use dotted notation to set the class attribute:

Program.version = '3.7'
Program.version #'3.7'
#But we can also use the functions getattr and setattr to read and write these attributes:

getattr(Program, 'version') #'3.7'
setattr(Program, 'version', '3.6')
Program.version, getattr(Program, 'version') #('3.6', '3.6')
getattr(Program,x,'N/a') #N/a
#Python is a dynamic language, and we can create attributes at run-time, outside of the class definition itself:

Program.x = 100
#Using dotted notation we added an attribute x to the Person class:

Program.x, getattr(Program, 'x') #(100, 100)
#We could also just have used a setattr function call:

setattr(Program, 'y', 200)
Program.y, getattr(Program, 'y') #(200, 200)
#So where is the state stored? Usually in a dictionary that is attached to the class object (often referred to as the namespace of the class):

Program.__dict__
'''
mappingproxy({'__module__': '__main__',
              'language': 'Python',
              'version': '3.6',
              '__dict__': <attribute '__dict__' of 'Program' objects>,
              '__weakref__': <attribute '__weakref__' of 'Program' objects>,
              '__doc__': None,
              'x': 100,
              'y': 200})
As you can see that dictionary contains our attributes: language, version, x, y with their corresponding current values.

Notice also that Program.__dict__ does not return a dictionary, but a mappingproxy object - this is essentially a read-only dictionary that we cannot modify directly (but we can modify it by using setattr, or dotted notation).

For example, if we change the value of an attribute:
'''

setattr(Program, 'x', -10) #We'll see this reflected in the underlying dictionary:

Program.__dict__
'''
mappingproxy({'__module__': '__main__',
              'language': 'Python',
              'version': '3.6',
              '__dict__': <attribute '__dict__' of 'Program' objects>,
              '__weakref__': <attribute '__weakref__' of 'Program' objects>,
              '__doc__': None,
              'x': -10,
              'y': 200})
'''
#Deleting Attributes
#So, we can create and mutate class attributes at run-time. Can we delete attributes too?

#The answer of course is yes. We can either use the del keyword, or the delattr function:

del Program.x
Program.__dict__
'''
mappingproxy({'__module__': '__main__',
              'language': 'Python',
              'version': '3.6',
              '__dict__': <attribute '__dict__' of 'Program' objects>,
              '__weakref__': <attribute '__weakref__' of 'Program' objects>,
              '__doc__': None,
              'y': 200})
'''
delattr(Program, 'y')

#Direct Namespace Access
Program.__dict__
'''
mappingproxy({'__module__': '__main__',
              'language': 'Python',
              'version': '3.6',
              '__dict__': <attribute '__dict__' of 'Program' objects>,
              '__weakref__': <attribute '__weakref__' of 'Program' objects>,
              '__doc__': None})
Although __dict__ returns a mappingproxy object, it still is a hash map and essentially behaves like a read-only dictionary:
'''

Program.__dict__['language']
'Python'
list(Program.__dict__.items())
'''
[('__module__', '__main__'),
 ('language', 'Python'),
 ('version', '3.6'),
 ('__dict__', <attribute '__dict__' of 'Program' objects>),
 ('__weakref__', <attribute '__weakref__' of 'Program' objects>),
 ('__doc__', None)]
'''
#One word of caution: not every attribute that a class has lives in that dictionary (we'll come back to this later).

#For example, you'll notice that the __name__ attribute is not there:

Program.__name__
'Program'
__name__ in Program.__dict__
False

