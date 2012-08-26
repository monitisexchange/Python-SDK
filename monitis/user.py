#!/usr/bin/env python
# encoding: utf-8
"""
user.py

Created by Jeremiah Shirk on 2012-08-25.
Copyright (c) 2012 Monitis. All rights reserved.
"""

from hashlib import md5

from monitis.api import get, resolve_secretkey, resolve_apikey


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
