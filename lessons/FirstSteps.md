# Lesson 1 - First Steps #

In this lesson we discover python and try a few things to get familiar with the environment.

## Starting python ##

Python is an interpreted language, and this means that there is no preparation needed to run the code that you write.

This means you can start the interpreter and type commands, and get the response back without actually writing any file, which is great for learning and for exploring new features.

There are several ways to do this, some of which offer a lot of extra features that make it easier to inspect more complicated objects, such as `ipython` or jupyter. Feel free to use them if you like, but the results should be similar to using just `python`.

Because of the python 2 to python 3 transition, in some systems you might not be able to just run `python`, but you might need to run specifically `python3` or even `python3.9`. In this guide we will use the command `python`, but you might need to adjust to match your own system, just make sure that you have a version of python that is above 3.5.

## Version ##

So, your first task is to find out what version of python you have on your system:

```shell
python --version
```

gives this result:

```shell
bash: python: command not found
```

Well, it looks like on this system, python is not installed ?

Actually, it's installed as python3 to avoid confusion over python2.

```shell
python3 --version
```

gives us this result:

```shell
Python 3.9.2
```

3.9.2 is quite recent, but don't worry, if you have an older version of 3.x, you should be fine.

## First steps ##

Now, start python and see what it looks like:

```shell
% python3
Python 3.9.2 (default, Feb 28 2021, 17:03:44)
[GCC 10.2.1 20210110] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>>
```

The `>>>` is the command prompt, it is waiting for you to type a command.

Let's try some commands!

```python
>>>1+1
2
```

Clearly, python can do math, can it work with strings ?

```python
>>> 'hello' + "world"
'helloworld'
>>>
```

Yes, and you can use either type of quoting: single, or double. This means that you can do something like this:

```python
>>> "You can't have single quotes inside single quotes"
"You can't have single quotes inside single quotes"
>>> 'You can have single quotes inside ""'
'You can have single quotes inside ""'
>>>
```

You can try placing a single quote inside a single quote, rather than double quotes, in the examples above. To print single quote inside single quotes, you can _escape_ it. The usual escape sequences can be used too, in both single or double quotes:

```python
>>> 'can\'t escape'
"can't escape"
```

So, when should you use single and when double ? It is mostly a matter of style and convention.

You can also have triple quotes and triple double-quotes !

```python
>>> '''
... this
... is
... a
... multi
... line
... string
... '''
'\nthis\nis\na\nmulti\nline\nstring\n'
>>>
```

Triple quotes are used to embed documents.

Python used like this, in interactive mode, prints the result of each operation back to you for inspection, but in a script, this is not happening, or it would become confusing.

If you want to print something on the screen, you can use the `print` built-in function. There is a bit of controversy around it, in particular because it changed drastically between version 2 and 3. In general, you should use it only in learning exercises, and not in scripts that you will use "in production". This is again mostly a matter of style, but it is much better if you use something like `sys.stdout` or the `logging` module.

Anyway, for learning, `print` is good enough. The main difference between letting the interpreter show the results, and using print is that the former typically shows you a representation of the object, while the latter displays it as it is intended to be seen: if we use the same multi-line string from above, it will be clear:

```python
>>> '\nthis\nis\na\nmulti\nline\nstring\n'
'\nthis\nis\na\nmulti\nline\nstring\n'
>>> print('\nthis\nis\na\nmulti\nline\nstring\n')

this
is
a
multi
line
string

>>>
```

In python, you can also have variables:

```python
>>> side = 3
>>> area = side * side
>>> print('The area of a square with size', side, 'is', area )
The area of a square with size 3 is 9
```

There is also a way to do a real square, represented by `**`:

```python
>>> side = 3
>>> area = side ** 2
>>> print('The area of a square with size', side, 'is', area )
The area of a square with size 3 is 9
```

## Syntax ##

Python tends to be more legible than other languages because its syntax avoids structuring the code in curly brackets (`{` and `}`) and similar constructs, but that comes at a cost. Python is quite specific about its syntax: it requires strict indentation. What this means is that all the code that belongs to the same scope needs to be indented at the same level. You can do this with either a tab, or a space, or a bunch of spaces, but whatever you chose needs to be consistent.

We will use `while True:` here as an example, but don't worry, we will revisit it a bit later to go more in details on how it works.

For now you just need to know that `while True:` repeats forever the code that is "inside". The important part here is: how do we define what is "inside" and what is "outside" ?

Now imagine you want to annoy someone, and you want to keep saying "hello!" forever. Let's try that in our interactive interpreter:

```python
>>> while True:
... print "hello"
  File "<stdin>", line 2
    print("Hello")
    ^
IndentationError: expected an indented block
>>>
```

As you can see, the interpreter already told you that it was expecting some additional input, because the prompt changed from `>>>` to `...` after the colon (`:`). This is because the colon is the most common way to start a new scope, and so the interpreter knows that it expects an indentation. The error message also is quite clear: it expected an indented block.

So, try it again, but this time, put a `tab` before the `print`, and then press enter twice (the 2nd to signal you're done with the indentation)

If you don't know how to break out of this infinite loop, try `control-c`

```python
>>> while True:
...     print("Hello")
...
Hello
Hello
Hello
Hello
^CTraceback (most recent call last):
  File "<stdin>", line 2, in <module>
KeyboardInterrupt
Hello
```

That worked! Now, can we use a single space, instead ?

```python
>>> while True:
...  print("Hello")
...
Hello
Hello
Hello
Hello
^CTraceback (most recent call last):
  File "<stdin>", line 2, in <module>
KeyboardInterrupt
Hello
```

What about 2 spaces ? And 3 sapces ? And … 7 ? Try them all!

Can you mix them? In other words, can you use a single space for the first level of nesting, and then a tab for the 2nd, and 3 spaces for the 3rd, and so on ?

```python
>>> while True:
...  print("Hello")
...  while True:
...     print("More Hello")
...
Hello
More Hello
More Hello
More Hello
More Hello
^CTraceback (most recent call last):
  File "<stdin>", line 2, in <module>
KeyboardInterrupt
Hello
```

Although this works, it is a __Very Bad Idea™__, because you will have to live by this in your whole script. This means that if you one day decide to add a new line to your script, you need to remember and repeat exactly the sequence of indentations. For this reason, nearly every group of developers with more than 1 member will demand and impose a certain coding guideline which will specify **one** type of indentation, be it 1 tab, 2 spaces, 3 spaces, or any other number, as long as it is consistently used across the project.

Python has its own guideline, which is called [PEP8](https://www.python.org/dev/peps/pep-0008/). This doesn't mean that any other style guideline is wrong, you just need to adhere to whatever guideline chosen by the project to which you're contributing.

These guidelines often include specifications about having 1 space on either side of an assignment (`=`) and any other operator (e.g. `+`, `-`, `*`, `**`) and so on, only 1 space after a comma (`,`), and no spaces between any type of braces and their content.

There are several reasons for these, but at the end, it's all a matter of style, what is strictly required is that the code is indented in the same way for the blocks that are intended to be part of the same scope.

This might seem a trivial point, but for complicated and nested code, mistaking deleting some indentation will have catastrophic effects, and recovering from these mistakes might be a colossal endeavour.

That completes the lesson. You should now be ready to move on to some additional topics. [Click here to return to the lesson list](../README.md)
