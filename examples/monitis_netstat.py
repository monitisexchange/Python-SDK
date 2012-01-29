#!/usr/bin/env python
# encoding: utf-8
"""
monitis_netstat.py

Created by Jeremiah Shirk on 2012-01-22.
Copyright (c) 2012 Monitis. All rights reserved.
"""

import sys
import getopt
from subprocess import Popen, PIPE
from re import findall,match
import platform

from monitis.monitors.custom import CustomMonitor, get_monitors
from monitis.monitors.params import ResultParams, DataType
from monitis.api import Monitis, MonitisError

help_message = '''
monitis_netstat.py

Simple Monitis custom monitor for reporting netstat statistics.

Options:

    -h or --help
        
        This help text
        
    -v  Verbose output
    
    -c  <name>
    
        Create new netstat custom monitor with name <name>
    
    -l  List IDs of existing netstat custom monitors
    
    -u <id>
        
        Gather the netstat statistics, and update the custom monitor
        
    -d <id>
        
        Delete the custom monitor with ID <id>
    
'''


class Usage(Exception):
    def __init__(self, msg):
        self.msg = msg


def create_monitor(name=None):
    params1 = ResultParams(
        'tcp_packets_in','TCP Packets In','pkts/s', DataType('integer'))
    params2 = ResultParams(
        'tcp_packets_out','TCP Packets Out','pkts/s', DataType('integer'))
    params3 = ResultParams(
        'udp_packets_in','UDP Packets In','pkts/s', DataType('integer'))
    params4 = ResultParams(
        'udp_packets_out','UDP Packets Out','pkts/s', DataType('integer'))
    try:
        cm = CustomMonitor.add_monitor(
            params1, params2, params3, params4, name=name, tag='netstat')
    except MonitisError, err:
        raise Usage(err)
    return cm

def list_monitors():
    try:
        cm_list = get_monitors(tag='netstat')
    except MonitisError, err:
        raise Usage(err)
    return cm_list
    
def delete_monitor(id):
    try:
        cm = CustomMonitor(monitor_id=id)
        cm.delete_monitor()
    except MonitisError, err:
        raise Usage(err)

def call_netstat():
    '''Quick and dirty but portable way to get packet stats'''
    
    # need platform to know how to call netstat
    platform_str = platform.platform()
    if match('Linux', platform_str):
        netstat_tcp_cmd = \
            'netstat -s --tcp | egrep "segments (received|send)$"'
        netstat_udp_cmd = \
            'netstat -s --udp | egrep "packets (received|send)$"'
    elif match('Darwin',platform_str):
        netstat_tcp_cmd = \
            'netstat -s -p tcp | egrep "packets (received|sent)$"'
        netstat_udp_cmd = \
            'netstat -s -p udp | egrep "datagrams (received|output)$"'
    else:
        raise Usage('Unknown platform')
    
    # using shell=True for convenience, avoid user-supplied input for safety
    # TCP
    subproc = Popen(netstat_tcp_cmd, shell=True, stdout=PIPE)
    (netstat_out, netstat_err) = subproc.communicate()
    count = {'tcp':{},'udp':{}}
    count['tcp']['rx'] = findall('(\d+) packets received', netstat_out)[0]
    count['tcp']['tx'] = findall('(\d+) packets sent', netstat_out)[0]
    # UDP
    subproc = Popen(netstat_udp_cmd, shell=True, stdout=PIPE)
    (netstat_out, netstat_err) = subproc.communicate()
    count['udp']['rx'] = findall('(\d+) datagrams received', netstat_out)[0]
    count['udp']['tx'] = findall('(\d+) datagrams output', netstat_out)[0]
    return count

def update_monitor(id):
    '''Update monitor <id> with the values from netstat'''
    
    packet_count = call_netstat()
    print ', '.join([
        packet_count['tcp']['tx'], packet_count['tcp']['rx'],
        packet_count['udp']['tx'], packet_count['udp']['rx']])
    cm = CustomMonitor(monitor_id=id)
    cm.add_result(
        tcp_packets_in=packet_count['tcp']['rx'], 
        tcp_packets_out=packet_count['tcp']['tx'],
        udp_packets_in=packet_count['udp']['rx'], 
        udp_packets_out=packet_count['udp']['tx'])
    
def main(argv=None):
    if argv is None:
        argv = sys.argv
    try:
        try:
            opts, args = getopt.getopt(
                argv[1:], "hvc:lu:d:s", ["help"])
        except getopt.error, msg:
            raise Usage(msg)
        
        # flags for the options
        verbose = False
        sandbox = False
        create_name = None
        list_flag = None
        update_id = None
        delete_id = None
        
        # option processing
        for option, value in opts:
            if option == "-v":
                verbose = True
                Monitis.debug = True
            if option == "-s":
                sandbox = True
                Monitis.sandbox = True
            
            # the remaining options are mutually exclusive
            if option in ("-h", "--help"):
                raise Usage(help_message)
            if option in ("-c"):
                create_name = value
            if option in ("-l"):
                list_flag = True
            if option in ("-u"):
                update_id = value
            if option in ("-d"):
                delete_id = value
        
        # execute the appropriate action based on the flags
        # list, update, create, delete are mutually exclusive
        # pick exactly one, with a preference in that order.
        if list_flag is not None:
            for monitor in list_monitors():
                print monitor.monitor_id + "\t" + monitor.name
        elif update_id is not None:
            update_monitor(update_id)
        elif create_name is not None:
            print "Using name " + create_name
            cm = create_monitor(name=create_name)
            print "Created new netstat monitor " + str(cm)
        elif delete_id is not None:
            delete_monitor(id=delete_id)
            print "Monitor " + str(delete_id) + " deleted"
        
    except Usage, err:
        print >> sys.stderr, sys.argv[0].split("/")[-1] + ": " + str(err.msg)
        print >> sys.stderr, "\t for help use --help"
        return 2


if __name__ == "__main__":
    sys.exit(main())
