from unittest import TestCase
from nose.tools import *
from binascii import b2a_hex
from os import urandom

from monitis.api import Monitis, get, post
import monitis.predefined.external as external


class TestExternalMonitorApi:

    def setUp(self):
        Monitis.debug = True
        self.temp_str = 'test_' + b2a_hex(urandom(4)).upper()

        # create an external monitor
        test_args = {'type': 'ping',
                     'name': self.temp_str,
                     'detailed_test_type': '1',
                     'url': 'google.com',
                     'interval': 5,
                     'location_ids': [1,5,9],
                     'tag': self.temp_str}
        res = external.add_external_monitor(**test_args)

        self.test_id = res['data']['testId']

    def tearDown(self):
        # delete the external monitor used in the tests
        external.delete_external_monitor(test_ids=self.test_id)
        # delete all where name ends with our temp str?

    def test_add_external_monitor(self):
        test_args = {'type': 'http',
                     'name': 'add_' + self.temp_str,
                     'detailed_test_type': '1',
                     'url': 'google.com',
                     'interval': 5,
                     'location_ids': [1,5,9],
                     'tag': self.temp_str}
        res = external.add_external_monitor(**test_args)
        assert_equals(res['status'],'ok')
        external.delete_external_monitor(testIds=res['data']['testId'])

    def test_edit_external_monitor(self):
        test_args = {'type': 'pint',
                     'test_id': self.test_id,
                     'name': self.temp_str,
                     'url': 'google.com',
                     'timeout': 5000,
                     'interval': 5,
                     'location_ids': ['1-5','5-5','9-5'],
                     'tag': self.temp_str}
        res = external.edit_external_monitor(**test_args)
        assert_equals(res['status'], 'ok')

    def test_delete_external_monitor(self):
        res = external.delete_external_monitor(test_ids=self.test_id)
        assert_equals(res['status'], 'ok')

    def test_suspend_external_monitor(self):
        res1 = external.suspend_external_monitor(tag=self.temp_str)
        assert_equals(res1['status'], 'ok')
        res2 = external.suspend_external_monitor(monitor_ids=self.test_id)
        assert_equals(res2['status'], 'ok')

    def test_activate_external_monitor(self):
        res1 = external.activate_external_monitor(tag=self.temp_str)
        assert_equals(res1['status'], 'ok')
        res2 = external.activate_external_monitor(monitor_ids=self.test_id)
        assert_equals(res2['status'], 'ok')

    def test_locations(self):
        res = external.locations()
        assert len(res) >= 3

    def test_tests(self):
        res = external.tests()
        assert len([x for x in res['testList']\
                       if x['id'] == self.test_id]) > 0

    def test_testinfo(self):
        res = external.testinfo(test_id=self.test_id)
        assert res['testId'] == self.test_id

    def test_testresult(self):
        res = external.testresult(test_id=self.test_id,
                                  year=2012, month=9, day=1)
        assert isinstance(res,list)

    def test_tests_last_values(self):
        res = external.tests_last_values()
        assert isinstance(res,list)

    def test_tags(self):
        res = external.tags()
        assert len([x for x in res['tags']\
                       if x['title'] == self.temp_str]) > 0

    def test_tagtests(self):
        res = external.tagtests(tag=self.temp_str)
        assert res['testList'][0]['id'] == self.test_id
