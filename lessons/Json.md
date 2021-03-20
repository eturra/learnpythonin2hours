# Lesson 10 - Modules: Part 2: json #

In this lesson we talk about json

## Basics ##

The json module is part of the python standard library, and it is documented [here](https://docs.python.org/3/library/json.html).

This module can be used to serialise and de-serialise python objects to and from a json string or file.

The `json` module also defines a command line tool called `json.tool`, that you can use to validate and pretty-print json files from the shell, with a command like this:

```shell
python3 -mjson.tool < /tmp/jsonfile
```

## From object to JSON ##

If you need to interact with an API that requires you to supply the data in json format, you need to build a python object that consists only of basic types (or define your on encoder as `cls` parameter, to deal with your custom objects, or a function, passed as `default`).

The basic types would be integers, floating point numbers, booleans, strings, lists, dictionaries or `None`.

Once the object is built, you have 2 options for converting it to json: store the output in a string, or write it to a file ?

If you want to write it to a file, you'd use the `json.dump` method, while for a string output, you'd use `json.dumps`

Let's start with he differences first, and then we'll look at what is in common:

`json.dump` has a mandatory second parameter that is a writable text file-like object (thus implementing `write()` in text mode, accepting str objects).

Everything else is the same:

The first parameter, mandatory, is the object that needs to be serialised.

After the mandatory parameter(s), there are a few optional parameters, the most commonly used are:

-	`indent`, which is how many spaces to indent, or what string to use (e.g. `\t` if you want tabulations)
-	`separators`, allows you to specify a 2 value tuple of strings representing what to use for separators between items and keys respectively. The default is (',', ': ') for most versions.
-	`sort_keys`, to specify that the keys should be sorted alphabetically.


So, let's try!

```python
import json

print(json.dumps(1))
```

Well, that doesn't seem to be doing much!

```
1
```

Let's try with a more complicated object:

```python
import json

print(json.dumps(list(range(10))))
```

Still, nothing really surprising: is this `json` module working ?

```
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
```

Let's try with a list of dictionaries maybe ?

```python
import json

o = [ {'Key{0}'.format(y):y for y in range(10)} for x in range(10) ]

print(json.dumps(o))
```

We are starting to see something that looks like json now: (not that the previous ones didn't look like json, but they didn't look different from python's `repr()`)

```json
[{"Key0": 0, "Key1": 1, "Key2": 2, "Key3": 3, "Key4": 4, "Key5": 5, "Key6": 6, "Key7": 7, "Key8": 8, "Key9": 9}, {"Key0": 0, "Key1": 1, "Key2": 2, "Key3": 3, "Key4": 4, "Key5": 5, "Key6": 6, "Key7": 7, "Key8": 8, "Key9": 9}, {"Key0": 0, "Key1": 1, "Key2": 2, "Key3": 3, "Key4": 4, "Key5": 5, "Key6": 6, "Key7": 7, "Key8": 8, "Key9": 9}, {"Key0": 0, "Key1": 1, "Key2": 2, "Key3": 3, "Key4": 4, "Key5": 5, "Key6": 6, "Key7": 7, "Key8": 8, "Key9": 9}, {"Key0": 0, "Key1": 1, "Key2": 2, "Key3": 3, "Key4": 4, "Key5": 5, "Key6": 6, "Key7": 7, "Key8": 8, "Key9": 9}, {"Key0": 0, "Key1": 1, "Key2": 2, "Key3": 3, "Key4": 4, "Key5": 5, "Key6": 6, "Key7": 7, "Key8": 8, "Key9": 9}, {"Key0": 0, "Key1": 1, "Key2": 2, "Key3": 3, "Key4": 4, "Key5": 5, "Key6": 6, "Key7": 7, "Key8": 8, "Key9": 9}, {"Key0": 0, "Key1": 1, "Key2": 2, "Key3": 3, "Key4": 4, "Key5": 5, "Key6": 6, "Key7": 7, "Key8": 8, "Key9": 9}, {"Key0": 0, "Key1": 1, "Key2": 2, "Key3": 3, "Key4": 4, "Key5": 5, "Key6": 6, "Key7": 7, "Key8": 8, "Key9": 9}, {"Key0": 0, "Key1": 1, "Key2": 2, "Key3": 3, "Key4": 4, "Key5": 5, "Key6": 6, "Key7": 7, "Key8": 8, "Key9": 9}]
```

What if now we want to indent the output a bit ?

```python
import json

o = [ {'Key{0}'.format(y):y for y in range(10)} for x in range(10) ]

print(json.dumps(o, indent=2))
```

Now it looks like what we're used to think about when we hear "json":

```json
[
  {
    "Key0": 0,
    "Key1": 1,
    "Key2": 2,
    "Key3": 3,
    "Key4": 4,
    "Key5": 5,
    "Key6": 6,
    "Key7": 7,
    "Key8": 8,
    "Key9": 9
  },
  {
    "Key0": 0,
    "Key1": 1,
    "Key2": 2,
    "Key3": 3,
    "Key4": 4,
    "Key5": 5,
    "Key6": 6,
    "Key7": 7,
    "Key8": 8,
    "Key9": 9
  },
  {
    "Key0": 0,
    "Key1": 1,
    "Key2": 2,
    "Key3": 3,
    "Key4": 4,
    "Key5": 5,
    "Key6": 6,
    "Key7": 7,
    "Key8": 8,
    "Key9": 9
  },
  {
    "Key0": 0,
    "Key1": 1,
    "Key2": 2,
    "Key3": 3,
    "Key4": 4,
    "Key5": 5,
    "Key6": 6,
    "Key7": 7,
    "Key8": 8,
    "Key9": 9
  },
  {
    "Key0": 0,
    "Key1": 1,
    "Key2": 2,
    "Key3": 3,
    "Key4": 4,
    "Key5": 5,
    "Key6": 6,
    "Key7": 7,
    "Key8": 8,
    "Key9": 9
  },
  {
    "Key0": 0,
    "Key1": 1,
    "Key2": 2,
    "Key3": 3,
    "Key4": 4,
    "Key5": 5,
    "Key6": 6,
    "Key7": 7,
    "Key8": 8,
    "Key9": 9
  },
  {
    "Key0": 0,
    "Key1": 1,
    "Key2": 2,
    "Key3": 3,
    "Key4": 4,
    "Key5": 5,
    "Key6": 6,
    "Key7": 7,
    "Key8": 8,
    "Key9": 9
  },
  {
    "Key0": 0,
    "Key1": 1,
    "Key2": 2,
    "Key3": 3,
    "Key4": 4,
    "Key5": 5,
    "Key6": 6,
    "Key7": 7,
    "Key8": 8,
    "Key9": 9
  },
  {
    "Key0": 0,
    "Key1": 1,
    "Key2": 2,
    "Key3": 3,
    "Key4": 4,
    "Key5": 5,
    "Key6": 6,
    "Key7": 7,
    "Key8": 8,
    "Key9": 9
  },
  {
    "Key0": 0,
    "Key1": 1,
    "Key2": 2,
    "Key3": 3,
    "Key4": 4,
    "Key5": 5,
    "Key6": 6,
    "Key7": 7,
    "Key8": 8,
    "Key9": 9
  }
]
```

What about `json.dump` ?

```python
import json

o = [ {'Key{0}'.format(y):y for y in range(10)} for x in range(10) ]

with open('/tmp/test1.json', 'wt') as f:
  json.dump(o, f, indent=2)
```

Check the file `/tmp/test1.json` to confirm it matches the output from the previous test.

You might ask now: why should I use `json.dump` when I can use `json.dumps` and then do `f.write()` ?

You need to keep in mind that `json.dump` done directly to the file is a lot more efficient, since there's much less memory allocation involved, especially for very large objects.

## From JSON to object ##

Ok, now we have a file with some json content: how do we use it ? 

Not surprisingly, the `json` module offers 2 specular methods called `json.load` and `json.loads`, and they share almost all the same parameters, so once again, let's start from the differences:

-	`json.load` expects, as first and mandatory argument, a text file-like object that can be `read()`
-	`json.loads` expects, as first and mandatory argument, a string (or a `bytearray`)

The parameters that are in common are quite rare and advanced, so we will leave them as an exercise for the reader.

Let's try to `load` some json:

```python
import json

text = '[{"Key0": 0, "Key1": 1, "Key2": 2, "Key3": 3, "Key4": 4, "Key5": 5, "Key6": 6, "Key7": 7, "Key8": 8, "Key9": 9}, {"Key0": 0, "Key1": 1, "Key2": 2, "Key3": 3, "Key4": 4, "Key5": 5, "Key6": 6, "Key7": 7, "Key8": 8, "Key9": 9}, {"Key0": 0, "Key1": 1, "Key2": 2, "Key3": 3, "Key4": 4, "Key5": 5, "Key6": 6, "Key7": 7, "Key8": 8, "Key9": 9}, {"Key0": 0, "Key1": 1, "Key2": 2, "Key3": 3, "Key4": 4, "Key5": 5, "Key6": 6, "Key7": 7, "Key8": 8, "Key9": 9}, {"Key0": 0, "Key1": 1, "Key2": 2, "Key3": 3, "Key4": 4, "Key5": 5, "Key6": 6, "Key7": 7, "Key8": 8, "Key9": 9}, {"Key0": 0, "Key1": 1, "Key2": 2, "Key3": 3, "Key4": 4, "Key5": 5, "Key6": 6, "Key7": 7, "Key8": 8, "Key9": 9}, {"Key0": 0, "Key1": 1, "Key2": 2, "Key3": 3, "Key4": 4, "Key5": 5, "Key6": 6, "Key7": 7, "Key8": 8, "Key9": 9}, {"Key0": 0, "Key1": 1, "Key2": 2, "Key3": 3, "Key4": 4, "Key5": 5, "Key6": 6, "Key7": 7, "Key8": 8, "Key9": 9}, {"Key0": 0, "Key1": 1, "Key2": 2, "Key3": 3, "Key4": 4, "Key5": 5, "Key6": 6, "Key7": 7, "Key8": 8, "Key9": 9}, {"Key0": 0, "Key1": 1, "Key2": 2, "Key3": 3, "Key4": 4, "Key5": 5, "Key6": 6, "Key7": 7, "Key8": 8, "Key9": 9}]'

o = json.loads(text)

print(type(o))
print(type(o[0]))
```

This worked: the object `o` is a list of dictionaries as we expected:

```
<class 'list'>
<class 'dict'>
```

Now you can use it as a standard python object.

What about reading it from file:

```python
import json

with open('/tmp/test1.json', 'rt') as f:
  o = json.load(f)

print(type(o))
print(type(o[0]))
```

Worked perfectly too:

```
<class 'list'>
<class 'dict'>
```

## Requests + json ##

Now that we both know about `json` and `requests`, let's try to put them together!

Imagine that you have to make an API call, and you know the API server can return json: how can you use it ?

```python
import json
import requests
s = requests.Session()
s.headers['Accept'] = 'application/json'
s.verify = True
r = s.get('https://httpbin.org/get')
if r.status_code == requests.codes.ok:
  o = json.loads(r.content)
print(o.keys())
print(o.get('headers',dict()).get('User-Agent'))
```

And the json response is now a python object, which we can inspect and use as we like:

```
dict_keys(['args', 'headers', 'origin', 'url'])
python-requests/2.25.1
```

Some websites and API servers might refuse to serve your requests if the User-Agent does not look like a browser, so you might want to change it in the session's headers.

That completes the lesson. You should now be ready to move on to some additional topics. [Click here to return to the lesson list](../README.md)
