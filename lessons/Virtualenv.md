# Lesson 11 - Pip and Virtualenv #

In this lesson we talk about virtualenv

## Virtualenv ##

When you are working with python, you might require different versions, or different installations with different modules, or modules with different versions installed, or maybe you might use a machine where you do not have administrative privileges, so you are not able to install new modules that you need.

To deal with all of the above situations and similar, python has introduced the concept of "Virtualenv", but as it doesn't come with the standard installation, you might still not be able to use it if it is not already installed.

There are multiple variants, but they all do the same thing, here we will look at the module called `virtualenv`, but if you use `venv` instead, or any of the other variants, there will be almost no difference.

### Creating a new virtualenv ###

If you have `virtualenv` installed (it might be called `python-virtualenv` in your system), you will have a command called `virtualenv` in your path:

```shell
% type virtualenv
```

Should say something like this:

```
virtualenv is hashed (/usr/bin/virtualenv)
```

rather than "not found".

If you want to create a new virtual env, you just call `virtualenv` with the path to the new virtualenv to be created (it will be a directory in the filesystem)

```shell
% virtualenv /tmp/firstenv
```

You will see some output, might be similar to this:

```
created virtual environment CPython3.9.2.final.0-64 in 134ms
  creator CPython3Posix(dest=/tmp/firstenv, clear=False, no_vcs_ignore=False, global=False)
  seeder FromAppData(download=False, pip=bundle, setuptools=bundle, wheel=bundle, via=copy, app_data_dir=/home/eturra/.local/share/virtualenv)
    added seed packages: pip==20.3.4, pkg_resources==0.0.0, setuptools==44.1.1, wheel==0.34.2
  activators BashActivator,CShellActivator,FishActivator,PowerShellActivator,PythonActivator,XonshActivator
```

If you check, the `/tmp/firstenv` directory now exists, and it will contain `/tmp/firstenv/bin/activate`, among other things.

### Activating a Virtualenv ###

The `/tmp/firstenv/bin/activate`, or any of the other variants (e.g. there's one for powershell, called `/tmp/firstenv/bin/activate.ps1`, and there should be many other, is used to activate the environment.

In a posix shell, such as bash, you can use the `source` (which can also be called dot, or `.`) to trigger the activation:

```shell
source /tmp/firstenv/bin/activate
```

Depending on how your system is configured, you might not see anything, or you might see your prompt change to mention `firstenv`.

To confirm that it worked, you can check if you now have a function called `deactivate`:

```shell
% type deactivate
```

If you do, the output will be something like this:

```
deactivate is a function
deactivate ()
{
[…]
```

That's the function to exit from the virtualenv.

The `virtualenv` command has a bunch of options, the most interesting are probably: `--python`, to specify a different binary to be used inside that virtualenv, if you have multiple versions, and the `--system-site-packages`, which allows the virtualenv to take advantage of any pre-installed 3rd party modules from the outer environment.

### Caveat ###

If you want to use virtualenv's, it is important that your shebang, in your scripts, are not too restrictive, and allow for the virtualenv to run them.

A very restrictive shebang would be something like this:

```python
#!/usr/bin/python3.9.2
```

Or one that uses a different path

```python
#!/home/vcoders/bin/python3
```

or

```python
#!/usrilocal//bin/python3
```

The best bet is to use `env` with `python3`, because just `python` might not work in some cases, where there's a conflict with python2:

```python
#!/usr/bin/env python3
```

## Pip ##

Once your virtualenv is ready, you can use `pip` to install whatever modules you need.

For example, if you want to install lxml, you can do this:

```shell
(firstenv)% pip install lxml
Collecting lxml
  Downloading lxml-4.6.3-cp39-cp39-manylinux1_x86_64.whl (5.4 MB)
     |████████████████████████████████| 5.4 MB 1.2 MB/s
Installing collected packages: lxml
Successfully installed lxml-4.6.3
```

This will install the latest version available. If you want a specific version, you can specify it to pip too:

```shell
(firstenv)% pip install requests==1.2.3
Collecting requests==1.2.3
  Downloading requests-1.2.3.tar.gz (348 kB)
     |████████████████████████████████| 348 kB 1.5 MB/s
Building wheels for collected packages: requests
  Building wheel for requests (setup.py) ... done
  Created wheel for requests: filename=requests-1.2.3-py3-none-any.whl size=372134 sha256=315c4a9e5d142697d7d5f7c37bf0f1f3c820e534f9c3204c600d248d18dda04b
  Stored in directory: /home/eturra/.cache/pip/wheels/3b/60/57/7d2865f5b0ffceff10b46ee45d6b92b046a6c049e5465d0d13
Successfully built requests
Installing collected packages: requests
Successfully installed requests-1.2.3
```

You can also say `>=`, if your version is the minimum you need to use.

Some times you end up building your project inside a virtualenv over time, and you end up installing a bunch of things, and then you don't remember anymore what you have installed, so you can't tell your friends what they need to install in their virtualenv to run your script.

If that happens, don't worry, because `pip` has a trick for you: `freeze`.

Activate the virtualenv and run `pip freeze`

```shell
(firstenv)% pip freeze
lxml==4.6.3
requests==1.2.3
```

Typically, python projects stored on github or gitlab, have a `requirements.txt` file with all the required modules, produced with `pip freeze`.


```shell
(firstenv)% pip freeze > requirements.txt
```

You probably want to edit the file to remove some things that are not meant to be there, or relax the version locking if necessary.

Later, if you have a new, empty virtualenv, that you want to bring up to speed, all you need to do is `pip install -r requirements.txt` from inside the virtualenv, and your script is ready to go.

That completes the lesson. You should now be ready to move on to some additional topics. [Click here to return to the lesson list](../README.md)
