#!/usr/bin/env python
# encoding: utf-8
"""
custom.py

Created by Jeremiah Shirk on 2011-10-02.
Copyright (c) 2011 Monitis. All rights reserved.
"""

from urllib import quote
from json import dumps

from monitis.api import Monitis, MonitisError, get, decode_json
from monitis.api import checktime as api_checktime
from monitis.monitors.params import MonitorParams, ResultParams
from monitis.monitors.params import AdditionalResultParams


# API operations on existing Custom Monitors are CustomMonitor methods
# API operations that return one or more monitors are functions

def _api_url():
    if Monitis.sandbox is True:
        return CustomMonitor.sandbox_url
    else:
        return CustomMonitor.default_url

# Custom Monitor API uses a different HTTP endpoint from the rest of the API
def _custom_get(**kwargs):
    '''HTTP GET using URL for customMonitor API'''
    return get(url=_api_url(), **kwargs)

def get_monitors(tag=None, m_type=None):
    """Return a list of CustomMontior instances that match the tag and m_type
    
    """
    get_args = dict()
    if m_type is not None:
        get_args['m_type'] = m_type
    if tag is not None:
        get_args['tag'] = tag
    mon_list =  _custom_get(action='getMonitors', **get_args)
    
    result_list = list()
    for mon in mon_list:
        result_list.append(CustomMonitor(monitor_id=mon['id'],
                                         name=mon['name'],
                                         **get_args))
    return result_list

# TODO make this work when keys aren't in the ENV
def get_monitor_info(monitor_id=None, exclude_hidden='false'):
    """Get information regarding the specified Custom monitor"""
    get_args = dict()
    get_args['action'] = 'getMonitorInfo'
    get_args['monitorId'] = monitor_id
    
    # cannonicalize exclude_hidden
    bool2string = {True:'true', False:'false'}
    if exclude_hidden in bool2string.keys():
        get_args['excludeHidden'] = bool2string[exclude_hidden]
    else:
        get_args['excludeHidden'] = exclude_hidden
    
    # sanity check
    if get_args['monitorId'] is None:
        raise MonitisError('get_monitor_info: monitor_id is required')
    if get_args['excludeHidden'] not in bool2string.values():
        raise MonitisError(
            'get_monitor_info: exclude_hidden is not boolean')
    
    try:
        result = _custom_get(**get_args)
    except Exception, msg:
        raise MonitisError(msg)
    
    return result

def _encode_params(*args):
    """Return a tuple of strings representing params lists suitable
    for posting to add_monitor
    
    (result_params, additional_result_params, monitor_params)
    """
    r_params = list() # result_params encoded strings
    a_params = list() # additional_result_params encoded strings
    m_params = list() # monitor_params encoded strings
    for arg in args:
        if isinstance(arg, ResultParams):
            r_params.append(arg.encode())
        elif isinstance(arg, AdditionalResultParams):
            a_params.append(arg.encode())
        elif isinstance(arg, MonitorParams):
            m_params.append(arg.encode())
        else:
            raise MonitisError("Non-param unnamed argument")
    result_params = ';'.join(r_params)
    additional_result_params = ';'.join(a_params)
    monitor_params = ';'.join(m_params)
    return (result_params, additional_result_params, monitor_params)

