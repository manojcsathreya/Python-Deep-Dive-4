'''
Class Methods
When we define a function in a class -> how we call it will alter behavior
class MyClass:
    def hello():
        return 'Hello'

MyClass.hello -> just a plain function defined in MyClass
MyClass.hello() -> Hello

m = MyClass()
m.hello ->method bound to object m   ->instance method
m.hello() ->TypeError(missing argument)

Can we create a function in a class that will always be bound to the class, and never the instance?
MyClass.fn ->method bound to MyClass
m.fn ->method bound to MyClass

->@classmethod
----------------------------------------------------------------------------------------------------
Class Methods 
class MyClass:
    def hello():
        print('hello…')
    def inst_hello(self):
        print(f'hello from {self}')
    @classmethod
    def cls_hello(cls):
        print(f'hello from {cls}') 


                           MyClass                             Instance
hello                   regular function                    method bound to instance ->call will fail!

inst_hello              regular function                     method bound to instance

cls_hello                method bound to class               method bound to class
----------------------------------------------------------------------------------------------------
Static Methods
So can we define a function in a class that will never be bound to any object when called?
->Yes!
->in Python, those are called static methods ->@staticmethod
class Circle:
    @staticmethod
    def help():
        return 'help available'

Circle.help() -> help available

c = Circle()

c.help() -> help available

type(Circle.help) -> function

type(c.help) -> function

'''

# =============================================================================
# Class and Static Methods
# Asd we saw, when we define a function inside a class, how it behaves (as a function or a method) depends on how the function is accessed: from the class, or from the instance. (We'll cover how that works when we look at descriptors later in this course).
# =============================================================================
class Person:
    def hello(arg='default'):
        print(f'Hello, with arg={arg}')
#If we call hello from the class:

Person.hello() #Hello, with arg=default
#You'll notice that hello was called without any arguments, in fact, hello is a regular function:

Person.hello
#<function __main__.Person.hello(arg='default')>
#But if we call hello from an instance, things are different:

p = Person()
p.hello
#<bound method Person.hello of <__main__.Person object at 0x7f8f287fb860>>
p.hello()
#Hello, with arg=<__main__.Person object at 0x7f8f287fb860>
hex(id(p))
#'0x7f8f287fb860'
#And as you can see the instance p was passed as an argument to hello.

# =============================================================================
# Sometimes however, we define functions in a class that do not interact with the instance itself, but may need something from the class. In those cases, we want the class to be passed to the function as an argument, whether it is called from the class or from an instance of the class.
# 
# These are called class methods. You'll note that the behavior needs to be different - we don't want the instance to be passed to the function when called from an instance, we want the class to be passed to it. In addition, when called from the class, we also want the class to be passed to it (this is similar to static methods in Java, not to be confused with, as we'll see in a bit, static methods in Python).
# 
# We use the @classmethod decorator to define class methods, and the first argument of these methods will always be the class where the method is defined.
# 
# Let's see a simple example first:
# =============================================================================

class MyClass:
    def hello():
        # this IS an instance method, we just forgot to add a parameter to capture the instance
        # when this is called from an instance - so this will fail
        print('hello...')
        
    def instance_hello(arg):
        print(f'hello from {arg}')
        
    @classmethod
    def class_hello(arg):
        print(f'hello from {arg}')
        
m = MyClass()
MyClass.hello()
#hello...
#But, as expected, this won't work:

try:
    m.hello()
except TypeError as ex:
    print(ex)
#hello() takes 0 positional arguments but 1 was given
#On the other hand, notice now the instance method when called from the instance and the class:

m.instance_hello()
#hello from <__main__.MyClass object at 0x7f8ed87fff60>
try:
    MyClass.instance_hello()
except TypeError as ex:
    print(ex)
#instance_hello() missing 1 required positional argument: 'arg'
#As you can see, the instance method needs to be called from the instance. If we call it from the class, no argument is passed to the function, so we end up with an exception.

#This is not the case with class methods - whether we call the method from the class, or the instance, that first argument will always be provided by Python, and will be the class object (not the instance).

#Notice how the bindings are different:

MyClass.class_hello
#<bound method MyClass.class_hello of <class '__main__.MyClass'>>
m.class_hello
#<bound method MyClass.class_hello of <class '__main__.MyClass'>>
#As you can see in both these cases, class_hello is bound to the class.

#But with an instance method, the bindings behave differently:

MyClass.instance_hello
#<function __main__.MyClass.instance_hello(arg)>
m.instance_hello
#<bound method MyClass.instance_hello of <__main__.MyClass object at 0x7f8ed87fff60>>
#So, whenever we call class_hello the method is bound to the class, and the first argument is the class:

MyClass.class_hello()
#hello from <class '__main__.MyClass'>
m.class_hello()
#hello from <class '__main__.MyClass'>
#Although in this example I used arg as the parameter name in our methods, the normal convention is to use self and cls - that way everyone knows what we're talking about!

