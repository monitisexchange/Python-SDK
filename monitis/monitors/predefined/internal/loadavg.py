#!/usr/bin/env python
# encoding: utf-8
"""
loadavg.py

Created by Jeremiah Shirk on 2012-09-04.
Copyright (c) 2012 Monitis. All rights reserved.
"""

from monitis.api import get, post, MonitisError, validate_kwargs
import monitis.monitors.predefined.internal as internal


common_required = {
    'limit1': 'limit1',
    'limit5': 'limit5',
    'limit15': 'limit15',
    'name': 'name',
    'tag': 'tag'
}


def add_load_average_monitor(**kwargs):
    ''' Add a new internal load monitor '''
    required = {'agentkey': 'agentkey'}
    required.update(common_required)
    optional = {}

    req_args = validate_kwargs(required, optional, **kwargs)
    return post(action='addLoadAverageMonitor', **req_args)


def edit_load_average_monitor(**kwargs):
    ''' Edit the specified load monitor '''
    required = {'test_id': 'testId'}
    required.update(common_required)
    optional = {}

    req_args = validate_kwargs(required, optional, **kwargs)
    return post(action='editLoadAverageMonitor', **req_args)


def delete_load_average_monitors(**kwargs):
    ''' Delete the specified load monitors '''
    req_args = {'type': 6}  # 6 is the type ID for load monitors
    req_args.update(kwargs)
    return internal.delete_internal_monitors(**req_args)


def agent_load_avg(**kwargs):
    ''' Get all internal load monitors of the specified agent '''
    return internal.agent_monitors(action='agentLoadAvg', **kwargs)


def load_avg_info(**kwargs):
    ''' Get information regarding the specified internal load monitor '''
    return internal.internal_info(action='loadAvgInfo', **kwargs)


def load_avg_result(**kwargs):
    ''' Get results for the specified internal load monitor '''
    return internal.internal_result(action='loadAvgResult', **kwargs)
