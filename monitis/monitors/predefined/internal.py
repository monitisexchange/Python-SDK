#!/usr/bin/env python
# encoding: utf-8
"""
internal.py

Created by Jeremiah Shirk on 2012-09-02.
Copyright (c) 2012 Monitis. All rights reserved.
"""

from monitis.api import get, post, MonitisError, validate_kwargs


def agents(**kwargs):
    ''' Get a user's agents '''
    required = {}
    optional = {'key_reg_exp': 'keyRegExp'}

    req_args = validate_kwargs(required, optional, **kwargs)

    return get(action='agents', **req_args)


def agent_info(**kwargs):
    ''' Get information regarding the specified agent '''
    required = {'agent_id': 'agentId'}
    optional = {'load_tests': 'loadTests'}

    req_args = validate_kwargs(required, optional, **kwargs)

    return get(action='agentInfo', **req_args)


def all_agents_snapshot(**kwargs):
    ''' Get last results for user's internal monitors '''
    required = {'platform': 'platform'}
    optional = {'timezone': 'timezone',
                'tag': 'tag'}

    req_args = validate_kwargs(required, optional, **kwargs)

    return get(action='allAgentsSnapshot', **req_args)


def agent_snapshot(**kwargs):
    ''' Get last results for all monitors of the specified agent '''
    required = {'agent_key': 'agentKey'}
    optional = {'timezone': 'timezone'}

    req_args = validate_kwargs(required, optional, **kwargs)

    return get(action='agentSnapshot', **req_args)


def delete_agents(**kwargs):
    ''' Delete agent from user's account '''
    required = {}
    optional = {'agent_ids': 'agentIds',     # one of agent_ids or key_reg_exp
                'key_reg_exp': 'keyRegExp'}  # is required

    req_args = validate_kwargs(required, optional, **kwargs)
    if not ('agentIds' in req_args or 'keyRegExp' in req_args):
        raise MonitisError('agent_ids or key_reg_exp is required')

    return post(action='deleteAgents', **req_args)


def download_agent(**kwargs):
    ''' Download the agent

    Returns a raw HTTP Response object instead of parsed JSON
    '''
    required = {'platform': 'platform'}
    optional = {}

    req_args = validate_kwargs(required, optional, **kwargs)
    return post(action='downloadAgent', _raw=True, **req_args)
