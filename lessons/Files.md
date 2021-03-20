# Lesson 8 - Reading and Writing Files #

In this lesson we look at using python for reading and writing files.

## Opening and closing a file ##

The most common way to open a file is to use the `open` object. The `open` object's constructor expects a few parameters, but only one is mandatory, which is the `filename`. The second most common parameter is the `mode`, which is a string describing how the file should be opened:

- `r` for reading from the file,
- `w` for writing to the file, after truncating it if it already exists
- `a` for writing to the file, but starting just after the end, if it already exists (append)

The mode can be followed by 1 or 2 more characters.

If the first character is either `w` or `r`, they can be followed by be an optional `+`, indicating that the file should be opened for both reading and writing, with the difference that `w+` means also truncate, while `r+` means don't truncate.

The last character of the `mode` can be omitted, or it can be one of the following:

- `t`, or text (this is the default if nothing is specified)
- `b`, or binary.

The optional `encoding` can be used for when reading a binary file that is to be decoded as text (so `t` in the `mode`) using a certain encoding that is not what `locale.getpreferredencoding()` says (typically, that is `utf-8`).

The optional `newline` can be used to perform translations between files from systems with different newlines. The default is typically what you want, and if you are in a situation where you need more, you will be able to find information in the [documentation](https://docs.python.org/3/library/functions.html#open) of `open()`

If there are issues with the procedure of opening the file, an exception will be generated, so it is typically a good idea to use `open` inside a `try`, but we'll talk about exceptions later. For now let's focus on what happens if `open` is successful, i.e. it will return a file-like object.

Just like many other things in python, a file-like object is an object that has methods such as `read`, `write`, and `__iter__`. If you open the file in text mode, the file will be a text file, otherwise it will be a binary file. The main difference is what `read()` will return, and what `write()` will expect.

Once you're done with a file, you need to close it, with the `close()` method. Let's try to open and close a couple of files!

```python
f = open('/tmp/abcd', 'r')
```

This will fail with an exception like the following:

```shell
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
FileNotFoundError: [Errno 2] No such file or directory: '/tmp/abcd'
```

You can't read a file that doesn't exist. But you can write to it! Let's try that next:

```python
f = open('/tmp/abcd', 'w')
f.close()
```

This worked, or at least, it didn't generate any exception, but is the file there ?

```shell
ls -l /tmp/abcd
```

And yes, the file is there. But it is empty (0 bytes in size), because we didn't write anything to it:

```shell
-rw-r--r-- 1 vcoders vcoders 0 Mar 23 16:40 /tmp/abcd
```

OK, now let's now try to read it:

```python
f = open('/tmp/abcd', 'r')
f.close()
```

Now it works!

For more details, the text mode file object returned by open is called `io.TextIOWrapper`, and it is documented [here](https://docs.python.org/3/library/io.html#io.TextIOWrapper), while the file object returned by open in byte mode, the file object is a `io.BufferedWriter`, which is documented [here](https://docs.python.org/3/library/io.html#io.BufferedWriter) for write, and `io.BufferedReader`, documented [here](https://docs.python.org/3/library/io.html#io.BufferedReader) for reading

## Writing to a file ##

It might be a good idea to learn how to write before we learn how to read, so that we end up with a file that we can read. If you opened the file in text mode (`t`), you can use the `write()` method of the file object, and pass a string object to it. Keep in mind that `write()` won't add newlines for you, so if you want them, you need to add them yourself, unlike what `print` does

If you opened the file in binary mode, you can still use the `write()` method, but this time it will expect a bytes-like object. For example, if we wanted to write integers, we need to use their `to_bytes` method to convert them to bytes:

```python
import sys
f = open('/tmp/abcd', 'w+b')
for b in range(10):
  f.write(b.to_bytes(4, sys.byteorder))
f.close()
```

What does the file look like then? Use `hexdump` in the shell to display it:

```shell
% hexdump /tmp/abcd
```

This is what it will show:

```shell
0000000 0000 0000 0001 0000 0002 0000 0003 0000
0000010 0004 0000 0005 0000 0006 0000 0007 0000
0000020 0008 0000 0009 0000
0000028
```

Don't get confused by the "little-endian-ness" of x86 processors, the bytes are ordered so that the most significant byte comes first, so `0001 0000` is actually `0000 0001`, and thus 1. Typically you would be using some way to serialise and de-serialise objects to files, so the `to_bytes` is one way to do it, there are many more, maybe more efficient.

Now, let's try to write a text file then!

```python

f = open('/tmp/abcd.txt', 'wt')
for b in range(10):
  f.write(str(b))
f.close()
```

What does the file look like? Being a text file, we can use `cat` to look at it from the shell:

```shell
% cat /tmp/abcd.txt
```

And the result is the numbers from 0 to 9, one per line:

```shell
0123456789
```

Ooops! We forgot the newline! Change the script to this:

```python

f = open('/tmp/abcd.txt', 'wt')
for b in range(10):
  f.write(str(b) + '\n')

f.close()
```

Let's check the file once more:

```shell
% cat /tmp/abcd.txt
```

And the result is the numbers from 0 to 9, one per line:

```shell
0
1
2
3
4
5
6
7
8
9
```

## Reading from a file ##

Once you've opened a file, how can you read from it ?

There are multiple ways, the most pythonic way is to use a comprehension, taking advantage of the fact that the file object is also an iterable; other ways include calling `read` or `readlines` (for text).

Let's try a few things:

First, let's try a for loop on the text file, reading one line at a time, taking advantage of the iterator:

```python
f = open('/tmp/abcd.txt', 'rt')

for line in f:
  print(line)

f.close()
```

Notice: the output has double new-lines!

```shell
0

1

2

3

4

5

6

7

8

9

```

This is because the file is not removing the newline it reads, but `print` is adding them! We can do many things, we can change the `end` parameter for `print`, to be nothing (`''`), or, we can use `sys.stdout`

Using `sys,stdout` is a bit more flexible, because it allows our code to work well even if we are using python 2, where `print` is different, and it allows us also to decide whether we want to print to `stderr`, without much change, so let's do that!

```python
import sys
f = open('/tmp/abcd.txt', 'rt')

for line in f:
  sys.stdout.write(line)

f.close()
```

And the output is what we expected:

```shell
0
1
2
3
4
5
6
7
8
9
```

Now, let's read from the binary file, instead

```python
import sys
f = open('/tmp/abcd', 'rb')

tmp = None

while tmp != b'':
  tmp = f.read(4)
  if tmp != b'':
    sys.stdout.write(str(int.from_bytes(tmp, sys.byteorder)) + '\n')

f.close()
```

It is a bit convoluted, because we can't use any iterator trick here, so we need to check if the `read` returns an empty value, to indicate that the end no file was reached.

But the result is the one we expected.

```shell
0
1
2
3
4
5
6
7
8
9
```

With the knowledge we have, we can also build an iterator to do what we need:

```python
import sys

class intFileIterator():
  """
  Given a file opened for binary reading, iterate until the file is finished, and return n bytes at a time as integer
  """
  def __init__(self, file, n_bytes=4):
    "Get ready to iterate file n_bytes at a time"
    self.file = file
    self.n_bytes = n_bytes
  def __iter__(self):
    "return self, as an iterator"
    return self
  def __next__(self):
    "return the next n_bytes"
    r = self.file.read(self.n_bytes)
    if r == b'':
      raise StopIteration
    else:
      return int.from_bytes(r, sys.byteorder)

f = open('/tmp/abcd', 'rb')

for i in intFileIterator(f, 4):
  sys.stdout.write(str(i) + '\n')

f.close()

```

Alternatively, we could have used `yield` and a generator:

```python
import sys

def intFileIterator(file, n_bytes=4):
  """
  Given a file opened for binary reading, iterate until the file is finished, and return n bytes at a time as integer
  """
  tmp = None
  while tmp != b'':
    tmp = f.read(n_bytes)
    if tmp != b'':
      yield int.from_bytes(tmp, sys.byteorder)

f = open('/tmp/abcd', 'rb')

for i in intFileIterator(f, 4):
  sys.stdout.write(str(i) + '\n')

f.close()
```

As you can see, it's handy that instantiating a class and calling a function has the same format, so we can swap them around as necessary.

That completes the lesson. You should now be ready to move on to some additional topics. [Click here to return to the lesson list](../README.md)
