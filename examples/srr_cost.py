"""
Copyright (c) 2022 Center for Astrophysics | Harvard & Smithsonian

This software is licensed for use as described in the LICENSE file in
the root directory of this distribution.

Code to demonstrate use of the cost model

Originator: Aaron Oppenheimer March 2020
"""
from ngehtutil.cost import calculate_costs, CostConfig, get_cost_constants
from ngehtutil import *


def main():

    config = CostConfig(
        dish_size=6,
        observations_per_year=1,
        days_per_observation=60,
        hours_per_observation=60*8,
        no_upgrade=['ALMA', 'NOEMA', 'SMA']
    )

    array = Array.from_name('eht2022')
    stns = array.stations()
    new_stn_list = ['BOL','BRZ','PIKE','GAM','CAT','HAY','OVRO']
    new_stns = [Station.from_name(i) for i in new_stn_list]

    bima_stn_list = ['LAS', 'CNI', 'BAJA']
    bima_stns = [Station.from_name(i) for i in bima_stn_list]
    for s in bima_stns:
        s.set_diameter(6)

    stns = stns + new_stns + bima_stns

    costs = calculate_costs(config, stns)
    
    print(f'array: {array}')
    print('CONFIGURATION:')
    for x in dir(config):
        if not x[0]=='_':
            print(f'{x}: {getattr(config,x)}')
    for k,v in costs.items():
        print(f'{k}: {v}')


if __name__ == '__main__':
    main()
