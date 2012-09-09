#!/usr/bin/env python
# encoding: utf-8
"""
contacts.py

Created by Jeremiah Shirk on 2012-08-28.
Copyright (c) 2012 Monitis. All rights reserved.
"""

from monitis.api import get, post, MonitisError, validate_kwargs


def add_contact(**kwargs):
    ''' Add a new contact

    Required fields: firstName, lastName, account, contactType, timezone.

    Optional fields: group, sendDailyReport, sendWeeklyReport,
    sendMonthlyReport, portable, country, textType

    '''
    required = ['firstName', 'lastName', 'account', 'contactType', 'timezone']
    optional = ['sendDailyReport', 'sendWeeklyReport','sendMonthlyReport',
                'portable', 'country', 'textType']

    post_args = validate_kwargs(required, optional, **kwargs)
    return post(action='addContact', **post_args)


def edit_contact(**kwargs):
    '''  '''
    required = ['contactId']
    optional = ['firstName', 'lastName', 'account', 'contactType', 'timezone',
                'portable', 'code', 'country', 'textType']

    post_args = validate_kwargs(required, optional, **kwargs)
    return post(action='editContact', **post_args)


def delete_contact(**kwargs):
    ''' Delete a contact

    Required fields: contactId, or contactType AND account
    '''
    required = []
    optional = ['contactId', 'contactType', 'account']
    req_args = validate_kwargs(required, optional, **kwargs)

    valid_args = bool(req_args['contactId'] or 
                     (req_args['contactType'] and req_args['account']))

    if not valid_args:
        raise MonitisError('Contact ID or Contact Type and Account required')

    post(action='deleteContact', **req_args)

def confirm_contact(**kwargs):
    ''' Confirm the specified contact '''
    required = ['contactId', 'confirmationKey']
    optional = []

    post_args = validate_kwargs(required, optional, **kwargs)
    return post(action='confirmContact', **post_args)


def contact_activate(**kwargs):
    ''' Activate the specified contact '''
    required = ['contactId']
    optional = []
    post_args = validate_kwargs(required, optional, **kwargs)
    return post(action='contactActivate', **post_args)


def contact_deactivate(**kwargs):
    ''' Deactivate the specified contact '''
    required = ['contactId']
    optional = []
    post_args = validate_kwargs(required, optional, **kwargs)
    return post(action='contactDeactivate', **post_args)


def get_contacts():
    ''' Get user's contacts '''
    return get(action='contactsList')


def get_contact_groups():
    ''' Get all contact groups for the user '''
    return get(action='contactGroupList')


def get_recent_alerts(**kwargs):
    ''' Get recent alerts history

    Start date and end date are in miliseconds since the Epoch'''
    required = []
    optional = ['timezone', 'startDate', 'endDate']
    post_args = validate_kwargs(required, optional, **kwargs)
    return get(action='recentAlerts', **post_args)
