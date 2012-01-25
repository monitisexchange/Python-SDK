#!/usr/bin/env python

from subprocess import Popen, PIPE
from re import findall
from datetime import datetime

from monitis.monitors.custom import CustomMonitor, get_monitors
from monitis.monitors.params import ResultParams, DataType
from monitis.api import Monitis

# Use the Monitis sandbox, sandbox.monitis.com
Monitis.sandbox = True

# create the monitor
rp = ResultParams(
    'tcp_packets_in','TCP Packets In','pkts/s', DataType('integer'))
cm = CustomMonitor.add_monitor(rp, name='netstat monitor', tag='netstat')
print "Created monitor: %s" % cm.monitor_id

# get the data from netstat
subproc = Popen(
    'netstat -s -p tcp | grep "packets received$"', shell=True, stdout=PIPE)
(netstat_out, netstat_err) = subproc.communicate()
count = findall('(\d+) packets received', netstat_out)[0]
print "Netstat count: %s" % count

# send the result to the Monitis sandbox
cm.add_result(tcp_packets_in=count)
print "Posted result"

# retrieve the results from the monitor and print it to verify that it worked
today = datetime.utcnow()
result = cm.get_monitor_results(today.year, today.month, today.day)
print "Retrieved result: %s" % result[0]['tcp_packets_in']

# delete the monitor
cm.delete_monitor()
print "Deleted monitor"



