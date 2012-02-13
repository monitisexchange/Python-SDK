#!/usr/bin/env python
# encoding: utf-8
"""
monitors.py

Created by Jeremiah Shirk on 2012-02-05.
Copyright (c) 2012 Monitis. All rights reserved.
"""

import sys
import os
import re

from monitis.monitors.params import DataType, ResultParams
from monitis.api import Monitis, checktime
from monitis.monitors.custom import CustomMonitor, get_monitors

from monitis.tools.awsmon.timeutil import (
    parse_date, epoch_to_datetime, timestamp_to_epoch)
from monitis.tools.awsmon.options import Usage

def parse_results(statistics, results):
    '''Take a list of results from get_metric_statistics and return a list
    formatted as name,timestamp,value,unit.
    
    It is expected that the name will be augmented higher in the call stack
    with a prefix including the instance and metric name
    
    '''
    ret = list()
    for result in results:
        timestamp = timestamp_to_epoch(result['Timestamp'])
        for statistic in statistics:
            value = result[statistic]
            unit = str(result['Unit'])
            ret.append((statistic,timestamp,value,unit))
    return ret

def create_monitor(name,aws_namespace,statistics,results):
    '''Create a custom monitor by using data from a result
    
    The monitor itself is has the given name, with each '''
    
    # identify all of the names in result
    # only need the first result, even if more than one is passed in
    
    # map the values from a AWS API result:
        # prefix+results[0]['statistic'] -> name and displayname
        # aws_namespace -> tag
        # results[0][Unit] -> uom
        # float -> datatype (since we won't know which can be ints)
    
    # create one monitor a result param per statistic in the result
    # for each statistic, also get the associated unit
    base_uom = results[0]['Unit']
    result_params = list()
    for statistic in statistics:
        # treat SampleCount differently, as the units don't apply
        if statistic is 'SampleCount':
            uom = 'Count'
            datatype = DataType('integer')
        else:
            uom = base_uom
            datatype = DataType('float')
        result_params.append(
            ResultParams(statistic, statistic, uom, datatype))
        # need name, tag, ResultParam
    CustomMonitor.add_monitor(name=name, tag=aws_namespace, *result_params)

def update_monitor(name,aws_namespace,statistics,results):
    '''Update the monitor with the specified results'''
    # keep a map of names to ids, to avoid unnecessary lookups
    # if update is going to be called more than once per run
    # or, persist the map
    
    count = 0
    
    # if no existing map, then find the existing monitor that matches
    monitors = [mon for mon in list_monitors(aws_namespace) 
        if name == mon.get_monitor_info()['name']]
    # TODO handle case where len(monitors) != 1
    if len(monitors) < 1:
        raise Usage("No matching monitors found")
    elif len(monitors) > 1:
        raise Usage("More than one monitor found with name %s") % name
    else:
        monitor = monitors[0]
    # post all of the results we found
    for result in results:
        result_checktime = checktime(result['Timestamp'])
        result_params = dict()
        for statistic in statistics:
            result_params[statistic] = result[statistic]
            count += 1
        ct = monitor.add_result(result_checktime, results=result_params)
    return count
    
def delete_monitor(id=None, name=None):
    '''Delete the specified monitor
    
    If both name and id are given, prefer id'''
    if id is None:
        # get the ID based on the name
        monitor_list = [mon for mon in get_monitors()
            if mon.get_monitor_info()['name'] == name]
        monitor = monitor_list[0] # TODO handle case where len != 1
    else:
        monitor = CustomMonitor.fetch(monitor_id=id)
    monitor.delete_monitor()
    
def list_monitors(aws_namespaces=None):
    '''List the monitors tagged with the matching namesspaces
    
        namespaces - list of AWS namespaces to match, i.e. ['AWS/EC2']
    
    If no aws_namespaces are provided, all tags starting with 'AWS/' will be
    matched.
        
    '''
    # TODO handle cases where we want to get them all and filter, as well
    # as multiple tagged queries to Monitis API, with flag or heuristic
    # For now, just grab them all and filter

    if aws_namespaces is not None:
        return [mon for mon in get_monitors() 
            if mon.get_monitor_info()['tag'] in aws_namespaces]
    else:
        # if no namespace given, match every tag starting with 'AWS/'
        return [mon for mon in get_monitors()
            if re.match('AWS/', mon.get_monitor_info()['tag']) ]

def print_monitors(monitors):
    '''Formatted output to show existing monitors
    
    Output contains name, tag, and id'''
    for monitor in monitors:
        monitor.refresh()
        print '{0:<6}{1:<8}{2}'.format(
            monitor.monitor_id, monitor.tag, monitor.name)


