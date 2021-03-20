# Lesson 10 - Modules: Part 4: re #

In this lesson we talk about the re module for regular expressions

## Regular expressions ##

Python's standard library comes with a module called `re` for regular expressions. The documentation is quite good, and can be found [here](https://docs.python.org/3/library/re.html).

Python's implementation of regular expressions is very similar to Perl's, so it would be classified as a PCRE, or Perl Compatible Regular Expression.

What this means is that the characters will have their special meaning enabled by default, and you'd need to escape them with a backslash to remove the special meaning.

There is a bit of a conflict between Python's way of dealing with quotes, backslashes and regular expressions, because python intercepts the `\` before it is seen by the `re` module, forcing the programmer to double or quadruple escape a backslash, for example, if you wanted to match literal `\`.

So, to remove this need, and to allow the programmer to type the regular expressions in a more comfortable format, and bypassing python's string and quote system, there's a special type of quoting called "raw", and is represented by an `r` in front of the quotes.

This disables all the parsing and quotes the string raw.

Example:

```python
print('\\')
print('\\\\')
print(r'\\')
```

Will produce this:

```
\
\\
\\
```

As you can see, the non-raw-quoted (i.e. normal) string lost a quote every 2, while the raw one didn't get changed at all.

With regular expressions it is better to remember to always use raw quotes.

We will not cover here how regular expressions work, because that's not just a module on itself, but a whole class. What we will cover here is how to use them in python, so we will assume that the reader has some basic understanding of regular expressions, and in particular the PCRE ones (although, if you are familiar with the BRE used in `grep`, you'll still be able to follow, just reverse the use of the backslash for most cases).

## Matching ##

Matching means checking if the beginning of the supplied string matches the supplied pattern, and is done using the `re.match` method, which takes 2 mandatory parameters, `pattern` and `string`, and the optional `flags`.

The `re` module supplies a bunch of flags, that are consistently usable across the module. The most common flag would be `re.IGNORECASE`.

If there is no match, `re.match` will return None, and otherwise, it will return a `match` object, which will contain all the details.

Let's try a match:

```python
import re

print(re.match('ab', 'abc'))
print(re.match('a', 'abc'))
print(re.match('b', 'abc'))
```

This will produce:

```
<re.Match object; span=(0, 2), match='ab'>
<re.Match object; span=(0, 1), match='a'>
None
```

Notice that here we didn't need to use raw quotes because the pattern is simple.

As you can see, looking for `b` fails because the pattern doesn't match from the beginning, but you can change the pattern to answer the question "is there a b in the string?":

```python
import re

print(re.match('.*b.*', 'abc'))
```

Or, if you want to see if there's a 'b' inside the string, but not at the end or at the beginning:

```python
import re

print(re.match('.+b.+', 'abc'))
```

What does the `match` object contain ? What can we do with it ?

We will see the group part later, but there are other things that you can get from the `match` object, such as:

-	`start` and `end` will tell you the positions in `string` that delimit the part that matched.
-	`re` is the pattern used to match
-	`string` is the text supplied to the match

If you want to check if a string matches a regular expression, therefore, you can just do `if re.match(pattern, string)`, but if you plan to then use the part of `string` that matched, it is better to do something like this:

```python
import re

m = re.match(pattern, string)
if m is not None:
  do_something(m)
```

You can do `if m:`, but as a matter of style, you can also chose to be explicit and check `if m is not None`.

## Searching ##

There is another function for matching or searching with regular expressions, called `search`.

The only difference between `match` and `search` is the fact that `search` is not anchored to the beginning of the string, it will search everywhere.

```python
import re
pattern = 'b'
print(re.match(pattern, 'abcd') is not None)
print(re.search(pattern, 'abcd') is not None)
```

```
False
True
```

If your pattern starts with `^` and ends with `$`, there's no difference between the 2:


```python
import re
pattern = r'^.*b.*$'
print(re.match(pattern, 'abcd') is not None)
print(re.search(pattern, 'abcd') is not None)
```

The 2 functions perform the same.

```
True
True
```

## Groups and Capturing ##

One of the biggest powers of regular expression is the grouping, and in particular capturing groups.

A group is defined by parenthesis (`(` and `)`), and some match definition inside.

In PCRE, and in python's `re` module too, there are several options you can specify inside a group, and this is done by adding a `?` just after the opening parenthesis (`(?…)`).

If you specify `P<name>` after the `?`, you have the very powerful named group.
If you specify `P=name`, you have what is called back-reference.
If you specify `:`, you have a non-capturing group.

