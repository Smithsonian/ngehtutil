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

    def test_station_list(self):
        sl1 = Station.get_list()
        self.assertTrue(len(sl1)>0) # should get all stations

        d = Array.get_default_array_name()
        sl2 = Array.get_station_names(d)
        self.assertTrue(len(sl2)<=len(sl1))

        with self.assertRaises(KeyError) as info:
            sl3 = Array.get_station_names('foo')

    def test_station_info(self):
        sl = Station.get_list()
        info = Station(sl[0])
        self.assertEqual(type(info),Station)
        self.assertEqual(info.name, sl[0])

    def test_station_SEFD(self):
        sl = Station.get_list()
        s = Station(sl[0])
        sefd = s.SEFD(230,90)
        self.assertTrue(sefd >= 0)

    def test_generic_station(self):
        s = Station('test')
        self.assertTrue(len(s.recording_frequencies),1)