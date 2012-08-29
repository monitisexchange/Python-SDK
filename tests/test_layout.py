from unittest import TestCase
from nose.tools import *
from binascii import b2a_hex
from os import urandom

import monitis.layout
from monitis.api import Monitis, get, post
from monitis.monitors.params import ResultParams, DataType
from monitis.monitors.custom import CustomMonitor


class TestLayoutApi:

    def setUp(self):
        Monitis.sandbox = False
        Monitis.debug = True

        self.test_page_ids = []
        # test page
        self.temp_str = 'test_' + b2a_hex(urandom(4)).upper()
        self.test_page_name = self.temp_str
        result = monitis.layout.add_page(title=self.test_page_name)
        self.test_page_ids.append(result['data']['pageId'])

        # need a custom monitor for the test page module
        rp = ResultParams('t', 'Test', 'test', DataType('integer'))
        cm = CustomMonitor.add_monitor(rp, name=self.temp_str, tag='test')
        self.custom = cm

        res = monitis.layout.add_page_module(module_name='CustomMonitor',
                                             page_id=self.test_page_ids[0],
                                             column=1,
                                             row=2,
                                             data_module_id=self.custom.monitor_id)
        self.test_page_module_id = res['data']['pageModuleId']

    def tearDown(self):
        for page_id in self.test_page_ids:
            monitis.layout.delete_page(page_id=page_id)
        self.custom.delete_monitor()

    def test_add_page(self):
        title = 'test_add_page_' + b2a_hex(urandom(4)).upper()
        res = monitis.layout.add_page(title=title)
        assert_equal(res['status'], 'ok')
        self.test_page_ids.append(res['data']['pageId'])

    def test_add_page_module(self):
        res = monitis.layout.add_page_module(module_name='CustomMonitor',
                                             page_id=self.test_page_ids[0],
                                             column=1,
                                             row=1,
                                             data_module_id=self.custom.monitor_id)
        assert_equal(res['status'], 'ok')

    def test_delete_page(self):
        title = title = 'test_delete_page_' + b2a_hex(urandom(4)).upper()
        temp_page_id = monitis.layout.add_page(title=title)['data']['pageId']
        res = monitis.layout.delete_page(page_id=temp_page_id)
        assert_equal(res['status'], 'ok')

    def test_delete_page_module(self):
        res = monitis.layout.delete_page_module(page_module_id=self.test_page_module_id)
        assert_equal(res['status'], 'ok')

    def test_pages(self):
        res = monitis.layout.pages()
        assert type(res) is list

    def test_page_modules(self):
        res = monitis.layout.page_modules(page_name=self.test_page_name)
        assert type(res) is list
