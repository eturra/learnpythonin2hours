# Lesson 5 - Functions and Comprehensions #

In this lesson we look at functions and comprehensions.

## Functions ##

Like in most programming languages, you can also group together statements into a function in python, so that they can be re-used as a new, single statement.

Also like in many other other languages, each function has its own scope in python, both for the validity of the variables, and for the parameters passed from the caller to the function by value.

It is good practice in python to add documentation to each object the programmer creates, and, unlike many other languages, in python functions are objects too, everything is an object. This means that you should try to add documentation to all the functions you write.

The structure of a function definition is as follows:

```python
def functionName(parameters):
 Documentation
 codeblock
```

This is a simplified version of the function, in some versions of python there are additional features such as type-hinting, but we will focus on the basic idea of a function.

`Documentation` is a string object that will be used as the function's documentation, and it is usually a triple-quoted, multi-line string, although it can be a single string.

The `codeblock` is the body of the function, and the indentation is the same for both `Documentation` and `codeblock`.

It is not mandatory for a function to return a value, but it is quite common, and it is usually done with the `return` keyword, followed by the value to be returned.

Let's have a look at a few examples. Let's start with a simple function that takes no parameters:

```python
def five():
  "Produce an integer of value 5"
  return 5
print(five())
print('-'*10)
print(five)
print('-'*10)
print(type(five()))
print('-'*10)
print(type(five))
print('-'*10)
print(five.__doc__)
print('-'*10)
print(five().__doc__)
print('-'*10)
print('__call__' in dir(five))
print('-'*10)
print(five.__call__())
print('-'*10)
print(help(five))
```

The output will be:

```shell
5
----------
<function five at 0x7f5dfdeaf310>
----------
<class 'int'>
----------
<class 'function'>
----------
Produce an integer of value 5
----------
int([x]) -> integer
int(x, base=10) -> integer

Convert a number or string to an integer, or return 0 if no arguments
are given.  If x is a number, return x.__int__().  For floating point
numbers, this truncates towards zero.

If x is not a number or if base is given, then x must be a string,
bytes, or bytearray instance representing an integer literal in the
given base.  The literal can be preceded by '+' or '-' and be surrounded
by whitespace.  The base defaults to 10.  Valid bases are 0 and 2-36.
Base 0 means to interpret the base from the string as an integer literal.
>>> int('0b100', base=0)
4
----------
True
----------
5
----------
Help on function five in module __main__:

five()
    Produce an integer of value 5
```

There are a few observations to make here:

- The function is an object when you use it without parenthesis (`(` and `)`). When used with parenthesis, it is considered a **call**, and it behaves as the value returned by the function.
- A function object has nothing special, it is a **callable** object if it has a `__call__` method, and when you make a call to a function, you just call its `__call__` method.
- The documentation of a function is available under the `__doc__` attribute, or via the `help` standalone function

The function can receive one or more parameters, which are passed by value:

```python

def double(value):
  """
   Double the value
  """
  value += value
  return value
A = 2
double(A)
print(A)
A = double(A)
print(A)
```

The result is the following:

```shell
4
2
4
```

As you can see, `double` tried to change its value, but it was a copy that was available only inside the scope of the function, so the "external" `A`, in the caller's scope, was not changed. The only way to change the value is to return it. If you want to return more than one value, you can use a `tuple`, or a `list`, or a `set`, or any other iterable.

```python

def double(value):
  """
  Return two times the supplied value
  """
  return value, value
A = 'message'

B = double(A)
print(type(B))
print(B)
B, C = double(A)
print(B)
print(C)
B, _ = double(A)
```

This will produce the following output:

```shell
<class 'tuple'>
('message', 'message')
message
message
```

What you can see here is that even if the function didn't explicitly create a `tuple`, the multiple values passed to `return` are wrapped into one, and you can either receive the `tuple` in a variable, on the caller side, or split out the values in variables too.

If you do not need one of the variables, you can use the `_` as the name of the variable that you want to discard.

