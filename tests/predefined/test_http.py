from unittest import TestCase
from nose.tools import *
from nose.plugins.skip import Skip, SkipTest
from binascii import b2a_hex
from os import urandom

from monitis.api import Monitis, get, post
import monitis.monitors.predefined.internal.agent as agent
import monitis.monitors.predefined.internal.http as http


class TestHttpApi:

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
                'name': self.temp_str,
                'tag': self.temp_str,
                'timeout': 30000,
                'redirect': 1,
                'post_data': 'apiKey%3Dkldfjeur84dfh%26user%3Dmon_user',
                'load_full': 1,
                'http_method': 1,
                'content_match_flag': 1,
                'content_match_string': 'OK',
                'over_ssl': 1,
                'user_auth': 'monUser',
                'pass_auth': 'monPass11'
            }
            mon = http.add_internal_http_monitor(**args)
            self.test_id = mon['data']['testId']
        else:
            self.agent_id = None

    def tearDown(self):
        if self.agent_id:
            http.delete_internal_http_monitors(test_ids=self.test_id)

    def test_edit_internal_http_monitor(self):
        args = {
            'test_id': self.test_id,
            'name': self.temp_str,
            'tag': self.temp_str,
            'timeout': 25000,
            'http_method': 1,
            'url_params': 'action%3Daddtest%26id%3D568',
            'post_data': 'apiKey%3Dkldfjeur84dfh%26user%3Dmon_user',
            'content_match_string': 'ok',
            'user_auth': 'monUser',
            'pass_auth': 'monPass'
        }
        res = http.edit_internal_http_monitor(**args)
        assert_equal(res['status'], 'ok')

    def test_agent_http_tests(self):
        res = http.agent_http_tests(agent_id=self.agent_id)
        assert_equal(res[0]['name'], self.temp_str)

    def test_internal_http_info(self):
        res = http.internal_http_info(monitor_id=self.test_id)
        assert_equal(res['name'], self.temp_str)

    def test_internal_http_result(self):
        args = {'monitor_id': self.test_id,
                'day': 1, 'month': 1, 'year': 2010}
        res = http.internal_http_result(**args)
        # there will be no results with this monitor
        assert isinstance(res['data'], list)
