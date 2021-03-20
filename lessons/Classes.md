# Lesson 6 - Classes and Objects #

In this lesson we look at classes and objects

## Classes ##

We have seen so far how everything in python is an object.  We have also seen how to create new "callable" objects, with `def` and `lambda`, but that doesn't cover all the other type of objects we have encountered in our study of python so far: is there a way to create custom objects and make them do whatever we want ?

The answer is yes: with the `class` keyword, which is the equivalent of `def`, but for defining classes.

A class could be seen as a template, or stencil, that is used to create objects that perform the same type of functions. When an object is created from a class, it is called an instance of this class, and two instances of the same class share the code, and some data, but not all. Some of the data is stored in the class, and other (most of the times) is stored in the instance: the class data is shared across all instances of the same class, while the instance data is unique for each instance.

The main purpose of a class is to group together data and functions in a single object, to perform a set of functions that are related, to simplify the dynamics of the script or program. The "variables" containing the data in a class or instance are called "properties", and the "functions" contained in a class are called "methods", but if you look carefully, they behave like a callable property.

When an instance of a class is created, it is done through what is some times called a "constructor".

There is a convention, in python, where all properties (and therefore also methods) that have a name that starts with an underscore (`_`) are considered private, and 2 underscore are reserved for internal use. One should never define new properties with 2 underscore at the beginning of the name, except for the case where the programmer wants to replace an existing one. We will see later some examples of this type of situation.

So, how does one create a new class ?

This is the way a `class` statement looks like:

```python
class Name (inheritance):
  codeblock
```

Most of the time, you won't need to specify `inheritance`, which states that this class _Name_ inherits functionalities from the object specificed in the round brackets (). If you do not specify anything, python will automatically assume that _Name_ will inherit from object by default, but if you want to inherit from another class that is not object, you need to specify it. We will look at inheritance in more detail towards the end of this lesson.

The `codeblock` is the important part, where you create your own class.

Let's create a class:

```python
class testing:
  pass
```

If you remember, we've discussed about `pass` previously, and we mentioned it's used as a place-holder for when you do not want to spend time typing something that is expected. This class is not very useful as is, although there are some cases where you might want to do this.

How do we use a class? Let's re-use the `testing` class from above.

```python
class testing:
  pass
a = testing()
b = testing()

print(a)
print(type(a))
print(a.__class__)
print(a.__class__.__name__)
```

This produces the following output:

```shell
<class '__main__.testing'>
<class '__main__.testing'>
<__main__.testing object at 0x7f74d200d1f0>
<class '__main__.testing'>
<class '__main__.testing'>
testing
```

So, we've seen that to instantiate an object from a class, we use the name of the class as a callable. In reality, `class(parameters)` will mean a call `class.__new__()` and then to `class.__init__(parameters)`. We won't look too much at `__new__`, but we will look at `__init__` later on.

In the example above, `a` and `b` are instances of class `testing`, and we can use them just as any other object in python.

## Properties ##

One of the reasons you might want to create a class is to keep some values together, and the way to do that is with "properties".

As we have seen, a class has 2 types of properties: the `class` properties, and the `instance` properties. Let's look at some examples:

```python
class test1:
  prop1 = 1
  prop2 = 2

a = test1()
b = test1()

print(a.prop1)
print(b.prop1)
a.prop1 = 5
print(a.prop1)
print(b.prop1)
print(test1.prop1)
```

The output shows something that might be surprising:

```shell
1
1
5
1
1
```

The `a` instance now has a different value for `prop1` from `b`, since we changed it with `a.prop1 = 5` Also, we can see how to access the class property, using the name of the class as if it were an instance What happens if we change that?

```python
class test1:
  prop1 = 1
  prop2 = 2

a = test1()
b = test1()

print(a.prop1)
print(b.prop1)
a.prop1 = 7
print(a.prop1)
test1.prop1 = 123
print(a.prop1)
print(b.prop1)

c = test1()
print(c.prop1)

```

