
# DreamPyLib
This is a Python library for interacting with DreamHost's API. It is based on the [work of Laurens Simonis](http://dreampylib.laurenssimonis.com/). Also included are some basic sample scripts which use the library.

## Installation
To install, clone this repo and then run the `setup.py` installation script:
```bash
git clone https://github.com/EliRibble/dreampylib.git
cd dreampylib
python setup.py install
```

Alternatively, if you just want to install for the current user or don't have permissions to install in the site-packages or dist-packages directory, simply use `python setup.py install --user` instead.
 
## Alternative installation method
To install, run the following:
```bash
pip install git+https://github.com/sahoahfoa/dreampylib.git
```

This has the added benefit of being able to use pip to automatically uninstall. `pip uninstall -y dreampylib`

If you just want to install for the current user or don't have permissions to install in the site-packages or dist-packages directory, simply use `pip install --user git+https://github.com/sahoahfoa/dreampylib.git` instead.

## Usage
The original author's [manual](http://dreampylib.laurenssimonis.com/?page_id=7) still mostly applies, but some of the function names have changed to a more pythonic style (i.e. lower-case with underscore separators), and a `user` is no longer needed for API access. See the `dreampylib/example.py` file for a simple example. The basic usage is outlined here, as well.

### Initialization
Either initialize the DreampyLib object with the API key to connect on construction:
```python
import dreampylib
key = '6SHU5P2HLDAYECUM'
connection = dreampylib.DreampyLib(key)
```
or initialize without the key to postpone connection:
```python
connection = dreampylib.DreampyLib()
connection.connect(key)
```

### Inspecting the connection
To verify the connection was established and check the status of the previous API call:
```python
if not connection.is_connected():
    print("Error connecting!")
    print(connection.status())
    return
```

### Checking available commands
Each API key is given access to a specific set of API functions for that user. The following lists the available commands for the given API key:
```python
print('Available commands:\n ')
commands = connection.available_commands()
command_names = [command['cmd'] for command in commands]
print('\n'.join(command_names))
```

### DreamHost API calls

 The DreamHost API [documentation](https://help.dreamhost.com/hc/en-us/sections/203903178-API-Application-Programming-Interface-) gives an outline of the available API commands, expected parameters, and return values. Each category of API calls (e.g. `dns`) has an associated set of functions (e.g. `list_records`). These are of the form `category-function` (e.g. `dns-list_records`). To use these functions with DreampyLib, the `connection` is invoked using an attribute syntax: `connection.category.function(**kwargs)` (e.g. `connection.dns.list_records(account=1234567)`), where `**kwargs` are the named arguments for the API function call.

The return value of these API calls take the form of a tuple with three values:
`success, msg, body = connection.category.function(**kwargs)`

where `success` is a boolean, `msg` is a string containing either `"success"` or the error message, and `body` is the actual content of the API function call return value. (`body` is a list of dictionaries with keys being the names of the table columns.) To view the results of a previous call, use `connection.result()`.

## License
The work by Laurens Simonis originally carried this license:
> Dreampylib is (c) 2009 by Laurens Simonis. Use it at your own risk, do with it whatever you like, but I am not responsible for whatever you do with it.

In the spirit of 'do with it whatever you like', it was put on github under an MIT license on May 7 2014.