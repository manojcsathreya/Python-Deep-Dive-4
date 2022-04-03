'''
CALLABLE CLASS ATTRIBUTES

Setting an Attribute Value to a Callable
Attribute values can be any object ->other classes ->any callable ->anything…

So we can do this: 
class MyClass:
    language = 'Python'
    def say_hello():
        print('Hello World!')

say_hello is also an attribute of the class ->its value happens to be a callable

mappingproxy({'language': 'Python',
              'say_hello': <function __main__.MyClass.say_hello()>, ...})
----------------------------------------------------------------------------------
How do we call it?
We could get it straight from the namespace dictionary:
my_func = MyClass.__dict__['say_hello']
my_func() -> 'Hello World!'

MyClass.__dict__['say_hello']() -> 'Hello World!'

or we could use getattr:

getattr(MyClass, 'say_hello')() -> 'Hello World!'

or we can use dot notation:
MyClass.say_hello() -> 'Hello World!'
'''

#Callable Class Attributes
#Class attributes can be any object type, including callables such as functions:

class Program:
    language = 'Python'
    
    def say_hello():
        print(f'Hello from {Program.language}!')

Program.__dict__
'''

mappingproxy({'__module__': '__main__',
              'language': 'Python',
              'say_hello': <function __main__.Program.say_hello()>,
              '__dict__': <attribute '__dict__' of 'Program' objects>,
              '__weakref__': <attribute '__weakref__' of 'Program' objects>,
              '__doc__': None})
As we can see, the say_hello symbol is in the class dictionary.

We can also retrieve it using either getattr or dotted notation:
    
    '''

Program.say_hello, getattr(Program, 'say_hello')
'''
(<function __main__.Program.say_hello()>,
 <function __main__.Program.say_hello()>)
And of course we can call it, since it is a callable:
    '''

Program.say_hello() #Hello from Python!
getattr(Program, 'say_hello')() #Hello from Python!
#We can even access it via the namespace dictionary as well:

Program.__dict__['say_hello']() #Hello from Python!
