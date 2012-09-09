#!/usr/bin/env python
# encoding: utf-8
"""
ping.py

Created by Jeremiah Shirk on 2012-09-04.
Copyright (c) 2012 Monitis. All rights reserved.
"""

from monitis.api import get, post, MonitisError, validate_kwargs
import monitis.monitors.predefined.internal as internal

common_required = ['maxLost', 'packetsCount', 'packetsSize', 'timeout',
                   'name', 'tag']


def add_internal_ping_monitor(**kwargs):
    ''' Add a new internal ping monitor '''
    required = ['userAgentId', 'url']
    required.extend(common_required)
    optional = []
    req_args = validate_kwargs(required, optional, **kwargs)
    return post(action='addInternalPingMonitor', **req_args)


def edit_internal_ping_monitor(**kwargs):
    ''' Edit the specified Ping monitor '''
    required = ['testId']
    required.extend(common_required)
    optional = []
    req_args = validate_kwargs(required, optional, **kwargs)
    return post(action='editInternalPingMonitor', **req_args)


def delete_internal_ping_monitors(**kwargs):
    ''' Delete the specified Ping monitors '''
    req_args = {'type': 5}  # 5 is the type ID for Ping monitors
    req_args.update(kwargs)
    return internal.delete_internal_monitors(**req_args)


def agent_ping_tests(**kwargs):
    ''' Get all internal Ping monitors of the specified agent '''
    return internal.agent_monitors(action='agentPingTests', **kwargs)


def internal_ping_info(**kwargs):
    ''' Get information regarding the specified internal Ping monitor '''
    return internal.internal_info(action='internalPingInfo', **kwargs)


def internal_ping_result(**kwargs):
    ''' Get results for the specified internal Ping monitor '''
    return internal.internal_result(action='internalPingResult', **kwargs)
