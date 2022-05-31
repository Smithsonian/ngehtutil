"""
Copyright (c) 2022 Center for Astrophysics | Harvard & Smithsonian

This software is licensed for use as described in the LICENSE file in
the root directory of this distribution.

Testing the Weather modeling code

Originator: Aaron Oppenheimer March 2020
"""
from multiprocessing.sharedctypes import Value
import ngehtutil.station_weather
from ngehtutil.station_weather import *
import unittest
from pathlib import Path


class TestClass(unittest.TestCase):
    def test_fetch_files(self):
        delete_sites()
        x = load_site('HAY',1)
        self.assertTrue(x > 1)
        homepath=str(Path(ngehtutil.station_weather.__file__).parent) + '/weather_data'
        self.assertTrue(os.path.isdir(f'{homepath}/HAY/01Jan'))
        self.assertTrue(os.path.exists(f'{homepath}/HAY/01Jan/RH.csv'))
        self.assertFalse(os.path.isdir(f'{homepath}/HAY/02Feb'))
        x = load_site('HAY',[1,2])
        self.assertTrue(x > 1)
        self.assertTrue(os.path.exists(f'{homepath}/HAY/02Feb/RH.csv'))
        
        # make sure that we don't reload files
        x = load_site('HAY',[1,2])
        self.assertTrue(x == 0)
        
        delete_sites()

    def test_delete_files(self):
        load_site('HAY')
        homepath=str(Path(ngehtutil.station_weather.__file__).parent) + '/weather_data'
        self.assertTrue(os.path.isdir(homepath))
        delete_sites()
        self.assertFalse(os.path.isdir(homepath))

    def test_fetch_fail(self):
        with self.assertRaises(ValueError):
            load_site('WOOHOO')
        with self.assertRaises(ValueError):
            load_site('HAY',15)
        with self.assertRaises(ValueError):
            load_site('HAY',[1,2,15])
        delete_sites()

    def test_get_data(self):
        data = get_weather_data('HAY','SEFD_info_230',2009,8,45)
        self.assertTrue(type(data) is dict)
        self.assertTrue(data['data'] is None)

        data = get_weather_data('HAY','SEFD_info_230',2009,8,16)
        self.assertTrue(type(data['data']) is list)
        self.assertTrue(len(data['data']) > 0)
        self.assertTrue(type(data['data'][0]) is tuple)

        data = get_weather_data('HAY','RH',2009,8,16)
        self.assertTrue(len(data['data']) > 0)
        self.assertTrue(type(data['data'][0]) is tuple)
        delete_sites()
