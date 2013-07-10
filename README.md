Toggl Target
============

At work, we track our working hours on Toggl (www.toggl.com), so @mos3abof and
@mtayseer created this small project to calculate how many hours they should
work to achieve their monthly goals.

Installation on Linux
---------------------

If you are using linux, you most probably have Python already installed on
your machine. If not, use your distro's package management system to install
Python 2.7

# using a virtualenv is recommended. eg. `mkvirtualenv togglcli`
# clone the source from this repository and `cd` to the source directory
# run `pip install .` to install in your current environment (using the `-e` switch you can install using the source where it is cloned)
# create a configuration file: `~/.togglcli/settings.py`
# get your Toggl API token from your Toggl account's settings and set `API_TOKEN = "<the token>" in `settings.py`
# you may override additional default settings in `settings.py` (find the defaults in `togglcli/settings.py` in the source package)

Installation on Windows
-----------------------

Install Python and pip, then follow the Linux instructions. Put the `.togglcli` directory in your user's home directory.

Usage
-----

To use the script run the following command :

```
$ target.py
```

The output will be something like :

```
Hi
Checking Internet connectivity...
Internet seems fine!

Trying to connect to Toggl, hang on!

So far you have tracked 120.00 hours

Business days left till deadline : 7
Total days left till deadline : 10

Required working hours for this month : 170

To achieve the minimum :
    you should log 4.00 hours every business day
    or log 3.00 hours every day

To achieve the required :
    you should log 7.00 hours every business day
    or log 5.0 hours every day

So far you have achieved:

70.59% [=================================================--------------|------]
```

Authors
-------------

* [@mos3abof](http://www.mos3abof.com)
* [@mtayseer](http://www.mtayseer.net)
* Florian Demmer


Bug Reports & Feature Requests
------------------------------

Please submit any issues or feature requests to the github tracker.
Pull requests welcome!


License
-------

see LICENSE.txt
