# Lesson 3 - Flow Control #

In this lesson we look at some basic forms of flow control. These are quite common across programming languages, but we will cover their basics if you haven't seen them before.

## If ##

The `if` construct allows the programmer to change the behaviour of the script depending on a condition. The format of this construct is:

```python
if condition: 
 codeblock1
elif othercondition:
 codeblock2
else:
 codeblock3
```

The `elsif` piece can be repeated indefinitely or not appear at all.

As it appears above, this will be the behaviour:

1. Evaluate `condition`
1. If true, execute `codeblock1`
1. Otherwise, `othercondition` is evaluated:
1. If true, execute `codeblock2`
1. Otherwise, execute `codeblock3`

As discussed earlier about indentation, the `if`, `elif` and `else` lines need to be vertically aligned with each other, and `condition1`, `condition2`, and `condition3` need to be one level of indentation more to the right.

All the lines that belong to each of these code blocks need to be aligned to each other.

Let's try an example:

```python
A = 1
B = 0
if A > B:
  print(A, 'is bigger than', B)
elif A == B:
  print(A, 'is the same as', B)
else:
  print(A, 'is less than', B)
```

Try changing the values of A and B to confirm the behaviour is always correct. Notice the indentation, and also how the assignment operator (`=`) is different from the equality operator (`==`). There is another operator that might look like an equality operator: `is`. This is called **identity** operator:

```python
A = 1
B = 1

if A == B:
  print('A is equal to B')
if A is B:
  print('A is B')
```

The output is misleading: it makes you believe `is` is the same as `==`:

```python
A is equal to B
A is B
```

But try to change the values:

```python
A = 123456
B = 123456

if A == B:
  print('A is equal to B')
if A is B:
  print('A is B')
```

This will show you the difference:

```python
A is equal to B
```

This is because `is` tries to find out whether the 2 objects are the same, and for smaller values, the interpreter tries to save memory and optimises the 2 objects to be the same, but in general that's not the case for larger numbers.

In general, you use `is` to check if 2 objects are the same object, and the `==` to check if the values of the objects are the same. The most common use for `is` is to check if an object is or is not `None`, which is the null object in Python

```python
A = None
B = 3
if A is None:
 print('A is None')
if B is not None:
 print('B is not None')
```

This will produce the following output

```python
A is None
B is not None
```

This way of using `is` is useful because comparing the value of a `None` object or trying to use its methods will produce an error. On the other hand, using the implicit falsehood of a `None` object is not a reliable way of detecting it:

```python
A = 0
B = None

if A:
 print('A is not None')
if B:
 print('B is not None')
```

As you can see, both `None` and `0` are detected as `False`. This might be what you desire, but it also might not, you need to make an informed decision when you use this implicit formt

## While ##

You can picture the `while` statement to be like a repeating `if` starement. A `while` construct, some times called a "while loop", looks like this:

```python
while condition:
  repeatingblock
else:
  exitingblock
```

The `repeatingblock` will be executed each time the evaluation of `condition` is `True`. The `else:` part is optional and rarely used, but the associated `exitingblock` will be executed once `condition` evaluates to `False`.

Let's see an example. What's the sum of the first 10 integers ?

```python
total = 0
i = 1

while i <= 10:
  total += i

print('The sum of the first 10 integers is', total)
```

Note that you need to leave a blank line between the last statement in the repeating block and the print statement.

Oooops! This never prints the expected result! It seems to be stuck! Why is that ?

Well, if you check the script, the condition for `while` to keep repeating is that `i` has to be `10` or less, which is the case, since `i` is 1.

So the `while` loop is doing what it is told: repeating the same command, of adding `i` (1) to `total`, over and over, but `i` never changes, so the loop will never stop!

You need to be careful to always make sure the block of code inside a while has an exit path, or, in other words, that there's a change that the condition will change to false at some stage.

In this case, what we are missing is: incrementing `i`.

```python
total = 0
i = 1

while i <= 10:
  total += i
  i += 1

print('The sum of the first 10 integers is', total)
```

This finally yields the result we wanted

```python
The sum of the first 10 integers is 55
```

You might want to run the `print` in the `else:` section of the `while` in this example, and it makes sense in this specific example, but it might not make sense in all the cases where you use `while`:

