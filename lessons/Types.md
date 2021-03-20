# Lesson 4 - Predefined Types #

In this lesson we look at some basic Types and Data Structures.

## Integers ##

`int` stands for *integer*, and it represents integer numbers, negative and positive. Integers are built-in, so they are automatically instantiated. You can explicitly instantiate them, for example, if you want to force the conversion (e.g. truncation)

```python
a = 1
b = 2
c = a / b
print(c)
```

This will produce:

```python
0.5
```

The division generates a number that is not an `int`, but we can force it to be an `int`, and thus discarding the decimal part:

```python
a = 1
b = 2
c = int(a / b)
print(c)
```

Which will print:

```python
0
```

Another reason for instantiating an `int` explicitly is to convert it from text:

```python
a = '3'
b = a + a
print(b)

a = int('3')
b = a + a
print(b)
```

Which of these 2 results is the one you wanted ?

```python
33
6
```

## Floating point ##

The `float` type is similar to an `int`, but it uses what is called *floating point arithmetic*, to represent decimal values. Please keep in mind that floating points numbers are based on base-2 calculations, and so any calculation you do with floating point is rounded to the nearest power of 2, so the precision of the calculation might be surprising. For most of the use-cases, you probably don't care, but if you need a certain level of precision, you might want to look at additional libraries. For example it is generally considered negligent to store currency as float.

Like `int`, a `float` is instantiated automatically, but can be forced with the `float` keyword. Python is usually smart enough to understand that when you divide two `int` types, you'll end up with a `float`. But if you want to convert some text to a float, `float` will do a decent job:

```python
pi = float('3.141529')
r = 3
print('The area of a circle with radius', r, 'is', pi*r**2)
```

```python
The area of a circle with radius 3 is 28.273760999999997
```

If you remember, we have talked about `str.format` in the past, this seems the perfect opportunity to use it:

```python
pi = float('3.141529')
r = 3
print('The area of a circle with radius {0} is {1:.6f}'.format(r, pi*r**2))
```

Since we defined `pi` with 6 decimals, it might look like we wanted 6 decimals back

```python
The area of a circle with radius 3 is 28.273761
```

