# Lesson 10 - Modules: Part 1: requests #

In this lesson we talk about the `requests` module

## Intro ##

There are multiple python modules for performing http requests in python, but the easiest to use and most popular is `requests`, which is said to be _"HTTP for Humans"_.

The documentation is [here](https://2.python-requests.org/en/master/).

This module is not part of the main python standard library, so you need to install it, either using the installation tools from your operating system, or with something like `pip`

## Basic Usage ###

Let's start with a small example:

```python
import requests
r = requests.get('http://wttr.in/ballincollig?format=%l:+%t')
print(r.status_code)
print(r.ok)
print(r.content)
print(r.content.decode('utf-8'))
```

This will tell us what's the temperature at the moment in Ballincollig:

```
200
True
b'ballincollig: +7\xc2\xb0C'
ballincollig: +7°C
```

As you can see, the http return code was 200, which is one of the "good" return codes, so `ok` returns `True`.

Also, the response's content is available under `content`, but it is not a string, but bytes (note the `b` in front), which means we need to translate the bytes to string, using `decode`, and we used UTF-8 for that.

Note also that the `get` received the full URL, including parameters, but that's normally not the case.

## Constructor ##

The `get` is a front-end for a `requests` constructor, so it's better to understand how the constructor works, as that will explain what shortcuts `get` is taking.

The constructor has a large amount of parameters, to cover all sort of conditions, we will look at the most commonly used ones:

-	`method`, required, which is any of the http methods, such as 'GET', 'POST' etc.
-	`url`, required
-	`params`, optional, a dictionary with all the http parameters to be added to the URL. This can also be a list of tuples or just bytes, but the most common format is a dictionary
-	`data`, optional, a dictionary, list of tuples, bytes or even a file-like object with the data that should be sent as body of the request (e.g. for a 'POST').
-	`headers`, optional, a dictionary of http headers to include in the request
-	`cookies`, optional, a dictionary or a `CookieJar` object representing the cookies to include in the request
-	`verify`, optional, `True` or `False` to indicate whether the https connection needs to be verified.

There are many more, and the documentation [here](https://requests.readthedocs.io/en/latest/api/) will provide more details

So, the `get` we used earlier to get the temperature, would actually translate to this:

```python
r = requests.request('GET', 'http://wttr.in/ballincollig', params={'format':'%l: %t'})
if r.ok:
  print(r.content.decode('utf-8'))
```

Notice how the parameter for "format" does not contain a `+` but a space: requests takes care of "http encoding" everything, so you don't have to.

## Sessions ##

If you need to do a lot (i.e. more than 1) of requests, you might want to think about using a `requests.Session` rather than doing the requests one by one.

A `Session` allows you to handle cookies automatically, and retain all sort of other settings, without having to repeat them every time.

Additionally, a `Session` implements the methods required for being considered a Context Manager, so you can use the session with `with` and avoid worrying about remembering to cleaning up.

You are probably not going to use `requests` to browse the web, the most likely use-case is scraping some web pages or, even more likely, to make API calls, and for that specifically, you should use a `Session`, if nothing, for the connection pooling functionality, and for centralising the authentication.

For example:

```python
import requests

s = requests.Session()
s.headers['Accept'] = 'application/xml'
s.headers['Content-type'] = `application/xml'
s.verify = False
s.auth = requests.auth.HTTPBasicAuth('admin', 'default')
r = s.get('https://manager.nsx.com/api/1.0/appliance-management/global/info')
if r.status_code == requests.codes.ok:
  print('Successfully connected to the manager')
```

Notice how we used the `requests.codes` to avoid having to hard-code the `200` as response.

But more importantly, look at the `get`: we don't need to remember what type of headers we need to specify, the common ones are all handled in our session! And the authentication too! And the ssl verification!

For the pooling, and other features like retrying to connect, you'll need to look at the `mount` method, which allows you to define protocol handlers. By default `Session` has 2 adapters mounted: `http` and `https`, but you can override them and redefine your own parameters, such as how many times to re-try, and how many connections to pool at the same time, and how many will be waiting (which is useful to avoid hammering the API server into becoming unavailable).

## POST ##

We've seen how to perform a `get`, but what about a `post` ?

If you need to do a POST with a payload, for example if you want to create a new virtual wire in an NSX manager, you need to prepare the payload, for example crafting a dictionary that you then convert to xml or json, and then:

```python
data = craftpayload()
r = s.post('https://manager.nsx.com/api/2.0/vdn/scopes/scopeID/virtualwires', data=data)
if r.status_code == requests.codes.ok:
  print('Successfully connected to the manager')
```

If you want to use a multipart encoding (typically used when you use an html form, but also when, for example, you upload a file), you can do something like the below:

When you upload a file using a form, the file will be uploaded in one of the form's field, so you need to specify the name. In our example we will pretend to start upgrading an NSX manager, and so we know from the documentation that the field is called `file`

```python
import requests
s = requests.Session()
s.headers['Accept'] = 'application/xml'
s.headers['Content-type'] = `application/xml'
s.verify = False
s.auth = requests.auth.HTTPBasicAuth('admin', 'default')

fieldname = 'file'
fname = '/isos/VMware/NSX/NSX_6.2.3a/VMware-NSX-Manager-upgrade-bundle-6.2.3-4167369.tar.gz'
payload = requests.MultipartEncoder(fields={fieldname:(fname, open(fname, 'rb'))})
r = s.post('https://manager.nsx.com/api/1.0/appliance-management/upgrade/uploadbundle/NSX', data=payload, headers={'Content-Type': payload.content_type})
if r.status_code == requests.codes.ok:
  print('Upgrade bundled uploaded successfully')
```

If you want to provide a progress update, you can modify the above to look like this:

```
import sys
import requests
s = requests.Session()
s.headers['Accept'] = 'application/xml'
s.headers['Content-type'] = `application/xml'
s.verify = False
s.auth = requests.auth.HTTPBasicAuth('admin', 'default')

def make_progress_callback(lenght):
   def cb(monitor):
      if monitor.bytes_read == lenght:
         sys.stderr.write("\rProgress: Completed\n")
      else:
         sys.stderr.write("\rProgress: {1}%".format(100*monitor.bytes_read/lenght))

fieldname = 'file'
fname = '/isos/VMware/NSX/NSX_6.2.3a/VMware-NSX-Manager-upgrade-bundle-6.2.3-4167369.tar.gz'
payload = requests.MultipartEncoder(fields={fieldname:(fname, open(fname, 'rb'))})
monitor = requests.MultipartEncoderMonitor(payload, make_progress_callback(sys.stderr, payload.len))
r = s.post('https://manager.nsx.com/api/1.0/appliance-management/upgrade/uploadbundle/NSX', data=monitor, headers={'Content-Type': payload.content_type})
if r.status_code == requests.codes.ok:
  print('Upgrade bundled uploaded successfully')
```

As you can see, it is not enough to know about requests to be able to make API calls, because you need to be able to deal with json and xml objects, but we will see these in one of the next modules.


## Playground ##

If you want to practice with REST API calls with `requests` (or with anything else), you can use [httpbin](https://httpbin.org/), if you don't have already a REST API server at hand.

That completes the lesson. You should now be ready to move on to some additional topics. [Click here to return to the lesson list](../README.md)
