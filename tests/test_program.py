"""
Copyright (c) 2022 Center for Astrophysics | Harvard & Smithsonian

This software is licensed for use as described in the LICENSE file in
the root directory of this distribution.

Testing the program model

Originator: Aaron Oppenheimer March 2020
"""
from ngehtutil import *
import unittest
import copy

class TestClass(unittest.TestCase):
    def test_program_cost(self):
        t = Target.get_default()
        s = Source.get_default()
        sch = Schedule(obs_per_year=1, obs_days=1, obs_hours=12)
        c = Campaign(t,s,sch)
        stn = Station.from_name('OVRO')
        array = Array(f'test', [stn])
        costs, site_costs = Program(array, c).calculate_costs()
        self.assertEqual(type(costs), dict)
        self.assertEqual(type(site_costs), dict)


    def test_program_cost_config_override(self):
        t = Target.get_default()
        s = Source.get_default()
        sch = Schedule(obs_per_year=1, obs_days=1, obs_hours=12)
        c = Campaign(t,s,sch)
        stn = Station.from_name('OVRO')
        array = Array(f'test', [stn])
        prog = Program(array, c)
        costs1, _ = prog.calculate_costs(dish_size=6)
        costs2, _ = prog.calculate_costs(dish_size=10)
        self.assertTrue(costs1['Antenna construction']<costs2['Antenna construction'])
        