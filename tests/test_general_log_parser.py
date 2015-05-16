#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_general_log_parser
----------------------------------

Tests for `general_log_parser` module.
"""


import sys, os, re
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest

from general_log_parser import parser


class TestGeneralLogParser(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_is_valid_date(self):
        log = "a.{}.log"
        file_regex = re.compile(log.replace("{}", "(\d*)"))

        assert parser.is_valid_date(file_regex, "20150505", "20150510", "a.20150505.log") == True
        assert parser.is_valid_date(file_regex, "20150505", "20150510", "a.20150504.log") == False
        assert parser.is_valid_date(file_regex, "20150505", "20150510", "a.20140505.log") == False

    def test_has_piped_input(self):
        assert parser.has_piped_input() == True



if __name__ == '__main__':
    unittest.main()