Functions can have multiple parameters, and some of them can be optional, by having default values:

```python
def increase(number, increment=1):
  """
  Return 'number' increased by 'increment', or by 1 if not specified
  """
  return number + increment

print(increase(1))
print(increase(1, 2))
```

This will produce:

```shell
2
3
```

You need to be very careful with the way you specify the default values, because the `def` command is the one that defines the default values, and this means they are defined only once, at the beginning of the program.

Imagine you want to create an "append" function that returns a list with a value appended to it, and, optionally, also extended by a supplied list.

```python
def append(obj, objects, extra=[]):
   """
   Return 'objects' with 'obj' appended to it
   If 'extra' is supplied, extend 'objects' to contain also 'extra'
   """
   extra.append(obj)
   objects.extend(extra)
   return objects
l = [1,2,3]
print(append(4, l))
print(append(5, l))
print(append(6, l))
```

This will produce an unexpected result!

```shell
[1, 2, 3, 4]
[1, 2, 3, 4, 4, 5]
[1, 2, 3, 4, 4, 5, 4, 5, 6]
```

What is happening here is that the optional value for `extra` is a new, empty list **only** when the `def` is executed, and not every time the function is called, so the `extra` accumulates the values over time, producing a result that was not expected! In the first call, `extra` only contains _4_ when it is added, but on the next call, it contain the _4_ from the first call and now contains _5_ as well. Same thing happens on the final call, where `extra` now contains _4, 5 and 6_.

How can we deal with this type of situation?  You could first do `objects.append(obj)`, and then `objects.extend(extra)`, and avoid changing `extra`, and thus avoiding the issue.

This is correct, but this is a bit of a forced example, to demonstrate the issue: what if you can't avoid changing `extra` because that is the logic of the function ?

It's better to use immutable values, or in other words, values that can't change, as default values for a function, and a list (the `[]`) is mutable.

In our example, avoid defining `extra` as `[]`, and instead use a value such as `None`. Then, check for it in the logic of the function and act accordingly.

```python
def append(obj, objects, extra=None):
   """
   Return 'objects' with 'obj' appended to it
   If 'extra' is supplied, extend 'objects' to contain also 'extra'
   """
   objects.append(obj)
   if extra is not None:
     objects.extend(extra)
   return objects
```

This is the right approach, because the value for `extra` is defined once when `def` is run, but it can't change, and the function's behaviour is well defined. Run the following code once again to prove it:

```python
l = [1,2,3]
print(append(4, l))
print(append(5, l))
print(append(6, l))
```

This will now produce the expected result!

```shell
[1, 2, 3, 4]
[1, 2, 3, 4, 5]
[1, 2, 3, 4, 4, 5, 6]
```

When you are using multiple parameters, especially if there are multiple optional ones, you might want to pass parameters by name, rather than by position. For example, imagine you want a function to print, but you want to be able to specify a prefix, a suffix, and an indentation level: it might be something like this:

```python
def printout(text, prefix=None, suffix=None, indentation=0):
  """
  print `text` preceded by prefix, if specified,
  followed by suffix, if specified,
  and indented by `indentation` spaces
  """
  print(' ' * indentation, end='')
  if prefix is not None:
    print(prefix, end='')
  print(text, end='')
  if suffix is not None:
    print(suffix, end='')
  print() 
```

With this function, if you want to print some text with no suffix or prefix, but with an indentation of 5, you'd have to do something like this: `printout('hello', '', '', 3)`: that's not convenient! Can you simply skip over the unused arguments? Yes you can. Instead of the previous command, you can do this, using a combination of _named_ and _positional_ arguments: `printout('hello', indentation=3)`. You can also just use named arguments: `printout(indentation=3, text='hello')`, but you can't have positional arguments **after** named ones.

```python
printout(indentation=3, 'hello')
  File "<stdin>", line 1
    printout(indentation=3, 'hello')
                                   ^
SyntaxError: positional argument follows keyword argument
```

