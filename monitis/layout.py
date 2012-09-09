#!/usr/bin/env python
# encoding: utf-8
"""
layout.py

Created by Jeremiah Shirk on 2012-08-27.
Copyright (c) 2012 Monitis. All rights reserved.
"""

from monitis.api import get, post, validate_kwargs


def add_page(**kwargs):
    ''' Add a new page to user's dash board. '''
    required = ['title']
    optional = ['columnCount']
    req_args = validate_kwargs(required, optional, **kwargs)
    return post(action='addPage', **req_args)


def add_page_module(**kwargs):
    ''' Add a module to the specified page. '''
    required = ['moduleName', 'pageId', 'column', 'row', 'dataModuleId']
    optional = ['height']

    req_args = validate_kwargs(required, optional, **kwargs)
    return post(action='addPageModule', **req_args)


def delete_page(**kwargs):
    ''' Delete the specified page from user's dash board. '''
    required = ['pageId']
    optional = []
    req_args = validate_kwargs(required, optional, **kwargs)
    return post(action='deletePage', **req_args)


def delete_page_module(**kwargs):
    ''' Delete the specified module from the page. '''
    required = ['pageModuleId']
    optional = []
    req_args = validate_kwargs(required, optional, **kwargs)
    return post(action='deletePageModule', **req_args)


def pages(**kwargs):
    ''' Get all of a user's pages. '''
    return get(action='pages', **kwargs)


def page_modules(**kwargs):
    ''' Get all modules of the specified page. '''
    required = ['pageName']
    optional = []
    req_args = validate_kwargs(required, optional, **kwargs)
    return get(action='pageModules', **req_args)
