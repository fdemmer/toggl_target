# -*- coding: utf-8 -*-


def ms_to_hr(ms):
    """
    Convert a string or number in milliseconds to a float in hours.
    """
    if ms is not None:
        return float(ms)/3600000.0
    return 0.0
