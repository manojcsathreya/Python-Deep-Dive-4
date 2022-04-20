'''
FUNCTION ATTRIBUTE
Function Attributes, Classes and Instances
What happens when attributes are functions is different!

class MyClass:
    def say_hello():
        print('Hello World!')
my_obj = MyClass()
MyClass.say_hello <function __main__.MyClass.say_hello()>
my_obj.say_hello<bound method MyClass.say_hello of <__main__.MyClass object at 0x10383f860>>


Same with getattr:
getattr(my_obj, 'say_hello') <bound method MyClass.say_hello of <__main__.MyClass object at 0x10383f860>>

MyClass.say_hello() -> 'Hello World!'

my_obj.say_hello() -> TypeError
say_hello() ERROR!!
takes 0 positional arguments but 1 was given
bound? method? 
---------------------------------------------------------------------------------------------------
Methods
method is an actual object type in Python
like a function, it is callable
but unlike a function if is bound to some object
and that object is passed to the method as its first parameter

my_obj.say_hello() -> say_hellois a method object
                    ->it is bound to my_obj
                    ->when my_obj.say_hellois called, the bound object my_obj is 
                    injected as the first parameter to the method say_hello
so it's essentially calling this: MyClass.say_hello(my_obj)
->but there's more to it than just calling the function this way – method object

One advantage of this is that say_hello now has a handle to the object's 
namespace! ->the object it is bound to
---------------------------------------------------------------------------------------------------
Methods

Methods are objects that combine:
->instance (of some class)
->function

->like any object it has attributes
__self__  ->the instance the method is bound to
__func__  ->the original function (defined in the class)


calling obj.method(args) ->method.__func__(method.__self__, args)

class Person:
    def hello(self):  #p.hello.__func__ 
        pass

p = Person()
|
p.hello.__self__
---------------------------------------------------------------------------------------------------
Instance Methods
This means we have to account for that "extra" argument when we define functions in our 
classes – otherwise we cannot use them as methods bound to our instances
These functions are usually called instance methods

class MyClass:
    def say_hello(obj):        -> first param will receive instance object<we often call this an instance method>
        print('Hello World!')     but not actually a methodobject yet!  at this point it's just a regular function

my_obj = MyClass()
my_obj.say_hello  ->now it's a method and is bound to my_obj, an instance of MyClass instance method



my_obj.say_hello() -> 'Hello World!'
MyClass.say_hello(my_obj) 
---------------------------------------------------------------------------------------------------
Instance Methods
Of course functions in our classes can have their own parameters
When we call the corresponding instance method with arguments ->passed to the method as well
And the method still receives the instance object reference as the first argument
                    ->we have access to the instance (and class) attributes!
class MyClass:
    language = 'Python'
    def say_hello(obj, name):
        return f'Hello {name}! I am {obj.language}. '

python = MyClass()
python.say_hello('John')  -> MyClass.say_hello(python, 'John')
-> 'Hello John! I am Python'

java = MyClass()
java.language = 'Java'
java.say_hello('John') -> MyClass.say_hello(java, 'John')

-> 'Hello John! I am Java'
'''

#Function Attributes
#So far, we have been dealing with non-callable attributes. When attributes are actually functions, things behave differently.

class Person:
    def say_hello():
        print('Hello!')
Person.say_hello #<function __main__.Person.say_hello()>
type(Person.say_hello) #function
#As we can see it is just a plain function, and be called as usual:

Person.say_hello() #Hello!
#Now let's create an instance of that class:

p = Person()
hex(id(p)) #'0x7f88a06937b8'
#We know we can access class attributes via the instance, so we should also be able to access the function attribute in the same way:

p.say_hello #<bound method Person.say_hello of <__main__.Person object at 0x7f88a06937b8>>
type(p.say_hello) #method
#Hmm, the type has changed from function to method, and the function representation states that it is a bound method of the specific object p we created (notice the memory address).

#And if we try to call the function from the instance, here's what happens:

try:
    p.say_hello()
except Exception as ex:
    print(type(ex).__name__, ex)