This will produce the following output:

```shell
1
1
7
7
123
123
```

As you can see, `a`'s `prop1` changed to the custom value (`7`) and remained with that value, while `b` got its value updated to the new value of the class property (`123`). Any new class instance, e.g. `c`,  also inherits the new value.

## Methods ##

A method is a function that is "bound" to the class. There is nothing special about a method to make it different from a stand-alone function, except for the convention that python uses to call it.

A function is called like this: `functionName(parameters)`.

A method is called like this: `instance.method(parameters)`, or `class.method(parameters)`. So, if you forget about the part before the dot, they look the same.

The convention is that when a method is called, like one of the 2 cases above, the part before the dot is passed as the first parameter to the function that implements the method, so these would be the same as the following calls: `method(instance, parameters)`, or `method(class, parameters)`. Another convention is to call the 1st parameter to the method definition `self` for instance methods, and `cls` for the class methods. You can use any name you want, but it is best to stick to these conventions or else you will confuse anyone who later wants to look at your code.

This 1st parameter gives the function access to the instance or class. The above might seem a bit complicated, but it really is simple. As we've already mentioned, the constructor of a class is called `__init__`, and with it we can help build the class instance, and customise its properties based on parameters.

Let's say we want to create a class to describe a circle. We need to store the radius and for convenience, pi. Also, since this is a proper class, rather than empty classes we created for test earlier, it's time we do proper documentation

```python
class circle:
  """
  A circle object is created from a radius, default is 1
  """
  pi = 3.141529
  
  def __init__(self, radius=1):
    "Initialise the circle from the specified radius"
    self.radius = radius

a = circle()
b = circle(7)

print (a.radius)
print (b.radius)
```

As you can see, we are now using `__init__` to customise the radius just at the time where the instance is created. Next, we can add a couple of methods, such as `area`, `perimeter`, `diameter`

```python
class circle:
  """
  A circle object is created from a radius, default is 1
  """
  pi = 3.141529
  def __init__(self, radius=1):
    "Initialise the circle from the specified radius"
    self.radius = radius
  def diameter(self):
    "Return twice the radius"
    return self.radius * 2
  def area(self):
    "calculate the area of the circle"
    return circle.pi * self.radius **2
  def perimeter(self):
    "calculate the perimeter of the circle"
    return self.diameter() * circle.pi

c = circle(7)
print('Area', c.area())
print('Diameter', c.diameter())
print('Perimeter', c.perimeter())
```

And the output is nothing special:

```shell
Area 153.934921
Diameter 14
Perimeter 43.981406
```

Notice how the methods are using the `self` object to obtain access to `radius`, but also `diameter`, while in this case we are using `circle.pi` to get pi. We could have used `self.pi`, or we could also have used `self.__class__.pi`, or `type(self).pi`

The choice of which one to use depends on many factors and conditions.

We know that `self.pi` would mean accessing the instance's private copy, so we should use that if we plan to have `pi` change for each instance. We should use `circle.pi` if we plan for `pi` to stay the same, and maybe change for everyone in the program.

It might look strange to think of `pi` changing value, but keep in mind that this is just a simple example, for more complicated classes, this might make more sense, but imagine changing `pi` to a more precise value depending on the calculations, if it makes more sense.

There is another consideration to make __inheritance__. If you plan to create other classes that inherit from circle, which `pi` do you want to use?

If you use `self.pi`, you'll use the instance's, as we said.

If you use `circle.pi`, you'll be using `circle`'s one, which might or might not be what you want.

This is why there is the option also to use `type(self).pi` (or the `self.__class__.pi`, which is more or less the same, but more frowned upon due to the `__` at the beginning of the method name). This would ensure that whatever class you are using, you'd be using the `pi` value of that class, rather than the `pi` value of the instance or of `circle`.

The choice, therefore, is down to each situation. Now, what happens if we print an instance of `circle` ? How does python know how to print it?

