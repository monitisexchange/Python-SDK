#!/usr/bin/env python
# encoding: utf-8
"""
drive.py

Created by Jeremiah Shirk on 2012-09-05.
Copyright (c) 2012 Monitis. All rights reserved.
"""

from monitis.api import get, post, MonitisError, validate_kwargs
import monitis.monitors.predefined.internal as internal


common_required = {
    'free_limit': 'freeLimit',
    'name': 'name',
    'tag': 'tag'
}


def add_drive_monitor(**kwargs):
    ''' Add a new internal drive monitor '''
    required = {'agentkey': 'agentkey', 'drive_letter': 'driveLetter'}
    required.update(common_required)
    optional = {}

    req_args = validate_kwargs(required, optional, **kwargs)
    return post(action='addDriveMonitor', **req_args)


def edit_drive_monitor(**kwargs):
    ''' Edit the specified drive monitor '''
    required = {'test_id': 'testId'}
    required.update(common_required)
    optional = {}

    req_args = validate_kwargs(required, optional, **kwargs)
    return post(action='editDriveMonitor', **req_args)


def delete_drive_monitors(**kwargs):
    ''' Delete the specified drive monitors '''
    req_args = {'type': 2}  # 2 is the type ID for drive monitors
    req_args.update(kwargs)
    return internal.delete_internal_monitors(**req_args)


def agent_drives(**kwargs):
    ''' Get all internal drive monitors of the specified agent '''
    return internal.agent_monitors(action='agentDrives', **kwargs)


def drive_info(**kwargs):
    ''' Get information regarding the specified internal drive monitor '''
    return internal.internal_info(action='driveInfo', **kwargs)


def drive_result(**kwargs):
    ''' Get results for the specified internal drive monitor '''
    return internal.internal_result(action='driveResult', **kwargs)
