#!/usr/bin/env python
# encoding: utf-8
"""
notifications.py

Created by Jeremiah Shirk on 2012-09-01.
Copyright (c) 2012 Monitis. All rights reserved.
"""

from monitis.api import get, post, MonitisError, validate_kwargs


def add_notification_rule(**kwargs):
    ''' '''
    required = {'monitor_id': 'monitorId',
                'monitor_type': 'monitorType',
                'period': 'period',
                'notify_backup': 'notifyBackup',
                'continuous_alerts': 'continuousAlerts',
                'failure_count': 'failureCount'}

    optional = {'weekday_from': 'weekdayFrom',
                'weekday_to': 'weekdayTo',
                'time_from': 'timeFrom',
                'time_to': 'timeTo',
                'contact_group': 'contactGroup',
                'contact_id': 'contactId',
                'min_failed_location_count': 'minFailedLocationCount',
                'param_name': 'paramName',
                'param_value': 'paramValue',
                'comparing_method': 'comparingMethod'}

    # paramName and paramValue are required when monitorType is custom
    # comparingMethod is required when paramName and paramValue are present
    # either contact_group or contact_id must be specified

    post_args = validate_kwargs(required, optional, **kwargs)
    return post(action='addNotificationRule', **post_args)


def delete_notification_rule(**kwargs):
    ''' '''
    required = {'contact_ids': 'contactIds',
                'monitor_id': 'monitorId',
                'monitor_type': 'monitorType'}

    post_args = validate_kwargs(required, **kwargs)

    # replace list with comma-separated string
    contact_ids = post_args['contactIds']
    if type(contact_ids) is list:
        post_args['contact_ids'] = ','.join(contact_ids)

    return post(action='deleteNotificationRule', **post_args)


def get_notification_rules(**kwargs):
    ''' '''
    required = {'monitor_id': 'monitorId',
                'monitor_type': 'monitorType'}

    get_args = validate_kwargs(required, **kwargs)
    return get(action='getNotificationRules', **get_args)
