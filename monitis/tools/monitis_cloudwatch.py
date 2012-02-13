#!/usr/bin/env python
# encoding: utf-8
"""
monitis_cloudwatch.py

Created by Jeremiah Shirk on 2012-01-30.
Copyright (c) 2012 Monitis. All rights reserved.
"""

import sys
from datetime import datetime, timedelta
from calendar import timegm

from boto.exception import BotoServerError

from monitis.api import MonitisError

from monitis.tools.awsmon.options import Options, Usage
from monitis.tools.awsmon.timeutil import (
    parse_date, epoch_to_datetime, timestamp_to_epoch)
from monitis.tools.awsmon.aws import (
    connect_to_cloudwatch, get_instance_name, metrics_catalog, 
    available_metrics, dimensions)
from monitis.tools.awsmon.monitors import (
    parse_results, create_monitor, update_monitor, delete_monitor,
    list_monitors, print_monitors)

def _monitor_name(prefix, instance, metric):
    '''Generate a monitor name based on prefix, the instance name
    and the metric name
    '''
    if prefix is '':
        monitor_name = '.'.join((instance,metric))
    else:
        monitor_name = '.'.join((prefix,instance,metric))
    return monitor_name

def get_options(argv):
    '''Create an awsmon.Options to parse argv arguments'''
    opt = Options(argv)
    opt.handle_args()
    return opt

def get_aws_results(opt):
    '''Return statistics for the given region, timeframe, and metric'''
    conn_cloudwatch = connect_to_cloudwatch(opt.region)
    return conn_cloudwatch.get_metric_statistics(opt.period, opt.from_time, 
        opt.until_time, opt.metric_name, opt.aws_namespace, opt.statistics,
        dimensions=dimensions(opt.aws_namespace, opt.instance_name),
        unit=opt.unit)

def print_catalog(opt):
    '''Get a list of available metrics and print a formatted list'''
    catalog = metrics_catalog(opt.region)
    for metric in available_metrics(catalog):
        print '{0:<20}{1:<40}{2}'.format(*metric)

def create(opt, results):
    '''Create a new monitor, in part based on the structure of the results'''
    # if metric_name was 'ALL' run create monitor for each metric
    # if opt.metric_name is 'ALL':
    #     metrics = 
    monitor_name = _monitor_name(
        opt.prefix, opt.instance_name, opt.metric_name)
    create_monitor(monitor_name, opt.aws_namespace, opt.statistics, results)

def _list(opt):
    '''Print a formatted list existing monitors'''
    if opt.aws_namespace is None:
        print_monitors(list_monitors())
    else:
        print_monitors(list_monitors(opt.aws_namespace))

def update(opt,results):
    '''Post the results to a Monitis monitor'''
    print "Using AWS data from {0} until {1}".format(
        opt.from_time, opt.until_time)
    monitor_name = _monitor_name(opt.prefix,opt.instance_name,opt.metric_name)
    count = update_monitor(
        monitor_name, opt.aws_namespace, opt.statistics, results)
    print "Posted %s results to Monitis" % count

def main(argv=None):
    if argv is None:
        argv = sys.argv
    try:
        opt = get_options(argv)
        if opt.print_catalog:
            print_catalog(opt)
        elif opt.delete_opt:
            # expect either --name or --id to identify the monitor to delete
            delete_monitor(id=opt.monitor_id, name=opt.monitor_name)
        elif (opt.statistics and opt.aws_namespace and opt.metric_name 
            and opt.instance_name):
            # we have everything we need to create or update a monitor
            results = get_aws_results(opt)
            if not results:
                raise Usage(
                    "No results found for the time period from %s until %s"
                    % (opt.from_time, opt.until_time))
            if opt.print_opt:
                print "\n".join([str(r) for r in results])
            if opt.create_opt:
                create(opt,results)
            if opt.update_opt:
                update(opt,results)
        # do list last, even if other actions were taken
        if opt.list_opt is True:
            _list(opt)
    except MonitisError, msg:
        print "Monitis API Error: %s" % msg
        return 4
    except BotoServerError, msg:
        print "Error accessing Amazon Web Services API"
        print msg
        return 3
    except Usage, err:
        print >> sys.stderr, sys.argv[0].split("/")[-1] + ": " + str(err.msg)
        print >> sys.stderr, "\t for help use --help"
        return 2


if __name__ == "__main__":
    sys.exit(main())
