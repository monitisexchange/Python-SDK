#!/usr/bin/env python
# encoding: utf-8
"""
cloud.py

Created by Jeremiah Shirk on 2012-09-05.
Copyright (c) 2012 Monitis. All rights reserved.
"""

from monitis.api import get, post, MonitisError, validate_kwargs


def cloud_instances(**kwargs):
    ''' Get a user's cloud instances

    Parameters:
        timezoneoffset - offset relative to GMT, in minutes
    '''
    required = {}
    optional = {'timezoneoffset': 'timezoneoffset'}

    req_args = validate_kwargs(required, optional, **kwargs)

    return get(action='cloudInstances', **req_args)


def cloud_instance_info(**kwargs):
    ''' Get information for the specified cloud instance '''
    required = {'type': 'type', 'instance_id': 'instanceId'}
    optional = {'timezoneoffset': 'timezoneoffset'}

    req_args = validate_kwargs(required, optional, **kwargs)

    return get(action='cloudInstanceInfo', **req_args)
