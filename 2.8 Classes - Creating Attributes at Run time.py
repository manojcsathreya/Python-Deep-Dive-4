'''
CREATING ATTRIBUTES AT RUN-TIME

Instances and Setting Function Attributes at Runtime
We saw that we can add to an instance namespace directly at runtime by using setattror the dot 
notation
class MyClass:
    language = 'Python'
obj = MyClass() 
obj.__dict__ -> {}
obj.version = '3.7' 
obj.__dict__ -> {'version': '3.7'}
What happens if we create a new attribute whose value is a function?
obj.say_hello = lambda: 'Hello World!'
then
obj.say_hello ->function not a bound method!
obj.say_hello() -> 'Hello World!'
but say_hello does not have access to the instance namespace
------------------------------------------------------------------------------------------------
Can we create and bind a method to an instance at runtime?
Yes
->just need to define a method that binds the function to the instance

class MyClass:
    language = 'Python'
obj = MyClass()

from types import MethodType MethodType(function<function we want to bind>, object<the object to bind to>)

obj.say_hello = MethodType(lambda self: f'Hello {self.language}!', obj)
say_hello is now a method bound to obj ->'Hello Python!

->only obj has been affected
->no other instances have that method
'''

#Creating Attributes at Run-Time
#We already saw that we can add attributes to instances at run-time, and that it affects just that single instance:

class Person:
    pass
p1 = Person()
p2 = Person()
​
p1.name = 'Alex'
p1.__dict__
#{'name': 'Alex'}
p2.__dict__
#{}
#So what happens if we add a function as an attribute to our instances directly (we can even do the same within an __init__ method, works the same way)?

#Remember that if we add a function to the class itself, calling the function from the instance will result in a method.

#Here, the result is different, since we are adding the function directly to the instance, not the class:

p1.say_hello = lambda: 'Hello!'
p1.__dict__
#{'name': 'Alex', 'say_hello': <function __main__.<lambda>()>}
p1.say_hello
#<function __main__.<lambda>()>
#As you can see, that attribute is a plain function - it is not being interpreted as a method.

p1.say_hello()
#'Hello!'
#Of course, the other instances do not know anything about that function:

p2.__dict__
#{}
#So, the question becomes, can we create a method on a specific instance?

#The answer (of course!) is yes, but we have to explicitly tell Python we are setting up a method bound to that specific instance.

#We do this by creating a method type object:

from types import MethodType
class Person:
    def __init__(self, name):
        self.name = name
p1 = Person('Eric')
p2 = Person('Alex')
#Now let's create a method object, and bind it to p1. First we create a function that will handle the bound object as it's first argument, and use the instance name property.

def say_hello(self):
    return f'{self.name} says hello!'
#Now we can use that function just by itself, passing in any object that has a name attribute:

say_hello(p1), say_hello(p2)
#('Eric says hello!', 'Alex says hello!')
#Now however, we are going to create a method bound to p1 specifically:

p1_say_hello = MethodType(say_hello, p1)
p1_say_hello
#<bound method say_hello of <__main__.Person object at 0x7f9750295630>>
#As you can see that method is bound to the instance p1. But how do we call it?

#If we try to use dotted notation or a getattr, that won't work because the p1 object does not know anything about that method:

try:
    p1.p1_say_hello()
except AttributeError as ex:
    print(ex)
#'Person' object has no attribute 'p1_say_hello'
#All we need to do is add that method to the instance dictionary - giving it whatever name we want:

p1.say_hello = p1_say_hello
p1.__dict__
#{'name': 'Eric',
# 'say_hello': <bound method say_hello of <__main__.Person object at 0x7f9750295630>>}
#OK, so now out instance knows about that method that we stored under the name say_hello:

p1.say_hello()
#'Eric says hello!'
#or, we can use the getattr function:

getattr(p1, 'say_hello')()
#'Eric says hello!'
#And of course, othe instances know nothing about this:

p2.__dict__
#{'name': 'Alex'}
#So, to create a bound method after the object has initially been created, we just create a bound method and add it to the instance itself.

#We can do it this way (what we just saw):

p1 = Person('Alex')
p1.__dict__
#{'name': 'Alex'}
p1.say_hello = MethodType(lambda self: f'{self.name} says hello', p1)
p1.say_hello()
#'Alex says hello'
#But we can also do this from any instance method too.

#Example
#Suppose we want some class to have some functionality that is called the same way but will differ from instance to instance. Although we could use inheritance, here I want some kind of 'plug-in' approach and we can do this without inheritance, mixins, or anything like that!

from types import MethodType
​
class Person:
    def __init__(self, name):
        self.name = name
        
    def register_do_work(self, func):
        setattr(self, '_do_work', MethodType(func, self))
        
    def do_work(self):
        do_work_method = getattr(self, '_do_work', None)
        # if attribute exists we'll get it back, otherwise it will be None
        if do_work_method:
            return do_work_method()
        else:
            raise AttributeError('You must first register a do_work method')
math_teacher = Person('Eric')
english_teacher = Person('John')
#Right now neither the math nor the english teacher can do any woirk because we haven't "registered" a worker yet:

try:
    math_teacher.do_work()
except AttributeError as ex:
    print(ex)
#You must first register a do_work method
#Ok, so let's do that:

def work_math(self):
     return f'{self.name} will teach differentials today.'
math_teacher.register_do_work(work_math)
math_teacher.__dict__
#{'name': 'Eric',
# '_do_work': <bound method work_math of <__main__.Person object at 0x7f97584cdac8>>}
math_teacher.do_work()
#'Eric will teach differentials today.'
#And we can create a different do_work method for the English teacher:

def work_english(self):
    return f'{self.name} will analyze Hamlet today.'
english_teacher.register_do_work(work_english)
english_teacher.do_work()
#'John will analyze Hamlet today.'