Additionally, you can receive positional and named (or keyword) arguments without defining all of them in the function, which is handy for more complicated functions. For example, `print` can receive any number of parameters, but our `printout` function requires the message to be all merged together into `text`.

How can we handle such a situation in our `printout` function? You can use dynamic positional and keyword arguments with `*positional` and `**keyword` arguments, which can handle multiple undefined arguments, like this:

```python
def printout(*args, **kwargs):
  """
  print `text` preceded by prefix, if specified,
  followed by suffix, if specified,
  and indented by `indentation` spaces
  """
  indentation = kwargs.get('indentation', 0)
  prefix = kwargs.get('prefix')
  suffix = kwargs.get('suffix')
  text = kwargs.get('text')
  output = list()
  if text is not None:
    output.insert(0, text)
  if args:
    output.extend(args)
  print(' ' * indentation, end='')
  if prefix is not None:
    print(prefix, end='')
  print(output, end='')
  if suffix is not None:
    print(suffix, end='')
  print() 
printout(1)
printout(text=1)
printout(1, indentation=9)
printout(1,2,3,4,5)
printout(1,2,3,4,5, indentation=5)
```

Try it out!

```shell
[1]
[1]
         [1]
[1, 2, 3, 4, 5]
     [1, 2, 3, 4, 5]
```

You will notice one kind of major issue: it doesn't behave like print! If you run `print(1,2,3,4,5)` you get something like the following:

```shell
1 2 3 4 5
```

So why is the output from `printout` a comma seperated list and `print` is not? This is because when we get to the printing of `output`, it is a list, and `print` thinks we want to print that list, rather than a bunch of objects represented by the elements of that list.

The feature of packing parameters into variables, which we used here for `printout`, with one star (`*`) for a tuple, and two stars (`**`) for a dictionary, works also for unpacking!

Simply change `print(output, end='')` to be `print(*output, end='')`:

```python
def printout(*args, **kwargs):
  """
  print `text` preceded by prefix, if specified,
  followed by suffix, if specified,
  and indented by `indentation` spaces
  """
  indentation = kwargs.get('indentation', 0)
  prefix = kwargs.get('prefix')
  suffix = kwargs.get('suffix')
  text = kwargs.get('text')
  output = list()
  if text is not None:
    output.insert(0, text)
  if args:
    output.extend(args)
  print(' ' * indentation, end='')
  if prefix is not None:
    print(prefix, end='')
  print(*output, end='')
  if suffix is not None:
    print(suffix, end='')
  print() 
printout(1)
printout(text=1)
printout(1, indentation=9)
printout(1,2,3,4,5)
printout(1,2,3,4,5, indentation=5)
```

Now we get the desired result!

```shell
1
1
         1
1 2 3 4 5
     1 2 3 4 5
```

This is because the "unpack" operator (the `*`) converts an iterable into a bunch of positional parameters, which `print` is happy to receive. This works also with double stars and dictionaries to obtain positional parameters. Let's say we want to print a bunch of things, but we want them to have all the same style. We could repeat the same command over and over, or we could define a style as a dictionary, and then unpack it:

```python
style = {
  'prefix': '>>>',
  'suffix': '<<<',
  'indentation': 8
}

printout(1, **style)
printout(1,2,3,4, **style)
```

And we get a consistent styling, with the unpacking of the `style` dictionary, as expected:

```shell
        >>>1<<<
        >>>1 2 3 4<<<
```

We're almost finished with functions, but there is one last topic - **generators**. We discussed about generators, when we talked about `range`: how can one create a generator like `range`? The key is to use `yield` instead of `return`.

Let's try to define our `range` function. It's ok if we don't get the exact behaviour, since that would require a few checks on the combination of keywords and positional parameters, and we haven't talked about exceptions yet.

```python
def r(*args, **kwargs):
  start = kwargs.get('start')
  stop = kwargs.get('stop')
  step = kwargs.get('step')
  if len(args) == 1:
    stop = args[0]
  elif len(args) == 2:
    start = args[0]
    stop = args[1]
  else:
    start = args[0]
    stop = args[1]
    step = args[2]
  if start is None:
    start = 0
  if step is None:
    step = 1
  i = start
  while i < stop:
    yield i
    i += step
```

