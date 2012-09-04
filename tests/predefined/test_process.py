from unittest import TestCase
from nose.tools import *
from nose.plugins.skip import Skip, SkipTest
from binascii import b2a_hex
from os import urandom

from monitis.api import Monitis, get, post
import monitis.monitors.predefined.internal.agent as agent
import monitis.monitors.predefined.internal.process as process


class TestProcessApi:

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
                'agentkey': self.agentkey,
                'cpu_limit': 60,
                'memory_limit': 100,
                'virtual_memory_limit': 100,
                'process_name': self.temp_str,
                'name': self.temp_str,
                'tag': self.temp_str}
            mon = process.add_process_monitor(**args)
            self.test_id = mon['data']['testId']
        else:
            self.agent_id = None

    def tearDown(self):
        if self.agent_id:
            process.delete_process_monitors(test_ids=self.test_id)

    def test_edit_process_monitor(self):
        args = {
            'test_id': self.test_id,
            'name': self.temp_str,
            'tag': self.temp_str,
            'cpu_limit': 70,
            'memory_limit': 100,
            'virtual_memory_limit': 100}
        res = process.edit_process_monitor(**args)
        assert_equal(res['status'], 'ok')

    def test_agent_processes(self):
        res = process.agent_processes(agent_id=self.agent_id)
        assert_equal(res[0]['name'], self.temp_str)

    def test_process_info(self):
        res = process.process_info(monitor_id=self.test_id)
        assert_equal(res['name'], self.temp_str)

    def test_process_result(self):
        args = {'monitor_id': self.test_id,
                'day': 1, 'month': 1, 'year': 2010}
        res = process.process_result(**args)
        # there will be no results with this monitor
        assert isinstance(res, list)
