"""
Code to cost out array configurations

Executing this file runs a calculation on a test setup.

Requires 'costmodel' as a library accessible from the execution directory

AO 20211012
"""
import sys
from costmodel import CostConfig, calculate_costs, calculate_costs_over_time
from argparse import ArgumentParser
import logging
import pandas as pd
import os

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

def load_array_config(config_file, site_file):
    """ load the array configurations to cost out """
    logging.info('reading configurations from %s', config_file)

    # read configuration for new sites and convert it to a dict
    new_site_config = pd.read_excel(f'{CURRENT_DIR}/{config_file}',index_col=0, \
        sheet_name='NewSiteDefinition')
    new_sites = new_site_config.iloc[:,1:].to_dict()

    # read array definitions and convert to dict of list of sites
    all_site_info = pd.read_excel(f'{CURRENT_DIR}/{site_file}', index_col=0)
    array_configs = pd.read_excel(f'{CURRENT_DIR}/{config_file}',index_col=0, \
        sheet_name='ArrayDefinition')

    arrays = {}
    for array_config in array_configs.columns:
        array_sites = array_configs.loc[:,array_config].dropna().to_list()
        # if a site isn't in our site_info file, take it out of the list
        real_array_sites = []
        for site in array_sites:
            if site in all_site_info.columns:
                real_array_sites.append(site)
            else:
                logging.info(f"Don't know about site {site} so dropping it from {array_config}")
        arrays[array_config] = all_site_info.loc[:,real_array_sites]

    return new_sites, arrays

def write_output(output_file, output_data):
    """ save the data out """
    outfile = f'{CURRENT_DIR}/{output_file}'
    logging.info('writing data to %s',outfile)
    with pd.ExcelWriter(outfile) as writer: # pylint: disable=abstract-class-instantiated
        for d in output_data.items():
            d[1].to_excel(writer, sheet_name=d[0])

def main():
    """ do the cost calculations """

    parser=ArgumentParser(description='Calculate ngEHT array costs')
    parser.add_argument('--const_file', required=False, default=None,
        help='File containing all of the calculation constants (default uses module version)')
    parser.add_argument('--setup_file', required=False, default='array_setup.xlsx',
        help='File containing the array setup(s) to evaluate (default array_setup.xlsx)')
    parser.add_argument('--new_site_config', required=False, default=1,
        help='Which column in setup file defines the new site setup for per-array \
            analysis (default = 1)')
    parser.add_argument('--array', required=False, default=1,
        help='Which column in setup file defines the array for per-config analysis (default = 1)')
    parser.add_argument('--site_file', required=False, default='site_info.xlsx',
        help='File containing info about sites (default site_info.xlsx)')
    parser.add_argument('--output_file', required=False, default='cost_output.xlsx',
        help='Destination file for cost data (default cost_output.xlsx)')
    parser.add_argument('-v', '--verbose', required=False, action='store_true',
        help='Print some progress info')
    args = parser.parse_args()

    if args.verbose:
        logging.basicConfig(level=0, format='%(message)s')

    output_data = {}

    new_site_configs, arrays = load_array_config(args.setup_file, args.site_file)

    # for each array config, assess it against the chosen new site config
    which_config = int(args.new_site_config)
    new_site_config = new_site_configs[list(new_site_configs.keys())[which_config-1]]
    the_config = CostConfig(**new_site_config)
    cost_data=pd.DataFrame()
    costs_over_time = {}
    for array_name, array_info in arrays.items():
        config_cost = calculate_costs(the_config, array_info, args.const_file)
        cost_data[array_name] = pd.Series(new_site_config).append(config_cost)
        config_cost_over_time = calculate_costs_over_time(new_site_config, array_name, config_cost)
        costs_over_time[array_name] = config_cost_over_time
    output_data['Costs by array'] = cost_data
    output_data['Costs over time by array'] = pd.concat(costs_over_time, axis=1)

    # for each site config, assess it against the chosen array
    which_array = int(args.array)
    array_name = list(arrays.keys())[which_array-1]
    array = arrays[array_name]
    cost_data=pd.DataFrame()
    costs_over_time = {}
    for config in new_site_configs.items():
        the_config = CostConfig(**config[1])
        config_cost = calculate_costs(the_config, array, args.const_file)
        config[1]['Array'] = array_name # stick the name of the array into the output
        cost_data[config[0]] = pd.Series(config[1]).append(config_cost)
        config_cost_over_time = calculate_costs_over_time(config[1], array_name, config_cost)
        costs_over_time[config[0]] = config_cost_over_time
    output_data['Costs by config'] = cost_data
    output_data['Costs over time by config'] = pd.concat(costs_over_time, axis=1)

    write_output(args.output_file, output_data)


if __name__ == '__main__':
    main()
