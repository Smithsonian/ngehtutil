"""
Copyright (c) 2022 Center for Astrophysics | Harvard & Smithsonian

This software is licensed for use as described in the LICENSE file in
the root directory of this distribution.

Testing Arrays

Originator: Aaron Oppenheimer March 2020
"""
from ngehtutil import *
import unittest

class TestClass(unittest.TestCase):
    def test_array_list(self):
        a = Array.get_list()
        self.assertEqual(type(a),list)
        self.assertTrue(len(a)>0)

    def test_default_array(self):
        d = Array.get_default_array_name()
        self.assertEqual(type(d),str)

        a = Array.get_default()
        self.assertEqual(type(a),Array)

    def test_array_init(self):
        with self.assertRaises(ValueError):
            a = Array('test','test')

        with self.assertRaises(ValueError):
            a = Array('test',['test'])
