"""
Copyright (c) 2022 Center for Astrophysics | Harvard & Smithsonian

This software is licensed for use as described in the LICENSE file in
the root directory of this distribution.

Testing the cost model

Originator: Aaron Oppenheimer March 2020
"""
import unittest
from pandas import Series
from ngehtutil.cost import calculate_costs, get_cost_constants
from ngehtutil.cost import CostConfig
from ngehtutil.cost.cost_model import *
from ngehtutil import *

class CostTestClass(unittest.TestCase):
    """ A set of tests for the cost module """

    def test_costmodel_constants(self):
        """
        In some circumstances we want a copy of the cost constants dictionary. Make sure
        we get a deep copy, not just a reference to the one loaded by the module.
        """
        a = get_cost_constants()
        b = a
        c = get_cost_constants()
        self.assertIs(a, b)
        self.assertIsNot(a,c)

        t = list(a.keys())[0]
        self.assertIs(a[t],b[t])
        self.assertIsNot(a[t],c[t])

    def test_costmodel_stationobjects(self):
        config = CostConfig()
        array = Array.from_name(Array.get_list()[0])
        costs = calculate_costs(config, array.stations())
        self.assertEqual(type(costs), dict)

    def test_capital_costs(self):
        config = CostConfig()
        array = Array.from_name(Array.get_list()[0])
        total_site_costs, new_site_costs = calculate_capital_costs(config, array.stations(), \
            get_cost_constants())
        all_site = sum([x for x in total_site_costs.to_dict().values() if not type(x) is str])
        all_new = sum([x for x in new_site_costs.to_dict().values() if not type(x) is str])
        self.assertTrue(all_site >= all_new)

    def test_operations_costs(self):
        config = CostConfig()
        array = Array.from_name(Array.get_list()[0])
        total_site_costs, new_site_costs = calculate_operations_costs(config, array.stations(), \
            get_cost_constants())
        all_site = sum([x for x in total_site_costs.to_dict().values() if not type(x) is str])
        all_new = sum([x for x in new_site_costs.to_dict().values() if not type(x) is str])
        self.assertTrue(all_site >= all_new)

    def test_data_costs(self):
        """
        TODO make this do something useful
        """
        config = CostConfig()
        array = Array.from_name(Array.get_list()[0])
        data_costs = calculate_data_costs(config, len(array.stations()), 1, 10, \
            get_cost_constants())
        self.assertEqual(type(data_costs.to_dict()), dict)

    def test_station_copies(self):
        """
        Verify that an array made of multiples of the same station works properly
        """

        config = CostConfig()

        # get the costs of an empty array
        array0 = Array('test',[])
        costs0 = calculate_costs(config, array0.stations())

        stn = Station.from_name('LOS')
        array1 = Array('test',[stn]) # one LOS
        costs1 = calculate_costs(config, array1.stations())

        multi = 10
        array2 = Array('test',[stn]*multi) # multiple LOSs
        costs2 = calculate_costs(config, array2.stations())

        base_cost = costs0['TOTAL CAPEX'] + costs1['Design NRE']
        array1_cost = costs1['TOTAL CAPEX'] - base_cost
        array2_cost = costs2['TOTAL CAPEX'] - base_cost
        array2_cost_per_site = array2_cost / multi

        # an array of 1 and an array of 10 should cost close to 10x - not exactly due to rounding
        # in the amount of data grabbed per site
        self.assertTrue(math.isclose(array1_cost, array2_cost_per_site, rel_tol=0.02))

    def test_dish_const_cost(self):
        # verify that costs are different for a site where we have to build a dish vs. one where
        # the dish already exists
        config = CostConfig()

        stn1 = Station.from_name('HAY') # pick one that already has a dish
        cost1 = calculate_costs(config, [stn1])

        stn1.dishes = None # get rid of the dish
        cost2 = calculate_costs(config, [stn1])

        self.assertTrue(cost1['TOTAL CAPEX'] < cost2['TOTAL CAPEX'])
