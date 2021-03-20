# Lesson 10 - Modules: Part 6: logging #

In this lesson we talk about logging

## Basics ##

Python has a `logging` module, which is part of the standard library.

You might be tempted to use `print`, or better `sys.stdout.write`, but in most cases `logging` is much better.

This is because most of the other modules, in the standard library or third party, will use `logging`, and that means that you might otherwise end up with different behaviours.

And using the `logging` module is not that more difficult that using `print`:

```python
import logging

logging.warning('Something is about to happen')
```

This will produce:

```
WARNING:root:Something is about to happen
```

The first part of the output is the log level, in this case "WARNING", the second part is the name of the logger, in this case "root", and then the message.

Logging using the root is usually not a good idea, because it doesn't tell the reader who actually was producing the message. You can use `logging.getLogger` to create a logger for your application or module, and then use that instead.

The `logging` module implements "hierarchical" logging, where all the loggers are descendant of `root`, and unless you change configuration of child modules, the configuration of the parent apply, meaning that you can make changes to the root logger in your application, and expect all the modules to follow your configuration.

## Logger set up ##

If you are writing a module, you should probably refrain from making changes to the logger, and instead just focus on logging, leaving the responsibility of the configuration to the application that uses your module.

Typically the sequence of logging related events in a module would be something like this:

-	Import the module
-	Create a logger that is specific to the module
-	Use the dedicated logger to log messages at various levels

A hypothetical module would look like this:

```python
import logging

logger = logging.getLogger(__name__)

def somefunction():
  […]
  logger.info('Starting to do something')
  […]
  if result is None:
    logger.error('This something did nto work very well')
  logger('Finished something')
```

The hierarchy of modules is implemented with the name, and the separator is the dot (`.`), so if you have different modules in a package, or if you just want to split your module in several different levels anyway, you can use something like `logger = logging.getLogger('something.somethingelse')`.

If, on the other hand, you are writing a script, rather than a module, you are entitled to configure your logging.

The easiest way to do this is to use `basicConfig`. You can either use `logging.basicConfig`, with the consequence that this will be applied to all the logging in any (nicely behaving) modules you are using.

There are typically 3 aspects of logging that you might want to change:
-	Level, that is the level threshold where you will suppress the logs
-	Handlers, which means where the logs will be sent to (e.g. to a file, to the screen, a syslog server, etc.)
-	Formatting, which means what each log line will look like, or what information is included in each log entry

### Levels ###

Log levels are assigned a certain value:

```python
logging.CRITICAL = 50
logging.ERROR = 40
logging.WARNING = 30
logging.INFO = 20
logging.DEBUG = 10
logging.NOTSET = 0
```

You can use the `setLevel`, either locally on the logger, or on the root logger, with `logging.setLevel`, to change the threshold used to suppress log entries. Any log message below the threshold will be suppressed.

By default the root level is `logging.WARNING`, meaning that INFO and lower will be suppressed:

Some indication on where to use the various levels:

-	**DEBUG** Detailed information, typically of interest only when diagnosing problems.
-	**INFO** Confirmation that things are working as expected.
-	**WARNING** An indication that something unexpected happened, or indicative of some problem in the near future (e.g. ‘disk space low’). The software is still working as expected.
-	**ERROR** Due to a more serious problem, the software has not been able to perform some function.
-	**CRITICAL** A serious error, indicating that the program itself may be unable to continue running.

```python
import logging

logging.warning('Something is about to happen')
logging.info('Today the weather is nice')
```

Will produce this output:

```
WARNING:root:Something is about to happen
```

```python
import logging
logging.getLogger().setLevel(logging.DEBUG)
logging.warning('Something is about to happen')
logging.info('Today the weather is nice')
```

Now it will produce the output also for INFO level:

```
WARNING:root:Something is about to happen
INFO:root:Today the weather is nice
```

`basicConfig` has a `level` parameter that can be used to initialise the logger to be at a certain level, but maybe what you really want to do is to use `argparse`, and allow the user to define what level to use, something like this:

