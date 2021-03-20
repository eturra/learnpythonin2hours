# Lesson 9 - Exceptions and Contexts #

In this lesson we look at Exceptions and Contexts

## Exceptions ##

An `Exception` is … you guessed, an object! It's an object that python uses to deal with situations that are not part of the normal flow of the program.

Most of the exceptions are errors, but in some occasions, they are more like out of band signals for an object to let another object know that something happened, which can't be `return`ed through the normal ways.

We have already seen an example of the latter, when we created our own iterator object for extracting integer 4 bytes at a time from a binary file, with the `StopIteration` exception, remember ?

Exceptions happen in all sort of ways, we've seen how you can get a `KeyError` exception when you try to get a value from a dictionary using a key that doesn't exist:

```python
d = dict()
print(d['a'])
```

Will return an error:

```
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
KeyError: 'a'
```

But you can generate exceptions in so many ways, such as opening a file that doesn't exist, remember ?

```
f = open('/tmp/non-existent', 'r')
```

```
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
FileNotFoundError: [Errno 2] No such file or directory: '/tmp/non-existent'
```

Or when you divide by zero:

```python
print(1/0)
```

```
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
ZeroDivisionError: division by zero
```

## Try and Catch ##

If you don't do anything, when your script or program hits an exception, the program will stop, and a backtrace will be printed.

We've seen this a few times already now, in the previous chapter.

But this is not the way a program should behave! What can we do ? 

This is called "catching" an exception: it's like setting up a trap, called `try`, and if an exception happens inside the trap, we've caught it!


The format of this "trap" is this:

```python
try:
  trapcodeblock
except: exceptionFilter as handyname:
  caughtcodeblock
else:
  elseblock
finally:
  cleanupblock
```

The `try:` part is mandatory, and it needs to be followed by either one or more `except` plus an optional `else` and an optional `finally` or just a `finally`.

The `elseblock` is executed only if the `trapcodeblock` caught no exceptions.

The `finally` is executed regardless of whether an exception occurs in the `trapcodeblock`, and also regardless of whether the `trapcodeblock` or the `caughtcodeblock` hits a return. If any exception remains active, it is paused for letting `cleanupblock` to finish.

The `caughtcodeblock` is executed if the `trapcodeblock` generated an exception that matches the `exceptionFilter`. Unless `caughtcodeblock` uses `raise` to re-activate the exception (or activate a new one), the exception that matched the `exceptionFilter`, called `handyname` inside `caughtcodeblock` will be neutralised, and therefore will be inactive.

Let's try:

```python
try:
  print(1/0)
except ZeroDivisionError as e:
  print('∞')
except Exception as e:
  print ('Uh oh!')
  raise 
else:
  print('Phew')
```

If you change the numbers in the 2nd line from `1/0` to `1/1` or `somenumber`, you'll see different behaviours:


```python
try:
  print(1/1)
except ZeroDivisionError as e:
  print('∞')
except Exception as e:
  print ('Uh oh!')
  raise 
else:
  print('Phew')
```

```python
try:
  print(somenumber)
except ZeroDivisionError as e:
  print('∞')
except Exception as e:
  print ('Uh oh!')
  raise
else:
  print('Phew')
```

You can nest `try` statement for different operations as many times as you feel necessary.

Notice also how we used multiple `except`, and the most generic is at the bottom: the order is important! If you reverse these `except` statements, you will never see `∞` printed.

As we said, exceptions are not necessarily an error:

```python
awesome = True

stuff = iter(range(10))

while awesome:
  try:
    print(next(stuff))
  except StopIteration:
    awesome = False
  except Exception:
    print('Oops!')
    raise
```

Why do we need `iter(range(…` ?

Try without `iter()` and see what happens ?

And how do we know that it's ok, instead, to run `iter()` on it ?

Try `dir(range(10))`, and if you can't spot it, try `'__iter__' in dir(range(10)))` 

## Raise ##

We've seen how `raise` alone just re-activates the exception that is currently dormant, but we've seen also how `raise` can be used to raise an arbitrary exception, such as `raise StopIteration`.

It can also chain exceptions, which is very useful if you are catching a low level exceptions in a higher-level function: imagine you're reading a configuration file, and the file doesn't exist: when you do an `open`, it will raise `FileNotFoundError`, but in the `read_configuration` function, you caught the exception, and you want to raise an exception that is something like `NoConfigurationAvailable` or something, but you want also to carry the reason for that: you want to embed the `FileNotFoundError` into it.

`raise` can do that, with the `from` optional statement, which in this case would look like something like this:

```python
try:
  f = open('/tmp/non-existent', 'r')
except FileNotFoundError as e:
  print("Can't read configuration file /tmp/non-existent")
  raise NoConfigurationAvailable() from e
```

## Context Managers ##

Dealing with exceptions is not that complicated, but it is tedious, as you need to discover all the exceptions you need to catch, and then you need to deal with each one differently, depending on what type of clean-up is needed, and then you need to remember to clean up everything too!

For this reason, python introduced a concept of context manager, and a statement called `with`, that activates these context managers.

A context manager is … an object ! Yes, an object is a context manager if it has the following methods: `__enter__` and `__exit__`.

The `with` statement looks like this:

```python
with expression as handyname:
  codeblock
```

`expression` is any expression that produces a context manager object, and `handyname` is the name to give to the result of the evaluation of `expression` (basically it's the same as `handyname = expression`)

Just after evaluating `expression`, and just before executing `codeblock`, the `with` statement loads the `__enter__` and `__exit__` methods from `handyname`, and keeps them ready to work, so that they are available also in case `handyname` is lost somehow.

Then, but still before executing `codeblock`, `with` will execute the `__enter__` that it loaded.

Then, `codeblock` is executed, and when it finishes, with or without exception, or for any other reason (e.g. a `return`), the `__exit__` that was already loaded, is executed.

This makes remembering to clean up, and dealing with all sort of unexpected ways that the program can flow out of the `codeblock` easy and automatic.

The easiest example of `with` is `open`! If you go back to the lesson about files, you'll notice that there's a `close()` hiding in plain sight, at the end of every exercise. If you use `with`, you don't even need it! You need to get `with` into your muscle memory, because it takes away so many headaches for such a small cost.

See this example from the files lesson:

```python
f = open('/tmp/abcd.txt', 'wt')
for b in range(10):
  f.write(str(b))

f.close()
```

And look at what it looks like if you use `with`:


```python
with open('/tmp/abcd.txt', 'wt') as f:
  for b in range(10):
    f.write(str(b))
```

It is much more elegant, more compact and also safer at the same time: you have no reason for not using `with`!

```

That completes the lesson. You should now be ready to move on to some additional topics. [Click here to return to the lesson list](../README.md)
