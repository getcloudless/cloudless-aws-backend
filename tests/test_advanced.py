# -*- coding: utf-8 -*-

from .context import cloudless_aws_backend

import unittest


class AdvancedTestSuite(unittest.TestCase):
    """Advanced test cases."""

    def test_thoughts(self):
        return True
        #self.assertIsNone(cloudless_aws_backend.deploy())


if __name__ == '__main__':
    unittest.main()
