from unittest import TestCase
from nose.tools import *
from nose.plugins.skip import Skip, SkipTest
from binascii import b2a_hex
from os import urandom

from monitis.api import Monitis, get, post
import monitis.monitors.predefined.visitortracker as vt


class TestVisitorTrackerApi:

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def find_visitor_tracker_site_id(self):
        vts = vt.visitor_tracking_tests()
        if len(vts) > 0:
            return vts[0][3]
        else:
            return None

    def test_visitor_tracking_tests(self):
        res = vt.visitor_tracking_tests()
        assert isinstance(res, list)

    def test_visitor_tracking_info(self):
        # TODO test this with an existing VT instance
        site_id = self.find_visitor_tracker_site_id()
        if not site_id:
            raise SkipTest
        res = vt.visitor_tracking_info(site_id=site_id)
        assert_equals(res['sId'], site_id)

    def test_visitor_tracking_results(self):
        # TODO test this with an existing VT instance
        site_id = self.find_visitor_tracker_site_id()
        if not site_id:
            raise SkipTest
        args = {'site_id': site_id, 'year': 1990, 'month': 1, 'day':1}
        res = vt.visitor_tracking_results(**args)
        assert isinstance(res['data'], list)
