"""
Slots
Remember that instance attributes are normally stored in a local dictionary of class instances

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

p = Point(0,0)

p.__dict__ -> {'x': 0, 'y': 0}

As we know there is a certain memory overhead with dictionaries
What happens if we have thousands of instances of Point?
->a lot of overhead!

Python 3.3 introduced key sharing dictionaries to help alleviate this problem

->but we can do even better
->slots
=======================================================================================================
Slots
We can tell Python that a class will contain only certain pre-determined attributes
->Python will then use a more compact data structure to store attribute values

class Point:
    __slots__ = ('x', 'y')     # an iterable containing the attribute names we will use in our class
    def __init__(self, x, y):
        self.x = x
        self.y = y

p = Point(0,0)
p.__dict__  -> Attribute Error: Point object has not attribute __dict__
vars(p)     -> TypeError: vars() argument must have __dict__ attribute 
dir(p)      -> […, 'x', 'y']
p.x -> 0 
p.x = 100 
p.x -> 100
=======================================================================================================
Slots
memory savings, even compared to key sharing dictionaries, can be substantial


class Point:                               class Point:
    def __init__(self, x, y):              __slots__ = ('x', 'y')
        self.x = x                         def __init__(self, x, y):
        self.y = y                             self.x = x
                                               self.y = y
10,000 instances

1,729 KB                                        635 KB
Isn’t creating that many instances of an object rare?

->depends on your program
->example: returning multiple rows from a database and putting each row into an object

->use slots in cases where you know you will benefit substantially
=======================================================================================================
Slots
using slots results in generally faster operations (on average)


class PersonDict:
    pass

class PersonSlots:
    __slots__ = ('name', )

def manipulate_dict():
    p = PersonDict()
    p.name = 'John'
    p.name
    del p.name

def manipulate_slots():
    p = PersonSlots()
    p.name = 'John'
    p.name
    del p.name

timeit(manipulate_dict)

timeit(manipulate_slots)

->about 30% faster
=======================================================================================================
Slots
So why not use slots all the time then?

->if we use slots, then we cannot add attributes to our objects that are not defined in slots

class Point:
    __slots__ = ('x', 'y')
    def __init__(self, x, y):
        self.x = x
        self.y = y

p = Point(0,0)

p.z = 100
->AttributeError: 'Point' object 
setattr(p, 'z', 100) has no attribute 'z'
->can cause difficulties in multiple inheritance ©2019 MathByte Academy
"""

#Let's start with an example of how we use slots:

class Location:
    __slots__ = 'name', '_longitude', '_latitude'
    
    def __init__(self, name, longitude, latitude):
        self._longitude = longitude
        self._latitude = latitude
        self.name = name
        
    @property
    def longitude(self):
        return self._longitude
    
    @property
    def latitude(self):
        return self._latitude
#Location still has that mapping proxy, and we can still add and remove class attributes from Location:

Location.__dict__
'''
mappingproxy({'__module__': '__main__',
              '__slots__': ('name', '_longitude', '_latitude'),
              '__init__': <function __main__.Location.__init__(self, name, longitude, latitude)>,
              'longitude': <property at 0x7feed0329ae8>,
              'latitude': <property at 0x7feed0329b38>,
              '_latitude': <member '_latitude' of 'Location' objects>,
              '_longitude': <member '_longitude' of 'Location' objects>,
              'name': <member 'name' of 'Location' objects>,
              '__doc__': None})
'''
Location.map_service = 'Google Maps'
Location.__dict__
'''
mappingproxy({'__module__': '__main__',
              '__slots__': ('name', '_longitude', '_latitude'),
              '__init__': <function __main__.Location.__init__(self, name, longitude, latitude)>,
              'longitude': <property at 0x7feed0329ae8>,
              'latitude': <property at 0x7feed0329b38>,
              '_latitude': <member '_latitude' of 'Location' objects>,
              '_longitude': <member '_longitude' of 'Location' objects>,
              'name': <member 'name' of 'Location' objects>,
              '__doc__': None,
              'map_service': 'Google Maps'})
'''
#But the use of slots affects instances of the class:

l = Location('Mumbai', 19.0760, 72.8777)
l.name, l.longitude, l.latitude
#('Mumbai', 19.076, 72.8777)
#The instance no longer has a dictionary for maintaining state:

try:
    l.__dict__
except AttributeError as ex:
    print(ex)
#'Location' object has no attribute '__dict__'
#This means we can no longer add attributes to the instance:

try:
    l.map_link = 'http://maps.google.com/...'
except AttributeError as ex:
    print(ex)
#'Location' object has no attribute 'map_link'
#Now we can actually delete the attribute from the instance:

del l.name
#And as we can see the instance now longer has that attribute:

try:
    print(l.name)
except AttributeError as ex:
    print(f'Attribute Error: {ex}')
#Attribute Error: name
#However we can still re-assign a value to that same attribute:

l.name = 'Mumbai'
l.name
#'Mumbai'
#Mainly we use slots when we expect to have many instances of a class and to gain a performance boost (mostly storage, but also attribute lookup speed).
