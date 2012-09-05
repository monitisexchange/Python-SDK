#!/usr/bin/env python
# encoding: utf-8
"""
visitortracker.py

Created by Jeremiah Shirk on 2012-09-05.
Copyright (c) 2012 Monitis. All rights reserved.
"""

from monitis.api import get, post, MonitisError, validate_kwargs


def visitor_tracking_tests(**kwargs):
    ''' Get a user's visitor trackers '''
    required = {}
    optional = {}

    req_args = validate_kwargs(required, optional, **kwargs)

    return get(action='visitorTrackingTests', **req_args)


def visitor_tracking_info(**kwargs):
    ''' get information about the specified Visitor Tracker '''
    required = {'site_id': 'siteId'}
    optional = {}

    req_args = validate_kwargs(required, optional, **kwargs)

    return get(action='visitorTrackingInfo', **req_args)


def visitor_tracking_results(**kwargs):
    ''' Get results of the specified Visitor Tracker '''
    required = {'site_id': 'siteId', 'year': 'year',
                'month': 'month', 'day': 'day'}
    optional = {'timezoneoffset': 'timezoneoffset'}

    req_args = validate_kwargs(required, optional, **kwargs)

    return get(action='visitorTrackingResults', **req_args)
