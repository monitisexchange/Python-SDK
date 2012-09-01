from unittest import TestCase
from nose.tools import *
from binascii import b2a_hex
from os import urandom

from monitis.contacts import add_contact, delete_contact
from monitis.api import Monitis, get, post
from monitis.monitors.params import ResultParams, DataType
from monitis.monitors.custom import CustomMonitor
from monitis.notifications import add_notification_rule
from monitis.notifications import delete_notification_rule
from monitis.notifications import get_notification_rules


class TestNotificationsApi:

    def setUp(self):
        # need a custom monitor for the test page module
        self.temp_str = 'test_' + b2a_hex(urandom(4)).upper()
        rp = ResultParams('t', 'Test', 'test', DataType('integer'))
        cm = CustomMonitor.add_monitor(rp, name=self.temp_str, tag='test')
        self.monitor_id = cm.monitor_id
        self.custom = cm

        # a contact or contact group is required
        test_email = 'test' + self.temp_str + '@test.com'
        test_contact = add_contact(first_name='Test',
                                   last_name='User',
                                   account=test_email,
                                   contact_type=1,
                                   timezone=-300,
                                   group='TestGroup_' + self.temp_str)
        self.contact_id = int(test_contact['data']['contactId'])

        # create a notification based on that custom monitor
        monitor_id = self.monitor_id
        monitor_type = 'custom'
        period = 'always'
        contact_id = self.contact_id
        notify_backup = 0
        continuous_alerts = 0
        failure_count = 1
        param_name = 't'
        param_value = '0'
        comparing_method = 'greater'

        self.test_notification = add_notification_rule(
            monitor_id=monitor_id,
            monitor_type=monitor_type,
            period=period,
            contact_id=contact_id,
            notify_backup=notify_backup,
            continuous_alerts=continuous_alerts,
            failure_count=failure_count,
            param_name=param_name,
            param_value=param_value,
            comparing_method=comparing_method)

    def tearDown(self):
        delete_notification_rule(contact_ids=self.contact_id,
                                 monitor_id=self.monitor_id,
                                 monitor_type='custom')
        # remove the temporary custom monitor
        self.custom.delete_monitor()
        delete_contact(contact_id=self.contact_id)

    def test_add_notification_rule(self):
        # already tested in setUp
        pass

    def test_delete_notification_rule(self):
        # already tested in tearDown
        pass

    def test_get_notification_rules(self):
        res = get_notification_rules(monitor_id=self.monitor_id,
                                     monitor_type='custom')

        assert [x['monitorId'] for x in res].count(str(self.monitor_id)) >= 1
