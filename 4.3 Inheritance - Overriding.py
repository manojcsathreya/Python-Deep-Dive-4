'''
Overriding Functionality
When we inherit from another a class, we inherit its attributes, including all callables
->we can choose to redefine an existing callable in the sub class
->this is called overriding

class Person:
    def say_hello(self):
        return 'Hello!'
    def say_bye(self):
        return 'Bye!'

class Student(Person):
    def say_hello(self):
        return 'Yo!'

                p = Person() s = Student()

<obj>.say_hello()   Hello!       Yo!        uses override

<obj>.say_bye()     Bye!        Bye!        uses inherited

When we create any class, we can override any method defined in the parent class, including 
inherited ones
->including those defined in object
class Person:
    def __init__(self, name):   #overrides __init__in object
        self.name = name
    def __repr__(self):         #overrides __repr__in object
        return f'Person(name={self.name})'


class Student(Person):                           inherits __init__from Person
    def __repr__(self):                          #overrides __repr__in Person
        return f'Student(name={self.name})'
    
p = Person('john') str(p) -> Person(name=john)
s = Student('eric'') str(s) -> Student(name=eric)
=======================================================================================================
Tip
Objects have a property: __class__->returns the class the object was created from
Classes have a property: __name__ ->returns a string containing the name of the class
To get the name (string) of the class used to create an object ->object.__class__.__name__
class Person:
    def __init__(self, name):
        self.name = name
    def __repr__(self):
        return f'Person(name={self.name})'

class Student(Person):
    def __repr__(self):
        return f'Student(name={self.name})'


instead we can do this, and get the same effect:
    
class Person:
    def __init__(self, name):
        self.name = name
    def __repr__(self):
        return f'{self.__class__.__name__}(name={self.name})'

class Student(Person):
    pass
======================================================================================================
Overriding and the inheritance chain ->there are some subtle points here to note.
Suppose we have this type of hierarchy:
Person
- eat() -> "Person eats"
- sleep() -> "Person sleeps"
- work() -> "Person works"
- routine() -> eat() work() sleep()

p = Person()
p.routine() -> Person eats
               Person works
               Person sleeps

Now we create a Studentclass that overrides the work()method only:
Student:
- work() -> "Student studies" what happens when we call routine() on a Studentinstance?

s = Student()   s.routine()
->runs routineas defined in Personclass – but bound to s
->routine calls eat()  ->eat()in Personclass bound to s  -> Person eats
->… calls work() ->finds the override in Student!!! ->uses the override in Student  -> Student studies
->… calls sleep()  ->sleep()in Personclass bound to s  -> Person sleeps
'''

#As we saw in the lecture, classes that inherit from another class inherit the functionality from the parent class (and all parent classes up the chain).

#Let's look at what happens when we override the __str__ method in a custom class (which remember inherits it from the object class):

class Person:
    pass

p = Person()
str(p)
#'<__main__.Person object at 0x7fbcb04c3908>'
#What happened here is that str() tries to call a __str__ method. Since the Person class does not define it, Python continues looking up the inheritance chain until it finds it - in this case it finds it in the object class, so it uses it.

#Now let's override the __str__ method in the Person class:

class Person:
    def __str__(self):
        return 'Person class'
p = Person()
str(p)
#'Person class'
#What happens if we implement a __repr__ method only, and still call the str() method:

class Person:
    def __repr__(self):
        return 'Person()'
p = Person()
str(p)
#'Person()'
#As you can see it ended calling __repr__ in the Person class, even though we did not have a __str__ method defined - that's because objects delegates str to __repr__ which in turn will find it in our class.

#As we discussed in the lecture, in an inheritance chain we have to be very aware of how overrides are handled.

#Let's create a simple chain:

class Shape:
    def __init__(self, name):
        self.name = name
        
    def info(self):
         return f'Shape.info called for Shape({self.name})'
    
    def extended_info(self):
        return f'Shape.extended_info called for Shape({self.name})'
    
class Polygon(Shape):
    def __init__(self, name):
        self.name = name  # we'll come back to this later in the context of using the super()
        
    def info(self):
        return f'Polygon info called for Polygon({self.name})'
p = Polygon('square')
p.info()
#'Polygon info called for Polygon(square)'
#But if we call extended_info:

p.extended_info()
#'Shape.extended_info called for Shape(square)'
#That makes sense, it uses extended_info in the superclass - but now let's add a twist - let's have extended_info in the Shape class also call info:

class Shape:
    def __init__(self, name):
        self.name = name
        
    def info(self):
         return f'Shape.info called for Shape({self.name})'
    
    def extended_info(self):
        return f'Shape.extended_info called for Shape({self.name})', self.info()
    
class Polygon(Shape):
    def __init__(self, name):
        self.name = name  # we'll come back to this later in the context of using the super()
        
    def info(self):
        return f'Polygon.info called for Polygon({self.name})'
p = Polygon('Square')
p.info()
#'Polygon.info called for Polygon(Square)'
#That works the same as before. But what about extended_info? Remember it will use the definition in Shape, which in turn calls info. Keep in mind that self in that context refers to p - a Polygon class which overrides info:

print(p.extended_info())
#('Shape.extended_info called for Shape(Square)', 'Polygon.info called for Polygon(Square)')
#And this is the same mechanism that results in str(Person) ending up calling the __repr__ method in the Person class instead of the __repr__ method in the object class which would have just printed out the name and memory address of the Person instance.

#In fact we can see how this happens exactly this way:

class Person:
    def __str__(self):
        return 'Person.__str__ called'
    
class Student(Person):
    def __repr__(self):
        return 'Student.__repr__ called'
s = Student()
str(s)
#'Person.__str__ called'
repr(s)
#'Student.__repr__ called'
#And if we now have __str__ delegate to __repr__ instead:

class Person:
    def __str__(self):
        print('Person.__str__ called')
        return self.__repr__()
    
class Student(Person):
    def __repr__(self):
        return 'Student.__repr__ called'
s = Student()
str(s)
#Person.__str__ called
#'Student.__repr__ called'
repr(s)
#'Student.__repr__ called'
#Basically just keep track of which instance the methods are bound to and always start working you way from there to find the "closest" relevant method.
