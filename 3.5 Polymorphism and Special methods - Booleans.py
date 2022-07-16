'''
BOOLEAN

Special Methods: Boolean
Every object in Python has an associated truth (boolean) value
any non-zero number ->True 
False otherwise (i.e if equal to 0)
an empty collection (len()is 0) ->False 
True otherwise

By default, any custom object also has a truth value
->can override this by defining the __bool__method ->must return True/ False

->if __bool__ is not defined
->Python looks for __len__ 0->False, anything else will be True
->if neither present, always returns True
'''
# =============================================================================
# As we know every object in Python has an associated truth value. Empty container types are falsy, non-zero numbers are truthy, zero numbers are falsy, etc.
# 
# The way Python determines the truth value of our custom classes is to:
# 
# first look for an implementation of the __bool__ method (which needs to return a boolean)
# if not present, looks for __len__ and will return False if that is 0, and True otherwise
# otherwise returns True
# Let's look at some example which illustrate this behavior:
# 
# First let's not define anything, so our objects should always have a True associated truth value:
# =============================================================================

class Person:
    pass
p = Person()
bool(p)
#True
#Now let's implement the __len__ method:

class MyList:
    def __init__(self, length):
        self._length = length
        
    def __len__(self):
        print('__len__ called')
        return self._length
l1 = MyList(0)  # so __len__ will return 0
l2 = MyList(10)  # so __len__ will return 10
bool(l1)
#__len__ called
#False
bool(l2)
#__len__ called
#True
#So when we create custom iterables, as long as we have a __len__ method implemented, we can actually skip implementing the __bool__ method, and our class will remain consistent with other collection types behaviors (empty collections are falsy, otherwise truthy).

#Let's implement the __bool__ method though, just to see that if it is present it will get called instead of the __len__ method:

class MyList:
    def __init__(self, length):
        self._length = length
        
    def __len__(self):
        print('__len__ called')
        return self._length
    
    def __bool__(self):
        print('__bool__ called')
        return self._length > 0
p1 = MyList(0)
p2 = MyList(100)
bool(p1)
#__bool__ called
#False
bool(p2)
#__bool__ called
#True
# =============================================================================
# For classes that do not define __len__ we may want to use the __bool__ method. For example, consider a 2D Point class where we want to consider the origin point (0,0) falsy, and everything else truthy.
# 
# By default, all instances of our Point class will be truthy (they have neither a __len__ nor a __bool__ method):
# =============================================================================

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
p1 = Point(0, 0)
p2 = Point(1, 1)
bool(p1), bool(p2)
#(True, True)
#So now let's implement __bool__ to get our desired functionality:

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
    def __bool__(self):
        return self.x != 0 or self.y != 0
p1 = Point(0, 0)
p2 = Point(1, 1)
bool(p1)
#False
bool(p2)
#True
#Note that with associated values, we could technically do something like this:

bool(p1.x or p1.y)
#False
bool(p2.x or p2.y)
#True
#This works because any 0 number is falsy.

#So we might think we can use this approach instead of the explicit != 0 comparisons:

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
    def __bool__(self):
        return self.x or self.y
p1 = Point(0, 0)
p2 = Point(1, 1)
#Then if we call __bool__ directly:

bool(p1.__bool__()), bool(p2.__bool__())
#(False, True)
#But it we try to use the bool() function:

try:
    bool(p1)
except TypeError as ex:
    print(ex)
#__bool__ should return bool, returned int
#we can see that we have an exception. Although we can work with truth values in most circumstances, Python insists that __bool__ should return an actual boolean type.

#If we really wanted to, we could write:

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
    def __bool__(self):
        return bool(self.x or self.y)
p1 = Point(0, 0)
p2 = Point(1, 1)
bool(p1), bool(p2)
#(False, True)
