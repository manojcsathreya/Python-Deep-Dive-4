'''
Instances
Objects that are created from a class are called instances of that class

    Person

Teacher Student

p1 = Person() s1 = Student() t1 = Teacher()

s1 is a Student ->s1 is an instance of Student

->Student inherits from Person

->s1 is a Person

p1 is a Person ->but p1 is not a Student

->s1 is not a Teacher

->but p1 is not a Teacher

->s1is an instance of Person
========================================================================================
isinstance()vs type()

    Person

Teacher Student

p1 = Person() s1 = Student() t1 = Teacher()

->s1 is an instance of Student  isinstance(s1, Student) -> True
->s1 is an instance of Person   isinstance(s1, Person) -> True
->s1 is not a Teacher           isinstance(s1, Teacher) -> False
->p1 is not a Student           isinstance(p1, Student) -> False

type(instance) ->returns the class the instance was created from
type(s1) -> Student type(t1) -> Teacher type(p1) -> Person

->more often use isinstance()rather than type() why?

->often more concerned whether an object has certain behaviors

Let's say we want to call the eat()method of an object if it has one
we could do this: 
if type(obj) is Person:
    obj.eat()
->but if obj is a Student(or Teacher), this won't call its eat() method
if type(obj) in [Person, Student, Teacher]:
    obj.eat()
    
Instead we could write:
Much simpler to use isinstance():
if isinstance(obj, Person):
    obj.eat()
tip: when using isinstance, try to use the least restrictive parent class you actually need
==============================================================================================
The issubclass()function
Used to inspect inheritance relationships between classes (not instances)

            Person

Teacher                 Student

        HighSchoolStudent   CollegeStudent

issubclass(Student, Person) ->True
issubclass(CollegeStudent, Student) ->True
issubclass(CollegeStudent, Person) ->True

issubclass(Student, Teacher) ->False
issubclass(Person, Student)  ->False

Note:
->Person is a parent of Student

->Person is an ancestor of CollegeStudent

->Person is not a parent of CollegeStudent

->parent is a direct relationship
->subclass is not necessarily direct
==============================================================================================
Defining Subclasses

class Person:                 -> what about this one?  is it inheriting from nothing? ->the object class
    pass

class Student(Person):
    pass

class Teacher(Person):
    pass

class CollegeStudent(Student):
    pass

class HighSchoolStudent(Student):
    pass

'''
# =============================================================================
# For now we're just going to define classes that inherit from another class, but we aren't going to bother implementing any functionality or state for these classes.
# 
# We just want to explore the relationships between objects created from classes that inherit from each other.
# =============================================================================

class Shape:
    pass

class Ellipse(Shape):
    pass

class Circle(Ellipse):
    pass

class Polygon(Shape):
    pass

class Rectangle(Polygon):
    pass

class Square(Rectangle):
    pass

class Triangle(Polygon):
    pass
# =============================================================================
# As you can see we created a single inheritance chain that looks something like this:
# 
#                          Shape
#      Ellipse                            Polygon
# 
#       Circle                   Rectangle          Triangle
#                                Square
# It is important to understand that these classes are subclasses of each other - just remember that subclass contains the word class - so it defines a relationship between classes, not instances:
# =============================================================================

issubclass(Ellipse, Shape)
#True
#But if we create instances of those two classes:

s = Shape()
e = Ellipse()
try:
    issubclass(e, s)
except TypeError as ex:
    print(ex)
# =============================================================================
# issubclass() arg 1 must be a class
# When we deal with instances of classes, we can instead use the isinstance() function:
# =============================================================================

isinstance(e, Ellipse)
#True
#But, not only is e an instance of an Ellipse, since Ellipse IS-A Shape, i.e. Ellipse is a subclass of Shape, it tunrs out thet e is also considered an instance of Shape:

isinstance(e, Shape)
#True
#Subclasses behave similarly in that a class may be a subclass of another class without being a direct subclass.

#In our example here, every class we defined is a subclass of Shape because the inheritance chains all go back up to the Shape class:

issubclass(Square, Shape)
# =============================================================================
# True
# And of course, the same works for instances when we look at isinstance:
# =============================================================================

sq = Square()
isinstance(sq, Square)
#True
isinstance(sq, Rectangle)
#True
isinstance(sq, Polygon)
#True
isinstance(sq, Shape)
#True
#But of course, a Square is not a subclass of Ellipse and Square instances are not instances of Ellipse:

issubclass(Square, Ellipse)
#False
isinstance(sq, Ellipse)
#False
#We'll come back to this later, but when we define a class in Python 3 that does not explicitly inherit from another class:

class Person:
    pass
#it is actually implicitly inheriting from a class!

#There is a class in Python called object - yes, it is a class, even though the name says object (but classes are objects - everything in Python is an object):

issubclass(Person, object)
#True
p = Person()
isinstance(p, Person)
# =============================================================================
# True
# This means that our Shape class we created actually inherits from object, and therefore every other class we created also inherits from object:
# =============================================================================

issubclass(Square, object)
#True
isinstance(sq, object)
#True
#We'll look at the object class in the next lecture.
