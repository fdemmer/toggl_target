# -*- coding: utf-8 -*-
import argh

#import pprint
from dateutil import parser

from targetlib.togglapi import TogglReportsAPI
from togglcli import settings
from togglcli.helpers import ms_to_hr


api = TogglReportsAPI(settings.API_TOKEN, settings.TIMEZONE)


@argh.arg('workspace-id', help='workspace id')
def weekly(workspace_id):
    data = api.get_weekly(workspace_id)
    #pprint.pprint(data)

    for d in data['data']:
        print d['title']['client'], d['title']['project']
        print "last 7:", [ms_to_hr(ms) for ms in d['totals'][:-1]]
        print "total:", ms_to_hr(d['totals'][-1])


@argh.arg('workspace-id', help='workspace id')
def details(workspace_id):
    data = api.get_details(workspace_id)
    #pprint.pprint(data)

    day = ""
    project = ""
    for d in data['data']:
        this_project = "{} {}".format(d['client'], d['project'])
        if project != this_project:
            project = this_project
            print project
        this_day = parser.parse(d['start']).date().isoformat()
        if day != this_day:
            day = this_day
            print day
        print "- {} ({})".format(d['description'], ms_to_hr(d['dur']))


@argh.arg('workspace-id', help='workspace id')
def summary(workspace_id):
    data = api.get_summary(workspace_id)
    #pprint.pprint(data)

    for d in data['data']:
        print "{} {} ({})".format(
            d['title']['client'],
            d['title']['project'],
            ms_to_hr(d['time']))
        for i in d['items']:
            print "- {} ({})".format(i['title']['time_entry'], ms_to_hr(i['time']))


argh_parser = argh.ArghParser()
argh_parser.add_commands([weekly, details, summary])

if __name__ == '__main__':
    argh_parser.dispatch()
