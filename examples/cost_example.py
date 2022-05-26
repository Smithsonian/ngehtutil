from ngehtutil.cost import calculate_costs, CostConfig
from ngehtutil import *


def main():

    config = CostConfig(
        observations_per_year=1,
        days_per_observation=60,
        hours_per_observation=60*8
    )
    array = Array.from_name('ngEHT Ref. Array 1.1A + EHT2022')
    costs = calculate_costs(config, array.stations())
    
    print(f'array: {array}')
    print('CONFIGURATION:')
    for x in dir(config):
        if not x[0]=='_':
            print(f'{x}: {getattr(config,x)}')
    for k,v in costs.items():
        print(f'{k}: {v}')


if __name__ == '__main__':
    main()
