# test arrays
from ngehtutil.station import *
import unittest

class TestClass(unittest.TestCase):
    def test_array_list(self):
        a = Array.get_array_list()
        self.assertEqual(type(a),dict)
        self.assertTrue(len(a.keys())>0)

    def test_default_array(self):
        d = Array.get_default_array_name()
        self.assertEqual(type(d),str)

    def test_station_list(self):
        sl1 = Station.get_station_list()
        self.assertTrue(len(sl1)>0) # should get all stations

        d = Array.get_default_array_name()
        sl2 = Array.get_station_names(d)
        self.assertTrue(len(sl2)<=len(sl1))

        with self.assertRaises(KeyError) as info:
            sl3 = Array.get_station_names('foo')

    def test_station_info(self):
        sl = Station.get_station_list()
        info = Station(sl[0])
        self.assertEqual(type(info),Station)
        self.assertEqual(info.name, sl[0])

    def test_station_SEFD(self):
        sl = Station.get_station_list()
        s = Station(sl[0])
        sefd = s.SEFD(230,90)
        self.assertTrue(sefd >= 0)
