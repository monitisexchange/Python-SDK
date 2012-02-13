#!/usr/bin/env python
# encoding: utf-8
"""
timeutil.py

Created by Jeremiah Shirk on 2012-02-07.
Copyright (c) 2012 Monitis. All rights reserved.
"""

import sys
import os
from datetime import datetime, timedelta
import parsedatetime.parsedatetime as pdt
import parsedatetime.parsedatetime_consts as pdc
from time import mktime


def parse_date(date_string):
    '''Parse a time input using parsedatetime, allowing natural language'''
    c = pdc.Constants()
    p = pdt.Calendar(c)
    (result,parsed_as) = p.parse(date_string)

    # result of parse can take several forms
    # we need to return a datetime, as expected by boto    
    if parsed_as is 0:
        raise opt.Usage("Couldn't parse date/time: " + date_string)
    elif parsed_as in (1,2,3):
        # result is a struct_time or a 9-tuple that can be handled by mktime
         return epoch_to_datetime(mktime(result))
    else:
        raise opt.Usage("Unexpected result from parse_date")

def epoch_to_datetime(seconds):
    '''Take a timestamp in seconds since the epoch (UTC)
    and return a datetime
    '''
    return datetime.fromtimestamp(seconds)

def timestamp_to_epoch(timestamp):
    '''Convert a AWS Timestamp datatime to unix epoch time (UTC)'''
    return int(mktime(timestamp.timetuple()))


