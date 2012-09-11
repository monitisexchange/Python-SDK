from unittest import TestCase
from nose.tools import *
from nose.plugins.skip import Skip, SkipTest
from binascii import b2a_hex
from os import urandom

from monitis.api import Monitis, MonitisError, get, post
import monitis.monitors.predefined.transaction as trans
import monitis.monitors.predefined.fullpageload as full


class TestTransactionMonitorApi:

    def setUp(self):
        Monitis.debug = True
        # find an existing transaction monitor
        res = trans.transaction_tests()
        if isinstance(res, list) and len(res) > 0:
            self.test_id = res[0]['id']
            self.test_ids = [x['id'] for x in res]
        else:
            self.test_id = None

    def tearDown(self):
        pass

    def test_suspend_transaction_monitor(self):
        res = trans.suspend_transaction_monitor(monitor_ids=self.test_ids)
        assert_equal(res['status'], 'ok')

    def test_activate_transaction_monitor(self):
        res = trans.activate_transaction_monitor(monitor_ids=self.test_ids)
        assert_equal(res['status'], 'ok')

    def test_transaction_tests(self):
        res = trans.transaction_tests()
        match = [x for x in res if x['id'] == self.test_id]
        assert len(match) > 0

    def test_transaction_test_info(self):
        res = trans.transaction_test_info(monitor_id=self.test_id)
        assert_equal(res['testId'], self.test_id)

    def test_transaction_test_result(self):
        res = trans.transaction_test_result(monitor_id=self.test_id,
                                            year=2000, month=1, day=1)
        assert isinstance(res, list)

    def test_transaction_step_result(self):
        # result_id=0 will yield an empty list, sufficient for testing code
        # but doesn't exercise the API.  Need to have a transaction
        # monitor with actual results to test fully
        res = trans.transaction_step_result(year=2000, month=1, day=1,
                                            result_id=0)
        assert isinstance(res, list)

    def test_transaction_step_capture(self):
        try:
            res = trans.transaction_step_capture(monitor_id=self.test_id,
                                                 result_id=0)
        except MonitisError, error:
            assert str(error.msg).startswith('API Error:')


    def test_transaction_step_net(self):
        res = trans.transaction_step_net(
            monitor_id=self.test_id, result_id=0, year=2000, month=1, day=1)
        assert isinstance(res['data'], dict)

    def test_transaction_locations(self):
        res = trans.transaction_locations()
        assert isinstance(res, list)

    def test_transaction_snapshot(self):
        locs = [x['id'] for x in trans.transaction_locations()]
        res = trans.transaction_snapshot(location_ids=locs)
        assert isinstance(res, list)