# =============================================================================
# We sometimes also want to define functions in a class and always have them be just that - functions, never bound to either the class or the instance, however we call them. Often we do this because we need to utility function that is specific to our class, and we want to keep our class self-contained, or maybe we're writing a library of functions (though modules and packages may be more appropriate for this).
# 
# These are called static methods. (So be careful here, Python static methods and Java static methods do not have the same meaning!)
# 
# We can define static methods using the @staticmethod decorator:
# 
# =============================================================================
class MyClass:
    def instance_hello(self):
        print(f'Instance method bound to {self}')
        
    @classmethod
    def class_hello(cls):
        print(f'Class method bound to {cls}')
        
    @staticmethod
    def static_hello():
        print('Static method not bound to anything')
m = MyClass()
m.instance_hello()
#Instance method bound to <__main__.MyClass object at 0x7f8ed8811a58>
MyClass.class_hello()
#Class method bound to <class '__main__.MyClass'>
m.class_hello()
#Class method bound to <class '__main__.MyClass'>
#And the static method can be called either from the class or the instance, but is never bound:

MyClass.static_hello
#<function __main__.MyClass.static_hello()>
m.static_hello
#<function __main__.MyClass.static_hello()>
MyClass.static_hello()
#Static method not bound to anything
m.static_hello()
#Static method not bound to anything
# =============================================================================
# Example
# Let's see a more concrete example of using these different method types.
# 
# We're going to create a Timer class that will allow us to get the current time (in both UTC and some timezone), as well as record start/stop times.
# 
# We want to have the same timezone for all instances of our Timer class with an easy way to change the timezone for all instances when needed.
# 
# If you need to work with timezones, I recommend you use the pyrz 3rd party library. Here, I'll just use the standard library, which is definitely not as easy to use as pytz.
# 
# =============================================================================
from datetime import datetime, timezone, timedelta
​
class Timer:
    tz = timezone.utc  # class variable to store the timezone - default to UTC
    
    @classmethod
    def set_tz(cls, offset, name):
        cls.tz = timezone(timedelta(hours=offset), name)
So tz is a class attribute, and we can set it using a class method set_timezone - any instances will share the same tz value (unless we override it at the instance level)

Timer.set_tz(-7, 'MST')
Timer.tz
#datetime.timezone(datetime.timedelta(-1, 61200), 'MST')
t1 = Timer()
t2 = Timer()
t1.tz, t2.tz
# =============================================================================
# (datetime.timezone(datetime.timedelta(-1, 61200), 'MST'),
#  datetime.timezone(datetime.timedelta(-1, 61200), 'MST'))
# =============================================================================
Timer.set_tz(-8, 'PST')
t1.tz, t2.tz
# =============================================================================
# (datetime.timezone(datetime.timedelta(-1, 57600), 'PST'),
#  datetime.timezone(datetime.timedelta(-1, 57600), 'PST'))
# =============================================================================
#Next we want a function to return the current UTC time. Obviously this has nothing to do with either the class or the instance, so it is a prime candidate for a static method:

class Timer:
    tz = timezone.utc  # class variable to store the timezone - default to UTC
    
    @staticmethod
    def current_dt_utc():
        return datetime.now(timezone.utc)
    
    @classmethod
    def set_tz(cls, offset, name):
        cls.tz = timezone(timedelta(hours=offset), name)
Timer.current_dt_utc()
#datetime.datetime(2019, 6, 2, 23, 25, 59, 714761, tzinfo=datetime.timezone.utc)
t = Timer()
t.current_dt_utc()
#datetime.datetime(2019, 6, 2, 23, 25, 59, 723565, tzinfo=datetime.timezone.utc)
#Next we want a method that will return the current time based on the set time zone. Obviously the time zone is a class variable, so we'll need to access that, but we don't need any instance data, so this is a prime candidate for a class method:

class Timer:
    tz = timezone.utc  # class variable to store the timezone - default to UTC
    
    @staticmethod
    def current_dt_utc():
        return datetime.now(timezone.utc)
    
    @classmethod
    def set_tz(cls, offset, name):
        cls.tz = timezone(timedelta(hours=offset), name)
        
    @classmethod
    def current_dt(cls):
        return datetime.now(cls.tz)
Timer.current_dt_utc(), Timer.current_dt()
# =============================================================================
# (datetime.datetime(2019, 6, 2, 23, 25, 59, 733420, tzinfo=datetime.timezone.utc),
#  datetime.datetime(2019, 6, 2, 23, 25, 59, 733423, tzinfo=datetime.timezone.utc))
# =============================================================================
t1 = Timer()
t2 = Timer()
t1.current_dt_utc(), t1.current_dt()
# =============================================================================
# (datetime.datetime(2019, 6, 2, 23, 25, 59, 741248, tzinfo=datetime.timezone.utc),
#  datetime.datetime(2019, 6, 2, 23, 25, 59, 741251, tzinfo=datetime.timezone.utc))
# =============================================================================
t2.current_dt()
# =============================================================================
# datetime.datetime(2019, 6, 2, 23, 25, 59, 745699, tzinfo=datetime.timezone.utc)
# And if we change the time zone (we can do so either via the class or the instance, no difference, since the set_tz method is always bound to the class):
# =============================================================================

