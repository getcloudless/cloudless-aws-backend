# -*- coding: utf-8 -*-

from .context import cloudless_aws_backend

import unittest


class AdvancedTestSuite(unittest.TestCase):
    """Advanced test cases."""

    def test_thoughts(self):
        self.assertIsNone(cloudless_aws_backend.hmm())


if __name__ == '__main__':
    unittest.main()
