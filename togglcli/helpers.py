# -*- coding: utf-8 -*-

from togglcli import settings
from targetlib.togglapi import TogglAPI

def ms_to_hr(ms):
    """
    Convert a string or number in milliseconds to a float in hours.
    """
    if ms is not None:
        return float(ms)/3600000.0
    return 0.0

def default_workspace_id(workspace_id=None):
    """Produce a default workspace ID"""

    # Return the input if we don't need to default it
    if workspace_id is not None and workspace_id != 'default':
        return workspace_id

    # Return an explicit default if set in settings.py
    try:
        if settings.WORKSPACE_ID is not None:
            return settings.WORKSPACE_ID
    except:
        pass

    # Return the user's first (often the only) workspace
    api = TogglAPI(settings.API_TOKEN, settings.TIMEZONE)
    workspaces = api.get_workspaces()
    default_workspace = workspaces[0]
    return default_workspace['id']
