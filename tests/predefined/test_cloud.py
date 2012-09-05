from unittest import TestCase
from nose.tools import *
from nose.plugins.skip import Skip, SkipTest
from binascii import b2a_hex
from os import urandom

from monitis.api import Monitis, get, post
import monitis.monitors.predefined.cloud as cloud


class TestCloudApi:

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_cloud_instances(self):
        res = cloud.cloud_instances()
        assert isinstance(res, dict)

    def test_cloud_instance_info(self):
        # find an instance to get info for
        res = cloud.cloud_instances()
        instances_list = [(x, y) for (x, y) in res.items() if len(y) > 0]
        if len(instances_list) > 0:
            # just take the first valid one
            _type, instance_data = instances_list[0]
            args = {'type': _type,
                    'instance_id': instance_data[0]['id']}
            res = cloud.cloud_instance_info(**args)
            assert_equal(res['id'], instance_data[0]['id'])
        else:
            raise SkipTest
