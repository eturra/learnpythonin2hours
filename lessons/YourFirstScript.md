# Lesson 2 - Your First Script #

In this lesson we will write our very first python script.

## Getting ready ##

Python is an interpreted language, which means that the scripts on their own can't work, they need an interpreter. This means that the system needs to know that an interpreter is needed, and it needs also to know which one.

In systems like Linux or MAC, this can be achieved with what is called "shebang", which is a specific format for the first line of the script: the line needs to start with a hash (`#`) followed by an exclamation mark, also called "bang" (`!`), followed by the command used as interpreter.

Note that this is not specific to python: every other interpreter (e.g. `bash`, `perl`, `awk` and many more) command does this.

For Windows systems, it depends on the specific installation of python. However, typically python is already associated with the `.py` extension, so in that case the shebang is irrelevant. Conversely, for  systems where the shebang is required, the extension `.py` is irrelevant.

A good compromise is to do both (shebang and extension), although there are many other considerations that need to be made for a script to work on all systems.

If you don't want to use a shebang, or if the shebang is pointing to a location that is not valid for your system, you can still run the script by passing the name of the script as a parameter to the interpreter itself. This works in any system, but in most cases it is undesirable because it makes the script more cumbersome to use. For this reason, there is a tendency to use a shebang with `env`, to let the system figure out the right path.

This is an example of an `env` based shebang:

```python
#!/usr/bin/env python
```

Unfortunately, because of this python 2 to python 3 migration, this tends not to be enough, since the binary might be called `python3`

For the rest of the lessons we will assume that the shebang `#!/usr/bin/env python` is sufficient, and even when we do not include it in our sample files, you will add it as required.

We will also assume that you will make the scripts executable, such as with `chmod a+x /path/to/scriptfile.py`.

Another thing that needs to be prepared is the way you create a new file: you will probably need an editor.

You can create the files in your desktop with your favourite editor, and then copy them over to the test machine, or even just issue `cat > filename` and paste the file, but if ssh is not possible for secure copies, you might need to use the editor that comes with the test machine.

If you are familiar with tools like `vi` or `vim`, you will be fine, but otherwise, if you are unfamiliar with the machine you are using for this course, and you don't have a "favourite editor", you can use `nano`. This is more friendly for inexperienced users. Just check the bottom part of the screen for hints about what steps to do, keeping in mind that `^` in that context means `control`, so `^X` means `control-x`.

This means that the command to create the file would be `nano /tmp/HelloWorld.py`. Type the line above, hit `control-X`, and follow the instructions (press `y` and then confirm the file name).

## Hello World ##

Now that we are ready, let's start with the traditional first script: Hello World!

Create a new file, called `/tmp/HelloWorld.py`, with the following content:

```python
'Hello World!'
```

You can run this script either by making it executable, and having the shebang at the top, or by running it directly, such as `python /tmp/HelloWorld.py`. Either way, the output will probably be a little disappointing: it produces no output! We need to use the `print` function. Change the script to say this:

```python
print('Hello World!')
```

The output will now be what we wanted:

```python
Hello World!
```

Now, can we make the script greet a given name ?

```python
name = 'Alice'
print("Hello", name)
```

This will produce what we wanted: a space is inserted automatically between the parameters:

```python
Hello Alice
```

What if we want to control the output and decide where the spaces go or not go ?

We can try to concatenate 2 strings:

```python
name = 'Alice'
print("Hello " + name)
```

The output is the same, but this time, we decide where it goes.

Python has more features for dealing with strings. Some are new in newer versions, and others have been around for much longer, such as the `str.format`. `str` is the name of the object in python that represents strings, and it contains a method called `format`.

If you have an Integrated Development Environment (IDE), e.g. Visual Studio Code, instead of an editor, you can probably get inline help about methods, objects and so on, but if you are in a situation where this is not available, and you need a quick reminder, you can use the `python` interpreter and the `help` function.

Start `python` and type `help(str.format)`:

```python
% python3
Python 3.9.2 (default, Feb 28 2021, 17:03:44)
[GCC 10.2.1 20210110] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> help(str.format)
```

It will give you a small description:

```python
Help on method_descriptor:

format(...)
    S.format(*args, **kwargs) -> str

    Return a formatted version of S, using substitutions from args and kwargs.
    The substitutions are identified by braces ('{' and '}').
```

The official documentation has a lot more, but this is usually enough to remember how it works. Let's try it! Change `/tmp/HelloWorld.py` to look like this:

```python
name = 'Alice'
print("Hello {0}".format(name))
```

Again, the output didn't change, but this allows you a lot more flexibility, for example if you need to mix together multiple variable, format numbers to a certain number of digits, and so on.

It also allows you to repeat the same variable, and access its methods:

```python
name = 'Alice'
print("Hello {0}! My name is also {0}!".format(name))
```

This will produce:

```python
Hello Alice! My name is also Alice
```

And you can align the text left or right:

```python
name = 'Alice'
print("Hello {0:>10}! My name is also {0:<10}!".format(name))
```

This will produce:

```python
Hello      Alice! My name is also Alice     !
```

This is not really useful, but in cases where you want to output a table or a report, for example, `format` might save you some headaches.

## Exercises ##

In the rest of the lessons, you will see exercises or examples like the above, with commands for you to try.

You can either type them out in a script, with the shebang added on top, or leave the shebang out and run the script with the interpreter in front of it, or you can type them directly into the interactive python shell.

If you decide to go for the interactive mode, keep in mind that the end of the indentation is not enough to tell the interpreter what you want it to do: you need an empty new-line to do this.

What this means is that you can't just copy-paste the exercises, you need to either add newlines after each indented block ends, or paste the sections separately and press enter to tell the interpreter what you want to do.

That completes the lesson. You should now be ready to move on to some additional topics. [Click here to return to the lesson list](../README.md)
