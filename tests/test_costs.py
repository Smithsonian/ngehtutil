# test costs
import unittest
from pandas import Series
from ngehtutil.costmodel.cost_model import calculate_costs
from ngehtutil.costmodel.cost_config import CostConfig

class TestClass(unittest.TestCase):

    def test_costmodel(self):
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