```python
total = 0
i = 1

while i <= 10:
  total += i
  i += 1 
else:
  print('The sum of the first 10 integers is', total)

```

The result is the same, as expected:

```python
The sum of the first 10 integers is 55
```

In this case, when `i` reaches 11, the condition is `False`, and the `else` is executed, but in some other cases, the while might be needed to work to complete a job that was already started, if necessary, so printing the result in the `else` part is not approrpiate.

## For ##

The `for` loop in python is a construct in python that will execute code "for each" of the elements provided.

A `for` loop looks like this:

```python
for variable in iterable:
  iteratingblock
else:
  exitingblock
```

It might look similar to a while, but the main difference is in this `iterable` thing: what is it ?

The simple explanation is that in python an object is said to be iterable if it allows you to read some parts of it, one by one.

The more complete explanation is that, in python, an object is iterable if it has a `__iter__` method, or if it has a method called `__getitem__`. The `__iter__` method returns an object that is called __"iterator"__, and which is expected to have a `__next__` method. In this case, `for` calls the `__iter__` method to get the iterator, and then calls `__next__` on it. For each of these items, the value is assigned to the specified variable, and then runs the code in `iteratingblock`. When the `__next__` reaches the end, the iterator object is expected to raise a `StopIteration` exception to signal that the `for` has to end, and the `else` part of the code, if present, will be executed.

If the iterable has no `__iter__` method, it will try the `__getitem__` method, which allows `for` to try and get items by index (that is, index 0, then 1, and so on) , until an exception of `IndexError` signals the end of the items to iterate over, and the `else` part, if present, will be executed.

Examples of *"iterable"* objects would include:

- ranges
- lists
- tuples
- strings
- dictionary (keys)
- files
- and many more

We will cover most of the above over the following lessons, but for now we can focus on `tuples` for a quick example, and then we'll talk about `ranges` after that.

A `tuple` is a mathematical term to indicate a finite sequence of elements. In python, a tuple is a sequence of pre-defined length of objects, and is created by using the `tuple()` constructor, or just the parenthesis (`(` and `)`).

Before proceeding, you might wonder: how do I know whether a `tuple` is "iterable" ? Well, if it isn't, `for` will complain:

```python
for a in 1:
 print(a)
```

Will give you this exception:

```python
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: 'int' object is not iterable
```

So if a tuple works in a `for`, it must be "iterable"! But how can you check ? You can use the `dir` object in python:

```python
print(dir(tuple))
```

```python
['__add__', '__class__', '__class_getitem__', '__contains__', '__delattr__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__getitem__', '__getnewargs__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__iter__', '__le__', '__len__', '__lt__', '__mul__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__rmul__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', 'count', 'index']
```

Or, if you don't even want to spend the time scanning the output:

```python
'__iter__' in dir(tuple)
```

Which returns:

```python
True
```

And, to confirm what we know about `int`:

```python
'__iter__' in dir(1)
'__iter__' in dir(int)
```

Will return:

```python
False
False
```

Now, let's try to use a tuple to calculate the sum of the first 10 integers using `for`:

```python
total = 0

for i in (1, 2, 3, 4, 5, 6, 7, 8, 9, 10):
  total += i
else:
  print('The sum of the first 10 integers is', total)
```

The result marches the behaviour of the `while` examples:

```python
The sum of the first 10 integers is 55
```

The main advantage here is that we do not to pre-initialise `i`, and we also do not need to increment it (the `i += 1` we needed in the `while`). The down-side is pretty obvious which is that you need to spell out all the integers you want to sum. Also, if you want this to be parametric, or in other words, sum up to the first `n` numbers, this is not doable with a tuple.

But before we move on to the next topic, some of you might want to ask _"But where is the tuple?"_. That's a fair question: in python, the presence of parenthesis with at least a comma inside is a shortcut to creating a tuple, except for function calls and class instantiations:

```python
type((1,))
type(tuple)
type(tuple())
```

All of the 3 above are a tuple:

```python
<class 'tuple'>
<class 'tuple'>
<class 'tuple'>
```

But parenthesis alone are just used for overriding precedence of operators:

```python
type((1))
type((1,))
```

