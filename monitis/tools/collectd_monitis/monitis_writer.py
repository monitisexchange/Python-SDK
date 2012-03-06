#!/usr/bin/env python

import os
import threading
import collectd
from copy import deepcopy

from monitis.api import Monitis
from monitis.monitors.custom import CustomMonitor

# Defaults
monitors = dict()
prefix = ''
apikey = ''
secretkey = ''
sandbox = False
debug = False
delta = False

monitor_defaults = {
    'id': '',
    'result_param': '',
    'delta': False,
    # 'last_value': None,
    # 'last_time': None
}


def writer_init():
    global sandbox, debug, apikey, secretkey, monitors

    # last values and timestamps must be shared across collectd threads
    # collectd will pass this shared object into write on all calls
    # all accessess to this data should be protected by threading.Lock
    
    shared_data = {
        'monitors': dict(),
        'lock': threading.Lock()
    }
    
    if sandbox:
        Monitis.sandbox = True
        os.environ['MONITIS_SANDBOX_APIKEY'] = apikey
        os.environ['MONITIS_SANDBOX_SECRETKEY'] = secretkey
    else:
        Monitis.sandbox = False
        os.environ['MONITIS_APIKEY'] = apikey
        os.environ['MONITIS_SECRETKEY'] = secretkey
    
    if debug:
        Monitis.debug = True
    else:
        Monitis.debug = False
    
    for monitor_name in monitors.keys():
        monitors[monitor_name]['monitis'] = CustomMonitor.fetch(
            monitor_id=monitors[monitor_name]['id'])
    
    # hold lock while initializing shared_data
    with shared_data['lock']:
        for monitor_name in monitors.keys():
            shared_data['monitors'][monitor_name] = {
                'last_value': None,
                'last_time': None
            }
            
    collectd.register_write(write, data=shared_data);


def write(vl, data):
    '''
    '''
    global prefix, apikey, secretkey, monitors
    
    #ex.: test-host.processes.fork_rate
    metric_name = '.'.join([prefix,vl.plugin,vl.type])
    
    # some types have multiple instances
    if vl.type_instance:
        # ex.: prefix.processes.ps_state.running
        metric_name = '.'.join([metric_name,vl.type_instance])

    if debug:
        print " ".join([metric_name,str(vl.values)])
    
    timestamp = int(vl.time)
    for i in vl.values:
        
        # only process the metrics named in the monitis_writer config
        if monitors.has_key(metric_name):
            
            result = None
            
            # report delta metrics as delta/second
            # raw delta isn't useful when the interval isn't fixed
            if monitors[metric_name]['delta'] is True:
                
                with data['lock']:
                    last_value = data['monitors'][metric_name]['last_value']
                    last_time = data['monitors'][metric_name]['last_time']
                
                # dx/dt
                if last_value is not None:
                    delta = i - last_value
                    delta_s = float(delta) / (timestamp - last_time )
                    result = delta_s
                
                # save the current values for the next run
                with data['lock']:
                    data['monitors'][metric_name]['last_value'] = i
                    data['monitors'][metric_name]['last_time'] = timestamp                
            
            # write raw metric value
            else:
                result = i
            
            # send the result
            # Monitis checktime format is (epochtime + "000")
            if result is not None:
                rp = monitors[metric_name]['result_param']
                monitors[metric_name]['monitis'].add_result(
                    results={rp: result}, checktime=(str(timestamp)+"000"))


def config(conf):
    global prefix, apikey, secretkey, monitors, sandbox, debug
    global monitor_defaults
    
    for child in conf.children:
        if child.key == 'Prefix':
            prefix = child.values[0]
            # print "Prefix: %s" % prefix
        elif child.key == 'ApiKey':
            apikey = child.values[0]
        elif child.key == 'SecretKey':
            secretkey = child.values[0]
        elif child.key == 'Sandbox':
            sandbox = child.values[0]
        elif child.key == 'Debug':
            debug = child.values[0]

        # Monitor block in config, one per Monitis custom monitor
        elif child.key == 'Monitor':
            
            # reset defaults
            monitor_delta = monitor_defaults['delta']
            
            # get monitor block child values
            for mon_child in child.children:
                if mon_child.key in ['Id','ID']:
                    monitor_id = str(int(mon_child.values[0]))
                elif mon_child.key == 'Name':
                    monitor_name = mon_child.values[0]
                elif mon_child.key == 'Delta':
                    monitor_delta = mon_child.values[0]
                elif mon_child.key == 'ResultParam':
                    result_param = mon_child.values[0]
                    
            # TODO raise exception if name or ID are missing
            monitors[monitor_name] = deepcopy(monitor_defaults)
            monitors[monitor_name]['id'] = monitor_id
            monitors[monitor_name]['delta'] = monitor_delta
            monitors[monitor_name]['result_param'] = result_param
        else:
            # ignore any unknown directives/blocks
            pass
    

collectd.register_config(config)
collectd.register_init(writer_init)