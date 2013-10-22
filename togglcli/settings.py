# -*- coding: utf-8 -*-
import imp
import os.path

from dateutil.rrule import SA, SU, MO, TU, WE, TH, FR

## default settings

# Toggl API Token
API_TOKEN = None

# Default workspace ID, where appropriate
WORKSPACE_ID = None

# Number Precision
PRECISION = 2

# Target Configurations
WORKING_HOURS_PER_DAY = 8
BUSINESS_DAYS = (SA, SU, MO, TU, WE)
WEEK_DAYS = (SA, SU, MO, TU, WE, TH, FR)
TOLERANCE_PERCENTAGE = 0.1

# Timezone
TIMEZONE = '+02:00'

# Salary Configurtions
SHOW_SALARY = False
SALARY = 0


## load settings from etc and home directory

SETTINGS_PATH = ["/etc/togglcli/", os.path.expanduser("~/.togglcli/"), ]

fp, pathname, description = imp.find_module("settings", SETTINGS_PATH)
if fp is not None:
    imp.load_module("togglcli.settings", fp, pathname, description)
