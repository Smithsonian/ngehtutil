# test arrays
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
