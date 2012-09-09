#!/usr/bin/env python
# encoding: utf-8
"""
memory.py

Created by Jeremiah Shirk on 2012-09-05.
Copyright (c) 2012 Monitis. All rights reserved.
"""

from monitis.api import get, post, MonitisError, validate_kwargs
import monitis.monitors.predefined.internal as internal

common_required = ['platform', 'name', 'tag']


def add_memory_monitor(**kwargs):
    ''' Add a new internal memory monitor '''
    required = ['agentkey']
    required.extend(common_required)
    optional = ['freeLimit', 'freeSwapLimit', 'freeVirtualLimit',
                'bufferedLimit', 'cachedLimit']
    req_args = validate_kwargs(required, optional, **kwargs)
    return post(action='addMemoryMonitor', **req_args)


def edit_memory_monitor(**kwargs):
    ''' Edit the specified memory monitor '''
    required = ['testId']
    required.extend(common_required)
    optional = ['freeLimit', 'freeSwapLimit', 'freeVirtualLimit',
                'bufferedLimit', 'cachedLimit']
    req_args = validate_kwargs(required, optional, **kwargs)
    return post(action='editMemoryMonitor', **req_args)


def delete_memory_monitors(**kwargs):
    ''' Delete the specified memory monitors '''
    req_args = {'type': 3}  # 3 is the type ID for memory monitors
    req_args.update(kwargs)
    return internal.delete_internal_monitors(**req_args)


def agent_memory(**kwargs):
    ''' Get all internal memory monitors of the specified agent '''
    return internal.agent_monitors(action='agentMemory', **kwargs)


def memory_info(**kwargs):
    ''' Get information regarding the specified internal memory monitor '''
    return internal.internal_info(action='memoryInfo', **kwargs)


def memory_result(**kwargs):
    ''' Get results for the specified internal memory monitor '''
    return internal.internal_result(action='memoryResult', **kwargs)
