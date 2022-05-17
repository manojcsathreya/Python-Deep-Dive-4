'''
Deleting Properties
Just like we can delete attributes from an object:
c = Circle()
c.color = 'yellow' c.color - yellow
del c.color
or delattr(c, 'color')
c.color - AttributeError

We can also support deleting properties from an instance object:
deleter argument of the property initializer @prop_name.deleter

-generally used to perform some cleanup activity upon deletion of the property
-not used very often
Important: calling the deleter runs code contained in the deleter method
-does not remove property from class itself
-it just calls the deleter method
-----------------------------------------------------------------------
Deleting Properties
class Circle:
    def __init__(self, color):
        self._color = color
    def get_color(self):
        return self._color
    def set_color(self, value):
        self._color = value
    def del_color(self):  --> when this method is invoked, it will remove _color from the instance namespace (dictionary)
        del self._color

    color = property(get_color, set_color, del_color)

c = Color('yellow')
c.color - 'yellow'

c.__dict__ - {'_color': 'yellow'}

del c.color c.__dict__ - {}
c.color - AttributeError
c._color - AttributeError
-----------------------------------------------------------------------------------------------
Deleting Properties
We can also use the decorator syntax:
class UnitCircle:
    def __init__(self, color):
        self._color = color
    @property
    def color(self):
        return self._color
    @color.setter
    def color(self, value):
        self._color = value
    @color.deleter
    def color(self):
        del self._color

c = UnitCircle('red')
c.__dict__ - {'_color': 'red'}
del c.color
c.__dict__ - {}
c.color - AttributeError = because getter tries to read self._color


But the property still exists defined on class

c.color = 'blue'

c.__dict__ - {'_color': 'blue'}
c.color - 'blue'
'''
#Deleting Properties
#Just like we can delete an attribute from an instance object, we can also delete a property from an instance object.

#Note that this action simply runs the deleter method, but the propertu remains defined on the class. It does not remove the property from the class, instead it is generally used to remove the property value from the instance.

#Properties, like attributes, can be deleted by using the del keyword, or the delattr function.

class Person:
    def __init__(self, name):
        self.name = name
​
    def get_name(self):
        print('getting name property value...')
        return self._name
    
    def set_name(self, value):
        print(f'setting name property to {value}...')
        self._name = value
    
    def del_name(self):
        # delete the underlying data
        print('deleting name property value...')
        del self._name
        
    name = property(fget=get_name, fset=set_name, fdel=del_name, doc='Person name.')
​
p = Person('Guido')
#setting name property to Guido...
p.name
#getting name property value...
#'Guido'
#And the underlying _name property is in our instance dictionary:

p.__dict__
#{'_name': 'Guido'}
del p.name
#deleting name property value...
#As we can see, the underlying _name attribute is no longer present in the instance dictionary:

p.__dict__ #{}
try:
    print(p.name)
except AttributeError as ex:
    print(ex)
#getting name property value...
#'Person' object has no attribute '_name'
#As you can see, the property deletion did not remove the property definition, that still exists.

#Alternatively, we can use the delattr function as well:

p = Person('Raymond')
#setting name property to Raymond...
delattr(p, 'name')
#deleting name property value...
#And we can of course use the decorator syntax as well:

class Person:
    def __init__(self, name):
        self.name = name
​
    @property
    def name(self):
        print('getting name property value...')
        return self._name
    
    @name.setter
    def name(self, value):
        """Person name"""
        print(f'setting name property to {value}...')
        self._name = value
    
    @name.deleter
    def name(self):
        # delete the underlying data
        print('deleting name property value...')
        del self._name
p = Person('Alex')
#setting name property to Alex...
p.name
#getting name property value...
#'Alex'
del p.name
#deleting name property value...
