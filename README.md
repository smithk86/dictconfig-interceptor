# dictconfig-interceptor

# About

This module was originally developed to be used with [logging518](https://github.com/mharrisb1/logging518).

Unlike using `logging.config.fileConfig()`, where the goal is to have a seperate configuration file for each environment, the goal of `logging518.config.fileConfig()` is to have a single logging configuration for an entire project defined in `pyproject.toml` (or similarly named toml file).

Using `with dictconfig_interceptor.dictConfigCallbacks()` allows one or more callbacks to be defined which will then perform additional processing to the config dictionary which is passed to `logging.config.dictConfig()`. This can be helpful with using a third-party module, like `logging518`, which is ultimately calling `dictConfig()` but in a way to which the user has no direct access.

# Example

```python
import os
import logging518.config
from dictconfig_interceptor import dictConfigCallbacks

# create a context which will store the callbacks
with dictConfigCallbacks() as callbacks:

  # callback to change set the root level
  @callbacks
  def set_root_level(config):
     config["root"]["level"] = os.environ.get("LOGLEVEL", "WARN")
 
  # callback to change the filename of the "file" handler
  @callbacks
  def set_filename(config):
     config["handlers"]["file"]["filename"] = os.environ.get("LOGFILENAME", "app.log")

  # commit the logging configurations which will also process the callbacks defined in the current context
  logging518.config.fileConfig("pyproject.toml")

```
