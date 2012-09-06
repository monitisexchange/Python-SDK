from unittest import TestCase
from nose.tools import *
from nose.plugins.skip import Skip, SkipTest
from binascii import b2a_hex
from os import urandom

from monitis.api import Monitis, get, post
import monitis.monitors.predefined.fullpageload as full


class TestFullPageLoadApi:

    def setUp(self):
        Monitis.debug = True
        self.temp_str = 'test_' + b2a_hex(urandom(4)).upper()

        # create a full page load test
        args = {'name': self.temp_str,
                'tag': self.temp_str,
                'location_ids': '5',
                'check_interval': 5,
                'url': self.temp_str + '.wordpress.com',
                'timeout': 20000}
        res = full.add_full_page_load_monitor(**args)
        self.test_id = res['data']['testId']

    def tearDown(self):
        full.delete_full_page_load_monitor(monitor_id=self.test_id)

    def test_add_full_page_load_monitor(self):
        args = {'name': self.temp_str + '2',
                'tag': self.temp_str,
                'location_ids': '5',
                'check_interval': 5,
                'url': self.temp_str + '.test.com',
                'timeout': 20000}
        res = full.add_full_page_load_monitor(**args)
        assert_equal(res['status'], 'ok')
        full.delete_full_page_load_monitor(monitor_id=res['data']['testId'])

    def test_edit_full_page_load_monitor(self):
        args = {'name': self.temp_str + '2',
                'monitor_id': self.test_id,
                'tag': self.temp_str,
                'location_ids': 5,
                'check_interval': 5,
                'url': self.temp_str + '.test.com',
                'timeout': 21000}
        res = full.edit_full_page_load_monitor(**args)
        assert_equal(res['status'], 'ok')

    def test_delete_full_page_load_monitor(self):
        res = full.delete_full_page_load_monitor(monitor_id=self.test_id)
        assert_equals(res['status'], 'ok')

    def test_suspend_full_page_load_monitor(self):
        res = full.suspend_full_page_load_monitor(monitor_ids=self.test_id)
        assert_equals(res['status'], 'ok')

    def test_activate_full_page_load_monitor(self):
        res = full.activate_full_page_load_monitor(monitor_ids=self.test_id)
        assert_equals(res['status'], 'ok')

    def test_full_page_load_test_info(self):
        res = full.full_page_load_test_info(monitor_id=self.test_id)
        assert_equals(res['testId'], self.test_id)

    def test_full_page_load_test_result(self):
        res = full.full_page_load_test_result(monitor_id=self.test_id,
                                              year=2012, month=1, day=1)
        assert isinstance(res, list)

    def test_full_page_load_locations(self):
        res = full.full_page_load_locations()
        assert isinstance(res, list)

    def test_full_page_load_tests(self):
        res = full.full_page_load_tests()
        assert isinstance(res, list)
