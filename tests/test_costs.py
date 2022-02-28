# test costs
import unittest
from pandas import Series
from ngehtutil.cost import calculate_costs
from ngehtutil.cost import CostConfig
from ngehtutil.station import get_station_list, get_station_info

class TestClass(unittest.TestCase):

    def test_costmodel_stationdicts(self):
        config = CostConfig()
        array = [
                    {
                        "name" : "teststation1",
                        "eht" : False,
                        "site_acquisition" : True,
                        "existing_infrastructure" : "Partial",
                        "region" : "N. America / Europe",
                        "polar_nonpolar" : "Non-polar",
                    },
                    {
                        "name" : "teststation2",
                        "eht" : False,
                        "site_acquisition" : True,
                        "existing_infrastructure" : "Partial",
                        "region" : "N. America / Europe",
                        "polar_nonpolar" : "Non-polar",
                    }

        ]
        costs = calculate_costs(config, array)
        self.assertEqual(type(costs), Series)

    def test_costmodel_stationobjects(self):
        config = CostConfig()
        array = [get_station_info(get_station_list()[0])]
        costs = calculate_costs(config, array)
        self.assertEqual(type(costs), Series)