If you check the documentation, there are a bunch of other options, we will focus on these 3.

### Named Groups ###

If you capture some text, you can extract the captured text by using the `match.groups(N)` syntax, where `N` is the ordinal position of the group. This is not very convenient, because if you later change the pattern, you need to scan all the code to see which part of the script is impacted by the change in group numbering. It is advisable to use numbered groups only for very small projects.

If you name a group, you can extract it by name, regardless of its position, and that's how you should always extract groups.

Let's see some examples:

Let's say you want to capture the last character in a string that contains `b`

```python
import re

pattern = r'^.*b.*(.)$'
m = re.match(pattern, 'abcd')
if m is not None:
  print(m.string, 'matches, and the last character is', m.group(1))
```

Which produces the expected output:

```
abcd matches, and the last character is d
```

Now, let's say we now also want to capture the character just after b:

```python
import re

pattern = r'^.*b(.).*(.)$'
m = re.match(pattern, 'abcd')
if m is not None:
  print(m.string, 'matches, and the last character is', m.group(1))
```

Ooops! The output is wrong now!

```
abcd matches, and the last character is c
```

If we used the named groups, this wouldn't have happened:

```python
import re

pattern = r'^.*b(?P<after>.).*(?P<last>.)$'
m = re.match(pattern, 'abcd')
if m is not None:
  print(m.string, 'matches, and the last character is', m.group('last'))
```

And we can then add the functionality that is related to the new group:


```python
import re

pattern = r'^.*b(?P<after>.).*(?P<last>.)$'
m = re.match(pattern, 'abcd')
if m is not None:
  print(m.string, 'matches, and the last character is', m.group('last'))
  print('The character just after b in', m.string, 'is', m.group('after'))
```

```
abcd matches, and the last character is d
The character just after b in abcd is c
```

The advice here is to try to use named groups as much as possible.

### Back References ###

What if we want to look for a string that contains a "-" surrounded by the same string ?

You can try to build all sort of regular expressions, but you won't succeed unless you use a back-reference:

```python
import re

pattern = r'^.*(?P<before>.+)-(?P=before).*$'
m = re.match(pattern, 'abcd-cdab')
if m is not None:
  print(m.string, 'contains a - surrounded by 2', m.group('before'))
```

This will print:

```
abcd-cdab contains a - surrounded by 2 cd
```

### Non-capturing groups ###

Some times you want to use a group for other purposes than extraction, such as alternative text, and you don't want it to disturb your code, for example if unfortunately, it does not use named groups.

In those cases, you need to use a non-capturing group.

For example, let's say you have this script, which expects text to say that something jumped over a certain type of dog, and we want to know what type of dog it is:

```python
import re

pattern = r'^.* jumps over the ([^ ]+) dog'

m = re.match(pattern, 'The quick brown fox jumps over the lazy dog')
if m is not None:
  print('The dog was', m.group(1))
```

This works:

```
The dog was lazy
```

Now, your product manager tells you that the customer would much prefer if we matched only on sentences where only either a fox or a cat jumped over the dog, and we'd like to know what type of dog then that was.

That's easy, you think, we just add a new group:

```python
import re

pattern = r'^.*(cat|fox) jumps over the ([^ ]+) dog'

m = re.match(pattern, 'The quick brown fox jumps over the lazy dog')
if m is not None:
  print('The dog was', m.group(1))

m = re.match(pattern, 'The quick brown cat jumps over the lazy dog')
if m is not None:
  print('The dog was', m.group(1))
```

Oops! Not using the named group was a mistake!

```
The dog was fox
The dog was cat
```

We can go through the whole script and look for places where we used `m.group(1)`, and hopefully find them all, or, we can use a non-capturing group:

```python
import re

pattern = r'^.*(?:cat|fox) jumps over the ([^ ]+) dog'

m = re.match(pattern, 'The quick brown fox jumps over the lazy dog')
if m is not None:
  print('The dog was', m.group(1))

m = re.match(pattern, 'The quick brown cat jumps over the lazy dog')
if m is not None:
  print('The dog was', m.group(1))
```

```
The dog was lazy
The dog was lazy
```

## Replacing ##

The `re` module has a `sub` method, which uses a pattern to search through a provided string, and replace the part that matches, with a supplied replacement text.

The replacement text can contain reference to any group found in the pattern.

Let's see a few examples:

```python
import re
pattern = r'^.*(?P<jumping>cat|fox) jumps over the (?P<dogattribute>[^ ]+) dog'
string = 'The quick brown fox jumps over the lazy dog'

print(re.sub(pattern, r'A \g<jumping> was involved with a \g<dogattribute> dog', string))
```

