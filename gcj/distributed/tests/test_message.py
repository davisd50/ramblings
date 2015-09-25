"""Test
"""
import unittest
from doctest import DocTestSuite
from doctest import DocFileSuite

import gcj.distributed

def test_suite():
    return unittest.TestSuite((
        DocTestSuite('gcj.distributed.message'),))

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')