Try it out! Is it the same as `range`? To understand how it works, ignore the first part about the parameters, and focus on the last part:

```python
  i = start
  while i < stop:
    yield i
    i += step
```

Run the following example:

```python
a=r(5)
list(a)
```

You should see:

```shell
[0, 1, 2, 3, 4]
```

Try the following example:

```python
a=r(5,30,5)
list(a)
```

You should see:

```shell
[5, 10, 15, 20, 25]
```

As you can see, we are looping until we reach the `stop` value, and for every cycle, we `yield` the value. If we had `return` there, the function would stop after the first cycle, while `yield` returns a value, and then waits for the iterator to call `__next__` again, to repeat the next cycle.

What do we get as return value when we call `r`?

```python
print(type(r(3,10,3))
print('__next__' in dir(r(3,10,3)))
```

This will produce:

```shell
<class 'generator'>
True
```

So, what `yield` does is create a generator object that the function returns, and the `__next__` method of this object points to the cycle of the loop inside which the `yield` was called, and once the loop terminates, a `StopIteration` exception will be automatically generated for you.

```python
def fibonacci(maxiteration=10):
  a = 0
  f = 1
  for _ in range(maxiteration):
    yield a
    a, f = f, f + a
```

Now try the following:

```python
f = fibonacci(10)
list(f)
```

This should display the following:

```shell
[0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
```

So a `yield` doesn't return all the values in one go, but one at a time. So you do not need to store all of the values. If we had to write the _fibonacci_ code without a `yield`, it would mean doing something like an `append` after every calculation, which is much less efficient. In general, a generator is always a much better idea in python.

## Lambdas ##

Functions are objects, just like everything in python, and this means that they can be used via variables.

The `def` statement is actually an assignment, creating a variable with the name of the function, pointing to a callable object that contains the body of the function. This means that you can pass functions to functions, and return them too!

Look at this, as an example:

```python
def test(func, val):
   """
   test a function with a value
   """
   print('{0}({1}) = '.format(func.__name__, val), end='')
   print(func(val))
test(sum, (1,2))
test(max, (1,2))
test(min, (1,2))
```

As you can see, we're able to pass a function to another function, and it all works:

```shell
sum((1, 2)) = 3
max((1, 2)) = 2
min((1, 2)) = 1
```

There are some functionalities in python where you need a function, but you might not want to keep it, as their use is limited to a single place. Examples are `filter`, `map`, `sorted`, and many more.

Let's have a look at `filter` to explain this better. `filter` receives 2 parameters: an iterable, and a function, which can be _None_. What `filter` does is iterate all the elements in `iterable`, and return only those that evaluate to True (if `function` is None, or `function(item)` otherwise).

`filter` actually returns an iterator. Some time ago we tried to sum up all the numbers that are a multiple of m up to n, and what we did was use `sum(range(m, n + 1, m))`. But then we tried to do this without using the `step` in range to see how we could use `continue`. This is a perfect time to try again, but this time with a `filter`:

```python
n = 12
m = 3

def isMult(x):
  """
  return true if x is a multiple of m
  """
  return x % m == 0

print(sum(filter(isMult, range(n + 1))))
```

This will print `30` as the previous examples (3 + 6 + 9 + 12). But, as we were saying, it looks like a waste to define `isMult` just for the filter since we are only using it once and then not using it again! Is there a way to avoid that?

Yes, with what is called `lambda`! `lambda` in python is a statement to declare an anonymous function, so it is similar to `def`, but more simplified. The format of a `lambda` statement is: `lambda parameters: returnexpression`.  All in one line.

This is equivalent to:

```python
def <lambda>(parameters:
  return returnexpression
```

Let's see an example: the multiples example from before:

```python
n = 12
m = 3

print(sum(filter(lambda x: x % m == 0, range(n + 1))))
```