```python
<class 'int'>
<class 'tuple'>
```

So, the comma forces python to see a tuple when there's only 1 element. In general, it is better to create tuples with the `tuple` keyword, to be explicit, the keyword requires an "iterable" object to initialise, and so you end up needing a tuple anyway:

```python
type(tuple(1))
```

This doesn't work:

```python
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: 'int' object is not iterable
```

You need to pass a tuple (or a list, or anything that is "iterable") to the `tuple()` constructor:

```python
type(tuple((1,)))
```

```python
<class 'tuple'>
```

So, you might as well just use the parenthesis and forget about the `tuple`.

### Range ###

A `range` is what python calls a "generator", and it it "iterable". A generator is an object that produces a sequence of values, but one by one, and not all at the same time.

A `range` object *generates* values from a range, defined by 3 parameters `start` (default 0), `stop`, and `step` (default 1): it will generate values from `start` (included) to `stop` (excluded), incrementing each time by `step`.

This might look complicated, but an example will clarify. In the previous `for` example, we used a `tuple` to contain all the values we wanted to sum, but it would have been equivalent if we used `range(1,11)`: it would be starting from 1, increment by 1 while we stay below 10:

```python
total = 0
for i in range(1,11):
  total += i
else:
  print('The sum of the first 10 integers is', total)

```

And the result is what we expected:

```python
The sum of the first 10 integers is 55
```

So, what does "generator" mean? Imagine that you wanted to sum all the first 1,000,000,000 numbers:

Typing up a tuple with all these numbers is not practical, it would take you ages to type! And imagine the memory cost of this tuple, just for us to iterate over it!

Using a `while` in that case would definitely help!

But `range` is a generator, and what it means is that it doesn't produce all the values at once. It returns an iterator, where every time you `__next__`, it returns the previous value + 1. So, the only memory used is enough needed to store the start, stop, and step values.

What happens if you print the range ?

```python
print(range(10))
```

It doesn't give us all the values:

```python
range(0, 10)
```

You need to iterate over all of them. Convert it to a tuple!

```python
print(tuple(range(10)))
```

As we've seen earlier, a `tuple` requires an iterator to initialise, and `range` returns a generator, which is "iterable", so we can use them together to get the values:

```python
(0, 1, 2, 3, 4, 5, 6, 7, 8, 9)
```

## Break and Continue ##

While iterating, either with `while` or with `for`, you might reach a situation where you might want to change the flow of execution, either by skipping the current item, or by quitting completely out of the loop. For these purpose, as in many other languages, python offers `continue` and `break` respectively.

For example, what if we wanted the sum of the first `n` numbers that are a multiple of `m` ? The so called "pythonic" way of doing this would be something like this:

```python
n = 12
m = 3
print('The sum of the first', n, 'integers that are a multiple of', m, 'is', sum(tuple(range(m, n + 1, m))))

```

This produces the expected result:

```python
The sum of the first 10 integers that are a multiple of 3 is 30
```

This works because the `range` produces the multiples as desired, and `sum` sums them up. But to demonstrate `continue` we need to assume that the concept of **multiple** needs to be formally verified by an `if`. It is a bit of a forced situation, because in python the tendency is to try and use iterations everywhere, just the `sum` of `range` example there, plus maybe `map` and `filter`. But these are for a more advanced lesson, for now let's assume we don't know these tricks. So, if we want to do this with a `while`, we could so this:

```python
total = 0
n = 12
m = 3
i = 0

while i <= n:
  i += 1
  if i % m > 0:
    print('Skipping', i)
    continue
  total += i
else:
  print('The sum of the first 10 integers is', total)

```

You could argue that if we had the `total += i` part in the `else` of the `if`, we'd get the same result, which is correct, but you need to imagine having multiple conditions in multiple parts of the code, where you'd have multiple instances of `continue`. The result shows the numbers we're skipping too, which is useful way to prove the correct execution:

```python
Skipping 1
Skipping 2
Skipping 4
Skipping 5
Skipping 7
Skipping 8
Skipping 10
Skipping 11
Skipping 13
The sum of the first 10 integers is 30
```

We can do the same with a `for` loop too:

