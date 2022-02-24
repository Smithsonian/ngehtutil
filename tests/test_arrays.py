# test arrays
from ngehtutil.arraymodel.arrays import get_array_list, get_default_array, get_station_list, \
    get_station_info, Station
import unittest

class TestClass(unittest.TestCase):
    def test_array_list(self):
        a = get_array_list()
        self.assertEqual(type(a),dict)
        self.assertTrue(len(a.keys())>0)

    def test_default_array(self):
        d = get_default_array()
        self.assertEqual(type(d),str)

    def test_station_list(self):
        sl1 = get_station_list()
        self.assertTrue(len(sl1)>0) # should get all stations

        d = get_default_array()
        sl2 = get_station_list(d)
        self.assertTrue(len(sl2)<=len(sl1))

        with self.assertRaises(ValueError) as info:
            sl3 = get_station_list('foo')

    def test_station_info(self):
        sl = get_station_list()
        info = get_station_info(sl[0])
        self.assertEqual(type(info),Station)
        self.assertEqual(info.name, sl[0])


