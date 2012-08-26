from re import match
from unittest import TestCase
from nose.tools import *

import monitis.user
from monitis.api import Monitis, resolve_secretkey, resolve_apikey


class TestUserApi:

    def setUp(self):
        self.mon = Monitis()
        Monitis.sandbox = True

    def test_auth_token(self):
        token = monitis.user.auth_token()
        # token is a string of exactly 26 uppercase alphanumeric characters
        matched = match('^[0-9A-Z]{26}$', token)
        assert matched is not None

    def test_secretkey(self):
        apikey = resolve_apikey()
        expected_secretkey = resolve_secretkey()
        returned_secretkey  = monitis.user.secretkey()
        assert_equal(expected_secretkey, returned_secretkey)

    # def test_apikey(self):
    #     expected_apikey = resolve_apikey()
    #     returned_apikey = monitis.user.apikey(username='username',
    #                                           password='password')
    #     assert_equal(expected_apikey, returned_apikey)