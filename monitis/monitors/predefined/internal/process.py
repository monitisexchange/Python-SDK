#!/usr/bin/env python
# encoding: utf-8
"""
process.py

Created by Jeremiah Shirk on 2012-09-05.
Copyright (c) 2012 Monitis. All rights reserved.
"""

from monitis.api import get, post, MonitisError, validate_kwargs
import monitis.monitors.predefined.internal as internal


common_required = {
    'cpu_limit': 'cpuLimit',
    'memory_limit': 'memoryLimit',
    'virtual_memory_limit': 'virtualMemoryLimit',
    'name': 'name',
    'tag': 'tag'
}


def add_process_monitor(**kwargs):
    ''' Add a new internal process monitor '''
    required = {'agentkey': 'agentkey', 'process_name': 'processName'}
    required.update(common_required)
    optional = {}

    req_args = validate_kwargs(required, optional, **kwargs)
    return post(action='addProcessMonitor', **req_args)


def edit_process_monitor(**kwargs):
    ''' Edit the specified process monitor '''
    required = {'test_id': 'testId'}
    required.update(common_required)
    optional = {}

    req_args = validate_kwargs(required, optional, **kwargs)
    return post(action='editProcessMonitor', **req_args)


def delete_process_monitors(**kwargs):
    ''' Delete the specified process monitors '''
    req_args = {'type': 1}  # 1 is the type ID for process monitors
    req_args.update(kwargs)
    return internal.delete_internal_monitors(**req_args)


def agent_processes(**kwargs):
    ''' Get all internal process monitors of the specified agent '''
    return internal.agent_monitors(action='agentProcesses', **kwargs)


def process_info(**kwargs):
    ''' Get information regarding the specified internal process monitor '''
    return internal.internal_info(action='processInfo', **kwargs)


def process_result(**kwargs):
    ''' Get results for the specified internal process monitor '''
    return internal.internal_result(action='processResult', **kwargs)
