from unittest import TestCase
from nose.tools import *
from nose.plugins.skip import Skip, SkipTest
from binascii import b2a_hex
from os import urandom

from monitis.api import Monitis, get, post
import monitis.monitors.predefined.internal.agent as agent
import monitis.monitors.predefined.internal.ping as ping


class TestPingApi:

    def setUp(self):
        '''
        These tests require an existing agent.  We cannot create one
        so work with test monitors on an existing agent if there is one.
        If none is available, then skip the test.
        '''
        Monitis.debug = True
        agents = agent.agents()
        if len(agents) > 0:
            self.agent_id = agents[0]['id']
            self.agentkey = agents[0]['key']
            self.platform = agents[0]['platform']

            self.temp_str = 'test_' + b2a_hex(urandom(4)).upper()

            # need to create a test monitor on the agent
            args = {
                'user_agent_id': self.agent_id,
                'url': 'mon.itor.us',
                'max_lost': 2,
                'packets_count': 5,
                'packets_size': 32,
                'timeout': 20000,
                'name': self.temp_str,
                'tag': self.temp_str
            }
            mon = ping.add_internal_ping_monitor(**args)
            self.test_id = mon['data']['testId']
        else:
            self.agent_id = None

    def tearDown(self):
        if self.agent_id:
            ping.delete_internal_ping_monitors(test_ids=self.test_id)

    def test_edit_internal_ping_monitor(self):
        args = {
            'test_id': self.test_id,
            'max_lost': 3,
            'packets_count': 6,
            'packets_size': 32,
            'timeout': 20000,
            'name': self.temp_str,
            'tag': self.temp_str
        }
        res = ping.edit_internal_ping_monitor(**args)
        assert_equal(res['status'], 'ok')

    def test_agent_ping_tests(self):
        res = ping.agent_ping_tests(agent_id=self.agent_id)
        assert_equal(res[0]['name'], self.temp_str)

    def test_internal_ping_info(self):
        res = ping.internal_ping_info(monitor_id=self.test_id)
        assert_equal(res['name'], self.temp_str)

    def test_internal_ping_result(self):
        args = {'monitor_id': self.test_id,
                'day': 1, 'month': 1, 'year': 2010}
        res = ping.internal_ping_result(**args)
        # there will be no results with this monitor
        assert isinstance(res['data'], list)
