# test arrays
from ngehtutil import *
import unittest

class TestClass(unittest.TestCase):
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

    def test_station_diameter(self):
        s = Station.from_name('CNI') # pick one we know doesn't have a dish
        self.assertEqual(s.dishes, None)

        s.set_diameter(10)
        self.assertEqual(len(s.dishes),1)
        self.assertEqual(s.dishes[0].diameter,10)

    def test_station_SEFD(self):
        sl = Station.get_list()
        s = Station(sl[0])

        s.dishes = None
        with self.assertRaises(ValueError):
            sefd = s.SEFD(230,90)

        s.set_diameter(6)
        sefd = s.SEFD(230,90)
        self.assertTrue(sefd >= 0)

    def test_generic_station(self):
        s = Station('test')
        self.assertTrue(len(s.recording_frequencies),1)

    def test_station_frequencies(self):
        """ make sure the stations have between 1 and 3 frequencies """
        for _,stn in Station.get_all().items():
            n = len(stn.recording_frequencies)
            self.assertTrue(n>=1)
            self.assertTrue(n<=3)