# Lesson 10 - Modules: Part 5: argparse #

In this lesson we talk about the `argparse` module

## Why isn't sys.argv enough? ##

If you want to deal with command line options in a python script, you can use `sys.argv`, which gives you access to each "word" as split by the shell where the command was written.

So, why do we need an additional module to do, basically, the same thing ?

The main reason is that the command line interface is an interface that connects the script with a human, and humans tend to remember things in different ways, which means that the order of the parameters tend to change.

If you use `sys.argv`, and you want to allow for the parameters to be specified in any order, you will end up writing your clone of `argparse`, which comes with python's standard library, and it creates the `--help` automatically.

There are several alternatives to `argparse`, some more specialised toward specific use=cases, but we will focus just on it, as it is the most popular.

The [documentation](https://docs.python.org/3/library/argparse.html) is quite good, but because of its popularity, the community is quite active, which means you will find a lot of online help and examples, and additional tools, such as tools to create the man-page of your script starting from the `argparse` script itself.

## Basic parameters ###

Let's try a small example:

```python
import argparse

parser = argparse.ArgumentParser(description="Let's try argparse.")
parser.add_argument('--test', help='This is a test option')

args = parser.parse_args()

print(args)
```

If you called the script `/tmp/test1.py`, when you run it, you get this:

```
% /tmp/test1.py
Namespace(test=None)
```

Let's try the script with `--help`:

```
% /tmp/test1.py
usage: test1.py [-h] [--test TEST]

Let's try argparse.

optional arguments:
  -h, --help   show this help message and exit
  --test TEST  This is a test option
```

This is pretty useful: Using the `help` and `description` properties of the argument and parser respectively, `argparse` built the script's help!

The help is telling us that the `--test` option has an optional argument, so what happens if we specify it ?

```
% /tmp/test1.py --test 1
Namespace(test='1')
```

And what if we specify `--help` with nothing else ?

```
% /tmp/test1.py --test
usage: test1.py [-h] [--test TEST]
test1.py: error: argument --test: expected one argument
```

And what do we need to do to get the supplied value?

```python
import argparse

parser = argparse.ArgumentParser(description="Let's try argparse.")
parser.add_argument('--test', help='This is a test option')

args = parser.parse_args()

print(args.test)
```

It's pretty simple: remove the dashes, and that's the name of the property:

```
% /tmp/test1.py --test 1
1
```


## Mandatory, Optional, Default ##

The `--test` in our script is optional, but what if we want another option, but make it mandatory ?

```python
import argparse

parser = argparse.ArgumentParser(description="Let's try argparse.")
parser.add_argument('--test', help='This is a test option')
parser.add_argument('--mandatory', required=True, help='This is a mandatory option')

args = parser.parse_args()

print(args.test)
print(args.mandatory)
```

```
% /tmp/test1.py --mandatory 1
None
1
```

And if `--mandatory` is not specified? 

```
% /tmp/test1.py --test 1
usage: test1.py [-h] [--test TEST] --mandatory MANDATORY
test1.py: error: the following arguments are required: --mandatory
```

See the help is using a form of BNF based syntax to show you the options, and it is telling you that test is optional, since it is enclosed in square brackets, while `--mandatory` is not.

Now the script has one mandatory option, and an optional one, so we know for sure that the mandatory will always have an option, but what about the optional?

When it is not specified, it gets `None` as value, as we can see above, but what if we want a different default value ?

You can use the `default` option:

```python
import argparse

parser = argparse.ArgumentParser(description="Let's try argparse.")
parser.add_argument('--test', default='test', help='This is a test option')
parser.add_argument('--mandatory', required=True, help='This is a mandatory option')

args = parser.parse_args()

print(args.test)
print(args.mandatory)
```

```
% /tmp/test1.py test1.py --mandatory 1
test
1
```

This will make it easier to deal with all sort of situations.

How can we print the defaults in the help ?

You can add the following to the parser's constructor: `formatter_class=argparse.ArgumentDefaultsHelpFormatter`


```python
import argparse

parser = argparse.ArgumentParser(description="Let's try argparse.", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('--test', default='test', help='This is a test option')
parser.add_argument('--mandatory', required=True, help='This is a mandatory option')

args = parser.parse_args()

print(args.test)
print(args.mandatory)
```

And now, if we run the `--help`:

```
% /tmp/test1.py --help
usage: test1.py [-h] [--test TEST] --mandatory MANDATORY

Let's try argparse.

optional arguments:
  -h, --help            show this help message and exit
  --test TEST           This is a test option (default: test)
  --mandatory MANDATORY
                        This is a mandatory option (default: None)
```

## Typing ##

We've seen now how `--test` received both a value of `1`, or `'test'`, or, in other words, some `int` and some `str`. Can we force the option to be a certain type ?

Yes: with the `type` option. Let's make `--mandatory` an `int` only option!

```python
import argparse

parser = argparse.ArgumentParser(description="Let's try argparse.")
parser.add_argument('--test', default='test', help='This is a test option')
parser.add_argument('--mandatory', required=True, type=int, help='This is a mandatory option')

args = parser.parse_args()

print(args.test)
print(args.mandatory)
```

```
% /tmp/test1.py --mandatory test
usage: test1.py [-h] [--test TEST] --mandatory MANDATORY
test1.py: error: argument --mandatory: invalid int value: 'test'
```

Now `--mandatory` has to be an integer.

You can take advantage of the fact that type is a python object, which will be "called" with he argument as a parameter, and you can create your own function, or class, to use as `type`.

For example, you can use `open` to force the file to be a file, which you will open in the default mode, since there is only one option, but you can easily create a wrapper function or even a lambda to open the file in whatever other mode you need, such as:

```python
parser.add_argument('--output', default='output.bin', type=lambda fname: open(fname, 'wb'),  help='Output file')
```

Remember to close the file! You can still use `with`:

```python
import argparse

parser = argparse.ArgumentParser(description="Let's try argparse.")
parser.add_argument('--test', default='test', help='This is a test option')
parser.add_argument('--mandatory', required=True, type=int, help='This is a mandatory option')
parser.add_argument('--output', default='output.bin', type=lambda fname: open(fname, 'wb'),  help='Output file')

args = parser.parse_args()

print(args.test)
print(args.mandatory)
with args.output:
  args.output.write(bytes(range(2)))
```

## Positional and Optional arguments ##

If your argument has a name with one or two dashes (`-` and `--` respectively), it is called **optional** argument.
If it does not, it is called a **positional** argument.

The difference between the 2 is that the optional argument can be anywhere in the command line, while, as the name suggests, the positional argument needs to be in the right place to get the right value.

If you are using `argparse`, you are probably going to use a lot of optional arguments, but there's a use case for positional arguments: if you want your command to be able to work with multiple files, and you want to allow the user to do something like `script.py --option a --otheroption b /tmp/*.txt`

The last portion of that command is a positional argument (actually multiple of them). We will see the "multiple" part just next.

## Multiple Values ##

We've seen how the argument requires 1 value: what if we need more ?

There's an option for that too: `nargs`:

-	If `nargs` is a number, say 3, `argparse` will expect exactly 3 values
-	If `nargs` is `?`, similarly to regular expressions and shell file globs, it means 0 or 1.
-	If `nargs` is `*`, just like for the `?` case, it will mean 0 or more values. Be careful with `*`, because it might "eat up" all the other arguments!. Typically the `*` is used as the only positional argument, for example for input files.
-	If `nargs` is `+`, keeping up with the regular expression analogy, it will mean 1 or more. The same caveat as `*` apply.

Whenever a `nargs` is specified, the property generated by the parser will be a list, **but** not when the default value is used, so make sure your default is a list too!

```python
import argparse

parser = argparse.ArgumentParser(description="Let's try argparse.")
parser.add_argument('--test', default='test', nargs=1, help='This is a test option')

args = parser.parse_args()

print(args.test)
```

```
% /tmp/test1.py test1.py
test
% /tmp/test1.py test1.py --test 1
['1']
```

So, in this case, you should set the default for test to be ['test'] for consistency:


```python
import argparse

parser = argparse.ArgumentParser(description="Let's try argparse.")
parser.add_argument('--test', default=['test'], nargs=1, help='This is a test option')

args = parser.parse_args()
for t in args.test:
  print(t)
```

And now we can deal with `args.test` regardless:

```
% /tmp/test1.py test1.py
test
% /tmp/test1.py test1.py --test 1
1
```

Or better, with `nargs` set to `*`:

```python
import argparse

parser = argparse.ArgumentParser(description="Let's try argparse.")
parser.add_argument('--test', default=['test'], nargs='*', help='This is a test option')

args = parser.parse_args()
for t in args.test:
  print(t)
```

Now the code deals with multiple options:

```
% /tmp/test1.py test1.py --test 1 2 3 4 5
1
2
3
4
5
```

And we can ask the shell to help us type multiple values too:

```
% /tmp/test1.py test1.py --test {1..5}
1
2
3
4
5
```

You might ask: what's the difference between `nargs` and `required` ? If I set `nargs` to 1, doesn't that imply `required=True` ?

No, they are working on different targets: `required` is for the argument, `--test` in this case: if it is required, you need to specify it.

The `nargs` is about the arguments to `--test`, so `nargs=1` means that **if** `--test` is specified (which doesn't need to be since `required=False`, it **must** have 1 value.

As we've seen, if `required` is `False`, and `--test` is not specified, `default` is used instead.

## Grouping ##

Some times you might want to group options according to various criteria, for example options about connecting to a server, options about formatting the output, and options about what the script should actually do.

This can be done with `add_argument_group(title=None, description=None)`.

The `title` and the `description` will be displayed in the help.

The `add_argument_group` method will return the group object, which you should now use to add arguments to (or other sub-groups, if you want). Let's try it a bit:

```python
import argparse

parser = argparse.ArgumentParser(description="Let's try argparse.")
parser.add_argument('--test', default=['test'], nargs='*', help='This is a test option')

g = parser.add_argument_group(title='Main group', description='This is the main group')
g.add_argument('--g1', help='This is a main.g1 option')
g.add_argument('--g2', help='This is a main.g2 option')
secondg = g.add_argument_group(title='Sub group', description='This is the sub group')
g.add_argument('--suboption', help='This is a sub option')

g = parser.add_argument_group(title='Secondary group', description='This is the second main group')
g.add_argument('--opta', help='This is a secondary option')
g.add_argument('--optb', help='This is another secondary option')

args = parser.parse_args()
```

And if we run the script with the `--help` option:

```
% /tmp/test1.py --help
usage: test1.py [-h] [--test [TEST ...]] [--g1 G1] [--g2 G2] [--suboption SUBOPTION] [--opta OPTA] [--optb OPTB]

Let's try argparse.

optional arguments:
  -h, --help            show this help message and exit
  --test [TEST ...]     This is a test option

Main group:
  This is the main group

  --g1 G1               This is a main.g1 option
  --g2 G2               This is a main.g2 option
  --suboption SUBOPTION
                        This is a sub option

Secondary group:
  This is the second main group

  --opta OPTA           This is a secondary option
  --optb OPTB           This is another secondary option
```

You get an idea of what a group does to the help.

There's another type of group: mutually exclusive.

This group is very handy, it allows you to group together options that can't be specified together.

You do this with the `add_mutually_exclusive_group(required=False)` method. The `required` option works like you would expect.

```python
import argparse

parser = argparse.ArgumentParser(description="Let's try argparse.")
parser.add_argument('--test', default=['test'], nargs='*', help='This is a test option')

g = parser.add_mutually_exclusive_group()
g.add_argument('--tea', help='Make tea')
g.add_argument('--cofee', help='Make cofee')

g = parser.add_mutually_exclusive_group(required=True)
g.add_argument('--bread', help='Eat bread')
g.add_argument('--pasta', help='Eat pasta')

args = parser.parse_args()
print(args)
```

First, let's look at the help: focus on the BNF part:

```
--help
usage: test1.py [-h] [--test [TEST ...]] [--tea TEA | --cofee COFEE] (--bread BREAD | --pasta PASTA)

Let's try argparse.

optional arguments:
  -h, --help         show this help message and exit
  --test [TEST ...]  This is a test option
  --tea TEA          Make tea
  --cofee COFEE      Make cofee
  --bread BREAD      Eat bread
  --pasta PASTA      Eat pasta
```

As you can see, the help is already telling you that you can specify `--tea` or `--cofee` but not both, and it is also telling you that you need to specify one of `--bread` or `--pasta`, but neither both nor none.

## Destination ##

At times, you might want to change the name of the property that ends up containing the value. This is useful, for example, if the name of the option makes for a weird property name, or if you want multiple options to assign different values:

This is done with the `dest` option.

```python
import argparse

parser = argparse.ArgumentParser(description="Let's try argparse.")

parser.add_argument('--double-check', help='Check twice')

args = parser.parse_args()
print(args)
```

```
% /tmp/test1.py test1.py --double-check everything
Namespace(double_check='everything')
```

```python
import argparse

parser = argparse.ArgumentParser(description="Let's try argparse.")

parser.add_argument('--double-check', dest='doublecheck', help='Check twice')

args = parser.parse_args()
print(args)
```

```
% /tmp/test1.py test1.py --double-check everything
Namespace(doublecheck='everything')
```

## Actions ##

The default action we've been using so far is `'store'`, bit there are a few more. Let's have a look:

-	`'store'` means store the value in the property. The value can be the one (or ones) supplied by the user, or the default
-	`'store_const'` is the same as `store`, but it doesn't need the user to supply any value, and it takes the value of the `const` option supplied to `add_argument`
-	`'store_true'` and `'store_false'` is very similar, but it forces the `const` to be `True` and `False` respectively. This means that in this case, the user doesn't need to supply any argument. This is handy for on/off switches.
-	`'append'` means attach the value to previous values. This is handy if you want your option to be repeatable. It is similar to `nargs` in the result, but the user has to type the option multiple times, and thus is usually not used that much because it's annoying.
-	`'append_const'` is similar, but it does not need the user to supply a value, it will use the value you supply in the `const` property. This might be a bit more usable, because you could use it, for example, to increase the verbosity of your script, with something like `--verbose --verbose --verbose`, but it is still a bit annoying, and the user might prefer to use something like `--verbose 3`

There are a few more, like `count`, `version` and `help`, but the main ones are the first 2 we have mentioned here, and we will focus on these.


Let's see an example:


```python
import argparse

parser = argparse.ArgumentParser(description="Let's try argparse.")

parser.add_argument('--double-check', action='store_true', dest='doublecheck', help='Check twice')
parser.add_argument('--dont-trust-anyone', action='store_false', dest='trust', help='Trust No one!')

args = parser.parse_args()
print(args)
```

```
% /tmp/test1.py test1.py
Namespace(doublecheck=False, trust=True)
% /tmp/test1.py test1.py --double-check
Namespace(doublecheck=True, trust=True)
% /tmp/test1.py test1.py --double-check --dont-trust-anyone
Namespace(doublecheck=True, trust=False)
```

As you can see, the `store_false` is like a double negative, so it is always a bit confusing. The best approach is to set the option name to be negative, and use the `dest` to change the property to be the opposite of the negation. This is confusing at first, but the code then is easy to read

If you use `dest` with the `store_const` property and the  mutually exclusive groups, you can give your script a sort of imperative behaviour:

```
import argparse

parser = argparse.ArgumentParser(description="Let's try argparse.")

op_list = 'list'
op_add = 'add'
op_delete = 'delete'


g = parser.add_mutually_exclusive_group(required=True)
g.add_argument('--list', action='store_const', dest='operation', const=op_list, help='List')
g.add_argument('--add', action='store_const', dest='operation', const=op_add, help='Add')
g.add_argument('--delete', action='store_const', dest='operation', const=op_delete, help='Delete')

args = parser.parse_args()
print(args)
if args.operation == op_list:
  print('This script would print a list')
elif args.operation == op_add:
  print('This script would add to a list')
elif args.operation == op_delete:
  print('This script would delete from a list')
```

This might make it easier to deal with multiple commands as options.

```
% /tmp/test1.py test1.py
usage: test1.py [-h] (--list | --add | --delete)
test1.py: error: one of the arguments --list --add --delete is required
% /tmp/test1.py test1.py --list
Namespace(operation='list')
This script would print a list
% /tmp/test1.py test1.py --add
Namespace(operation='add')
This script would add to a list
% /tmp/test1.py test1.py --delete
Namespace(operation='delete')
This script would delete from a list
```

You could even store the options in a dictionary indexed by the options name, and as the value you could have a function to run, so you wouldn't even need the `if` - `elif` part.

## Choices ##

Validating the input is important, and we've seen how we can use the `type` parameter to specify what value we want. You can use the `type` converter to implement custom validations, but for a simple "choose from a list" type of validation, there's a simpler approach: the `choices` parameter.

Remember the list/add/delete example from before ? Let's see what that looks like if we use `choices` instead:

```
import argparse

parser = argparse.ArgumentParser(description="Let's try argparse.")

op_list = 'list'
op_add = 'add'
op_delete = 'delete'

ops = (op_list, op_add, op_delete)

parser.add_argument('--operation', choices=ops, help='Operation')

args = parser.parse_args()
print(args)
if args.operation == op_list:
  print('This script would print a list')
elif args.operation == op_add:
  print('This script would add to a list')
elif args.operation == op_delete:
  print('This script would delete from a list')
```

And the result is quite nice, including the help, which shows what are the allowed values:

```
% /tmp/test1.py test1.py --help
usage: test1.py [-h] [--operation {list,add,delete}]

Let's try argparse.

optional arguments:
  -h, --help            show this help message and exit
  --operation {list,add,delete}
                        Operation
% /tmp/test1.py test1.py --operation test
usage: test1.py [-h] [--operation {list,add,delete}]
test1.py: error: argument --operation: invalid choice: 'test' (choose from 'list', 'add', 'delete')
% /tmp/test1.py test1.py --operation list
Namespace(operation='list')
This script would print a list
% /tmp/test1.py test1.py --operation add
Namespace(operation='add')
This script would add to a list
% /tmp/test1.py test1.py --operation delete
Namespace(operation='delete')
This script would delete from a list
```

Notice also that invalid values are detected immediately, and a nice help explains the issue.

If the allowed values is long, the help might be a bit confusing.

That completes the lesson. You should now be ready to move on to some additional topics. [Click here to return to the lesson list](../README.md)
