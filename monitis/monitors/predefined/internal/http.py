#!/usr/bin/env python
# encoding: utf-8
"""
http.py

Created by Jeremiah Shirk on 2012-09-04.
Copyright (c) 2012 Monitis. All rights reserved.
"""

from monitis.api import get, post, MonitisError, validate_kwargs
import monitis.monitors.predefined.internal as internal


common_required = {
    'content_match_string': 'contentMatchString',
    'http_method': 'httpMethod',
    'pass_auth': 'passAuth',
    'user_auth': 'userAuth',
    'post_data': 'postData',
    'timeout': 'timeout',
    'name': 'name',
    'tag': 'tag'
}


def add_internal_http_monitor(**kwargs):
    ''' Add a new internal http monitor '''
    required = {'user_agent_id': 'userAgentId',
                'url': 'url',
                'content_match_flag': 'contentMatchFlag',
                'load_full': 'loadFull',
                'over_ssl': 'overSSL',
                'redirect': 'redirect'}
    required.update(common_required)
    optional = {}

    req_args = validate_kwargs(required, optional, **kwargs)
    return post(action='addInternalHttpMonitor', **req_args)


def edit_internal_http_monitor(**kwargs):
    ''' Edit the specified http monitor '''
    required = {'test_id': 'testId', 'url_params': 'urlParams'}
    required.update(common_required)
    optional = {}

    req_args = validate_kwargs(required, optional, **kwargs)
    return post(action='editInternalHttpMonitor', **req_args)


def delete_internal_http_monitors(**kwargs):
    ''' Delete the specified http monitors '''
    req_args = {'type': 5}  # 5 is the type ID for http monitors
    req_args.update(kwargs)
    return internal.delete_internal_monitors(**req_args)


def agent_http_tests(**kwargs):
    ''' Get all internal http monitors of the specified agent '''
    return internal.agent_monitors(action='agentHttpTests', **kwargs)


def internal_http_info(**kwargs):
    ''' Get information regarding the specified internal http monitor '''
    return internal.internal_info(action='internalHttpInfo', **kwargs)


def internal_http_result(**kwargs):
    ''' Get results for the specified internal http monitor '''
    return internal.internal_result(action='internalHttpResult', **kwargs)
