#!/usr/bin/env python
# encoding: utf-8
"""
cpu.py

Created by Jeremiah Shirk on 2012-09-03.
Copyright (c) 2012 Monitis. All rights reserved.
"""

from monitis.api import get, post, MonitisError, validate_kwargs
from monitis.monitors.predefined.internal import delete_internal_monitors


def add_cpu_monitor(**kwargs):
    ''' Add a CPU monitor '''
    required = ['agentkey', 'kernelMax', 'usedMax', 'name', 'tag']
    optional = ['idleMin', 'ioWaitMax', 'niceMax']
    req_args = validate_kwargs(required, optional, **kwargs)
    return post(action='addCPUMonitor', **req_args)


def edit_cpu_monitor(**kwargs):
    ''' Edit an existing CPU monitor '''
    required = ['testId', 'kernelMax', 'usedMax', 'name', 'tag']
    optional = ['idleMin', 'ioWaitMax', 'niceMax']
    req_args = validate_kwargs(required, optional, **kwargs)
    return post(action='editCPUMonitor', **req_args)


def delete_cpu_monitors(**kwargs):
    ''' Delete the specified CPU monitors '''
    required = ['testIds']
    optional = []

    req_args = validate_kwargs(required, optional, **kwargs)
    req_args['type'] = 7  # 7 is the type ID for CPU monitors
    return delete_internal_monitors(**req_args)


def agent_cpu(**kwargs):
    ''' Get the CPU monitor of the specified agent '''
    required = ['agentId']
    optional = []
    req_args = validate_kwargs(required, optional, **kwargs)
    return get(action='agentCPU', **req_args)


def cpu_info(**kwargs):
    ''' Get information about the given CPU monitor '''
    required = ['monitorId']
    optional = []
    req_args = validate_kwargs(required, optional, **kwargs)
    return get(action='CPUInfo', **req_args)


def cpu_result(**kwargs):
    ''' Get results of the specified CPU monitor '''
    required = ['monitorId', 'day', 'month', 'year']
    optional = ['timezone']
    req_args = validate_kwargs(required, optional, **kwargs)
    return get(action='cpuResult', **req_args)
