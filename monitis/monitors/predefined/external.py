#!/usr/bin/env python
# encoding: utf-8
"""
external.py

Created by Jeremiah Shirk on 2012-09-01.
Copyright (c) 2012 Monitis. All rights reserved.
"""

from monitis.api import get, post, MonitisError, validate_kwargs


def add_external_monitor(**kwargs):
    ''' add a new External monitor '''
    required = ['type', 'name', 'url', 'interval', 'locationIds', 'tag']
    optional = ['detailedTestType', 'timeout', 'overSSL', 'postData',
                'contentMatchFlag', 'contentMatchString', 'params',
                'uptimeSLA', 'responseSLA', 'basicAuthUser', 'basicAuthPass']
    req_args = validate_kwargs(required, optional, **kwargs)

    # params required only for DNS and MySQL
    test_type = req_args.get('type')
    if test_type is 'mysql' or test_type is 'dns':
        if not req_args.has_key('params'):
            raise MonitisError('params is required for DNS and MySQL tests')

    # locationIds may be a list
    location_ids = req_args.get('locationIds')
    if type(location_ids) is list:
        req_args['locationIds'] = ','.join(str(x) for x in location_ids)

    return post(action='addExternalMonitor', **req_args)


def edit_external_monitor(**kwargs):
    ''' Edit an external monitor '''
    required = ['testId', 'name', 'url', 'locationIds', 'timeout', 'tag']
    optional = [
        'contentMatchString', 'maxValue', 'uptimeSLA', 'responseSLA'
    ]
    req_args = validate_kwargs(required, optional, **kwargs)

    # locationIds may be a list
    location_ids = req_args.get('locationIds')
    if type(location_ids) is list:
        req_args['locationIds'] = ','.join(str(x) for x in location_ids)
    
    return post(action='editExternalMonitor', **req_args)


def delete_external_monitor(**kwargs):
    ''' Delete one or more external monitors '''
    required = ['testIds']
    optional = []
    req_args = validate_kwargs(required, optional, **kwargs)

    # if test_ids is a list, make a comma delimited string
    test_ids = req_args.get('testIds')
    if type(test_ids) is list:
        req_args['testIds'] = ','.join(test_ids)
    return post(action='deleteExternalMonitor', **req_args)


def suspend_external_monitor(**kwargs):
    ''' Suspend an external monitor '''
    required = []
    optional = ['monitorIds', 'tag']
    req_args = validate_kwargs(required, optional, **kwargs)

    # only one of monitor_ids and tag is required
    if not  (req_args.has_key('monitorIds') or (req_args.has_key('tag'))):
        raise MonitisError('monitorIds or tag is required')

    # monitorIds might be a list
    monitor_ids = req_args.get('monitorIds')
    if type(monitor_ids) is list:
        req_args['monitorIds'] = ','.join(monitor_ids)

    return post(action='suspendExternalMonitor', **req_args)


def activate_external_monitor(**kwargs):
    ''' Suspend an external monitor '''
    required = []
    optional = ['monitorIds', 'tag']
    req_args = validate_kwargs(required, optional, **kwargs)

    # only one of monitor_ids and tag is required
    if not  (req_args.has_key('monitorIds') or (req_args.has_key('tag'))):
        raise MonitisError('monitorIds or tag is required')

    # monitorIds might be a list
    monitor_ids = req_args.get('monitorIds')
    if type(monitor_ids) is list:
        req_args['monitorIds'] = ','.join(monitor_ids)

    return post(action='activateExternalMonitor', **req_args)


def locations(**kwargs):
    ''' Get all of the locations for the user's external monitors '''
    required = []
    optional = []
    req_args = validate_kwargs(required, optional, **kwargs)
    return get(action='locations', **req_args)


def tests(**kwargs):
    ''' Get all external monitors for the user '''
    required = []
    optional = []
    req_args = validate_kwargs(required, optional, **kwargs)
    return get(action='tests', **req_args)


def testinfo(**kwargs):
    ''' Get information for the specified external monitor '''
    required = ['testId']
    optional = ['timezone']
    req_args = validate_kwargs(required, optional, **kwargs)
    return get(action='testinfo', **req_args)


def testresult(**kwargs):
    ''' Get results of the specified External monitor '''
    required = ['testId', 'day', 'month', 'year']
    optional = ['locationIds', 'timezone']
    req_args = validate_kwargs(required, optional, **kwargs)

    # locationIds may be a list
    location_ids = req_args.get('locationIds')
    if type(location_ids) is list:
        req_args['locationIds'] = ','.join(location_ids)

    return get(action='testresult', **req_args)


def tests_last_values(**kwargs):
    ''' Get the last results of a user's external monitors '''
    required = []
    optional = ['locationIds']
    req_args = validate_kwargs(required, optional, **kwargs)

    # locationIds may be a list
    location_ids = req_args.get('locationIds')
    if type(location_ids) is list:
        req_args['locationIds'] = ','.join(location_ids)

    return get(action='testsLastValues', **req_args)


def tags(**kwargs):
    ''' Get all tags for the user's external monitors '''
    required = []
    optional = []
    req_args = validate_kwargs(required, optional, **kwargs)
    return get(action='tags', **req_args)


def tagtests(**kwargs):
    ''' Get external monitors for the specified tag '''
    required = ['tag']
    optional = []
    req_args = validate_kwargs(required, optional, **kwargs)
    return get(action='tagtests', **req_args)

