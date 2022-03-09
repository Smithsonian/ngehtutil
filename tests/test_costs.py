# test costs
import unittest
from pandas import Series
from ngehtutil.cost import calculate_costs
from ngehtutil.cost import CostConfig
from ngehtutil.cost.cost_model import *
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
        self.assertEqual(type(costs), dict)

    def test_costmodel_stationobjects(self):
        config = CostConfig()
        array = [get_station_info(get_station_list()[0])]
        costs = calculate_costs(config, array)
        self.assertEqual(type(costs), dict)

    def test_capital_costs(self):
        config = CostConfig()
        array = get_station_info(get_station_list())
        total_site_costs, new_site_costs = calculate_capital_costs(config, array)
        all_site = sum([x for x in total_site_costs.values() if not type(x) is str])
        all_new = sum([x for x in new_site_costs.values() if not type(x) is str])
        self.assertTrue(all_site >= all_new)

    def test_operations_costs(self):
        config = CostConfig()
        array = get_station_info(get_station_list())
        total_site_costs, new_site_costs = calculate_operations_costs(config, array)
        all_site = sum([x for x in total_site_costs.values() if not type(x) is str])
        all_new = sum([x for x in new_site_costs.values() if not type(x) is str])
        self.assertTrue(all_site >= all_new)