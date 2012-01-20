#!/usr/bin/env python
# encoding: utf-8
"""
params.py

Created by Jeremiah Shirk on 2011-10-04.
Copyright (c) 2011 Monitis. All rights reserved.
"""

from urllib import quote

from monitis.api import MonitisError

class DataType:
    '''Helper class for representing dataType parameters
    
    dataType is used in the arguments to add_monitor and included
    in the response to get_monitor_info.  Types are represented by four
    integer string values as follows:
    
        '1' for boolean
        '2' for integer
        '3' for string
        '4' for float
    
    That same representation is used internally in the DataType class,
    with methods available to return the longer string form.
    
    The constructor is tolerant, and will accept numeric and string
    types, such as:
    
        DataType(1)
        DataType('boolean')
        DataType('1')
    '''
    def __init__(self, datatype):
        """Accept various representations of a Monitis dataType"""
        self.datatype = DataType.canonical(datatype)
        
    @staticmethod
    def canonical(datatype):
        """Convert many variations of dataType into canonical form
        
        The canonical form is any one of ('1', '2', '3', '4')
        """
        
        # if someone passes a DataType instance to canonical
        # just return the internal representation, since it's
        # already been through canonical in the constructor
        if isinstance(datatype, DataType):
            return datatype.datatype
        
        ret_datatype = None
        datatype = str(datatype)
        str2int = {'boolean':'1', 'integer':'2', 'string':'3', 'float':'4'}
        # if m_type(datatype) is int:
        #     ret_datatype = str(datatype)
        # elif m_type(datatype) is str:
        if datatype in str2int.keys():
            ret_datatype = str2int[datatype]
        else:
            ret_datatype = str(datatype)
        
        # ret_datatype is definitely a string, is it a good one?
        if ret_datatype not in str2int.values():
            raise MonitisError('Invalid dataType: ' + repr(datatype))
        else:
            return ret_datatype
    
    def __str__(self):
        """The integer string representation expected by the Monitis API"""
        return self.datatype

class AdditionalResult():
    
    '''additionalResult to add to existing results posted to custom monitors
    
    In the Monitis API, additional results can be added to existing results 
    that have been posted to custom monitors.  AdditionalResult encapsulates
    one instance of such.  These are aggregated in AdditionalResults, which 
    are composed of one or more instances of AdditionalResult.
    '''
    
    def __init__(self, **kwargs):
        '''Initialize an AdditionalResult with kwargs corresponding with
        the expected parameters.

        Input of (paramName1=paramValue1, paramName2=paramValue2) will
        correspond to an additionalResult parameter in the API of
        "paramName1:paramValue1, paramName2:paramValue2"
        '''
        self.result = kwargs
    
    def __str__(self):
        """AdditionalResult as expected by the Monitis API
        e.g. {paramName1:paramValue1, paramName2:paramValue2, ...}
        """
        result_list = list()
        for key, value in self.result.items():
            result_list.append(':'.join([key, value]))
        return '{' + ','.join(result_list) + '}'

class AdditionalResults():
    
    '''additionalResults to add to existing results posted to custom monitors
    
    In the Monitis API, additional results can be added to existing results
    that have been posted to custom monitors. An instance of AdditionalResults
    is composed of one or more instances of AdditionalResult.
    '''
    def __init__(self, *args):
        self.results = args
    
    def __str__(self):
        return '[' + ','.join([str(x) for x in self.results]) + ']'

class Params:
    
    '''Base class for ResultParams, AdditionalResultParams, and MonitorParams
    '''
    
    def __init__(self, name, displayname, datatype):
        """docstring for __init__"""
        self.name = name
        self.displayname = displayname
        self.datatype = DataType.canonical(datatype)
        
class ResultParams(Params):
    
    '''ResultParams describe the format of metrics that will be posted to
    a custom monitor.
    
    name -- The name of the metric used to post results
    displayname -- The name of the metric displayed in the web interface
    uom -- unit of measure, the units associated with the metric
    datatype -- the type of the metric, i.e. boolean, integer, string, float
    
    '''
    
    def __init__(self, name, displayname, uom, datatype):
        '''
        UOM is unit of measure(user defined string parameter, e.g. ms, s, kB, 
        MB, GB, GHz, kbit/s, ... ).

        If dataType is a number, then the following values are allowed:
            1 for boolean
            2 for integer
            3 for string
            4 for float

        dataType can also be given as a a string from the set
            ['boolean', 'integer', 'string', 'float']
        '''
        Params.__init__(self, name, displayname, datatype)
        self.uom = uom

    def encode(self):
        """Format ResultParams object as a string suitable for add_monitor"""
        return ':'.join([quote(x) for x in (
            self.name, self.displayname, self.uom, self.datatype)])
    
    def __str__(self):
        return self.encode()


class AdditionalResultParams(ResultParams):
    
    '''Describes the format of additional results 
    
    '''
    
    def __init__(self, name, displayname, uom, datatype):
        ResultParams.__init__(self, name, displayname, uom, datatype)


class MonitorParams(Params):
    
    '''Monitor params for custom monitors
    
    '''
    
    def __init__(self, name, displayname, value, datatype, hidden):
        # it appears that the docs for monitorParams are incorrect
        # the actual params are:
        #   name1:displayName1:value1:dataType1:isHidden1
        Params.__init__(self, name, displayname, datatype)
        self.hidden = hidden
        self.value = value

    def encode(self):
        """Format ResultParams object as a string suitable for add_monitor"""
        return ':'.join([quote(x) for x in (
                                            self.name, 
                                            self.displayname, 
                                            self.value, 
                                            self.datatype, 
                                            self.hidden)])
    
    def __str__(self):
        return self.encode()