```python
class circle:
  """
  A circle object is created from a radius, default is 1
  """
  pi = 3.141529
  def __init__(self, radius=1):
    "Initialise the circle from the specified radius"
    self.radius = radius
  def diameter(self):
    "Return twice the radius"
    return self.radius * 2
  def area(self):
    "calculate the area of the circle"
    return circle.pi * self.radius **2
  def perimeter(self):
    "calculate the perimeter of the circle"
    return self.diameter() * circle.pi

a = circle()
print(a)
```

This will produce something like this:

```shell
<__main__.circle object at 0x7fe6be6ab4f0>
```

When python is asked to print an object, it will look at whether the object has a `__repr__` method, and if so, use it. If not, it will try `__str__`, and if that exists, use that.

`__repr__` issued to show a __representation__ of the object, and if you remember, we saw the output of it when we printed lists, dictionaries, tuples and so on.

You can access the `__repr__` of an object with the `repr` built-in object and, as you probably have guessed, `__str__` is accessed by using `str`

```python
print(repr([1, 2, 3]))
```

This use of `repr` here is pointless, since `print([1, 2, 3])` would have called `str` and, since `__str__` is not yet defined, `repr` is used anyway, but the purpose is to show the output:

```shell
[1, 2, 3]
```

There is a sort of convention that `__repr__` should try to give you an output that you'd use to build a copy of that object. This is not strictly required, and many times this is not followed, but as it looks like a nice idea, we will try to do it:

```python
class circle:
  """
  A circle object is created from a radius, default is 1
  """
  pi = 3.141529
  def __init__(self, radius=1):
    "Initialise the circle from the specified radius"
    self.radius = radius
  def diameter(self):
    "Return twice the radius"
    return self.radius * 2
  def area(self):
    "calculate the area of the circle"
    return circle.pi * self.radius **2
  def perimeter(self):
    "calculate the perimeter of the circle"
    return self.diameter() * circle.pi
  def __repr__(self):
    "representation of a circle"
    return '{0}({1})'.format(self.__class__.__name__, self.radius)

c = circle()
print(c)
print(repr(c))
print(str(c))
```

As you can see from the output below, they all produce the same output. This is because python finds out that `__str__` is not there, and it fails back to `__repr__` in the hope that it will help.

```shell
circle(1)
circle(1)
circle(1)
```

So, let's define `__str__` to be a bit more descriptive, because `__repr__` is meant for people troubleshooting, and `__str__` is meant for people consuming the class, so `__str__` is meant to be pretty and handy. Let's use something like the initial `print` commands we used earlier:

```python
class circle:
  """
  A circle object is created from a radius, default is 1
  """
  pi = 3.141529
  def __init__(self, radius=1):
    "Initialise the circle from the specified radius"
    self.radius = radius
  def diameter(self):
    "Return twice the radius"
    return self.radius * 2
  def area(self):
    "calculate the area of the circle"
    return circle.pi * self.radius **2
  def perimeter(self):
    "calculate the perimeter of the circle"
    return self.diameter() * circle.pi
  def __repr__(self):
    "representation of a circle"
    return '{0}({1})'.format(self.__class__.__name__, self.radius)
  def __str__(self):
    "Pretty representation of a circle"
    return 'circle with radius: {r:.6f}, diameter(d:.6f) area: {a:.6f}, perimeter: {p:.6f}'.format(r=self.radius, d=self.diameter(), a=self.area(), p=self.perimeter())

c = circle()
print(c)
print(repr(c))
print(str(c))
```

And finally, we can see that `print` calls `str` first, and `repr` when `__str__` is not defined:

```shell
circle with radius: 1.000000, diameter(d:.6f) area: 3.141529, perimeter: 6.283058
circle(1)
circle with radius: 1.000000, diameter(d:.6f) area: 3.141529, perimeter: 6.283058
```

If your class is more than a couple of things, define at least `__repr__`, as it will help you with troubleshooting.

