"""
Copyright (c) 2022 Center for Astrophysics | Harvard & Smithsonian

This software is licensed for use as described in the LICENSE file in
the root directory of this distribution.

Testing the Target model

Originator: Aaron Oppenheimer March 2020
"""
from ngehtutil.target import Target
import unittest


class TestClass(unittest.TestCase):
    def test_target_list(self):
        a = Target.get_list()
        self.assertEqual(type(a),list)
        self.assertTrue(len(a)>0)


    def test_target_info(self):
        a = Target.get_list()
        info = Target.from_name(a[0])
        self.assertEqual(type(info),Target)

        with self.assertRaises(KeyError):
            info = Target.from_name('aaron')

    def test_default_target(self):
        t = Target.get_default()
        self.assertEqual(type(t),Target)

