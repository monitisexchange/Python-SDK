from unittest import TestCase
from nose.tools import *
from nose.plugins.skip import Skip, SkipTest
from binascii import b2a_hex
from os import urandom

from monitis.api import Monitis, get, post
import monitis.monitors.predefined.internal.agent as agent
import monitis.monitors.predefined.internal.cpu as cpu


class TestCPUMonitor:

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
                'idle_min': 0,
                'io_wait_max': 100,
                'kernel_max': 100,
                'nice_max': 100,
                'used_max': 100,
                'name': self.temp_str,
                'tag': self.temp_str
            }
            mon = cpu.add_cpu_monitor(**args)
            self.test_id = mon['data']['testId']
        else:
            self.agent_id = None

    def tearDown(self):
        if self.agent_id:
            cpu.delete_cpu_monitors(test_ids=self.test_id)

    # already tested in setUp
    # def test_add_cpu_monitor(self):
    #     pass

    def test_edit_cpu_monitor(self):
        if not self.agent_id:
            raise SkipTest
        else:
            args = {
                'test_id': self.test_id,
                'idle_min': 1,
                'io_wait_max': 99,
                'kernel_max': 99,
                'nice_max': 99,
                'used_max': 99,
                'name': self.temp_str,
                'tag': self.temp_str
            }
            res = cpu.edit_cpu_monitor(**args)
            assert_equal(res['status'], 'ok')

    def test_agent_cpu(self):
        res = cpu.agent_cpu(agent_id=self.agent_id)
        assert_equal(res[0]['name'], self.temp_str)

    def test_cpu_info(self):
        res = cpu.cpu_info(monitor_id=self.test_id)
        assert_equal(res['name'], self.temp_str)

    def test_cpu_result(self):
        args = {'monitor_id': self.test_id,
                'day': 1, 'month': 1, 'year': 2010}
        res = cpu.cpu_result(**args)
        # there will be no results with this monitor
        assert isinstance(res, list)