This returns `30` too, and this is specifically the type of use-case for `lambda`!

## Comprehensions ##

One last topic for this lesson is **comprehensions**. In python there is the tendency to try to do everything iteratively, and it is used so frequently, that python decided to dedicate a special construct for it, called comprehension.

Let's look at a typical example where you have a sequence of elements, and you want to produce another sequence where each element is doubled. Your first approach might be a `for` loop:

```python
firstinput = (1,2,3,4,5,6,7,8)
secondinput = ('a', 'b', 'c', 'd', 'e')

output = list()
for x in firstinput:
  output.append(x + x)

print(firstinput)
print(output)
output.clear()

for x in secondinput:
  output.append(x + x)

print(secondinput)
print(output)
```

This works, and it produces this output:

```shell
(1, 2, 3, 4, 5, 6, 7, 8)
[2, 4, 6, 8, 10, 12, 14, 16]
('a', 'b', 'c', 'd', 'e')
['aa', 'bb', 'cc', 'dd', 'ee']
```

But let's see what it looks like with a `list comprehension` which can be used to define and create lists based on existing lists. It can also use an expression, e.g. `expression for item in list`, as shown below.

```python
firstinput = (1,2,3,4,5,6,7,8)
secondinput = ('a', 'b', 'c', 'd', 'e')

print(firstinput)
print([x + x for x in firstinput])
print(secondinput)
print([x + x for x in secondinput])
```

And the result is the same! An expression `x + x` is run against every items in the lists `firstinput` and `secondinput`.

So, when should you use a `for`, and when a `comprehension`?

It depends™: if the logic of the operation to be applied is simple, and you want to retain the resulting list, a comprehension is to be preferred. If, on the other hand, the logic is complex, and you might end up needing flow control (e.g. `continue` or `break`, or calling of other functions depending on certain conditions, and so on, you'll be better off with a `for`

Comprehension can be conditional, so you can replace `filter` and also `map` with comprehensions. For example, our "sum of multiples" example could be rewritten as follows:

```python
n = 12
m = 3

print(sum([x for x in range(n + 1) if x % m == 0]))
```

This produces `30` as well, and it is showcasing the `if` component of the comprehension too.

Comprehensions can also be nested! For example, if you want to calculate a Cartesian product of 2 iterables, you could do something like this. Note how we are also using a `comprehension` to generate the input lists too, and we use `chr` and `ord` to convert numbers to letters:

```python
letters = [chr(ord('A')+x) for x in range(3)]
numbers = [str(x) for x in range(3)]
print([l + n for l in letters for n in numbers ])
```

And here is the Cartesian product, obtained by nesting the 2 comprehensions:

```shell
['A0', 'A1', 'A2', 'B0', 'B1', 'B2', 'C0', 'C1', 'C2']
```

If the comprehension is done with square brackets, it is called `list comprehension`, if it is with curly braces, it is a `set` unless the values are actually keys colon (`:`) values, in which case it will be a `dictionary comprehension`. If the parenthesis are used to delimit a comprehension (`(` and `)`), it is the same as a list comprehension, but via a generator.

Let's see some examples. This is a list comprehension:

```python
lc = [x for x in range(10)]
print(type(lc))
print(lc)
```

Set comprehension:

```python
sc = {x for x in range(10)}
print(type(sc))
print(sc)
```

Dict comprehension:

```python
dc = {'key' + str(x):x for x in range(10)}
print(type(dc))
print(dc)
```

And a generator-list-comprehension:

```python
glc = (x for x in range(10))
print(type(glc))
print(list(glc))
```

Converting a generator to a list is a waste of time, but we are doing it here just to show what it contains. Typically, you'd use a generator-list-comprehension if you need to make sure that you don't need to wait for the whole comprehension to complete before processing its elements, so typically it would be passed to some other code that will deal with an iterator.

That completes the lesson. You should now be ready to move on to some additional topics. [Click here to return to the lesson list](../README.md)