One last thing to notice: `radius` was created in the `__init__`, rather than in the `class`. This is quite common in python, and the choice between which one to use is a matter of style: in general, the properties defined at `class` are to be used as a class property (like `pi`), and the properties defined in `__init__` are definitely going to be only available as instance properties, and are not available via `class.property`

## Class methods and static methods ##

As we've seen, properties can be either class or instance but what about methods? Yes, there are also class methods, and also static methods, so lets see what the difference is next. It is quite similar to what we've already discussed about properties, but not exactly the same. The distinction is mostly on what _access_ each method has to the class and the instance:

- methods (we could call them "instance methods" in this context) are methods that work on instances, and have access to the class, either directly (e.g. `circle.pi`) or through the instance (e.g. `type(self)` or `self.__class__`)
- class methods, which have **no access** to any instance, but have access to the class, via `cls`
- static methods, which have **no access** to any instance or class

We have seen examples of the methods, or "instance methods" as we call them here to differentiate from the others, so we don't need to look further there.

The "class methods" are methods that perform generic functions that are associated to the class, but not to the instance. These methods can be called as `class.method()` even when there is no instance. A class method needs to be "decorated" as `@classmethod`

The "static methods" are usually utility methods, that do not need to know anything about the class or its instances, but they are grouped inside the class because their utility function can be associated with the class. These methods also can be called as `class.method()` without any instance. A static method needs to be decorated as `@staticmethod`

Let's look at a couple of examples. In our example of a circle, we might want a function to provide a text representation of pi, similar to `__repr__` and `__str__`, in case we want to print it. This doesn't need access to methods.

Also, we might want to replace the `pi` property with a function that calculates `pi` with a certain precision. This method doesn't need any access to a class or instance.

Now, there are ways to replace the property with what is called a "getter", so that we don't need to change the rest of our class to deal with the fact that `pi` is not a property any more, but a method. However this is a bit of a deep-dive concept, and since we are just learning about python, we can do without that at the moment.

```python
class circle:
  """
  A circle object is created from a radius, default is 1
  """
  def __init__(self, radius=1):
    "Initialise the circle from the specified radius"
    self.radius = radius
  @staticmethod
  def pi():
    "Decent approximation of a circle"
    return 355/113
  @classmethod
  def strpi(cls):
    "Format pi to look nice"
    return "{cls}'s π = {pi:6f}".format(cls=cls.__name__, pi=cls.pi())
  def diameter(self):
    "Return twice the radius"
    return self.radius * 2
  def area(self):
    "calculate the area of the circle"
    return circle.pi() * self.radius **2
  def perimeter(self):
    "calculate the perimeter of the circle"
    return self.diameter() * circle.pi()
  def __repr__(self):
    "representation of a circle"
    return '{0}({1})'.format(self.__class__.__name__, self.radius)
  def __str__(self):
    "Pretty representation of a circle"
    return 'circle with radius: {r:.6f}, diameter(d:.6f) area: {a:.6f}, perimeter: {p:.6f}'.format(r=self.radius, d=self.diameter(), a=self.area(), p=self.perimeter())
```

You can print `pi` as follows:

```shell
c = circle()
print('Pi', c.pi())
print('Pretty Pi', c.strpi())
```

The decorator is a way for python to simplify some syntax when making changes to objects, and it means that the following 2 statements would be equivalent:

```python
def something():
  pass

a = decorator(a)
```

and

```python
@decorator
def something():
  pass
```

As you can see, it's much easier to deal with the second format.

`classmethod` and `staticmethod` are the most common use-cases for a decorator, but since a decorator is just another object, you can create your own, or use someone else's ones too.

## Inheritance ##

We discussed briefly about "inheritance", but let's look at it a bit more here:

Inheritance is a very common concept in object-oriented languages, and it can become very complicated very quickly. We will try to keep it simple here, so we could describe it as a way to create an object that receives functionalities from another, with the intention of adding or replacing functionalities.

