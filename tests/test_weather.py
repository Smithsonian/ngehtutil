# test weather
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
        
        # make sure that we don't reload files - except we do now because it's safer as the data
        # isn't finalized. So even though we have downloaded the files already, make sure that
        # when we request them again, we still download them.
        x = load_site('HAY',[1,2])
        self.assertTrue(x > 0)
        # self.assertTrue(x == 0) # for the future, makes sure we did *not* download anything

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

        data = get_weather_data('HAY','RH',9,8,16)
        self.assertTrue(len(data['data']) > 0)
        self.assertTrue(type(data['data'][0]) is tuple)
