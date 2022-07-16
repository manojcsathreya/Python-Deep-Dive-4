'''
Yet another representation…

We know we can use the format()function to precisely format certain types
->numbers, dates, etc

We can support this in our custom classes by implementing the __format__method

->see https://docs.python.org/3/library/string.html#formatspec

format(value, format_spec)
->if format_specis not supplied, it defaults to an empty string
->and it will instead use str(value)
(which in turn may fall back to repr)
©2019 MathByte Academy


Implementation

Implementing our own format specification is difficult!
->beyond scope of this course

Frequently we delegate formatting back to another type that already supports it
'''

# =============================================================================
# The __format__ Method
# We saw before the use of __str__ and __repr__.
# 
# However we have one more formatting function to look at!
# 
# The format() function.
# 
# For example we can use format() with a format specification for floats:
# =============================================================================

a = 0.1
format(a, '.20f')
#'0.10000000000000000555'
#Or we can use it with a datetime object:

from datetime import datetime
now = datetime.utcnow()
now
#datetime.datetime(2019, 6, 13, 3, 43, 48, 904829)
format(now, '%a %Y-%m-%d  %I:%M %p')
#'Thu 2019-06-13  03:43 AM'
# =============================================================================
# We can implement support for format specifiers in our own classes by implementing the __format__ method.
# 
# This is actually quite complicated to do, so we usually delegate back to some other type's formatting.
# 
# Just like with __str__ and __repr__, __format__ should return a string.
# =============================================================================

class Person:
    def __init__(self, name, dob):
        self.name = name
        self.dob = dob
        
    def __repr__(self):
        print('__repr__ called...')
        return f'Person(name={self.name}, dob={self.dob.isoformat()})'
    
    def __str__(self):
        print('__str__ called...')
        return f'Person({self.name})'
    
    def __format__(self, date_format_spec):
        print(f'__format__ called with {repr(date_format_spec)}...')
        dob = format(self.dob, date_format_spec)
        return f'Person(name={self.name}, dob={dob})'
#So now have:

from datetime import date
p = Person('Alex', date(1900, 10, 20))
str(p)
# =============================================================================
# __str__ called...
# 'Person(Alex)'
# =============================================================================
repr(p)
# =============================================================================
# __repr__ called...
# 'Person(name=Alex, dob=1900-10-20)'
# =============================================================================
format(p, '%B %d, %Y')
# =============================================================================
# __format__ called with '%B %d, %Y'...
# 'Person(name=Alex, dob=October 20, 1900)'
# If we do not specify a format, then the format function will use an empty string:
# =============================================================================

format(p)
#__format__ called with ''...
#'Person(name=Alex, dob=1900-10-20)'
