#!/usr/bin/env python
# encoding: utf-8
"""
layout.py

Created by Jeremiah Shirk on 2012-08-27.
Copyright (c) 2012 Monitis. All rights reserved.
"""

from monitis.api import get, post


def add_page(title=None, column_count=None, **kwargs):
    ''' Add a new page to user's dash board. '''
    if title is None:
        raise MonitisError('Page title is required')
    if column_count is not None:
        kwargs['columnCount'] = column_count

    return post(action='addPage', title=title, **kwargs)


def add_page_module(module_name=None, page_id=None, column=None, row=None,
                    data_module_id=None, **kwargs):
    ''' Add a module to the specified page. '''
    if module_name is None:
        raise MonitisError("Module name is required")
    if page_id is None:
        raise MonitisError("Page ID is required")
    if column is None:
        raise MonitisError("Column is required")
    if row is None:
        raise MonitisError("Row is required")
    if data_module_id is None:
        raise MonitisError("Data module ID name is required")

    return post(action='addPageModule', moduleName=module_name,
                pageId=page_id, column=column, row=row,
                dataModuleId=data_module_id, **kwargs)


def delete_page(page_id=None, **kwargs):
    ''' Delete the specified page from user's dash board. '''
    if page_id is None:
        raise MonitisError('Page ID is required')
    return post(action='deletePage', pageId=page_id)


def delete_page_module(page_module_id=None, **kwargs):
    ''' Delete the specified module from the page. '''
    if page_module_id is None:
        raise MonitisError("Page module ID is required")

    return post(action='deletePageModule',
                pageModuleId=page_module_id, **kwargs)


def pages(**kwargs):
    ''' Get all of a user's pages. '''
    return get(action='pages', **kwargs)


def page_modules(page_name=None, **kwargs):
    ''' Get all modules of the specified page. '''
    if page_name is None:
        raise MonitisError('Page name is required')
    return get(action='pageModules', pageName=page_name, **kwargs)
