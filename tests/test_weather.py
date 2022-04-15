# test weather
from multiprocessing.sharedctypes import Value
import ngehtutil.station_weather
from ngehtutil.station_weather import *
import unittest
from pathlib import Path


class TestClass(unittest.TestCase):
    def test_fetch_files(self):
        load_site('HAY',1)
        homepath=str(Path(ngehtutil.station_weather.__file__).parent) + '/weather_data'
        self.assertTrue(os.path.isdir(f'{homepath}/HAY/01Jan'))
        self.assertTrue(os.path.exists(f'{homepath}/HAY/01Jan/RH.csv'))
        self.assertFalse(os.path.isdir(f'{homepath}/HAY/02Feb'))
        load_site('HAY',2)
        self.assertTrue(os.path.exists(f'{homepath}/HAY/02Feb/RH.csv'))
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