You might think "ok, I don't need to know this, I don't plan to do any such thing", but keep in mind that any class you create will automatically inherit from `object`!

Let's say we want to create a new type of integer, we will call it `Int` instead of `int`. We don't plan to change anything else for now, but as we might change it in the future, we want to prepare our code to offer the possibility.

The `int` class has a lot of functionalities, so it would take ages to re-write them all in our `Int` so that we can use it in our script. This re-write would also be a waste of time, since it's quite easy to do this with inheritance:

```python
class Int(int):
  pass

a = Int(3)
b = Int(5)

print(a + b)
```

So our new class `Int` has inherited its functionalities from `int`. This will produce `8` as if we used `int`. Now, our script is working, but we can change `Int` whenever we want. For example, let's say we want to change the `+`, for whatever reason:

```python
class Int(int):
  def __add__(self, other):
    "Funny version of add"
    return self * other

a = Int(3)
b = Int(5)

print(a + b)
```

And now, the script returns `15`, but if we change the last line to say `print(a - b)`, or any other operation, it will work as if we were using `int`, because all the other functions are "inherited".

Let's say we want to hide our funny version of `+` a bit more, and we want the usual behaviour most of the time, and we want our funny behaviour only if the first number is 3

```python
class Int(int):
  def __add__(self, other):
    "Funny version of add"
    if self == Int(3):
      return self * other
    else:
      return super().__add__(other)

a = Int(3)
b = Int(5)

print(a + b)

print(b + a)
```

This will do! The output is `15` for the first `print` and `8` for the second.

`super()` is a way to get access to the "parent" of the class, or in other words, the object from which this object inherits, so that you can use the unmodified methods and properties, such as `__add__` in this case.

Let's look at another example of inheritance, this time with more classes involved:

```python
class animal:
  def eat(self, food):
    print('the', type(self).__name__, 'eats', food)

class cat(animal):
  def noise(self):
    print('the', type(self).__name__, 'says meow')

class dog(animal):
  def noise(self):
    print('the', type(self).__name__, 'says woof')

class terrier(dog):
  def noise(self):
    for _ in range(10):
      super().noise()

a = animal()
a.eat('cake')

b = cat()
b.noise()
b.eat('fish')

c = dog()
c.noise()
c.eat('meat')

d = terrier()
d.noise()
d.eat('kibble')


isinstance(d, dog)
isinstance(d, animal)
isinstance(d, cat)
```

As you can see, the animal objects all have `eat`, and the `terrier` also inherits the `noise` method from `dog`, but it repeats it many times instead (using `super()`)


```
the animal eats cake
the cat says meow
the cat eats fish
the dog says woof
the dog eats meat
the terrier says woof
the terrier says woof
the terrier says woof
the terrier says woof
the terrier says woof
the terrier says woof
the terrier says woof
the terrier says woof
the terrier says woof
the terrier says woof
the terrier eats kibble
True
True
False
```

Also, the above shows you that `isinstance()` allows you to check if an object is or has, among its ancestors, a certain class, which is useful to understand what type of object you are working with. In our example, a `terrier` is a `dog`, so you can expect to be able to use it in all the places where a dog is expected, while you can't use it in a place where a `cat` is expected.

As you can see, inheritance is a handy way to extend or change the functionalities of built-in or 3rd party objects without actually re-writing them. You can just inherit, and override only what you need.

Another use-case is if you have a bunch of different behaviours that you need to code, but a large part of these different behaviours is in common: what you do is write a class for the common functionalities, and then create a bunch of classes that inherit from this, and change the behaviours that are different.

The choice of using inheritance or instead including objects inside objects, to obtain the same behaviour is a matter of more in depth analysis, and it is probably at a python usage level that is much deeper than simple scripting, so for now the scope of this lesson, this is just a way to make you aware. If you are writing a python script that needs this level of complexity, you'll probably know how to consider all the pros and cons of all the options.

That completes the lesson. You should now be ready to move on to some additional topics. [Click here to return to the lesson list](../README.md)
