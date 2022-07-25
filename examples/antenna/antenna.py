"""
Copyright (c) 2022 Center for Astrophysics | Harvard & Smithsonian

This software is licensed for use as described in the LICENSE file in
the root directory of this distribution.

Code that exercises the utilities library. Generates information about how many dishes can be
built for fixed capital and operational costs to optimize a couple of performance parameters.

Originator: Aaron Oppenheimer March 2020
"""
from ngehtutil import Array, Target, Source, Schedule, Campaign, Program, Station
import random
import pandas as pd
import numpy as np
from copy import copy
import sys
import math


def make_array():
    # make a large array out of real stations
    array = Array.from_name('ngEHT Ref. Array 1.1A')
    stns = array.stations()
    # we want to have a few extras, just pick an average station and add a few
    s = Station.from_name('BAR')
    for i in range(0,4):
        s=copy(s)
        s.name=f'{s.name}{i}'
        stns.append(s)
    array.stations(stns)
    return array


def do_average(func):
    """
    Decorator that runs the function a number of times and returns the average
    """
    def wrapper(*args, **kwargs):
        d = pd.DataFrame()
        reps = 25
        for i in range(0,reps):
            d[i] = func(*args, **kwargs)
        return tuple(np.average(d,axis=1))
    return wrapper


@do_average
def number_for_diameter(diameter, construction_limit, ops_limit):
    """ 
    Find the number of antennas we can build that fit in the budget constraints. If an array
    is too expensive, drop one of the antennas at random.
    """
    t = Target.get_default()
    s = Source.get_default()
    sch = Schedule(obs_per_year=1, obs_days=5, obs_hours=24)
    c = Campaign(t,s,sch)

    array = make_array()
    while array.stations():
        cost = Program(array, c).calculate_costs(dish_size=diameter)
        if cost['TOTAL CAPEX'] <= construction_limit and \
            cost['ANNUAL OPEX'] <= ops_limit:
            # we found a set of dishes that are cheap enough
            break
        # too expensive - get rid of one site at random
        array._stations.pop(random.randrange(len(array._stations)))
    return len(array.stations()), cost['TOTAL CAPEX'], cost['ANNUAL OPEX']


def calc_metrics(construction_limit=999e9, ops_limit=999e9):

    data = pd.DataFrame()
    data.index.name = 'diameter'

    for d in range(4,16): # tdqm animates a progress bar
        num, c, o = number_for_diameter(diameter = d, \
           construction_limit=construction_limit, ops_limit = ops_limit )
        data.loc[d,'number'] = num
        sens = d * d
        data.loc[d,'sensitivity'] = sens
        fid = num * num
        data.loc[d,'fidelity'] = fid
        data.loc[d,'CAPEX'] = c
        data.loc[d,'OPEX'] = o
        data.loc[d,'TCO'] = c + (10 * o)

    # Create normalized version of the sensitivies and fidelities
    data.loc[:,'norm sens'] = data.loc[:,'sensitivity'] / np.max(data.loc[:,'sensitivity'])
    data.loc[:,'norm fid'] = data.loc[:,'fidelity'] / np.max(data.loc[:,'fidelity'])
    data.loc[:,'norm TCO'] = np.max(data.loc[:,'TCO']) - data.loc[:,'TCO']
    data.loc[:,'norm TCO'] = (data.loc[:,'norm TCO'] / np.max(data.loc[:,'norm TCO']))

    # reorder the columns so they match what's in the graphing spreadsheet
    data = data[[
        'number',
        'sensitivity',
        'fidelity',
        'OPEX',
        'CAPEX',
        'norm sens',
        'norm fid',
        'TCO',
        'norm TCO',
    ]]

    a = f'performance for const limit of {construction_limit} and ops limit of {ops_limit}\n'
    b = data.to_csv()
    return f'{a}\n{b}\n\n'


def main():
    output = []
    constlimit = 100e6
    opslimit_fraction = .10
    opslimit = constlimit * opslimit_fraction
    print(f'working on construction-limit only', file=sys.stderr)
    output.append(calc_metrics(construction_limit=constlimit))
    print(f'working on operations-limit only',  file=sys.stderr)
    output.append(calc_metrics(ops_limit=opslimit))
    print(f'working on both limits', file=sys.stderr)
    output.append(calc_metrics(construction_limit=constlimit, ops_limit=opslimit))

    # print the output in a format that is easily pasted into excel
    print('\n')
    print('\n\n\n\n\n\n\n\n'.join(output))

if __name__ == '__main__':
    main()