class CustomMonitor(Monitis):
    #  This constructor generally should not be called directly.
    # Rather, construct a CustomMonitor either via
    # CustomMonitor.add_monitor or CustomMonitor.fetch
    '''
    CustomMonitor encapsulates the API for Monitis custom monitors.
    
    Generally, do not instantiate CustomMonitor directly using the 
    constructor.  Instead, to add a new monitor, use CustomMonitor.addMonitor.
    To create an instance for working with an existing monitor, use
    CustomMonitor.fetch.
    '''
    
    debug = False
    default_url = 'http://monitis.com/customMonitorApi'
    sandbox_url = 'http://sandbox.monitis.com/customMonitorApi'
    
    def __init__(self, apikey=None, secretkey=None, url=None,
                 version=None, validation=None,
                 monitor_id=None, name=None, m_type=None, tag=None):
        customurl = url or _api_url()
        self.monitor_id = monitor_id
        self.name = name
        self.m_type = m_type
        self.tag  = tag
        self.monitor_params = None
        # if monitor_id is None:
        #     raise MonitisError("monitor_id is required")
        Monitis.__init__(self, apikey=apikey, secretkey=secretkey,
                         url=customurl, version=version,
                         validation=validation)

    def get_monitor_info(self):
        """Return the information for an existing CustomMonitor instance"""
        return get_monitor_info(monitor_id=self.monitor_id)
    
    def refresh(self):
        '''Update the monitor with fresh data from the API
        
        This option is currently limited to getting the tag'''
        # TODO complete the mapping of API params to class attributes
        # and refresh all of them
        monitor_info = self.get_monitor_info()
        self.tag = monitor_info['tag']
        
    @classmethod
    def fetch(cls, monitor_id=None, **kwargs):
        """Create a CustomMonitor instance based on get_monitor_info"""
        if monitor_id is None:
            raise MonitisError('fetch: monitor_id is required')
        
        mon_data = get_monitor_info(monitor_id)
        mon = CustomMonitor(monitor_id=monitor_id, **kwargs)
        for i in ['name', 'tag', 'm_type']:
            try:
                mon.__dict__[i] = mon_data[i]
            except KeyError:
                pass
        
        # result_params
        for par in mon_data['resultParams']:
            mon.__dict__['resultParams'] = ResultParams(par['name'], 
                                                        par['displayName'], 
                                                        par['uom'], 
                                                        par['dataType'])
                
        # additional_result_params
        for par in mon_data['additionalResultParams']:
            mon.__dict__['additionalResultParams'] = AdditionalResultParams(
                                                       par['name'], 
                                                       par['displayName'], 
                                                       par['uom'], 
                                                       par['dataType'])
        
        # monitor_params
        # hidden is not returned in getMonitorInfo in the API, so we have to
        # make an assumption that it is false
        for par in mon_data['monitorParams']:
            mon.__dict__['monitorParams'] = MonitorParams(par['name'], 
                                                          par['displayName'], 
                                                          par['value'],
                                                          par['dataType'],
                                                          'false')
        
        return mon
    
    @staticmethod
    def _validate_kwargs(required, allowed, **kwargs):
        '''Validate keyword arguments passed in as **kwargs
        
        required: kwargs that must exist and evaluate to true
        allowed: kwargs that may exist
        kwargs : the kwargs to validate
        
        Return true if all required kwargs exist, and no kwargs
        exist that are neither allowed or required
        
        Raise MonitisError if any arguments are missing or if any
        invalid arguments are found
        '''
        
        all_allowed = allowed
        all_allowed.extend(required)
        
        # input validataion
        for key in required:
            if not key in kwargs.keys():
                raise MonitisError("Argument " + key + " is required")
        
        for key in kwargs.keys():
            if not key in all_allowed:
                raise MonitisError("Unexpected kwarg " + key)
        
        return True
        
    @classmethod
    def add_monitor(cls, *args, **kwargs):
        """Add a custom monitor

        Required parameters:
            name - string
            tag - string
            One or more ResultParams instances

        Optional parameters:
            customUserAgentId - the id of the custom user agent
            m_type - custom string that represents monitor type
            One or more MonitorParams instances
            One or more AdditionalResultParams instances

        Note that all Params objects must come before the keyword arguments
        
        Return a CustomMonitor instance if the operation suceeds, or raises
        MonitisError if the operation fails.
        """

        # Need to use kwargs rather than named args so we can have
        # a variable numer of args for *Params
        required = ['name','tag']
        allowed = ['customUserAgentId','m_type']
        
        # ensure that we have the correct args
        # raises MonitisError if it fails
        CustomMonitor._validate_kwargs(required, allowed, **kwargs)
        # all required keys exist in kwargs, none unexpected
        
        # build the dict to pass to post
        add = dict()
        add.update(**kwargs) # everything in kwargs passed on to post
        add['action'] = 'addMonitor'
        
        result_params, additional_result_params, monitor_params = \
                                                         _encode_params(*args)
        
        # add the *params args to add
        if result_params:
            add['resultParams'] = result_params
        else:
            raise MonitisError('add_monitor: result_params is required')
        if monitor_params:
            add['monitorParams'] = monitor_params
        if additional_result_params:
            add['additionalResultParams'] = additional_result_params

        # Create a mostly empty CustomMonitor, and then populate it
        # once we've successfully created it on the server
        mon = cls(url=_api_url())
        json_result = mon.post(**add)
        result = decode_json(json_result)

        if result['status'] == 'ok':
            mon.monitor_id = result['data']

            # copy additional values into the new CustomMonitor object
            for key in ('name', 'm_type', 'tag', 'customUserAgentId'):
                if key in kwargs:
                    mon.__dict__[key] = kwargs[key]
        else:
            raise MonitisError("add_monitor failed: " + json_result)
        return mon 
    
    def _set_id(self, monitor_id):
        """Set the monitor_id when creating a new instance via add_monitor"""
        self.monitor_id = monitor_id
    
    def __repr__(self):
        """Nicer string representation of CustomMonitor"""
        return "<CustomMonitor(id={0}, name={1})>".format(self.monitor_id,
                                                       self.name)
    def edit_monitor(self, *args, **kwargs):
        """Edit an existing custom monitor
        
        monitor_params
        name
        tag
        """
        
        # Need to use kwargs rather than named args so we can have
        # a variable numer of args for *Params
        required = []
        allowed = ['name', 'tag', 'monitor_params']

        CustomMonitor._validate_kwargs(required, allowed, **kwargs)

        # build the dict to pass to post
        add = dict()
        # copy name and tag to add, if they exist
        for arg_name in ['name', 'tag']:
            if arg_name in kwargs.keys():
                add[arg_name] = kwargs[arg_name]
        # copy monitorParams into add, if it exists
        if 'monitor_params' in kwargs.keys():
            add['monitorParams'] = kwargs['monitor_params']
        add['action'] = 'editMonitor'
        add['monitorId'] = self.monitor_id
        
        result_params, additional_result_params, monitor_params = \
                                                         _encode_params(*args)
        
        # add the *params args to add
        if monitor_params:
            add['monitorParams'] = monitor_params
        if result_params:
            raise MonitisError("edit_monitor: result_params not allowed")
        if additional_result_params:
            raise MonitisError("edit_monitor: additional_result_params " + \
                                   "not allowed")
        
        json_result = self.post(**add)
        result = decode_json(json_result)

        if result['status'] == 'ok':
            # copy additional values into the new CustomMonitor object
            for key in ('name','tag'):
                if key in kwargs:
                    self.__dict__[key] = kwargs[key]
            
            self.monitor_params = monitor_params
        else:
            raise MonitisError("add_monitor failed: " + json_result)
        
        return result
    
    def delete_monitor(self):
        """Delete the custom monitor with ID monitor_id"""
        result = decode_json(self.post(action='deleteMonitor',
                                        monitorId=self.monitor_id))
        if result['status'] != 'ok':
            raise MonitisError(
                'delete_monitor error: ' + result['status'])

    # @classmethod
    # def add_result_and_monitor(
    #     self, checktime=None, name, tag=None, result_params, **kwargs):
    #     '''Add results as with add_result, but also create the named monitor if
    #     none with that name exists.
    # 
    #         checktime - optional, the current time is used if none given
    #         name - required, if it matches an existing name, that will be used
    #         tag - required, used if creating a new monitor
    #         result_params - list of one or more ResultParams for the monitor
    #     
    #     '''
    #     # check to see if the monitor already exists
    # 
    #     # if not, create it
    #     # in either case, we now have a handle to a monitor
    #     # post the results to the monitor
    #     pass
    
    def add_result(self, checktime=None, results=None, **kwargs):
        """add results for the specified Custom monitor
        
        One or more results should be passed in a kwargs of the form:
            paramName1=paramValue1,paramName2=paramValue2,...
        
        Returns the checktime, whether passed in as a parameter
        or automatically generated.  This is useful for passing
        to add_additional_results

        """
        action = 'addResult'
        # use the current time if the user didn't specify one
        result_checktime = checktime or api_checktime()
        
        # merge kwargs and results items into one list
        if results is None:
            results_items = list()
        else:
            results_items = results.items()
        results_items.extend(kwargs.items())

        # build post string elements from combined results items
        result_strings = list()
        for name, value in results_items:
            # urllib.quote each to implement "double encoding"
            # http://monitis.com/api/api.html#api_home
            result_strings.append(quote(':'.join((name, str(value)))))
        
        result_string =  self.post(action=action, monitorId=self.monitor_id,
                         checktime=result_checktime,
                         results=';'.join(result_strings))
        result = decode_json(result_string)
        if result['status'] != 'ok':
            raise MonitisError('add_result failed')
            
        return result_checktime
    
    def add_additional_results(self, checktime=None, results=None):
        """Add additional results to an existing result
        
        checktime: the checktime of a previously submitted result
        results: an instance of AdditionalResults 
        
        """
        
        if not checktime:
            raise MonitisError("addAdditionalResults: checktime required")
        
        if not results:
            raise MonitisError("addAdditionalResults: " + \
                                   "results required")
        
        action = 'addAdditionalResults'
        # use the current time if the user didn't specify one
        checktime = checktime or api_checktime()
        
        # use dumps to format the results parameter as a JSON list
        response_string =  self.post(action=action,
                                     monitorId=self.monitor_id,
                                     checktime=checktime,
                                     results=dumps(results))
        response = decode_json(response_string)
        if response['status'] != 'ok':
            raise MonitisError('addAdditionalResults failed: ' + response)
            
        return checktime
        
        
    def get_monitor_results(self, year=None, month=None, day=None,
                          timezone=None):
        """Get results from the specified custom monitor"""
        get_args = dict()
        if year is None or month is None or day is None:
            raise MonitisError(
                'get_monitor_results: year, month, and day are required')
        get_args['action'] = 'getMonitorResults'
        get_args['monitorId'] = self.monitor_id
        for i, j in ((year, 'year'), (month, 'month'), (day, 'day')):
            get_args[j] = i
        if timezone:
            get_args['timezone'] = timezone
        
        return _custom_get(**get_args)
    
    def get_additional_results(self, checktime=None):
        """Get additional results associated with a specific posted result
        
        Given an existing result and associated additional results, retrieve
        those additional results, using the checktime as the key to identify 
        the specific additional result.
        
        checktime -- identifies which additional result to retrieve
        """
        
        if checktime is None:
            raise MonitisError("getAdditionalResults: checktime required")
        
        get_args = {'action': 'getAdditionalResults',
                    'monitorId': self.monitor_id,
                    'checktime': checktime}
        
        return _custom_get(**get_args)
