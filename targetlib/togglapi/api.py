#!/usr/bin/python
# -*- coding: utf-8 -*-
#@author Mosab Ahmad <mosab.ahmad@gmail.com>
import logging
log = logging.getLogger(__name__)

import requests
from requests.exceptions import RequestException, ConnectionError

from urllib import urlencode
from requests.auth import HTTPBasicAuth

TOGGL_API_URL = "https://www.toggl.com/api/v8/"
REPORTS_API_URL = "https://toggl.com/reports/api/v2/"

REPORT_TYPES = ["weekly", "details", "summary"]

JSON_HEADER = {'content-type': 'application/json'}

USER_AGENT = "toggl_target"


class TogglAPI(object):
    """A wrapper for Toggl API v8"""

    def __init__(self, api_token, timezone):
        self.api_token = api_token
        self.timezone = timezone

    def _make_url(self, section='time_entries', params={}):
        """Constructs and returns an api url to call with the section of the API to be called
        and parameters defined by key/pair values in the paramas dict.
        Default section is "time_entries" which evaluates to "time_entries.json"

        >>> t = TogglAPI('_SECRET_TOGGLE_API_TOKEN_')
        >>> t._make_url(section='time_entries', params = {})
        'https://www.toggl.com/api/v8/time_entries'

        >>> t = TogglAPI('_SECRET_TOGGLE_API_TOKEN_')
        >>> t._make_url(section='time_entries', params = {'start_date' : '2010-02-05T15:42:46+02:00', 'end_date' : '2010-02-12T15:42:46+02:00'})
        'https://www.toggl.com/api/v8/time_entries?start_date=2010-02-05T15%3A42%3A46%2B02%3A00%2B02%3A00&end_date=2010-02-12T15%3A42%3A46%2B02%3A00%2B02%3A00'
        """
        url = TOGGL_API_URL + section
        if params:
            url = url + '?' + urlencode(params)
        return url

    def _query(self, url, method):
        """Performs the actual call to Toggl API"""
        if method == 'GET':
            return requests.get(url, headers=JSON_HEADER, auth=HTTPBasicAuth(self.api_token, 'api_token'))
        elif method == 'POST':
            return requests.post(url, headers=JSON_HEADER, auth=HTTPBasicAuth(self.api_token, 'api_token'))
        else:
            raise ValueError('Undefined HTTP method "{}"'.format(method))

    ## Time Entry functions
    def get_time_entries(self, start_date='', end_date='', timezone=''):
        """Get Time Entries JSON object from Toggl"""

        url = self._make_url(section='time_entries', params={'start_date': start_date+self.timezone, 'end_date': end_date+self.timezone})
        r = self._query(url=url, method='GET')
        return r.json()

    def get_hours_tracked(self, start_date, end_date):
        """Count the total tracked hours excluding any RUNNING real time tracked time entries"""
        time_entries = self.get_time_entries(start_date=start_date.isoformat(), end_date=end_date.isoformat())

        if time_entries is None:
            return 0

        total_seconds_tracked = sum(max(entry['duration'], 0) for entry in time_entries)

        return (total_seconds_tracked / 60.0) / 60.0


class TogglReportsAPI(TogglAPI):
    """
    Toggl Reports API v2 wrapper.
    """
    def __init__(self, api_token, timezone, **kwargs):
        """
        :param api_url: override the default api url
        """
        super(TogglReportsAPI, self).__init__(api_token, timezone)
        self.user_agent = USER_AGENT
        self.api_url = kwargs.get('api_url', REPORTS_API_URL)
        # make sure the url ends with a / to append a report_type savely later
        if not self.api_url.endswith('/'):
            self.api_url = self.api_url + '/'

    def _make_url(self, report_type='weekly'):
        """
        :param report_type: "weekly", "details" or "summary"
        """
        if report_type not in REPORT_TYPES:
            log.error("Invalid report_type ({}).".format(report_type))
            raise ValueError("Invalid report_type ({}).".format(report_type))
        return self.api_url + report_type

    def _query(self, report_type, **kwargs):
        params = {'user_agent': self.user_agent}
        params.update(kwargs)

        url = self._make_url(report_type)
        auth = HTTPBasicAuth(self.api_token, 'api_token')
        try:
            return requests.get(url, headers=JSON_HEADER, auth=auth,
                params=params)
        except ConnectionError:
            log.error("ConnectionError: %s %s", self.api_url, params)
            raise RequestException

    def get_report(self, report_type, workspace_id, **kwargs):
        """
        Fetch some kind of report.
        """
        response = self._query(report_type, workspace_id=workspace_id, **kwargs)
        if response is not None and response.status_code == 200:
            data = response.json()
            return data

    def get_weekly(self, workspace_id, **kwargs):
        """
        Fetch a weekly report (last 7 days actually).
        """
        return self.get_report("weekly", workspace_id, **kwargs)

    def get_details(self, workspace_id, **kwargs):
        """
        Fetch a detailed report.
        """
        return self.get_report("details", workspace_id, **kwargs)

    def get_summary(self, workspace_id, **kwargs):
        """
        Fetch a summary report.
        """
        return self.get_report("summary", workspace_id, **kwargs)


if __name__ == '__main__':
    import doctest
    doctest.testmod()
