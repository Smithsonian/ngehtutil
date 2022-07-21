"""
Copyright (c) 2022 Center for Astrophysics | Harvard & Smithsonian

This software is licensed for use as described in the LICENSE file in
the root directory of this distribution.

Code to demonstrate use of the cost model

Originator: Aaron Oppenheimer July 2020
"""
from ngehtutil.cost import calculate_costs, CostConfig
from ngehtutil import *

def main():

    config = CostConfig(
        observations_per_year=1,
        days_per_observation=60,
        hours_per_observation=60*8,
        no_upgrade = ['ALMA', 'NOEMA', 'SMA']
    )


    site_names = ['OVRO', 'CNI', 'BAJA', 'LAS', 'HAY', 'PIKE', 'BOL', 'CAT', 'BRZ', 'GAM'] + \
        Array.get_station_names("eht2022")
    
    # array = Array.from_name('ngEHT Ref. Array 1.1A + EHT2022')
    array = Array('Phase 1 + 2', [Station.from_name(x) for x in site_names])
    costs, site_costs = calculate_costs(config, array.stations())
    
    print(f'array: {array}')
    print('CONFIGURATION:')
    for x in dir(config):
        if not x[0]=='_':
            print(f'{x}: {getattr(config,x)}')
    for k,v in costs.items():
        print(f'{k},{v}')

    print('\n')

    # print site names, skip first column
    names = ','.join(['SITE'] + list(site_costs.keys()))
    print(names)

    # get the list of things we want to look at for each site
    line_items = site_costs[list(site_costs.keys())[0]].keys()

    for li in line_items:
        print(','.join([li]+[str(site_costs[x][li]) for x in site_costs.keys()]))

    # for k,v in site_costs.items():
    #     print(k)
    #     for sk, sv in v.items():
    #         print(f'{sk},{sv}')


if __name__ == '__main__':
    main()