t2.set_tz(-7, 'MST')
Timer.__dict__
# =============================================================================
# mappingproxy({'__module__': '__main__',
#               'tz': datetime.timezone(datetime.timedelta(-1, 61200), 'MST'),
#               'current_dt_utc': <staticmethod at 0x7f8ed8836d30>,
#               'set_tz': <classmethod at 0x7f8ed8836d68>,
#               'current_dt': <classmethod at 0x7f8ed8836da0>,
#               '__dict__': <attribute '__dict__' of 'Timer' objects>,
#               '__weakref__': <attribute '__weakref__' of 'Timer' objects>,
#               '__doc__': None})
# =============================================================================
Timer.current_dt_utc(), Timer.current_dt(), t1.current_dt(), t2.current_dt()
# =============================================================================
# (datetime.datetime(2019, 6, 2, 23, 25, 59, 761523, tzinfo=datetime.timezone.utc),
#  datetime.datetime(2019, 6, 2, 16, 25, 59, 761526, tzinfo=datetime.timezone(datetime.timedelta(-1, 61200), 'MST')),
#  datetime.datetime(2019, 6, 2, 16, 25, 59, 761526, tzinfo=datetime.timezone(datetime.timedelta(-1, 61200), 'MST')),
#  datetime.datetime(2019, 6, 2, 16, 25, 59, 761527, tzinfo=datetime.timezone(datetime.timedelta(-1, 61200), 'MST')))
# So far we have not needed any instances to work with this class!
# 
# Now we're going to add functionality to start/stop a timer. Obviously we want this to be instance based, since we want to be able to create multiple timers.
# =============================================================================

class TimerError(Exception):
    """A custom exception used for Timer class"""
    # (since """...""" is a statement, we don't need to pass)
    
class Timer:
    tz = timezone.utc  # class variable to store the timezone - default to UTC
    
    def __init__(self):
        # use these instance variables to keep track of start/end times
        self._time_start = None
        self._time_end = None
        
    @staticmethod
    def current_dt_utc():
        """Returns non-naive current UTC"""
        return datetime.now(timezone.utc)
    
    @classmethod
    def set_tz(cls, offset, name):
        cls.tz = timezone(timedelta(hours=offset), name)
        
    @classmethod
    def current_dt(cls):
        return datetime.now(cls.tz)
    
    def start(self):
        # internally we always non-naive UTC
        self._time_start = self.current_dt_utc()
        self._time_end = None
        
    def stop(self):
        if self._time_start is None:
            # cannot stop if timer was not started!
            raise TimerError('Timer must be started before it can be stopped.')
        self._time_end = self.current_dt_utc()
        
    @property
    def start_time(self):
        if self._time_start is None:
            raise TimerError('Timer has not been started.')
        # since tz is a class variable, we can just as easily access it from self
        return self._time_start.astimezone(self.tz)  
        
    @property
    def end_time(self):
        if self._time_end is None:
            raise TimerError('Timer has not been stopped.')
        return self._time_end.astimezone(self.tz)
    
    @property
    def elapsed(self):
        if self._time_start is None:
            raise TimerError('Timer must be started before an elapsed time is available')
            
        if self._time_end is None:
            # timer has not ben stopped, calculate elapsed between start and now
            elapsed_time = self.current_dt_utc() - self._time_start
        else:
            # timer has been stopped, calculate elapsed between start and end
            elapsed_time = self._time_end - self._time_start
            
        return elapsed_time.total_seconds()
from time import sleep
​
t1 = Timer()
t1.start()
sleep(2)
t1.stop()
print(f'Start time: {t1.start_time}')
print(f'End time: {t1.end_time}')
print(f'Elapsed: {t1.elapsed} seconds')
# =============================================================================
# Start time: 2019-06-02 23:25:59.777250+00:00
# End time: 2019-06-02 23:26:01.781431+00:00
# Elapsed: 2.004181 seconds
# =============================================================================
t2 = Timer()
t2.start()
sleep(3)
t2.stop()
# =============================================================================
# print(f'Start time: {t2.start_time}')
# print(f'End time: {t2.end_time}')
# print(f'Elapsed: {t2.elapsed} seconds')
# Start time: 2019-06-02 23:26:01.787596+00:00
# End time: 2019-06-02 23:26:04.792814+00:00
# Elapsed: 3.005218 seconds
# So our timer works. Furthermore, we want to use MST throughout our application, so we'll set it, and since it's a class level attribute, we only need to change it once:
# =============================================================================

Timer.set_tz(-7, 'MST')
print(f'Start time: {t1.start_time}')
print(f'End time: {t1.end_time}')
print(f'Elapsed: {t1.elapsed} seconds')
# =============================================================================
# Start time: 2019-06-02 16:25:59.777250-07:00
# End time: 2019-06-02 16:26:01.781431-07:00
# Elapsed: 2.004181 seconds
# =============================================================================
print(f'Start time: {t2.start_time}')
print(f'End time: {t2.end_time}')
print(f'Elapsed: {t2.elapsed} seconds')
# =============================================================================
# Start time: 2019-06-02 16:26:01.787596-07:00
# End time: 2019-06-02 16:26:04.792814-07:00
# Elapsed: 3.005218 seconds
# =============================================================================
​
