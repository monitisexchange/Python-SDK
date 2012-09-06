#!/usr/bin/env python
# encoding: utf-8
"""
fullpageload.py

Created by Jeremiah Shirk on 2012-09-05.
Copyright (c) 2012 Monitis. All rights reserved.
"""

from monitis.api import get, post, MonitisError, validate_kwargs


def add_full_page_load_monitor(**kwargs):
    ''' Add a new full page load monitor '''
    required = {'name': 'name', 'tag': 'tag', 'location_ids': 'locationIds',
                'check_interval': 'checkInterval', 'url': 'url',
                'timeout': 'timeout'}
    optional = {'uptime_sla': 'uptimeSLA', 'response_sla': 'responseSLA'}

    req_args = validate_kwargs(required, optional, **kwargs)
    location_ids = req_args['locationIds']
    if isinstance(location_ids, list):
        req_args['locationIds'] = ','.join(location_ids)

    return post(action='addFullPageLoadMonitor', **req_args)


def edit_full_page_load_monitor(**kwargs):
    ''' Edit an existing full page load monitor '''
    required = {'name': 'name', 'tag': 'tag', 'location_ids': 'locationIds',
                'check_interval': 'checkInterval', 'url': 'url',
                'timeout': 'timeout', 'monitor_id': 'monitorId'}
    optional = {'uptime_sla': 'uptimeSLA', 'response_sla': 'responseSLA'}

    req_args = validate_kwargs(required, optional, **kwargs)
    location_ids = req_args['locationIds']
    if isinstance(location_ids, list):
        req_args['locationIds'] = ','.join(location_ids)

    return post(action='editFullPageLoadMonitor', **req_args)


def delete_full_page_load_monitor(**kwargs):
    ''' Delete an existing full page load monitor '''
    required = {'monitor_id': 'monitorId'}
    optional = {}

    req_args = validate_kwargs(required, optional, **kwargs)
    monitor_id = req_args['monitorId']
    if isinstance(monitor_id, list):
        req_args['monitorId'] = ','.join(monitor_id)
    return post(action='deleteFullPageLoadMonitor', **req_args)


def suspend_full_page_load_monitor(**kwargs):
    ''' Suspend full page load monitors '''
    required = {}
    optional = {'monitor_ids': 'monitorIds', 'tag': 'tag'}

    req_args = validate_kwargs(required, optional, **kwargs)

    return post(action='suspendFullPageLoadMonitor', **req_args)


def activate_full_page_load_monitor(**kwargs):
    ''' Activate full page load monitors '''
    required = {}
    optional = {'monitor_ids': 'monitorIds', 'tag': 'tag'}

    req_args = validate_kwargs(required, optional, **kwargs)

    return post(action='activateFullPageLoadMonitor', **req_args)


def full_page_load_test_info(**kwargs):
    ''' Get information about the specified Full Page Load monitor '''
    required = {'monitor_id': 'monitorId'}
    optional = {}

    req_args = validate_kwargs(required, optional, **kwargs)

    return get(action='fullPageLoadTestInfo', **req_args)


def full_page_load_test_result(**kwargs):
    ''' Get results for the specified Full Page Load monitor '''
    required = {'monitor_id': 'monitorId', 'year': 'year',
                'month': 'month', 'day': 'day'}
    optional = {'location_ids': 'locationIds', 'timezone': 'timezone'}

    req_args = validate_kwargs(required, optional, **kwargs)
    location_ids = req_args.get('locationIds', None)
    if isinstance(location_ids, list):
        req_args['locationIds'] = ','.join(location_ids)

    return get(action='fullPageLoadTestResult', **req_args)


def full_page_load_locations(**kwargs):
    ''' Get all locations for full page load monitors '''
    required = {}
    optional = {}

    req_args = validate_kwargs(required, optional, **kwargs)

    return get(action='fullPageLoadLocations', **req_args)


def full_page_load_tests(**kwargs):
    ''' Get all Full Page Load monitors '''
    required = {}
    optional = {}

    req_args = validate_kwargs(required, optional, **kwargs)

    return get(action='fullPageLoadTests', **req_args)
