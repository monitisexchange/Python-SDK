from unittest import TestCase
from nose.tools import *
from nose.plugins.skip import Skip, SkipTest
from binascii import b2a_hex
from os import urandom

from monitis.api import Monitis, get, post
import monitis.monitors.custom.agent as agent


class TestAgentApi:

    def setUp(self):
        Monitis.sandbox = False
        Monitis.debug = True
        self.temp_str = 'test_' + b2a_hex(urandom(4)).upper()

        # create an agent
        res = agent.add_agent(name=self.temp_str)
        self.agent_id = res['data']

        # add a job
        res = agent.add_job(name=self.temp_str, params='x:ms',
                            interval=3, agent_id=self.agent_id, type='custom')
        self.job_id = res['data']

    def tearDown(self):
        if self.agent_id:
            agent.delete_agent(agent_ids=self.agent_id,
                               delete_monitors='false')

    def test_add_agent(self):
        temp_str = 'test_' + b2a_hex(urandom(4)).upper()
        res = agent.add_agent(name=temp_str)
        assert_equal(res['status'], 'ok')
        agent.delete_agent(agent_ids=res['data'], delete_monitors='false')

    def test_add_job(self):
        res = agent.add_job(name=self.temp_str + '2', params='x:ms',
                            interval=3, agent_id=self.agent_id, type='custom')
        assert_equal(res['status'], 'ok')

    def test_edit_agent(self):
        res = agent.edit_agent(agent_id=self.agent_id, name='foo')
        assert_equal(res['status'], 'ok')

    def test_edit_job(self):
        res = agent.edit_job(job_id=self.job_id, name=self.temp_str + '3')
        assert_equal(res['status'], 'ok')

    def test_delete_agent(self):
        res = agent.delete_agent(agent_ids=self.agent_id,
                                 delete_monitors='false')
        assert_equal(res['status'], 'ok')
        self.agent_id = None

    def test_delete_job(self):
        res = agent.delete_job(job_ids=self.job_id)
        assert_equal(res['status'], 'ok')

    def test_get_agents(self):
        res = agent.get_agents()
        assert isinstance(res, list)
        assert len(res) > 0

    def test_get_jobs(self):
        res = agent.get_jobs(agent_id=self.agent_id)
        assert isinstance(res, list)
        assert len(res) > 0

    def agent_info(self):
        res = agent.agent_info(agent_id=self.agent_id)
        assert_equal(res['id'], self.agent_id)
