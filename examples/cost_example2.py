"""
Copyright (c) 2022 Center for Astrophysics | Harvard & Smithsonian

This software is licensed for use as described in the LICENSE file in
the root directory of this distribution.

Code to demonstrate use of the cost model

Originator: Aaron Oppenheimer March 2020
"""
from ngehtutil.cost import *
from ngehtutil import Array, Station
import time


def test():
    config = CostConfig()
    s1 = Station.from_name('KILI')
    s2 = Station.from_name('HAY')
    s3 = Station.from_name('LOS')

    costs1 = calculate_costs(config, [s1])
    costs2 = calculate_costs(config, [s2])
    costs3 = calculate_costs(config, [s3])
    
    print(f'{s1.name} capex:{costs1["TOTAL CAPEX"]}')
    print(f'{s2.name} capex:{costs2["TOTAL CAPEX"]}')
    print(f'{s3.name} capex:{costs3["TOTAL CAPEX"]}')
    

def doit():
    config = CostConfig(
        observations_per_year=1,
        days_per_observation=60,
        hours_per_observation=60*8
    )
    a = Array.from_name('ngEHT Ref. Array 1.1A + EHT2022')
    costs, nscosts = calculate_capital_costs(config, a.stations(), get_cost_constants())

def doit2():
    config = CostConfig(
        observations_per_year=1,
        days_per_observation=60,
        hours_per_observation=60*8
    )
    a = Array.from_name('ngEHT Ref. Array 1.1A + EHT2022')
    t, n = calculate_operations_costs(config, a.stations(), get_cost_constants())

def dishtest():
    config = CostConfig()
    stat = Station.from_name('HAY')
    stat.dishes = None
    for i in range(6,11):
        config.dish_size = i
        costs = calculate_costs(config, [stat])
        print(str(i)+' meters:',costs["TOTAL CAPEX"])
        # for k,v in costs.items():
        #     print(f'{k}: {v}')

def main():
    reps = 1000
    t1 = time.time()
    for i in range(0,reps):
        doit()
    t2 = time.time()
    print(f'time for capital cost calc: {(t2-t1)/reps}')

    t1 = time.time()
    for i in range(0,reps):
        doit2()
    t2 = time.time()
    print(f'time for operations cost calc: {(t2-t1)/reps}')

    test()

if __name__ == '__main__':
    main()
    dishtest()
