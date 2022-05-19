'''
Nested scopes in Class definitions

# module1.py
class Python:
    kingdom = 'animalia'
    phylum = 'chordata'
    family = 'pythonidae'
    def __init__(self, species):
        self.species = species 
    def say_hello(self):
        return 'ssss…'

p = Python('monty')

->module has its own (global) scope
contains Python, p

->class body has its own scope
contains kingdom, phylum, family, __init__, say_hello


->what about the scope of functions defined in the body of a class?

->turns out they are NOT nested inside the class body scope
->symbols __init__, say_helloare in the class body scope
->but functions themselves are nested in the class's containing scope
(module1in this example)
--------------------------------------------------------------------------------------
Think of it this way

# module1.py
class Python:
    kingdom = 'animalia'
    phylum = 'chordata'
    family = 'pythonidae'
    __init__ = callable_1
    say_hello = callable_2

p = Python('monty')
def callable_1(self, species):
    self.species = species

def callable_2(self):
    return 'ssss…'

->when Python looks for a symbol in a function, it will therefore not use the class body scope!
--------------------------------------------------------------------------------------
In practical terms…
class Account:
    COMP_FREQ = 12
    APR = 0.02  # 2%
    APY = (1 + APR/COMP_FREQ) ** COMP_FREQ - 1  -> this works because APR and COMP_FREQ are symbols in the same (class body) namespace

    def __init__(self, balance):
        self.balance = balance
        
    def monthly_interest(self):                 -> this works because we used self.APY
        return self.balance * self.APY

    @classmethod                                -> this works because we used cls.APY
    def monthly_interest_2(cls, amount):
        return amount * cls.APY
    
    @staticmethod
    def monthly_interest_3(amount):             -> this works because we used Account.APY
        return amount * Account.APY

    def monthly_interest_3(self):               -> this will fail if APYis not defined in this function's scope or in any enclosing scope
        return self.amount * APY

BEWARE: This can produce subtle bugs!
'''

# =============================================================================
# Class Body Scope
# The class body is a scope and therefore has it's own namespace. Inside that scope we can reference symbols like we would within any other scope:
# =============================================================================

class Language:
    MAJOR = 3
    MINOR = 7
    REVISION = 4
    FULL = '{}.{}.{}'.format(MAJOR, MINOR, REVISION)
Language.FULL
#'3.7.4'
#However, functions defined inside the class are not nested in the body scope - instead they are nested in whatever scope the class itself is in.

#This means that we cannot reference the class symbols inside a function without also telling Python where to look for it:

class Language:
    MAJOR = 3
    MINOR = 7
    REVISION = 4
    
    @property
    def version(self):
        return '{}.{}.{}'.format(self.MAJOR, self.MINOR, self.REVISION)
    
    @classmethod
    def cls_version(cls):
        return '{}.{}.{}'.format(cls.MAJOR, cls.MINOR, cls.REVISION)
    
    @staticmethod
    def static_version():
        return '{}.{}.{}'.format(Language.MAJOR, Language.MINOR, Language.REVISION)
l = Language()
l.version
#'3.7.4'
Language.cls_version()
#'3.7.4'
Language.static_version()
#'3.7.4'
#Basically think that the function symbols are in the class body namespace, but the functions themselves are defined externally to the class - just as if we had written it this way:

def full_version():
 return '{}.{}.{}'.format(Language.MAJOR, Language.MINOR, Language.REVISION)
full_version()
#'3.7.4'
#So writing something like this will not work:

class Language:
    MAJOR = 3
    MINOR = 7
    REVISION = 4
    
    @classmethod
    def cls_version(cls):
        return '{}.{}.{}'.format(MAJOR, MINOR, REVISION)
Language.cls_version()
# =============================================================================
# ---------------------------------------------------------------------------
# NameError                                 Traceback (most recent call last)
# <ipython-input-10-7a3f9fd88d68> in <module>
# ----> 1 Language.cls_version()
# 
# <ipython-input-9-18992503fb74> in cls_version(cls)
#       6     @classmethod
#       7     def cls_version(cls):
# ----> 8         return '{}.{}.{}'.format(MAJOR, MINOR, REVISION)
# 
# NameError: name 'MAJOR' is not defined
# 
# This behavior can lead to subtle bugs if we aren't careful.
# 
# What happens if the names MAJOR, MINOR and REVISION are defined in the enclosing scope?
# =============================================================================

MAJOR = 0
MINOR = 0
REVISION = 1
Language.cls_version()
#'0.0.1'
#See what happened?!!

#Now of course, the nested scopes follow the same usual rules, so we could technically have something like this:

MAJOR = 0
MINOR = 0
REVISION = 1
​
def gen_class():
    MAJOR = 0
    MINOR = 4
    REVISION = 2
    
    class Language:
        MAJOR = 3
        MINOR = 7
        REVISION = 4
​
        @classmethod
        def version(cls):
            return '{}.{}.{}'.format(MAJOR, MINOR, REVISION)
        
    return Language
cls = gen_class()
cls.version()
#'0.4.2'
# =============================================================================
# Notice how the scope of version was nested inside gen_class which itself is nested in the global scope.
# 
# When we called the version method, it found the MAJOR, MINOR and REVISION in the closest enclosing scope - which turned out to be the gen_class scope.
# 
# This means by the way, that version is not only a method, but actually a closure.
# =============================================================================

import inspect
inspect.getclosurevars(cls.version)
#ClosureVars(nonlocals={'MAJOR': 0, 'MINOR': 4, 'REVISION': 2}, globals={}, builtins={'format': <built-in function format>}, unbound=set())
#This last example of "unexpected" behavior I want to show you was show to me by a friend who was puzzled by it:

name = 'Guido'
​
class MyClass:
    name = 'Raymond'
    list_1 = [name] * 3
    list_2 = [name.upper() for i in range(3)]
    
    @classmethod
    def hello(cls):
        return '{} says hello'.format(name)
MyClass.list_1
#['Raymond', 'Raymond', 'Raymond']
#Since the expression [name] * 3 lives in the class body, it uses name that it finds in the class namespace.

MyClass.hello()
#'Guido says hello'
#Here, name is used inside a function, so the closest name symbol is the one in the module/global scope. Hence we see that Guido was used.

MyClass.list_2
#['GUIDO', 'GUIDO', 'GUIDO']
#That one is more puzzling... Why is the expression [name.upper() for i in range(3)] using name from the enclosing (module/global) scope, and not the one from the class namespace like [name] * 3 did?

# =============================================================================
# Remember what we discussed about comprehensions?
# 
# They are essentially thinly veiled functions!!!
# 
# So they behave like a function would, and therefore are not nested in the class body scope, but, in this case, in the module/global scope!
# =============================================================================
