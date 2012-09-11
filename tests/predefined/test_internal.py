from unittest import TestCase
from nose.tools import *
from nose.plugins.skip import Skip, SkipTest
from binascii import b2a_hex
from os import urandom

from monitis.api import Monitis, get, post
import monitis.monitors.predefined.internal as internal


class TestInternalApi:

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_internal_monitors(self):
        res = internal.internal_monitors()
        assert isinstance(res, dict)
        assert isinstance(res['processes'], list)

    def test_internal_monitors_list(self):
        res = internal.internal_monitors(types=['memory', 'process'])
        assert isinstance(res, dict)
        assert isinstance(res['processes'], list)

