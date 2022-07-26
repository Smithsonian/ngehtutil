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
    """ tests for array objects """

    def test_array_list(self):
        """ show we can get arrays from our database """
        array = Array.get_list()
        self.assertEqual(type(array),list)
        self.assertTrue(len(array)>0)

    def test_default_array(self):
        """ show we can get a default array """
        def_array = Array.get_default_array_name()
        self.assertEqual(type(def_array),str)

        array = Array.get_default()
        self.assertEqual(type(array),Array)

    def test_array_init(self):
        """ show we can make an array from scratch """
        with self.assertRaises(ValueError):
            array = Array('test','test')

        with self.assertRaises(ValueError):
            array = Array('test',['test'])

    def test_array_immutable(self):
        """ show the arrays in the database can't be changed """
        arrays = Array.get_list()
        array1 = Array.from_name(arrays[0])
        array1_len = len(array1.stations())
        array2 = Array.from_name(arrays[1])
        array2_len = len(array2.stations())
        array2_len_orig = array2_len
        self.assertTrue(array1_len != array2_len)
        # we have two different arrays so let's now put the stations from 1 into 2
        array2.stations(array1.stations())
        array2_len = len(array2.stations())
        self.assertTrue(array1_len == array2_len)

        # now, make another array like array2 from the database and show that it's the old one
        array3 = Array.from_name(arrays[1])
        array3_len = len(array3.stations())
        self.assertTrue(array3_len == array2_len_orig)