And the result is:

```
A fox was involved with a lazy dog
```

In the replacement string, you can also use `\1` and `\2`, or `\g<1>` and `\g<2>` if you prefer to use the number reference to groups, but keep in mind the risks of doing that as mentioned above.

IF you really have to, prefer the `\g<N>` format as it is less ambiguous.

You might also use `\&` to refer to the whole matching string.

If you used `sed`, this will all look familiar to you.

There are other options for `sub`, such as the number of matches, we'll leave these as an exercise for the student.

## Compiling ##

Regular expressions are known for their great power, but not for being easy to learn nor for their performance.

One of the reason for the latter is that for a regular expression to be used, it needs to be "compiled", or converted from the textual representation that the programmer wrote, to something that the `re` engine can then use.

This compilation is expensive, but you wouldn't see the impact in the scripts we've done so far, because you'd be compiling only once or twice.

In a script used in a real scenario, it's likely that you will be scanning for multiple lines in a file, repeating the same `re.match`, `re.search` or `re.sub` multiple times, and each time the pattern would be compiled, for no reason, since it wouldn't be changing.

For this reason, there's a function in the `re` module called `re.compile`. It will produce an object of type `Pattern`, which implements all the functions you've seen in the `re` module, such as `match`, `search` and `sub`, so you can replace the call to `re.` to `mypattern.`: the only difference is that you don't need to pass the pattern, it is done automatically for you.

Let's look at a previous example:

```python
import re
pattern = r'^.*(?P<jumping>cat|fox) jumps over the (?P<dogattribute>[^ ]+) dog'
string = 'The quick brown fox jumps over the lazy dog'

print(re.sub(pattern, r'A \g<jumping> was involved with a \g<dogattribute> dog', string))
```

Imagine this being a function, where you'd receive the string, and you'd return the modified one:


```python
import re

def change(string):
  '''
  Check whether the supplied string  contains "cat" or "fox", followed by " jumps over <some type of> doc"
  And if so, return a string that says "cat/fox was involved with a <type of dog> dog"
  '''
  pattern = r'^.*(?P<jumping>cat|fox) jumps over the (?P<dogattribute>[^ ]+) dog'
  return re.sub(pattern, r'A \g<jumping> was involved with a \g<dogattribute> dog', string)

print(change('The quick brown fox jumps over the lazy dog'))
```

Now, imagine this `change` function being called for each line in a file with thousands of lines. The conversion of `pattern` will be very expensive for no reason, since it never changes.

Much better would be to do this:


```python
import re
pattern = re.compile(r'^.*(?P<jumping>cat|fox) jumps over the (?P<dogattribute>[^ ]+) dog')

def change(string):
  '''
  Check whether the supplied string  contains "cat" or "fox", followed by " jumps over <some type of> doc"
  And if so, return a string that says "cat/fox was involved with a <type of dog> dog"
  '''
  return pattern.sub(r'A \g<jumping> was involved with a \g<dogattribute> dog', string)

print(change('The quick brown fox jumps over the lazy dog'))
```

As a rule of thumb, you should always compile your patterns, and re-use the compiled ones as much as possible, even if your script is very small, so that you don't need to remember 2 different syntax for the `match`, `search` and `sub` methods (with or without pattern passed as parameter).

## Splitting ##

`re.split` and `Pattern.split` behave like the `str.split`, but the separator has the power of regular expressions!

Let's say you have to extract words from lines you receive, where the words can be separated by spaces, tabs, or numbers

```python
import re

sample_line = `The quick	brown1fox123jumps12	12over the    lazy dog`
print(re.split(r'[ \t0-9]+', l))
```

This would produce the sentence split in words as we needed:

```
['The', 'quick', 'brown', 'fox', 'jumps', 'over', 'the', 'lazy', 'dog']
```

The split has a bunch of other functionalities, such as extracting groups, which would mean that the result would receive also captured groups.

For example, imagine that the numbers in the previous sentence needed to be captured as well:

```python
import re

sample_line = `The quick	brown1fox123jumps12	12over the    lazy dog`
re.split(r'(?:[ \t]+|([0-9]+))', l)
```

```
['The', None, 'quick', None, 'brown', '1', 'fox', '123', 'jumps', '12', '', None, '', '12', 'over', None, 'the', None, 'lazy', None, 'dog']
```

That completes the lesson. You should now be ready to move on to some additional topics. [Click here to return to the lesson list](../README.md)