```python
import argparse
import logging

logger = logging.getLogger(__main__)

def getArgs():
  """
    get the cli arguments
  """
  parser = argparse.ArgumentParser(
      description='Some script',
      formatter_class=argparse.ArgumentDefaultsHelpFormatter
      )
  parser.add_argument('-D', '--debug', action='store_true',
                      required=False, default=False,
                      help='Set the debug level to DEBUG')
  return parser.parse_args()

if __name__ == "__main__":
  args = getArgs()
  if args.debug:
    logging.getLogger().setLevel(logging.DEBUG)
  else:
    logging.getLogger().setLevel(logging.INFO)
  logger.info("About to start doing whatever")
```

This way, if the script works fine, the output will be terse, but if something goes wrong, one can re-run the script with `--debug` or `-D`, and the output will be much more detailed.

### Formats ###

The default format is brief, but if you want, you can customise it, the documentation on how to determine what you can do in the format is [here](https://docs.python.org/3/library/logging.html#formatter-objects).

There are 2 ways to set the format, the easiest is to use the `basicConfig`, for example like this:

```python
import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(module)s:%(lineno)d- %(levelname)s - %(message)s')
logging.warning('Something is about to happen')
```

```
2021-03-25 16:10:37,876 - root - test1:3- WARNING - Something is about to happen
```

The other, less preferred, option is to use the `Handler.setFormatter` method, after creating one. We will see Handlers in the next chapter, so we will see an example of setting a formatter this way in the next chapter.

### Handlers ###

A handler is an object that describers what to do with logs.

The `logging` module has several examples of handler, including:

-	`StreamHandler`, which writes to a stream, such as `sys.stderr` (the default when logging is set up)
-	`FileHandler`, for writing to a single file
-	`NullHandler` to discard everything
-	`WatchedFileHandler`, which is similar to `FileHandler`, but it is compatible with tools like `logrotate`
-	`RotatingFileHandler` and `TimedRotatingFileHandler`, which are similar to `FileHandler`, but rotate the file on its own based on size or time parameters respectively.
-	`SocketHandler` and `DatagramHandler`, which is similar to the `StreamHandler`, but it logs to a TCP or UDP socket respectively.
-	`SysLogHandler`, which logs to a local or remote syslog.

We don't need to review all of them, just know that they exist, the documentation is quite good to help you decide which one is more suitable for your situation.

What we will see here is how to add a handler to a logger:

Let;'s say we want to log to `sys.stderr`, but if an option is set, also to a file, and we want to set the format too

```python
import logging
import argparse
import sys


logger = logging.getLogger(__name__)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(module)s:%(lineno)d- %(levelname)s - %(message)s')

handler = logging.StreamHandler(sys.stderr)
handler.setFormatter(formatter)
handler.set_name('Default')
logger.addHandler(handler)

def getArgs():
  """
    get the cli arguments
  """
  parser = argparse.ArgumentParser(
      description='Some script',
      formatter_class=argparse.ArgumentDefaultsHelpFormatter
      )
  parser.add_argument('-D', '--debug', action='store_true',
                      required=False, default=False,
                      help='Set the debug level to DEBUG')
  parser.add_argument('-L', '--logtofile', action='store',
                      help='Also log to this file')
  return parser.parse_args()

if __name__ == "__main__":
  args = getArgs()
  if args.debug:
    logging.getLogger().setLevel(logging.DEBUG)
  else:
    logging.getLogger().setLevel(logging.INFO)
  logger.info("About to start doing whatever")
  if args.logtofile is not None:
    logger.debug('Adding file handler pointing to %s', args.logtofile)
    fhl = logging.FileHandler(args.logtofile)
    fhl.setFormatter(formatter)
    fhl.set_name(__name__+'.file' )
    #Switch to the child logger with the name of the input file, which is os.path.basename(fname)
    logger = logging.getLogger(__name__+'.file')
    logger.addHandler(fhl)
  logger.warning('Something is about to happen')
```

Now, try to run the script with no options, with `-L /tmp/a`, and with `-DL /tmp/a`, and observe the outputs:

With no options, it produces these log entries:

```
% /tmp/test1.py test1.py
2021-03-25 16:39:39,402 - __main__ - test1:36- INFO - About to start doing whatever
2021-03-25 16:39:39,402 - __main__ - test1:45- WARNING - Something is about to happen
```

With `-L` the output didn't seem to have changed

```
% /tmp/test1.py test1.py -L /tmp/a
2021-03-25 16:39:42,960 - __main__ - test1:36- INFO - About to start doing whatever
2021-03-25 16:39:42,960 - __main__.file - test1:45- WARNING - Something is about to happen
```

But let's check the `/tmp/a` file:

```
cat /tmp/a
2021-03-25 16:39:42,960 - __main__.file - test1:45- WARNING - Something is about to happen
```

The logs after the new handler was added are captured here too

We are missing the line telling us that we are adding a file handler, because that is logged at DEBUG level, so we need to add the `-D`:

```
% /tmp/test1.py test1.py -DL /tmp/a
2021-03-25 16:39:46,930 - __main__ - test1:36- INFO - About to start doing whatever
2021-03-25 16:39:46,930 - __main__ - test1:38- DEBUG - Adding file handler pointing to /tmp/a
2021-03-25 16:39:46,931 - __main__.file - test1:45- WARNING - Something is about to happen
```

And the log file now contains the 2 entries:

```
cat /tmp/a
2021-03-25 16:39:42,960 - __main__.file - test1:45- WARNING - Something is about to happen
2021-03-25 16:39:46,931 - __main__.file - test1:45- WARNING - Something is about to happen
```
## Optimisations ##

When preparing a message to be logged, you can use python formatting to merge values into the message itself, but it is recommended to use the older `%` format for compatibility.

This formatting is quite expensive, so it is deferred to the moment when the message is printed, and if the current log level is too high for this message, the merging / formatting is skipped.

This means that you should try to defer as much as possible any sort of formatting operation to the logger, rather than preparing the message yourself before calling the logger's method.

For example:

```python
import logging
logging.info('Printing "%s" is deferred', 'message'')
```

The merging of 'message' to replace the `%s` is deferred, and actually is not performed in this case, since INFO is not printed by default.

It is better to do that rather than something like this:

```python
import logging
message = 'message'
message = 'Printing "' + message + '" is deferred'
logging.info(message)
```

Because in this latter case, the cost of merging is always incurred, even when the log level is not allowing INFO.

## Exceptions ##

One last observation is how to log exceptions?

All the logging methods that log something support the option `exc_info`, and if that is set to True, a backtrace will be printed.

For example: Let's say we have a part of the code that "might" fail, and we want to log it:

```python
import logging
try:
  a = 1/0
except Exception:
  logging.error('Something went wrong')
```

This will print the message, but it won't look very useful for troubleshooting:

```
ERROR:root:Something went wrong
```

Now, let's add `exc_info=True`:

```python
import logging
try:
  a = 1/0
except Exception:
  logging.error('Something went wrong', exc_info=True)
```

```
ERROR:root:Something went wrong
Traceback (most recent call last):
  File "<stdin>", line 2, in <module>
ZeroDivisionError: division by zero
```

Now it looks like a real exception, with the backtrace and the file name and everything.

But you might want to log stacks even without an exception, so you can use `stack_info=True` instead:

```python
import logging
logging.error('Something went wrong', stack_info=True)
```

As you can see, it looks similar, although there was no exception, so you can print this anywhere:

```
ERROR:root:Something went wrong
Stack (most recent call last):
  File "<stdin>", line 1, in <module>
```

Lastly, instead of having to remember to specify `exc_info=True`m you can use `exception`:

```python
import logging
try:
  a = 1/0
except Exception:
  logger.exception('Something went wrong')
```

Which will produce something like this:

```
ERROR:__main__:Something went wrong
Traceback (most recent call last):
  File "<stdin>", line 2, in <module>
ZeroDivisionError: division by zero
```

That completes the lesson. You should now be ready to move on to some additional topics. [Click here to return to the lesson list](../README.md)
