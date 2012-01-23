from re import match
from datetime import datetime
from time import time
from unittest import TestCase
from nose.tools import *

from monitis.monitors.custom import CustomMonitor
from monitis.api import get, resolve_apikey, resolve_secretkey, Monitis
from monitis.api import MonitisError, timestamp, checktime, decode_json
from monitis.api import environ_key


class TestMonitisApi:
    def setUp(self):
        self.mon = Monitis()
        Monitis.sandbox = True
    
    def test_environ_key(self):
        env_key = environ_key("HOME")
        assert(env_key is not None)
        env_key = environ_key("A_VERY_VERY_UNLIKELY_ENV_VARIABLE")
        assert(env_key is None)
        
    def test_resolve_apikey(self):
        apikey = resolve_apikey()
        # apikey is a string of exactly 26 uppercase alphanumeric characters
        matched = match('^[0-9A-Z]{26}$', apikey)
        assert matched is not None
    
    def test_resolve_secretkey(self):
        secretkey = resolve_secretkey()
        matched = match('^[0-9A-Z]{26}$', secretkey)
        assert matched is not None
    
    def test_checksum(self):
        assert_equal(self.mon.checksum(secretkey='notReallyASecret',
                                       key2="foo", key1="bar"),
                          "ML1TdJ/wQc06CdIREtddB19wsKM=")
    
    def test_checktime(self):
        # delta between checktime and the current time should be < 5 sec
        assert abs(int(checktime()) - int(str(int(time())) + "000")) < 5000
    
    def test_timestamp(self):
        # TODO allow for a delta, though at 1 sec resolution this will 
        # rarely fail
        assert_equal(timestamp(), datetime.utcnow().strftime("%F %T"))
    
    def test_get(self):
        # this test needs a simple API call, secretkey fits the bill
        # http://www.monitis.com/api?action=secretkey&apikey=${MONITIS_APIKEY}
        secret_key = get(action='secretkey')['secretkey']
        assert_equals(secret_key,resolve_secretkey())
    
    def test_MonitisError(self):
        '''Test calls to the API that raise a MonitisError'''
        try:
            get(action='secretkey',apikey='bad_api_key')
        except MonitisError, error:
            assert_equal(str(error), 
                'MonitisError(API Error: {"error":"Authentication failure"})')
    
    def test_decode_json_error(self):
        '''Test decode_json in the case that parsing the JSON fails'''
        try:
            # the single quotes are invalid for JSON strings
            decode_json(json="[{'foo':1}]")
        except MonitisError, error:
            assert_equal(str(error.msg),
                'JSON parse error: '
                + 'Expecting property name: line 1 column 2 (char 2)')
    
    def test_post(self):
        '''Test the monitis.api post method
    
        Note that this test only tests for cases where the post fails.  Successful
        calls to post will be covered in other tests, i.e. 
        test_custom.test_add_result
        '''
        # test of the API post method is covered by test_custom.test_add_result
        try:
            self.mon.post(action='noSuchAction')
        except MonitisError, error:
            assert_equal(str(error.msg), 
                'API Error: ' +
                '{"status":"Action \'noSuchAction\' is not supported"}')