import os
from re import match
from unittest import TestCase
from nose.tools import *

import monitis.user
from monitis.api import Monitis, resolve_secretkey, resolve_apikey, get


class TestUserApi:

    def setUp(self):
        # Monitis.sandbox = True
        Monitis.debug = True

        [monitis.user.delete_sub_account(x['id'])
            for x in monitis.user.sub_accounts()
            if x['account'].endswith('@test.com')]

        first_name = 'Test'
        last_name = 'Account'
        email = '8u8r43r43@test.com'
        password = 'testpass'
        group = 'testgroup'

        ret = monitis.user.add_sub_account(first_name, last_name, email,
                                           password, group)

        self.test_account_id = ret['data']['userId']

        page_title = get(action='pages')[0]['title']
        res = monitis.user.add_sub_account_pages(user_id=self.test_account_id,
                                                 pages=[page_title])

    def tearDown(self):
        [monitis.user.delete_sub_account(x['id'])
            for x in monitis.user.sub_accounts()
            if x['account'].endswith('@test.com')]

    def test_auth_token(self):
        token = monitis.user.auth_token()
        # token string of uppercase alphanumeric characters
        # sometimes the most significant bits are dropped, apparently
        # a range of 23 to 26 characters should fail *very* rarely
        matched = match('^[0-9A-Z]{23,26}$', token)
        assert matched is not None

    def test_secretkey(self):
        apikey = resolve_apikey()
        expected_secretkey = resolve_secretkey()
        returned_secretkey = monitis.user.secretkey()
        assert_equal(expected_secretkey, returned_secretkey)

    def test_apikey(self):
        expected_apikey = resolve_apikey()
        username = os.environ.get('MONITIS_USER')
        password = os.environ.get('MONITIS_PASS')
        returned_apikey = monitis.user.apikey(username=username,
                                              password=password)
        assert_equal(expected_apikey, returned_apikey)

    def test_add_sub_account(self):
        first_name = 'Test'
        last_name = 'Account'
        email = '8u8r43r44@test.com'
        password = 'testpass'
        group = 'testgroup'

        ret = monitis.user.add_sub_account(first_name, last_name, email,
                                           password, group)
        assert_equal("ok", ret['status'])

    def test_delete_sub_account(self):
        status = monitis.user.delete_sub_account(self.test_account_id)
        assert_equal(status['status'], 'ok')

    def test_sub_accounts(self):
        ret_sa = monitis.user.sub_accounts()
        # all we can check is that some list is returned
        assert type(ret_sa) is list

    def test_add_sub_account_pages(self):
        page_title = get(action='pages')[0]['title']
        res = monitis.user.add_sub_account_pages(user_id=self.test_account_id,
                                                 pages=[page_title])
        assert_equal(res['status'], 'ok')

    def sub_account_pages(self):
        res = monitis.user.sub_account_pages()
        assert type(res) is list

    def test_delete_sub_account_pages(self):
        page_title = get(action='pages')[0]['title']
        res = monitis.user.add_sub_account_pages(user_id=self.test_account_id,
                                                 pages=[page_title])
        assert_equal(res['status'], 'ok')
