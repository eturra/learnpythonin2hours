# Lesson 7 - Modules #

In this lesson we look at modules

## Why modules ? ##

A module is a way for a python programmer to re-use functionalities without having to add them to the script every time.

Python is famous for having a philosophy of "batteries included", which means that, unlike many other languages, python comes with everything you might need. But these additional features are not available to your script by default. They are stored in separate modules, so if you want to take advantage of them, you need to learn how to use these and other modules.

We will look at the so called "Standard Library" in the next few lessons, here we will focus on the basics of using modules.

## Creating a Module ##

Let's start with an example of a new module, and then we look at how we use it. Remember the `circle` class we created in the last lesson? If you don't, here it is:

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
    "Formast pi to look nice"
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

Now, let's say this is a very useful class for a bunch of projects you plan to create. Therefore you wouldn't want to copy this code into every project you write, because it's a waste of space. More importantly, if there's a change required, you'd have to go and edit every project. Although there are handy tools like `git` that make this easier, it is still a waste of resources when you can easily create a module.

Let's just do that!

Create a file in your working directory (let's say you work in `/tmp`, for example), for example `/tmp/geometry.py`, and place the `circle` class from above into it.

Let's say we call the file "geometry", rather than "circle", because we plan later to add other classes, such as `square`, `rectangle`, and so on. That is an interesting exercise for the reader!

That's it! You've created a module!

Often, you will find that the module contains some code at the end, that looks like this:

```python
if __name__ == "__main__":
  somestuff
```

What this does is it checks whether the name of the module is `geometry` or `__main__`, or anything else, and if it is `__main__`, run some code.

What you can run there could be tests, to check if the module works, or a demo, to show how to use the objects, or anything else. But when the module is used somewhere else, the module's name will not be `__main__`, and that part of the code will not be active.

## Importing ##

What good is it to create a module, if you can't use it ? And how does one use it ?

Using a module, in python terminology, is called "importing" it. There are many different ways to do this, we will focus on the `import` built-in command, because it's the most commonly used and simplest way to achieve this.

So, let's try! Create a new file in the working directory, it doesn't matter where this is, as long as it is in the same directory as `geometry.py`, so in our case it will be `/tmp/`. Chose any name you like, and put the following as its content:

```python
import geometry

c = circle()
```

You will get something like this:

```shell
Traceback (most recent call last):
  File "test.py", line 2, in <module>
NameError: name 'circle' is not defined
```

What happened ? Where is the `circle` class ? Why is it not defined ?

This is a desired behaviour: you don't want circle to re-define something you are using in your scripts, such as `int`, with a funny addition, and mess up your script: so when you import a module, its content goes into a namespace object called … module, that has the same name as the module you imported.

Go to the same working directory, and run python interactively, and try this:

```python
import geometry
type(geometry)
dir(geometry)
```

This will be the output:

```shell
<class 'module'>
['__builtins__', '__cached__', '__doc__', '__file__', '__loader__', '__name__', '__package__', '__spec__', 'circle']
```

So, as you can see, `import geometry` created a new object, called `geometry`, which is an instance of the class `module`, and this `geometry` object contains `circle`.

This might be confusing, but it's quite simple to show you what it means: you need to prepend the name of the module to the objects from the module that you want to use.

So, let's try again:

```python
import geometry

c = geometry.circle()
print(c)
```

This will produce the expected result:

```shell
circle with radius: 1.000000, diameter(d:.6f) area: 3.141593, perimeter: 6.283186
```

It is a good idea to leave things as they are, to avoid namespace clashes, but if you feel annoyed at having to type `geometry.` in front of everything, there are a few things you can do:

1. You can take advantage of the fact that in python, everything is an object, and therefore, everything can be assigned to a variable

 ```python
 import geometry

 circle = geometry.circle
 c = circle()
 print(c)
 ```

1. Ask `import` to explicitly merge some of the objects of the module into the main namespace, using `from`

 ```python
 from geometry import circle
 c = circle()
 print(c)
 ```

Which one you use is, again, a matter of style. Many will suggest to just type `circle.` and avoid the namespace clash potential, but if you are writing a small script, you can reasonably feel in total control of any possible conflict, and therefore consider the risk of a clash to be negligible.

The `from` has also the ability to import `*` from a module, so that everything in the module is now merged in the current namespace. The same caveats we discussed apply, so try to avoid it if you can.

`import` allows you also to rename a module, if you want, for example, if there's a module called `vmware.vsi`, which is a bit annoying to use, you can rename it to `vsi` if you do `import vmware.vsi as vsi`.

## Search Path ##

Where does python go to find `geometry` when we say `import geometry`?

It will go and look in its search path, which is defined by a few different components, such as the `PYTHONPATH` environment variable, the directory where the main python script is located, and the system installation dependent defaults.

In our example above, we've used the second, and the first (`PYTHONPATH`) is not frequently used. The system default is typically pre-configured with your installation of python.

So, how can one re-use modules? We will see later how something called "Virtual Environment" helps with this, but in general, you can just modify the path, or place the modules somewhere that is already in the current path.

Among the pre-defined modules that come with python (the "batteries included" part), there is a module called `sys`, which contains a lot of system related objects, and one of them is called `path`.

Try a script like this:

```python
import sys
print('\n'.join(sys.path))
```

It will give you an output that might look like this:

```shell
/usr/lib/python39.zip
/usr/lib/python3.9
/usr/lib/python3.9/lib-dynload
/usr/local/lib/python3.9/dist-packages
/usr/lib/python3/dist-packages
/usr/lib/python3.9/dist-packages
```

If you want, you can even use `sys.path.append(somePath)` to add some additional path to be used in your script.

## Packages ##

If you have a collection of modules that all serve a common purpose, you can group them together in what is called a "Package".

A Package is just a directory somewhere in the search path, that contains a file called `__init__.py`, which can be empty, and then the modules (or other packages) that you want to group together.

Remember our `geometry` module? Rename it to `circle.py`, create a directory called `geometry`, move `circle.py` inside it, together with an empty `__init__.py`.

```shell
mkdir geometry
mv geometry.py geometry/circle.py
touch geometry/__init__.py
```

And now try:

```python
import geometry.circle

c = geometry.circle.circle()
print(c)
```

The main purpose of Packages is to allow an easier distribution of modules that belong to the same library, without risking of clashing with other projects.

For example, there could be a graphical library that has a `circle` module, to draw circles. If each library declared the module outside of its own package, we would have a conflict, and we wouldn't be able to use these 2 modules together when they clearly seem related.

Using the package system helps prevent this type of conflict between entities that can't coordinate the naming of modules.

## Standard Library ##

The standard library in python comes with a very large number of modules, ready to use. We won't look at them here, we just mention that they are documented [here](https://docs.python.org/3/library/).

You will need to get familiar with the method for finding which module contains what you need.

For example, consider the following:

We have already mentioned `sys` when we talked about `sys.path`. It is documented [here](https://docs.python.org/3/library/sys.html), and it offers access to the system where the script is running. This includes accessing standard file descriptors such as `sys.stdin`, `sys.stdout` and `sys.stderr`, but also `sys.argv` to get the command line parameters, `sys.platform`, to understand whether we are running in `linux`, `win32`, `darwin`, or respectively Linux, Windows, or MacOs, or even `sys.byteorder`, to know if the current cpu is big or little endian.

The `os` module, documented [here](https://docs.python.org/3/library/os.html), abstracts Operating System functions such as looking at the environment variables (`os.environ`), or using file paths (`os.path`) without specifically having to know whether the file path separator is `/` or `\`.

This latter feature is quite important: you should not build your paths using directly `/`, you should use `os.path.sep`, and `os.path.join` and all the other objects defined in `os`, to make sure your script will work on as many operating systems as possible without effort from your side.

The `time` module has a few objects you can use to convert timestamps to and from various format, but it also contains the `time.sleep` function, which is handy if you need to make your script wait for some time.

The `datetime` module is handy for dealing with timestamps too, and performing conversions and other date-time arithmetic.

We will look at some of the modules more in depth in the next few modules:

- re
- argparse
- logging
- subprocess
- json

That completes the lesson. You should now be ready to move on to some additional topics. [Click here to return to the lesson list](../README.md)
