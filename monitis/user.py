#!/usr/bin/env python
# encoding: utf-8
"""
user.py

Created by Jeremiah Shirk on 2012-08-25.
Copyright (c) 2012 Monitis. All rights reserved.
"""

from hashlib import md5

from monitis.api import get, resolve_secretkey, resolve_apikey
from monitis.api import post


def auth_token(apikey=None, secretkey=None):
    ''' Generate an auth token

    If the apikey and/or secretkey are not specified as parameters,
    then they will be resolved, if possible.
    '''

    if apikey is None:
        apikey = resolve_apikey()

    if secretkey is None:
        secretkey = resolve_secretkey()

    return get(action='authToken', apikey=apikey,
               secretkey=secretkey)['authToken']


def secretkey(apikey=None):
    ''' The secret key associated with the given API key '''

    if apikey is None:
        apikey = resolve_apikey()

    return get(action='secretkey', apikey=apikey)['secretkey']


def apikey(username, password):
    ''' The API key associated with the given username and password '''

    password_hash = md5()
    password_hash.update(password)
    password_digest = password_hash.hexdigest()

    result = get(action='apikey', userName=username, password=password_digest)
    return result['apikey']


def add_sub_account(first_name, last_name, email, password, group):
    post_args = {'firstName': first_name, 'lastName': last_name,
                 'email': email, 'password': password,
                 'group': group}
    return post(action='addSubAccount', **post_args)


def delete_sub_account(user_id):
    return post(action='deleteSubAccount', userId=user_id)


def sub_accounts(**kwargs):
    ''' The subaccounts associated with the given API key

    Results resturned as a JSON structure
    '''

    return get(action='subAccounts', **kwargs)


def sub_account_pages(**kwargs):
    return get(action='subAccountPages', **kwargs)


def add_sub_account_pages(apikey=None, user_id=None, pages=[]):
    if user_id is None:
        raise MonitisError("user_id is required")
    pages_arg = ';'.join(pages)
    if pages_arg is '':
        raise MonitisError("One or more pages required")
    post_args = {'userId': user_id, 'pageNames': pages_arg}

    return post(action='addPagesToSubAccount', **post_args)


def delete_sub_account_pages(user_id=None, pages=[]):
    if user_id is None:
        raise MonitisError("user_id is required")
    pages_arg = ';'.join(pages)
    if pages_arg is '':
        raise MonitisError("One or more pages required")
    post_args = {'userId': user_id, 'pageNames': pages_arg}

    return post(action='deletePagesFromSubAccount', **post_args)
