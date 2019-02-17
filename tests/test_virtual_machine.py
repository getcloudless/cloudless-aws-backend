# -*- coding: utf-8 -*-

from .context import cloudless_aws_backend

import unittest
import boto3
from moto import mock_ec2


@mock_ec2
class BasicTestSuite(unittest.TestCase):
    """Basic test cases."""

    vm_definition = {"version" : "1.0.0", "name" : "foo",
                     "region": "bar", "availability_zone": "baz",
                     "instance_type": "m1.medium"}
    maxDiff = None

    @mock_ec2
    def test_apply(self):
        instance_type = cloudless_aws_backend.get("GET", [("InstanceType", {"version": "1.0.0", "arch": arch, "mem": "$minimize,$cap(%s)" % mem, "price": "$minimize"})])
        cloudless_aws_backend.apply("CREATE", [("VirtualMachine", self.vm_definition)])
        cloudless_aws_backend.apply("CREATE", [("VirtualMachineGroup", self.vm_definition)])
        self.assertEqual(
                cloudless_aws_backend.apply("GET", [("VirtualMachine", self.vm_definition)]),
                {"instance_type": self.vm_definition["instance_type"]})

if __name__ == '__main__':
    unittest.main()
