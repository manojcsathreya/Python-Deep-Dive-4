'''
Data Attributes, Classes and Instances
Let's focus on data attributes first (i.e. not functions) 
class MyClass:
    language = 'Python'
my_obj = MyClass()
MyClass.__dict__ -> {'language': 'Python'}
my_obj.__dict__ -> {}
MyClass.language ->Python starts looking for language attribute in MyClassnamespace
-> MyClass.language -> 'Python'
my_obj.language ->Python starts looking in my_objnamespace
->if it finds it, returns it
->if not, it looks in the type (class) of my_obj, i.e. MyClass
->'Python'
----------------------------------------------------------------------------------------
Data Attributes, Classes and Instances

class MyClass:
    language = 'Python
MyClass.language -> 'Python' 
my_obj = MyClass()
my_obj.__dict__ -> {}

my_obj.language = 'java'
my_obj.__dict__ -> {'language': 'java'}

my_obj.language -> 'java'
MyClass.language -> 'Python'

other_obj = MyClass()
other_obj.__dict__ = {}
other_obj.language -> 'Python'

class attribute
instance attribute
'''

#Data Attributes
#Let's focus on data attributes first (non-callables).

#As we saw before we can have class attributes - they live in the class dictionary:

class BankAccount:
    apr = 1.2
BankAccount.__dict__
'''
mappingproxy({'__module__': '__main__',
              'apr': 1.2,
              '__dict__': <attribute '__dict__' of 'BankAccount' objects>,
              '__weakref__': <attribute '__weakref__' of 'BankAccount' objects>,
              '__doc__': None})
'''
BankAccount.apr #1.2
#Now when we create instances of that class:

acc_1 = BankAccount()
acc_2 = BankAccount()
#The instance dictionaries are currently empty:

acc_1.__dict__, acc_2.__dict__
#({}, {})
#Yet, these instances do have an apr attribute:

acc_1.apr, acc_2.apr
#(1.2, 1.2)
#Where is that value coming from? The class the objects were created from!

#In fact, if we modify the class attribute:

BankAccount.apr = 2.5
#We'll see this reflected in the instances as well:

acc_1.apr, acc_2.apr
#(2.5, 2.5)
#And if we a a class attribute to BankAccount:

BankAccount.account_type = 'Savings'
acc_1.account_type, acc_2.account_type
#('Savings', 'Savings')
#As you can see modifying attributes in the class are reflected in the instances too - that's because Python does not find an apr attribute in the instance dic tionary, so next it looks in the class that was used to create the instance.

#Which raises the question, what happens if we add apr to the instance dictionary?

acc_1.apr = 0
#Well that did not raise an exception - so what's happening now:

acc_1.__dict__, acc_2.__dict__
#({'apr': 0}, {})
#As you can see, we actually create an entry for apr in the state dictionary of acc_1.

#Now that we have it there, it we try to get the attribute value apr for acc_1, Python will find it in the instance dictionary, so it will use that instead!

acc_1.apr, acc_2.apr
#(0, 2.5)
#In effect, the instance attribute apr is hiding the class attribute.

#You'll notice also that acc_2 was not affected - this is because we did not modify acc_2's dictionary, just the dictionary for acc_1.

#And the getattr and setattr functions work the same way as dotted notation:

acc_1 = BankAccount()
print(acc_1.__dict__) #{}
print(acc_1.apr) #2.5
print(getattr(acc_1, 'apr')) #2.5


setattr(acc_1, 'apr', 0) 
print(acc_1.__dict__) #{'apr': 0}
print(acc_1.apr) #0
print(getattr(acc_1, 'apr')) #0
#We can even add instance attributes directly to an instance:

acc_1.bank = 'Acme Savings & Loans'
acc_1.__dict__
#{'apr': 0, 'bank': 'Acme Savings & Loans'}
#But this is specific to the instance, and only that specific instance:

acc_2 = BankAccount()
acc_2.__dict__
#{}
'''
As you can see acc_2 has an empty instance dictionary.

So it is really important to distingush between class attributes and instance attributes.

Class attributes are like attributes that are "common" to all instances - because the attribute does not live in the instance, but in the class itself.

On the other hand, instance attributes are specific to each instance, and values for the same attribute can be different across multiple instances, as we just saw with acc_1.apr and acc_2.apr.

So, in summary, classes and instances each have their own state - usually maintained in a dictionary, available through __dict__. Irrespective of where the state is stored, when we look up an attribute on an instance, Python will first look for the attribute in the instance's local state. If it does not find it there, it will next look for it in the class of the instance.

One other thing to note is the difference in type between class and instance __dict__.

Classes as we saw, return a mapping proxy object:
    '''

BankAccount.__dict__
'''mappingproxy({'__module__': '__main__',
              'apr': 2.5,
              '__dict__': <attribute '__dict__' of 'BankAccount' objects>,
              '__weakref__': <attribute '__weakref__' of 'BankAccount' objects>,
              '__doc__': None,
              'account_type': 'Savings'})
    '''
#But instances, return a real dictionary:

acc_1.__dict__
#{'apr': 0, 'bank': 'Acme Savings & Loans'}
#So with instances, unlike with classes, we can manipulate that dictionary directly:

class Program:
    language = 'Python'
p = Program()
p.__dict__ #{}
p.__dict__['version'] = '3.7'
p.__dict__ #{'version': '3.7'}
p.version, getattr(p, 'version')
#('3.7', '3.7')
#But once again, this only affects that specific instance.

​
