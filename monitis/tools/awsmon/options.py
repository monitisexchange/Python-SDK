#!/usr/bin/env python
# encoding: utf-8
"""
options.py

Created by Jeremiah Shirk on 2012-02-05.
Copyright (c) 2012 Monitis. All rights reserved.
"""

import sys
import getopt
from datetime import datetime, timedelta
import parsedatetime.parsedatetime as pdt
import parsedatetime.parsedatetime_consts as pdc
from time import mktime

from monitis.api import Monitis
from monitis.tools.awsmon.timeutil import (
    parse_date, epoch_to_datetime, timestamp_to_epoch)

help_message = '''
monitis_cloudwatch.py  -- record AWS CloudWatch metrics in Monitis

    --help      This help message

    --create    Create a new Monitis monitor based on an AWS metric
    --update    Update an existing monitor with additional results
    --list      List existing monitors tagged with an AWS namespace
    --delete    Delete the monitor identified by the --id or --name flag
    --catalog   Print a catalog of available metrics

    --region    <region>
                AWS region to query, defaults to 'us-east-1'

    --period    <seconds>
                Granularity of data from AWS in seconds, minimum and default
                is 60 seconds.

    --unit      <>

    --ec2       AWS/EC2 namespace, for Elastic Compute Cloud metrics
    --ebs       AWS/EBS namespace, for Elastic Block Store metrics
    --elb       AWS/ELB namespace, for Elastic Load Balancer metrics
    --rds       AWS/RDS namespace, for Relational Data Store metrics

    --name      <name>
                Metric name

    --id        <id>
                Metric ID

    --from      <time>
                Date/time for start of metric result query, or in some
                "natural" forms, i.e. "-1d midnight" refers to 0:00 UTC
                yesterday. Defaults to 1 hour prior to the time specified with
                --until

    --until     <time>
                Date/time for the end of  the metric result query, or in some
                "natural" forms, i.e. "-1d midnight" refers to 0:00 UTC
                yesterday.  Defaults to the current time.

    --metric    <metric name>
                The name of the metric to query from AWS.

    --instance  <instance name>
                The name of the AWS resource/instance that the named metric
                applies to

    --min       Report the minimum of the requested metric over the selected
                period of granularity

    --max       Report the maximum of the requested metric over the selected
                period of granularity

    --avg       Report the average of the requested metric over the selected
                period of granularity

    --count     Report the count of the data points for the requested metric 
                over the selected period of granularity

    --sum       Report the sum of the requested metric values over the 
                selected period of granularity

    --prefix    <prefix>
                Prepend the specified prefix to the monitor name when
                reporting it to Monitis.

    --sandbox   Use the Monitis sandbox for all API operations
    --debug     Turn on debugging output

    --print-results
                Print out each metric that is returned from AWS 
    
    Environment Variables
    
    In addition to the arguments above, two environment variables
    are required:
    
                MONITIS_APIKEY
                MONITIS_SECRETKEY
    
    If using the sandbox via the --sandbox flag, instead ensure that you set:
    
                MONITIS_SANDBOX_APIKEY
                MONITIS_SANDBOX_SECRETKEY

    Please refer to http://monitis.com/api/api.html for more information.
'''

class Usage(Exception):
    def __init__(self, msg):
        self.msg = msg

class Options:
    '''Process command-line options for monitis_clouwatch'''
    def __init__(self,argv):
        self.argv = argv
        # default option values
        self.help = False
        self.debug = False
        self.sandbox = False
        self.region = 'us-east-1'
        self.print_catalog = False
        self.aws_namespace = None
        self.metric_name = None
        self.all_metrics = False
        self.monitor_name = None
        self.monitor_id = None
        # period for GetMetricStatistics API call
        # The granularity, in seconds, of the returned datapoints. 
        # Period must be at least 60 seconds and must be a multiple of 60
        self.period = 60 # TODO add params for coarser granularity
        self.statistics = list()
        # TODO instance is not the best name in some cases
        self.instance_name = None
        self.unit = None
        self.prefix = ''
        self.create_opt = False
        self.update_opt = False
        self.list_opt = False
        self.delete_opt = False
        self.print_opt = False
        self.from_time = None
        self.until_time = None
        
    def handle_args(self,argv=None):
        # set_trace()
        if argv is None:
            argv = sys.argv
        try:
            try:
                opts, args = getopt.getopt(
                    argv[1:], 
                    "ho:vr:", 
                    ["help", "region=", 
                    "catalog", "period=", "unit=",
                    'ec2', 'ebs', 'elb', 'rds',
                    'name=','id=', 'from=', "until=",
                    'metric=', 'max', 'min', 'avg', 'count', 'sum', 
                    'instance=','prefix=', 
                    'create', 'update', 'list', 'delete', 
                    'sandbox', 'debug','print-results'])
            except getopt.error, msg:
                raise Usage(msg)
        
            # option processing
            for option, value in opts:
                if option == "-v":
                    self.verbose = True
                if option in ("-h", "--help"):
                    self.help = True
                if option in ("-o", "--output"):
                    self.output = value
                if option in ("-r", "--region"):
                    self.region = value
                if option in ("--catalog"):
                    self.print_catalog = True
                if option in ("--ec2"):
                    self.aws_namespace = 'AWS/EC2'
                if option in ("--ebs"):
                    self.aws_namespace = 'AWS/EBS'
                if option in ("--elb"):
                    self.aws_namespace = 'AWS/ELB'
                if option in ("--rds"):
                    self.aws_namespace = 'AWS/RDS'
                if option in ("--metric"):
                    self.metric_name = value
                    if value is 'ALL':
                        self.all_metrics = True
                if option in ("--name"):
                    self.monitor_name = value
                if option in ("--id"):
                    self.monitor_id = value
                if option in ("--from"):
                    self.from_time = parse_date(value)
                if option in ("--until"):
                    self.until_time = parse_date(value)
                if option in ("--instance"):
                    self.instance_name = value
                if option in ("--avg"):
                    self.statistics.append('Average')
                if option in ("--min"):
                    self.statistics.append('Minimum')
                if option in ("--max"):
                    self.statistics.append('Maximum')
                if option in ("--sum"):
                    self.statistics.append('Sum')
                if option in ("--count"):
                    self.statistics.append('SampleCount')
                if option in ("--period"):
                    self.period = value
                if option in ("--unit"):
                    self.unit = value
                if option in ("--prefix"):
                    self.prefix = value
                if option in ("--create"):
                    self.create_opt = True
                if option in ("--update"):
                    self.update_opt = True
                if option in ("--list"):
                    self.list_opt = True
                if option in ("--delete"):
                    self.delete_opt = True
                if option in ("--print-results"):
                    self.print_opt = True
                if option in ("--sandbox"):
                    Monitis.sandbox = True
                    self.sandbox = True
                if option in ("--debug"):
                    Monitis.debug = True
                    self.debug = True

            if self.help:
                raise Usage(help_message)

            # if until is missing, assume end=now
            # if from is missing, assume from = until-1h
            if self.until_time is None:
                self.until_time = datetime.now()
            if self.from_time is None:
                self.from_time = self.until_time - timedelta(hours=1)
            # TODO error handling for missing/incompatible options
            
            # if no statistic options were selected, select all of them
            if not self.statistics:
                self.statistics = [
                    'Average', 'Sum', 'SampleCount', 'Maximum', 'Minimum' ]
        except Usage, err:
            print >> sys.stderr, \
                sys.argv[0].split("/")[-1] + ": " + str(err.msg)
            if not self.help:
                print >> sys.stderr, "\t for help use --help"
            return 2                

