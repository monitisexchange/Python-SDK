from unittest import TestCase
from nose.tools import *
from nose.plugins.skip import Skip, SkipTest
from binascii import b2a_hex
from os import urandom

from monitis.api import Monitis, get, post
import monitis.monitors.predefined.internal.agent as agent


class TestAgentApi:

    def setUp(self):
        # if there is an existing agent, we can use it
        agents = agent.agents()
        if len(agents) > 0:
            self.agent_id = agents[0]['id']
            self.agent_key = agents[0]['key']
            self.platform = agents[0]['platform']
        else:
            self.test_agent_id = None

    def tearDown(self):
        pass

    def test_agents(self):
        # don't have a way to create an agent for the test
        # just make sure there's a list returned
        assert isinstance((agent.agents()), list)

    def test_agent_info(self):
        if self.agent_id:
            res = agent.agent_info(agent_id=self.agent_id)
            assert_equal(res['id'], self.agent_id)
        else:
            raise SkipTest

    def test_all_agents_snapshot(self):
        res = agent.all_agents_snapshot(platform=self.platform)
        assert isinstance(res['agents'], list)

    def test_agent_snapshot(self):
        if self.agent_id:
            res = agent.agent_snapshot(agent_key=self.agent_key)
            assert_equal(res['id'], self.agent_id)
        else:
            raise SkipTest

    def test_delete_agents(self):
        ''' Delete agent

        Since we cannot create a test agent, just skip this test
        '''
        raise SkipTest

    def test_download_agent(self):
        res = agent.download_agent(platform='linux32')
        assert res.code == 200
        res.close
