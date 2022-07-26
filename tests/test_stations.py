"""
Copyright (c) 2022 Center for Astrophysics | Harvard & Smithsonian

This software is licensed for use as described in the LICENSE file in
the root directory of this distribution.

Testing the Station model

Originator: Aaron Oppenheimer March 2020
"""
import unittest
from ngehtutil import Station, Array
from ngehtutil.station_weather import delete_sites

class TestClass(unittest.TestCase):
    """ tests for the Station """

    def test_station_list(self):
        """ show that we can get stations from the Station class """
        sl1 = Station.get_list()
        self.assertTrue(len(sl1)>0) # should get all stations

        array = Array.get_default_array_name()
        sl2 = Array.get_station_names(array)
        self.assertTrue(len(sl2)<=len(sl1))

        with self.assertRaises(KeyError):
            _ = Array.get_station_names('foo')

    def test_station_info(self):
        """ show that stations have names and things """
        station_list = Station.get_list()
        info = Station(station_list[0])
        self.assertEqual(type(info),Station)
        self.assertEqual(info.name, station_list[0])

    def test_station_diameter(self):
        """ show that we can get/set dish diameters """
        station = Station.from_name('CNI') # pick one we know doesn't have a dish
        self.assertEqual(station.dishes, None)

        station.set_diameter(10)
        self.assertEqual(len(station.dishes),1)
        self.assertEqual(station.dishes[0].diameter,10)

    def test_station_sefd(self):
        """ show that we get something resonable from SEFD """
        station_list = Station.get_list()
        station = Station(station_list[0])

        station.dishes = None
        with self.assertRaises(ValueError):
            sefd = station.SEFD(230,90)

        station.set_diameter(6)
        sefd = station.SEFD(230,90)
        self.assertTrue(sefd >= 0)

    def test_generic_station(self):
        """ show that we can make a generic station with defaults """
        station = Station('test')
        self.assertTrue(len(station.recording_frequencies),1)

    def test_station_frequencies(self):
        """ make sure the stations have between 1 and 3 frequencies """
        for _,stn in Station.get_all().items():
            num_freq = len(stn.recording_frequencies)
            self.assertTrue(num_freq >= 1)
            self.assertTrue(num_freq <= 3)

    def test_station_weather(self):
        """ show that we get weather data out of known stations """
        station = Station.from_name('HAY')
        data = station.get_weather('SEFD_info_230',2009,8,16)
        self.assertTrue(isinstance(data['data'], list))
        self.assertTrue(len(data['data']) > 0)
        self.assertTrue(isinstance(data['data'][0], tuple))
        delete_sites()

    def test_station_dupes(self):
        """ demonstrate that we can't have an array with stations with same name """
        stn1 = Station(name="s1")
        stn2 = Station(name="s2")
        stn3 = Station(name="s1")
        with self.assertRaises(ValueError):
            _ = Array(name="test", stations=[stn1, stn2, stn3])

    def test_station_immutable(self):
        """ make sure that when we request a station, we can't change it for other people """
        cni = Station.from_name("CNI")
        self.assertTrue(cni.dishes is None)
        cni.set_diameter(9)
        self.assertTrue(isinstance(cni.dishes, list))
        cni2 = Station.from_name("CNI")
        self.assertTrue(cni2.dishes is None)