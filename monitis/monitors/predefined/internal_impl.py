#!/usr/bin/env python
# encoding: utf-8
"""
internal.py

Created by Jeremiah Shirk on 2012-09-04.
Copyright (c) 2012 Monitis. All rights reserved.
"""

from monitis.api import get, post, MonitisError, validate_kwargs


def internal_monitors(**kwargs):
    ''' Get a user's internal monitors

    Monitors returned can be filtered by type, such as:
        - memory
        - load
        - drive
        - process
        - cpu
        - agentHttpTest
        - agentPingTest

    '''
    required = []
    optional = ['types', 'tag', 'tagRegExp']

    req_args = validate_kwargs(required, optional, **kwargs)
    types = req_args.get('types', None)
    if isinstance(types, list):
        req_args['types'] = ','.join(types)
    return get(action='internalMonitors', **req_args)


def delete_internal_monitors(**kwargs):
    ''' Delete the specified internal monitors

    type is the type of the monitors specified in test_ids.  Possible values:
        - 1 for process monitors
        - 2 for drive monitors
        - 3 for memory monitors
        - 4 for internal HTTP monitors
        - 5 for internal ping monitors
        - 6 for load average monitors
        - 7 for CPU monitors
    '''
    required = ['testIds', 'type']
    optional = []
    req_args = validate_kwargs(required, optional, **kwargs)
    return post(action='deleteInternalMonitors', **req_args)


def agent_monitors(**kwargs):
    ''' Helper function to get agent monitors

    This function does not directly map to any specific action in the
    Monitis API.  Rather, it is a helper, and requires that the calling
    function supply the action, in addition to the agent ID.
    '''
    required = ['agentId', 'action']
    optional = []
    req_args = validate_kwargs(required, optional, **kwargs)
    return get(**req_args)


def internal_info(**kwargs):
    ''' Helper function to get info for internal monitors

    This function does not directly map to any specific action in the
    Monitis API.  Rather, it is a helper, and requires that the calling
    function supply the action, in addition to the agent ID.
    '''
    required = ['monitorId', 'action']
    optional = []
    req_args = validate_kwargs(required, optional, **kwargs)
    return get(**req_args)


def internal_result(**kwargs):
    ''' Helper function to get results for internal monitors

    This function does not directly map to any specific action in the
    Monitis API.  Rather, it is a helper, and requires that the calling
    function supply the action, in addition to the agent ID.
    '''
    required = ['monitorId', 'day', 'month', 'year', 'action']
    optional = ['timezone']
    req_args = validate_kwargs(required, optional, **kwargs)
    return get(**req_args)
