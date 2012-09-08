#!/usr/bin/env python
# encoding: utf-8
"""
agent.py

Created by Jeremiah Shirk on 2012-09-08.
Copyright (c) 2012 Monitis. All rights reserved.
"""

from monitis.api import MonitisError, validate_kwargs
from monitis.monitors.custom import custom_get as get
from monitis.monitors.custom import custom_post as post


def add_agent(**kwargs):
    ''' Register a new custom agent in Monitis '''
    required = {'name': 'name'}
    optional = {'params': 'params'}

    req_args = validate_kwargs(required, optional, **kwargs)

    return post(action='addAgent', **req_args)


def add_job(**kwargs):
    ''' Add a job to a custom agent '''
    required = {'agent_id': 'agentId', 'name': 'name', 'type': 'type',
                'interval': 'interval', 'params': 'params'}
    optional = {'monitor_id': 'monitorId'}

    req_args = validate_kwargs(required, optional, **kwargs)

    return post(action='addJob', **req_args)


def edit_agent(**kwargs):
    ''' Edit an existing custom agent '''
    required = {'name': 'name', 'agent_id': 'agentId'}
    optional = {'params': 'params'}

    req_args = validate_kwargs(required, optional, **kwargs)

    return post(action='editAgent', **req_args)


def edit_job(**kwargs):
    ''' Edit an existing custom agent job '''
    required = {'job_id': 'jobId'}
    optional = {'name': 'name', 'type': 'type', 'interval': 'interval',
                'params': 'params', 'active_flag': 'activeFlag'}

    req_args = validate_kwargs(required, optional, **kwargs)

    return post(action='editJob', **req_args)


def delete_agent(**kwargs):
    ''' Delete a custom agent '''
    required = {'agent_ids': 'agentIds'}
    optional = {'delete_monitors': 'deleteMonitors'}

    req_args = validate_kwargs(required, optional, **kwargs)

    return post(action='deleteAgent', **req_args)


def delete_job(**kwargs):
    ''' Delete custom agent jobs '''
    required = {'job_ids': 'jobIds'}
    optional = {}

    req_args = validate_kwargs(required, optional, **kwargs)

    return post(action='deleteJob', **req_args)


def get_agents(**kwargs):
    ''' Get user's custom agents '''
    required = {}
    optional = {'load_tests': 'loadTests', 'load_params': 'loadParams',
                'type': 'type'}

    req_args = validate_kwargs(required, optional, **kwargs)

    return get(action='getAgents', **req_args)


def get_jobs(**kwargs):
    ''' Get jobs for the specified custom agent '''
    required = {'agent_id': 'agentId'}
    optional = {}

    req_args = validate_kwargs(required, optional, **kwargs)

    return get(action='getJobs', **req_args)


def agent_info(**kwargs):
    ''' Get information for the specified agent '''
    required = {'agent_id': 'agentId'}
    optional = {}

    req_args = validate_kwargs(required, optional, **kwargs)

    return get(action='agentInfo', **req_args)
