from datetime import date, datetime
from time import time, gmtime
from json import dumps, loads

from monitis.api import Monitis
from monitis.monitors.custom import CustomMonitor, get_monitors
from monitis.monitors.params import ResultParams, MonitorParams, DataType
from monitis.monitors.params import AdditionalResultParams, AdditionalResult
from monitis.monitors.params import AdditionalResults

from nose.tools import set_trace, assert_equal

# since this is making API calls, it should generally point at the sandbox

class TestCustomMonitor:
    @classmethod
    def tearDownClass(self):
        # set_trace()
        self.cm.delete_monitor()
    
    @classmethod
    def setUpClass(self):
        # Turn on API debugging
        Monitis.debug = True
        
        self.result_params = ResultParams('foo',
                                   'Foo Rate',
                                   'foo/s', 
                                   DataType('integer'))
        monitor_params = MonitorParams('bar',
                                      '',
                                      '5',
                                      DataType('integer'),
                                      'false')
        ARParams = AdditionalResultParams ('bar',
                                           'Bar Rate',
                                           'bar/s',
                                           DataType('integer'))
        
        self.cm = CustomMonitor.add_monitor(self.result_params,
                                           monitor_params,
                                           ARParams,
                                           name="test",
                                           tag='testMonitor'
                                           )
    
    def test_add_result(self):
        # set_trace()
        checktime = self.cm.add_result(results={'foo':10})
        assert abs(int(checktime) 
                   - int(str(int(time())) + "000")) < 5000
    
    def test_get_monitors(self):
        mon = CustomMonitor.add_monitor(
            self.result_params,name='gmtest',tag='gmtesttag')
        mon_list = get_monitors(tag='gmtesttag',m_type='custom')
        mon.delete_monitor()
        assert_equal(len(mon_list), 1)
        assert_equal(mon_list[0].tag, 'gmtesttag')
        
    def test_fetch(self):
        '''Test CustomMonitor.fetch()'''
        mon = CustomMonitor.fetch(monitor_id=self.cm.monitor_id)
        assert_equal(mon.monitor_id, self.cm.monitor_id)
    
    def test_get_monitor_results(self):
        self.test_add_result() # to be order independent, add a result
        today = datetime.utcnow()
        year = today.year
        month = today.month
        day = today.day
        # set_trace()
        monitor_results = self.cm.get_monitor_results(year, month, day)
        assert abs(int(monitor_results[0]['checkTimeInGMT'])
                   - int(str(int(time())) + "000")) < 5000        
    
    def test_edit_monitor_tag(self):
        api_result = self.cm.edit_monitor(tag='newtag')
        # on failure, edit_monitor raises an exception
        # check the result status anyway
        assert_equal(api_result['status'], 'ok')
    
    def test_edit_monitor_name(self):
        api_result = self.cm.edit_monitor(name='newname')
        # on failure, edit_monitor raises an exception
        # check the result status anyway
        assert_equal(api_result['status'], 'ok')
    
    def test_get_monitor_info(self):
        api_result = self.cm.get_monitor_info()
        # set_trace()
        assert_equal(api_result['monitorParams'][0]['name'], 'bar')
    
    def test_edit_monitor_params(self):
        params = MonitorParams('bar',
                               '',
                               '6', 
                               DataType('string'),
                               'true')
        # set_trace()
        api_result = self.cm.edit_monitor(monitor_params=params)
        # on failure, edit_monitor raises an exception
        # check the result status anyway
        assert_equal(api_result['status'], 'ok')
        
        # ensure that value was updated
        api_result = self.cm.get_monitor_info()
        assert_equal(api_result['monitorParams'][0]['value'], '6')
        # changing the dataType doesn't appear to work
        # assert_equal(api_result['monitorParams'][0]['dataType'],
        #              str(DataType('string')))
    
    def test_AdditionalResult(self):
        # set_trace()
        result = AdditionalResult(foo='1',bar='2')
        assert_equal(str(result), '{foo:1,bar:2}')
        
    def test_AdditionalResults(self):
        results = AdditionalResults(AdditionalResult(foo='1', bar='2'),
                                    AdditionalResult(foo='5', bar='3'))
        # set_trace()
        assert_equal(str(results), '[{foo:1,bar:2},{foo:5,bar:3}]')
    
    def test_add_additional_results(self):
        checktime = self.cm.add_result(results={'foo':10})
        assert abs(int(checktime)
                   - int(str(int(time())) + "000")) < 5000
        api_result = self.cm.add_additional_results(checktime=checktime,
                                                    results=[{'foo':10}])
        assert_equal(str(api_result), str(checktime))
    
    def test_get_additional_results(self):
        # to test getting additional results, first add some
        checktime = self.cm.add_result(results={'foo':10})
        api_result = self.cm.add_additional_results(checktime=checktime,
                                                    results=[{"bar":90}])
        # set_trace()                                            
        api_result = self.cm.get_additional_results(checktime=checktime)
        assert_equal(dumps(api_result), dumps([{'bar':90}]))