#TypeError say_hello() takes 0 positional arguments but 1 was given
#method is an actual type in Python, and, like functions, they are callables, but they have one distinguishing feature. They need to be bound to an object, and that object reference is passed to the underlying function.
'''
Often when we define functions in a class and call them from the instance we need to know which specific instance was used to call the function. This allows us to interact with the instance variables.

To do this, Python will automatically transform an ordinary function defined in a class into a method when it is called from an instance of the class.

Further, it will "bind" the method to the instance - meaning that the instance will be passed as the first argument to the function being called.

It does this using descriptors which we'll come back to in detail later.

For now let's just explore this a bit more:
'''
class Person:
    def say_hello(*args):
        print('say_hello args:', args)
Person.say_hello()
say_hello args: ()
#As we can see, calling say_hello from the class, just calls the function (it is just a function).

#But when we call it from an instance:

p = Person()
hex(id(p)) #'0x7f88d0428748'
p.say_hello()
#say_hello args: (<__main__.Person object at 0x7f88d0428748>,)
#You can see that the object p was passed as an argument to the class function say_hello.

#The obvious advantage is that we can now interact with instance attributes easily:

class Person:
    def set_name(instance_obj, new_name):
        instance_obj.name = new_name  # or setattr(instance_obj, 'name', new_name)
        
p = Person()
p.set_name('Alex')
​
p.__dict__ #{'name': 'Alex'}
#This has essentially the same effect as doing this:

Person.set_name(p, 'John')
p.__dict__
#{'name': 'John'}
#By convention, the first argument is usually named self, but asd you just saw we can name it whatever we want - it just will be in the instance when the method variant of the function is called - and it is called an instance method.

#But methods are objects created by Python when calling class functions from an instance.

#They have their own unique attributes too:

class Person:
    def say_hello(self):
        print(f'{self} says hello')
p = Person()
p.say_hello
#<bound method Person.say_hello of <__main__.Person object at 0x7f88d0428c18>>
m_hello = p.say_hello
type(m_hello)
#method
#For example it has a __func__ attribute:

m_hello.__func__
#<function __main__.Person.say_hello(self)>
#which happens to be the class function used to create the method (the underlying function).

#But remember that a method is bound to an instance. In this case we got the method from the p object:

hex(id(p))
#'0x7f88d0428c18'
m_hello.__self__
#<__main__.Person at 0x7f88d0428c18>
#As you can see, the method also has a reference to the object it is bound to.

#So think of methods as functions that have been bound to a specific object, and that object is passed in as the first argument of the function call. The remaining arguments are then passed after that.

#Instance methods are created automatically for us, when we define functions inside our class definitions.

#This even holds true if we monkey-patch our classes at run-time:

class Person:
    def say_hello(self):
        print(f'instance method called from {self}')
p = Person()
hex(id(p)) #'0x7f88d0435f28'
p.say_hello() #instance method called from <__main__.Person object at 0x7f88d0435f28>
Person.do_work = lambda self: f"do_work called from {self}"
Person.__dict__
'''
mappingproxy({'__module__': '__main__',
              'say_hello': <function __main__.Person.say_hello(self)>,
              '__dict__': <attribute '__dict__' of 'Person' objects>,
              '__weakref__': <attribute '__weakref__' of 'Person' objects>,
              '__doc__': None,
              'do_work': <function __main__.<lambda>(self)>})
'''
#OK, so both functions are in the class __dict__.

#let's create an instance and see what happens:

p.say_hello #<bound method Person.say_hello of <__main__.Person object at 0x7f88d0435f28>>
p.do_work #<bound method <lambda> of <__main__.Person object at 0x7f88d0435f28>>
#But be careful, if we add a function to the instance directly, this does not work the same - we have create a function in the instance, so it is not considered a method (since it was not defined in the class):

p.other_func = lambda *args: print(f'other_func called with {args}')
p.other_func #<function __main__.<lambda>(*args)>
'other_func' in Person.__dict__
#False
p.other_func() ##other_func called with ()
#As you can see, other_func is, and behaves, like an ordinary function.

#Long story short, functions defined in a class are transformed into methods when called from instances of the class. So of course, we have to account for that extra argument that is passed to the method.
