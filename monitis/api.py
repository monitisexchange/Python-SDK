#!/usr/bin/env python
# encoding: utf-8
"""
api.py

Created by Jeremiah Shirk on 2011-10-01.
Copyright (c) 2011 Monitis. All rights reserved.
"""

import os
from hashlib import sha1
from hmac import new as new_hmac
from base64 import b64encode
from datetime import datetime
from time import time
from urllib import urlencode
from urllib2 import Request, urlopen, HTTPError
from json import loads
from copy import deepcopy

class MonitisError(Exception):
    
    '''Errors encountered during interaction with the Monitis API
    
    On encountering an error, the Monitis API web service will return either
    a JSON or XML encoded error response, or else a HTTP error response with
    the error message in the body of the page.  In the case that an HTTP error
    is returned, MonitisError will be raised, with the error in 
    MonitisError.msg.
    '''
    
    msg = None
    
    def __init__(self, msg):
        Exception.__init__(self, msg)
        self.msg = msg
    
    def __str__(self):
        return 'MonitisError({0})'.format(self.msg)

# API operations on existing instances are methods
# Other API operations, new operations, and helpers are functions

def decode_json(json=None):
    '''Deserialize json to a python object.'''
    try:
        return loads(json)
    except ValueError, error:
        raise MonitisError(': '.join(['JSON parse error', str(error)]))

def environ_key(name=None):
    """Helper method to get a key from os.environ
    
    Return value of environment variable name if it exists, None otherwise
    """
    try:
        return os.environ[name]
    except KeyError:
        return None

def resolve_apikey():
    """Resolve the Monitis API Key from the invoking shell
    
    Find the API Key in the shell environment variable MONITIS_APIKEY
    """
    return environ_key('MONITIS_APIKEY')

def resolve_secretkey():
    """Resolve the Monitis Secret Key from the invoking shell
    
    Find the API Key in the shell environment variable MONITIS_SECRETKEY
    """
    return environ_key('MONITIS_SECRETKEY')

def timestamp():
    """Timestamp in the format required for Monitis API post requests
    
    Return a string containing current datetime in GMT 
    with yyyy-MM-dd HH:mm:ss format
    """
    return datetime.utcnow().strftime("%F %T")

def checktime():
    """Timestamp in the format required for monitor results

    Returns a string containing number of milliseconds 
    since January 1, 1970, 00:00:00 GMT
    """
    return str(int(time())) + "000"

def get(apikey=None, action=None, version='2',
        url='http://monitis.com/api', **kwargs):
    """GET requests to the Monitis API
    
    Returns Python objects based on the JSON-encoded responses
    """

    output = 'JSON' # don't allow XML, so we can parse JSON response
    apikey = apikey or resolve_apikey()
    
    # sanity checks
    if not apikey:
        raise MonitisError("get: apikey is required")
    if not action:
        raise MonitisError("get: action is required")
    
    # build the request
    req_params = [('apikey', apikey), ('action', action),
                 ('output', output), ('version', version)]
    req_params.extend(kwargs.items())
    req_url = url + '?' + urlencode(req_params)

    # make the request
    if Monitis.debug is True:
        print "Request URL: " + req_url
    req = Request(req_url)
    try:
        res = urlopen(req)
    except HTTPError, error:
        raise MonitisError('API Error: ' + error.read())
    res_json = res.read()
    if Monitis.debug is True:
        print "Response: " + res_json
    
    # build a python object out of the result
    return decode_json(res_json)

class Monitis:
    
    '''Encapsulate the Monitis API
    
    Encapsulate the Monitis RESTFUL API, to be subclassed by specific
    components of the API.
    
    '''
    
    debug = False
    
    def __init__(self, apikey=None, secretkey=None, url=None,
                 version=None, validation=None):
        '''Create a new Monitis object'''
        self.auth_token = None
        self.url = url or 'http://monitis.com/api'
        self.apikey = apikey or resolve_apikey()
        self.secretkey = secretkey or resolve_secretkey()
        self.validation = validation or 'HMACSHA1' # TODO: implement authToken
        self.version = version or '2'

    def post(self, **kwargs):
        """Post the dict in post_args to the Monitis REST API"""
        post_args = deepcopy(kwargs)
        post_args['apikey'] = self.apikey
        post_args['version'] = self.version
        post_args['timestamp'] = timestamp()

        # calculate a checksum based on the values and secret key
        post_checksum = self.checksum(**post_args)

        # use urllib to post the values
        post_args['checksum'] = post_checksum
        
        params = urlencode(post_args)
        try:
            if Monitis.debug is True:
                print "Request URL: " + self.url
                print "Request params: " + str(post_args)
            result = urlopen(self.url, params)
        except HTTPError, error:
            raise MonitisError('API Error: ' + error.read())
        ret = result.read()
        if Monitis.debug is True:
            print "Response: " + ret
        result.close()
        return ret

    def checksum(self, **kwargs):
        """Base64-encoded HMAC signature of the parameters string
        
        The checksum is caclulated as documented at:
            
            http://monitis.com/api/api.html#checkSum
            
            - sort all request parameters alphabetically by param name
            - join param-value pairs in a string: param1value1param2value2...
            - return Base64-encoded RFC 2104-compliant HMAC signature of the 
              constructed string using your secrect key
        """
        try:
            # if a secretkey is in **kwargs, use it, and remove it
            secretkey = kwargs['secretkey']
            del kwargs['secretkey']
        except KeyError:
            # if the kwargs lookup fails, get secretkey elsewhere
            secretkey = self.secretkey or resolve_secretkey()
        args = kwargs.items()
        args.sort()
        
        param_string = ''
        for key, value in args:
            param_string += str(key)
            param_string += str(value)
        return b64encode(str(new_hmac(secretkey, param_string, sha1).digest()))
        

