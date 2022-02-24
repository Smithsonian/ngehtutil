"""
Code to cost out array configurations for science meeting exercise

AO 20211021
"""
import itertools
import pandas as pd
from tqdm import tqdm
import sys
sys.path.insert(0,'..')
from cost_config import CostConfig
from cost_model import calculate_costs
import os

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

# options for each of the input parameters
DISH_DIAMETERS = [4, 6, 8, 10]
NGEHT_ANTENNAS = [ # 4, 6, 8, 10 sites
    [],
    ['BAJA'],
    ['OVRO', 'LLA', 'BAJA', 'HAY'],
    ['OVRO', 'LLA', 'BAJA', 'HAY', 'CNI', 'GAM'],
    ['OVRO', 'LLA', 'BAJA', 'HAY', 'CNI', 'GAM', 'GARS', 'CAT'],
    ['OVRO', 'LLA', 'BAJA', 'HAY', 'CNI', 'GAM', 'GARS', 'CAT', 'SGO', 'NZ']
]
EHT_SITES = [ # all 11, 4
    [],
    ['GLT', 'SMA', 'LMT'],
    ['ALMA', 'APEX', 'GLT', 'IRAM-30m', 'JCMT', 'KP', 'LMT', 'NOEMA', 'SMA', 'SMT', 'SPT'],
]
BANDWIDTH = [4, 8, 12]
FREQUENCIES = [2, 3]
CAMPAIGNS = [1, 4, 12]
PARAMETER_NAMES = [
    'dish_size', 'ngeht_sites', 'eht_sites', 'recording_bandwidth', 'recording_frequencies', \
    'campaigns_per_year'
]

ALL_SITE_INFO = None
def load_array_config(sites, site_file='site_info.xlsx'):
    """ load the site information """
    global ALL_SITE_INFO
    if ALL_SITE_INFO is None: # just read it once
        ALL_SITE_INFO = pd.read_excel(f'{CURRENT_DIR}/{site_file}', index_col=0)
    return ALL_SITE_INFO.loc[:,sites]


def main():
    """ do the cost calculations """

    # make all possible combinations and turn it into a list of dicts describing each of the
    # parameters as needed by the cost model
    all_combinations = list(itertools.product(
        DISH_DIAMETERS,
        NGEHT_ANTENNAS,
        EHT_SITES,
        BANDWIDTH,
        FREQUENCIES,
        CAMPAIGNS,
    ))
    all_configurations = [CostConfig(**dict(zip(PARAMETER_NAMES, c))) for c in all_combinations]

    output_data=[]
    for configuration in tqdm(all_configurations):
        array = load_array_config(configuration.eht_sites + configuration.ngeht_sites)
        config_cost = calculate_costs(configuration, array)
        output_data.append(pd.Series(configuration).append(config_cost))

    pd.DataFrame(output_data).transpose().to_excel(f'{CURRENT_DIR}/exercise_out.xlsx')

if __name__ == '__main__':
    main()