```python
total = 0
n = 12
m = 3

for i in range(1,n + 1):
  if i % m > 0:
    print('Skipping', i)
    continue
  total += i
else:
  print('The sum of the first 10 integers is', total)
```

And the result is the same:

```python
Skipping 1
Skipping 2
Skipping 4
Skipping 5
Skipping 7
Skipping 8
Skipping 10
Skipping 11
Skipping 13
The sum of the first 10 integers is 30
```

Similarly, you can use `break` to stop iterating, for example, once you find what you're looking for. If you want to check whether an object is in a sequence, the `in` keyword does it nicely for you:

```python
'i' in 'team'
```

As everyone knows, there's no `i` in `team`

```python
False
```

But what if we do not accept this "dogma" and want to write a `for` loop to verify this ourselves?

```python
sentence = 'team'
search = 'i'
found = 'not '

for c in sentence:
  if c == search:
    found = ''
print('"{0}" was {1}found in "{2}"'.format(search, found, sentence))
```

And the script works well too. The `{0}`, `{1}` and `{2}` are variables, the values of which are respectively replaced by the variables listed in the _format_ part of the print statement.

```python
"i" was not found in "team"
```

But what if we are looking for 'q' in "The quick brown fox jumps over the lazy dog" ?

We know for sure that every letter is included in that sentence. The purpose of the sentence is to try out a typeface font with all the letters. But let's pretend we didn't know that it contains all the letters. The same code as before works fine:

```python
sentence = 'The quick brown fox jumps over the lazy dog'
search = 'q'
found = 'not '

for c in sentence:
  if c == search:
    found = ''
print('"{0}" was {1}found in "{2}"'.format(search, found, sentence))
```

But, as you might have observed: why do we keep comparing all the letters after `q` in `quick`? We have enough information to answer the question, why keep wasting CPU cycles? Can't we bail out?

That's what `break` is for!

```python
sentence = 'The quick brown fox jumps over the lazy dog'
search = 'q'
found = 'not '

for c in sentence:
  if c == search:
    found = ''
    break

print('"{0}" was {1}found in "{2}"'.format(search, found, sentence))
```

You might not see the difference in execution, since the sentence is quite small, but in real life examples, this has a massive difference in performance! Also, notice how `break` actually breaks the `else` as we mentioned in the `for` section!

```python
sentence = 'The quick brown fox jumps over the lazy dog'
search = 'q'
found = 'not '

for c in sentence:
  if c == search:
    found = ''
    break
else:
  print('"{0}" was {1}found in "{2}"'.format(search, found, sentence))

```

This produces no output! This is because the `else` is activated only when the `for` has reached the point where the iterator's `__next__` reports `StopIteration` or `IndexError`, or in other words, when the iterator has reached its end. But with `break`, we stopped before reaching the end!

In this script, we'd hit the `else` only if the `search` is not found:

```python
sentence = 'The quick brown fox jumps over the lazy dog'
search = '?'
found = 'not '

for c in sentence:
  if c == search:
    found = ''
    break
else:
  print('"{0}" was {1}found in "{2}"'.format(search, found, sentence))
```

Only in this case we see the output, because we've scanned the whole sentence and reached the end without hitting `break`:

```python
"?" was not found in "The quick brown fox jumps over the lazy dog"
```

So, there's nothing wrong with using the `else`, but it has some subtle consequences that leads the vast majority of the programmers not to use it in a `while` or `for` loop.

## Pass ##

The last section for this lesson is the `pass` instruction: it does nothing. It exists only to make sure that the interpreter is happy, for cases where it is expecting a statement, but the programmer doesn't want to provide one. Typically this is for place-holders, or for constructs that try to document something without using comments.

An example is:

```python
if something is None:
  pass
else:
  print(something)
```

One could negate the test in the `if`, and write the code this way:

```python
if something is not None:
  print(something)
```

And if later, there's the need to print a message also for the case where `something` is None, it can be added in the else

```python
if something is not None:
  print(something)
else:
 print("There's a None value")
```

`pass` also has some advanced uses for classes, but in general, it is almost always possible to avoid using it with a little bit of effort.

That completes the lesson. You should now be ready to move on to some additional topics. [Click here to return to the lesson list](../README.md)
