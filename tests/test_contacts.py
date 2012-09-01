from unittest import TestCase
from nose.tools import *

import monitis.contacts
from monitis.api import Monitis, get, post
import monitis.contacts


class TestContactsApi:

    def setUp(self):
        test_contact = \
            monitis.contacts.add_contact(first_name='Test',
                                         last_name='User',
                                         account='test949r43@test.com',
                                         contact_type=1,
                                         timezone=-300,
                                         group='TestGroupr43r43f')
        self.test_id = test_contact['data']['contactId']
        self.test_key = test_contact['data']['confirmationKey']

    def tearDown(self):
        monitis.contacts.delete_contact(contact_id=self.test_id)

    def test_add_contact(self):
        # already tested by setUp
        pass

    def test_edit_contact(self):
        res = monitis.contacts.edit_contact(contact_id=self.test_id,
                                            first_name='Foo')
        assert_equals(res['status'], 'ok')

    def test_delete_contact(self):
        # already tested by tearDown
        pass

    def test_confirm_contact(self):
        test_key = self.test_key
        test_id = self.test_id
        res = monitis.contacts.confirm_contact(contact_id=test_id,
                                               confirmation_key=test_key)
        assert_equals(res['status'], 'ok')

    def test_contact_activate(self):
        res = monitis.contacts.contact_activate(contact_id=self.test_id)
        assert_equals(res['status'], 'ok')

    def test_contact_deactivate(self):
        res = monitis.contacts.contact_deactivate(contact_id=self.test_id)
        assert_equals(res['status'], 'ok')

    def test_get_contacts(self):
        res = monitis.contacts.get_contacts()
        assert [x['contactId'] for x in res].count(self.test_id) == 1

    def test_get_contact_groups(self):
        res = monitis.contacts.get_contact_groups()
        assert type(res) is list

    def test_get_recent_alerts(self):
        res = monitis.contacts.get_recent_alerts()
        assert_equals(res['status'], 'ok')