If you want to know more about `str.format`, try the [Documentation](https://docs.python.org/3.8/library/string.html#formatspec) (This links to the 3.8 version)

## Strings ##

The `str` object represents a sequence of characters. In programming, a sequence of characters is called "string" and, in python, it is a basic type. It can be initialised with single, double and what in python is called "triple" quoting.

The `str` object has a few handy methods that can be useful. We will have a look at a few, but the [documentation](https://docs.python.org/3.8/library/stdtypes.html#string-methods) can give you access to the rest:

- `format(`): replace place-holders in the string (identified by curly brackets, or `{` and `}`) with values supplied as parameters. The syntax of the place-holders is a language in itself, and can be found in the [documentation](https://docs.python.org/3.8/library/stdtypes.html#string-methods)
- `replace(old, new, count)`: find each occurrence of `old` and replace it with `new`, up to `count` times, or all of them if `count` is 0 or not specified. The original string is not changed, `replace` returns a modified copy of the source.
- `join(iterable)`: iterate over the "iterable", and join together each element, by interposing the string between each.

 Example:

 ```python
 print(' - '.join(('a', 'b', 'c')))
 ```

 This will produce the following output

 ```python
 'a - b - c'
 ```

- `strip(characters)`: return a copy of the source string, where leading and trailing characters have been removed. If `characters` is not supplied or is None, it will be replaced with white-spaces. This function has 2 siblings called `rstrip` and `lstrip`, which operates only on right and left sides of the string respectively

 Example:

 ```python
 print(' this is text '.strip())
 print('this is text'.strip('t'))
 ```

 will produce:

 ```python
 this is a test
 his is tex
 ```

- `split(sep, maxsplit)`: `split` is the opposite of `join`, and it will split the main string into segments separated by the `sep` separator, up to `maxsplit` times.

 ```python
 print('this is text'.split(' '))
 print('this is text'.split(' ', 1))
 ```

 This will produce:

 ```python
 ['this', 'is', 'text']
 ['this', 'is text']
 ```

 The square brackets seen here is an indication that `split` is not returning a tuple (which would show up with parenthesis, or `(` and `)`), but a list, which is identified by square brackets, and which will be discussed a bit further down here.

- `startswith(prefix, start, end)` / `endswith(prefix, start, end)`: check whether the string starts or ends with the supplied `prefix`. If `start` is specified, it means start from the specified position rather than the beginning, and if `end` is specified, stop looking for a match after the specified position

 Example:

```python
print('The quick brown fox jumps over the lazy dog'.startswith('The'))
print('The quick brown fox jumps over the lazy dog'.startswith('quick', 4))
print('The quick brown fox jumps over the lazy dog'.endswith('dog'))
```

 This will return:

```python
True
True
True
```

- `encode(encoding)`: convert the string into a `bytes` object using the specified `encoding`, or `utf-8` if not specified. A `bytes` object can be converted back to string with the `decode()` method. When reading from, or writing to, files in binary mode, these methods might be necessary.

Additionally, the `str` object can behave also like a sequence (of characters):

- you can calculate its length with `len`:

```python
print(len('The quick brown fox jumps over the lazy dog'))
```

- You can index the sequence and access the nth element (character): (remember that the index of a sequence is 0 based, so 2 is the 3rd element)

```python
print('The quick brown fox jumps over the lazy dog'[2])
```

- slice: parts of a string can be accessed using a slice, using this format: `str[start:end:step]`. Basically the slice is a list of indexes, using something similar to a `range`.

```python
s = 'The quick brown fox jumps over the lazy dog'
print(s[10:15])
print(s[10:20:2])
```

```python
'brown'
'bonfx'
```

And lastly, the `in` (and its negative form `not in`) operator can be used to check if a string is contained in another:

```python
sentence = 'The quick brown fox jumps over the lazy dog'
print('fox' in sentence)
```

## Lists ##

A `list` is an ordered sequence of objects that are indexed by their position (which is 0 based).

This might look just the same as a `tuple` which we saw in the Flow Control lesson previously, but the main differences are that the `list` is variable length, and it is possible to assign new values to any of its indexes.

Both `tuple`s and a `list`s are iterable, so it is possible to instantiate one from the other, and this means that if you want to make changes to a tuple you can convert it to a list, make the changes and convert it back.

```python
t = tuple(range(10))
l = list(t)

l[0] = l[3]
print(l)
t[0] = t[3]
print(t)
```

As you can see, it is possible to change the list, but not the tuple:

```python
[3, 1, 2, 3, 4, 5, 6, 7, 8, 9]
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: 'tuple' object does not support item assignment
```

```python
l = list()
print(l)
l.append(1)
print(l)
l.extend(range(10))
print(l)
```

This example demonstrates how you can append items to the list, and even extend the list with another list or other iterable

```python
[]
[1]
[1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
```

You can `sort` or `reverse` the list, to re-arrange its items to be sorted.

```python
l = [1, 4, 3, 5, 2, 6, 7, 9, 8, 0]
print(l)
l.sort()
print(l)
l.reverse()
print(l)
```

As you can see, the `sort` and `reverse` functions change the list in place:

```python
[1, 4, 3, 5, 2, 6, 7, 9, 8, 0]
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
[9, 8, 7, 6, 5, 4, 3, 2, 1, 0]
```

You can use the standalone `sorted` and `reversed` objects if you do not want the list to be changed. Keep in mind that `reversed` is a generator that returns an iterator, so you can't just print it. You can iterate it with `for` however. You can use a list as a *stack*, or FIFO, with the `append` and `pop` function:

```python
stack = list()
stack.append('1')
stack.append('2')
stack.append('+')

while stack:
  print(stack.pop())
```

This looks like the beginning of a Polish Notation calculator using a list as a stack:

```python
+
2
1
```

The shortcut for creating a list is to use square brackets (`[`, `]`).

```python
print(type([1,2,3]))
print(type([]))
print(type(list()))
```

They are all lists

```python
<class 'list'>
<class 'list'>
<class 'list'>
```

## Sets ##

A `set` is similar to a list, but sets are not ordered, and they do not allow duplicate items. Additionally, they implement mathematical operations like `union`, `intersection` and `difference`.

```python
s = set((1, 2, 3, 4, 5, 6, 1))
print(s)
```

Duplicates are removed:

```python
{1, 2, 3, 4, 5, 6}
```

```python
s = set(range(10))
ss = set(range(20))
print(ss - s)
print(s - ss)
print(s.difference(ss))
print(ss.difference(s))
print(ss | s)
print(s | ss)
print(ss.union(s))
print(s.union(ss))

print(s & ss)
print(ss & s)
print(s.intersection(ss))
print(ss.intersection(s))
```

As you can see, you can either use the methods by their name, or as an operator:

```python
{10, 11, 12, 13, 14, 15, 16, 17, 18, 19}
set()
set()
{10, 11, 12, 13, 14, 15, 16, 17, 18, 19}

{0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19}
{0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19}
{0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19}
{0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19}

{0, 1, 2, 3, 4, 5, 6, 7, 8, 9}
{0, 1, 2, 3, 4, 5, 6, 7, 8, 9}
{0, 1, 2, 3, 4, 5, 6, 7, 8, 9}
{0, 1, 2, 3, 4, 5, 6, 7, 8, 9}

```

Additionally, you can see that the shortcut to create a set is with curly braces. However you can't use a shortcut to create an empty set, because that is the same as an empty dictionary. Since the dictionary is more common, the set has to be explicitly created empty with `set()`.

The `set` has a bunch of other commands that might be useful, for example to check if one set is contained in the other, and so on. Refer to the documentation if you plan to use a set.

One of the reasons to use a set is its ability to automatically remove duplicates, so you can convert a list to a set and then back to a list (or tuple) to ensure uniqueness of the elements.

Another use case is for the `in` keyword, which is faster to use in a set than a list.

## Dictionaries ##

The dictionary, called map, or associative array in other languages, is similar to a list, but the objects are not ordered. Objects are not accessed by their position, but by an arbitrary key, defined by the user.

Let's use an example to clarify:

```python

d = dict()

d['first'] = 1
d['second'] = 2
d['third'] = 3

for k in d:
  print('{0} translates to {1}'.format(k, d[k]))
```

If the user provided the input as "first", the `d` dictionary would allow the script to map it to `1`, for further use:

```python
first translates to 1
second translates to 2
third translates to 3
```

If you try to access a key that doesn't exist, a `KeyError` exception will be raised. Also, the curly braces are used as a shortcut to initialise a dictionary, and the column is used to separate the key from its value:

```python
d = {
'first':1,
'second':2,
'third':3
}
print(d['thirst'])
```

Will produce an error:

```python
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
KeyError: 'thirst'
```

So, either you check before you access the dictionary, or you "catch" the exception (a topic for another lesson) , or you use `get`:

```python
d = {
'first':1,
'second':2,
'third':3
}
k = 'thirst'
if k in d:
  print(d['thirst'])
else:
  print(k, 'is not a valid key')
```

So, if you are receiving the key from somewhere else, you can make sure you deal with the situation:

```python
thirst is not a valid key
```

Or, more elegantly, use `dict.get`, because it has the following format: `dict.get(key, default)`, so if key exists, it returns the value, if it doesn't exist, it returns `default`, which if not specified, it is None

```python
d = {
'first':1,
'second':2,
'third':3
}
k = 'thirst'
v = d.get(k)
if v is not None: 
  print(v)
else:
  print(k, 'is not a valid key')
```

It is recommended to use `dict.get` rather than indexing the dictionary with the `[]`, because it is much easier to deal with missing key conditions, without having to check first with `in`.

In python, the typical approach is called EAFP, which means "it's easier to ask for forgiveness than permission", so the idea of using the `d[k]` blindly and catching the `KeyError` exception is more "pythonic", but this is a matter of style.

Some people are more comfortable with what python calls LBYL, or "look before you leap", which is the `if k in d:` approach above. For non-complicated scripts, the difference is negligible. For multi threaded programs, it might be safer to use EAFP, but it requires accuracy in identifying all the exceptions.

That completes the lesson. You should now be ready to move on to some additional topics. [Click here to return to the lesson list](../README.md)
