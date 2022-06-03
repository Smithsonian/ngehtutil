"""
Copyright (c) 2022 Center for Astrophysics | Harvard & Smithsonian

This software is licensed for use as described in the LICENSE file in
the root directory of this distribution.

Cost model code

Originator: Aaron Oppenheimer March 2020
"""
import functools
import operator
import logging
import os
import pandas as pd
from ngehtutil.station import Station
import math

# constants from file - we don't want to have to read these every time
CONSTANTS_TABLES = None

def read_constants(infile_name=None):
    """ Read in all of the constants used for calculations as pandas dataframes """
    global CONSTANTS_TABLES # pylint: disable=global-statement
    if CONSTANTS_TABLES is None:

        if infile_name is None:
            infile_name = f'{os.path.dirname(__file__)}/cost_constants.xlsx'

        logging.info('loading cost contants from %s', infile_name)

        tables = {}
        tables['site_development_values_table'] = pd.read_excel(
            infile_name, sheet_name="SiteDevelopmentValues", index_col=0)
        tables['labor_cost_values_table'] = pd.read_excel(
            infile_name, sheet_name="LaborCostValues", index_col=0)
        tables['travel_cost_values_table'] = pd.read_excel(
            infile_name, sheet_name="TravelCostValues", index_col=0)
        tables['autonomy_mode_values_table'] = pd.read_excel(
            infile_name, sheet_name="AutonomyModeValues", index_col=0)
        tables['data_management_values_table'] = pd.read_excel(
            infile_name, sheet_name="DataManagementValues", index_col=0)
        tables['data_management_option_values_table'] = pd.read_excel(
            infile_name, sheet_name="DataManagementOptionValues", index_col=0)
        CONSTANTS_TABLES = tables

    return CONSTANTS_TABLES

def get_cost_constants():
    """
    for purposes of processing on a cluster, we need a deep copy of the constants that
    can be passed to the cost calculation functions instead of using the global one which
    we think is causing headaches.
    """
    if CONSTANTS_TABLES is None:
        read_constants()
    new_const = {k:v.copy() for k,v in CONSTANTS_TABLES.items()}
    return new_const


def calculate_costs(cost_config, sites, cost_constants=None, const_filename=None):
    """
    Perform cost calculations for an array of ngEGT sites

    INPUTS
    ------
    cost_config: CostConfig object

    sites: list of Station objects

    OUTPUTS
    -------
    dataframe of cost information
    """
    # Read the cost constant spreadsheet
    if cost_constants:
        const = cost_constants
    else:
        const = read_constants(const_filename)

    # const = update_constants_from_config(const, cost_config)

    logging.info('calculating costs')

    #
    # Calculate statistics like number of sites, collecting days, amount of data collected
    #
    array_stats = {}
    # add a row just to hold the name of the category.
    array_stats['ARRAY STATS'] = ''

    total_sites_count = len(sites)
    # new_sites = sites.loc[:,sites.loc['eht']==0].to_dict()
    new_sites = [x for x in sites if not x.eht]
    new_sites_count = len(new_sites)
    array_stats['New Sites Count'] = new_sites_count
    array_stats['EHT Sites Count'] = total_sites_count - new_sites_count
    array_stats['Total Sites Count'] = total_sites_count

    array_stats = pd.Series(array_stats)
    array_stats = pd.concat([array_stats,calculate_operating_mode(cost_config, sites, const)])

    total_site_costs, new_site_costs = calculate_capital_costs(cost_config, sites, const)

    t, n = calculate_operations_costs(cost_config, sites, const)
    total_site_costs = pd.concat([total_site_costs, t])
    new_site_costs = pd.concat([new_site_costs, n])

    data_management_costs = calculate_data_costs(cost_config, total_sites_count, \
        array_stats["Data Per Year - Full Array (PB)"], \
            cost_config.observations_per_year*cost_config.days_per_observation, \
                const )

    #
    # work out the average costs for new sites
    #
    avg_new_site_build_costs = new_site_costs[1:].copy()
    new_names = {i:f'New Site Avg {i}' for i in avg_new_site_build_costs.index}
    avg_new_site_build_costs.rename(new_names, inplace=True)
    avg_new_site_build_costs[:] = (avg_new_site_build_costs[:] / new_sites_count) \
        if new_sites_count else 0
    avg_new_site_data_costs = data_management_costs[['Site Recorders','Site Media']]
    new_names = {i:f'New Site Avg {i}' for i in avg_new_site_data_costs.index}
    avg_new_site_data_costs.rename(new_names, inplace=True)
    avg_new_site_data_costs[:] = (avg_new_site_data_costs[:]/ total_sites_count) \
        if new_sites_count else 0

    # add a row just to hold the name of the category.
    avg_new_site_costs = pd.Series(dtype='float')
    avg_new_site_costs['NEW SITE AVG COSTS'] = ''
    avg_new_site_costs = pd.concat([avg_new_site_costs, \
                                    avg_new_site_build_costs, \
                                    avg_new_site_data_costs])

    capex_costs = [
        'New Site Avg Design NRE',
        'New Site Avg Site acquisition / leasing',
        'New Site Avg Infrastructure',
        'New Site Avg Antenna construction',
        'New Site Avg Antenna commissioning',
        'New Site Avg Site Recorders',
        'New Site Avg Site Media',
    ]
    avg_new_site_costs['New Site Total CAPEX'] = \
        sum([avg_new_site_costs[i] for i in capex_costs])

    total_costs = pd.Series(dtype='float')
    total_costs['TOTAL COSTS'] = ''
    total_costs['TOTAL CAPEX'] = total_site_costs[1:].drop('Antenna operations').sum() +\
                                 data_management_costs[['Cluster Build Cost',
                                                        'Site Recorders',
                                                        'Site Media']].sum()
    total_costs['ANNUAL OPEX'] = total_site_costs[['Antenna operations', 'Fulltime staff']].sum() +\
                                 data_management_costs[['Personnel',
                                                        'Holding Data Storage Costs',
                                                        'Fast Data Storage Costs',
                                                        'Transfer Costs',
                                                        'Computation Costs',
                                                        'Data Shipping']].sum()

    everything = pd.concat([pd.Series(array_stats), total_site_costs, data_management_costs, \
                      avg_new_site_costs, total_costs])
    return everything.to_dict()




    ##
    ## OPERATION MODE CALCULATIONS
    ##

def calculate_operating_mode(cost_config, sites, const):
    array_stats = {}

    # calculate stuff about operation mode
    observations_per_year = cost_config.observations_per_year
    days_per_observation = cost_config.days_per_observation
    collecting_days_per_year = observations_per_year * days_per_observation
    hours_per_observation = cost_config.hours_per_observation
    collecting_hours_per_year = observations_per_year * hours_per_observation


    # calculate the amount of data collected per site per hour
    # 'bandwidth' can be overridden by specifying 'recording_bandwidth' in configuration
    vals = const['data_management_values_table'].loc[['Recording bit depth',
                                                  'Sidebands', 'Polarizations',
                                                  'Oversampling factor']].Value
    bandwidth = cost_config.recording_bandwidth
    frequencies = cost_config.recording_frequencies
    gbits_per_second = functools.reduce(operator.mul, vals) * bandwidth * frequencies
    pb_per_hour = gbits_per_second / 8 * 3600 / 1e6
    pb_per_day = pb_per_hour * (hours_per_observation / days_per_observation)
    array_stats["Data Per Observation Per Station"] = pb_per_hour * hours_per_observation

    # calculate the total amount of data for this configuration
    total_data_collected_per_year = math.ceil(len(sites) * collecting_hours_per_year * pb_per_hour)
    array_stats["Data Per Year - Full Array (PB)"] = total_data_collected_per_year

    return pd.Series(array_stats)


###
### CAPITAL COSTS FOR ANTENNAS
###
def calculate_capital_costs(cost_config, sites, const):

    #
    #  calculate costs based on the array configuration - NRE, construction costs, operating costs
    #
    site_costs = pd.DataFrame(index=['Site acquisition / leasing', 'Infrastructure',
                                     'Antenna construction', 'Antenna commissioning'])
    total_site_costs = pd.Series(dtype='float') # holds total cost for all sites
    new_site_costs = pd.Series(dtype='float') # holds total cost for just new sites
    # add a row just to hold the name of the category.
    total_site_costs['SITE COSTS'] = ''
    new_site_costs['NEW SITE COSTS'] = ''

    # calculate the total NRE costs for designing new stations
    total_new_site_nre = 0
    if len(sites):
        new_dish_size = cost_config.dish_size
        dish_cost_multiplier = new_dish_size / 4.0 # not sure where this is from
        autonomy_multiplier = const['autonomy_mode_values_table'].loc['Manual'][
            'complexity_factor']
        nre_costs = const['site_development_values_table'].at['antenna_development_nre','Value'] * \
                        dish_cost_multiplier * autonomy_multiplier
        prototype_costs = const['site_development_values_table'].at[
            'antenna_prototype', 'Value'] * dish_cost_multiplier * autonomy_multiplier

        total_new_site_nre = nre_costs + prototype_costs
    total_site_costs['Design NRE'] = total_new_site_nre
    new_site_costs['Design NRE'] = total_new_site_nre

    # now some numbers for each site, depending on its location, whether it alreasy exists, etc.
    for siteindex, site in enumerate(sites):

        site_costs.loc[:, siteindex] = 0  # everything starts out FREE!!

        # For new sites we have to worry about costs to acquire, build, commission

        if site.dishes is None: # this is a new site

            # Aquisition Costs
            site_aquisition_baseline = const['site_development_values_table']\
                .at['site_acquisition_and_leasing', 'Value']
            site_costs.at['Site acquisition / leasing',
                            siteindex] = site_aquisition_baseline if site.site_acquisition else 0

            # Infrastructure Development
            infrastructure_baseline = const['site_development_values_table'].loc[
                'infrastructure_development', 'Value']
            infrascruture_scaling_factor = const['site_development_values_table'].loc[
                site.existing_infrastructure, 'Value']
            site_costs.at['Infrastructure',
                            siteindex] = infrastructure_baseline * infrascruture_scaling_factor

            # Antenna Construction
            #
            # implements the cost equation as C + kd^e
            dish_size = cost_config.dish_size
            antenna_constant = \
                const['site_development_values_table'].at['antenna_cost_constant','Value']
            antenna_factor1 = const['site_development_values_table'].at['antenna_cost_factor1','Value']
            antenna_factor2 = const['site_development_values_table'].at['antenna_cost_factor2','Value']
            antenna_exp = const['site_development_values_table'].at['antenna_cost_exponent','Value']
            single_antenna_cost = antenna_constant + \
                        (antenna_factor1 * dish_size) + \
                        (antenna_factor2 * pow(dish_size, antenna_exp))

            # site.set_diameter(dish_size) # the site was under-defined, so give it a dish

            construction_cost = single_antenna_cost

            construction_cost = construction_cost * \
                const['site_development_values_table']\
                    .at[site.polar_nonpolar, 'Value']  # polar multiplier

            site_costs.at['Antenna construction', siteindex] = construction_cost
        else:
            # for existing sites, don't need to build dish
            site_costs.at['Site acquisition / leasing', siteindex] = 0
            site_costs.at['Infrastructure', siteindex] = 0
            site_costs.at['Antenna construction', siteindex] = 0

        # Backend - receiver, maser, correlator
        receiver_cost_factor = const['site_development_values_table']\
            .at['receiver_cost_factor', 'Value']
        if cost_config.recording_frequencies > 2:
            triband_cost_multiplier = const['site_development_values_table']\
                .at['triband_cost_multiplier', 'Value']
            receiver_cost_factor = receiver_cost_factor * triband_cost_multiplier
        correlator_cost_factor = const['site_development_values_table']\
            .at['correlator_cost_factor', 'Value']
        maser_cost = const['site_development_values_table'].at['maser_cost', 'Value']
        num_dishes = len(site.dishes) if site.dishes else 1
        backend_cost = (receiver_cost_factor * num_dishes) + \
            (correlator_cost_factor * pow(num_dishes, 2)) + \
            maser_cost

        site_costs.at['Backend costs', siteindex] = backend_cost

        # Antenna Commissioning
        if not site.eht:
            if site.existing_infrastructure == 'Complete':
                # cost to commission existing site
                commissioning_cost = const['site_development_values_table']\
                    .at['commissioning_existing', 'Value']
            else:
                # cost to commission new facility * polar/non-polar factor
                commissioning_cost = const['site_development_values_table']\
                    .at['commissioning_new', 'Value'] * \
                    const['site_development_values_table']\
                        .loc[site.polar_nonpolar, 'Value']
            site_costs.at['Antenna commissioning', siteindex] = commissioning_cost

    total_site_costs = pd.concat([total_site_costs, site_costs.sum(axis=1)])
    
    new_sites = [i for i,x in enumerate(sites) if not x.eht]
    new_site_costs = \
        pd.concat([new_site_costs, site_costs[site_costs.columns.intersection(new_sites)].sum(axis=1)])
    return total_site_costs, new_site_costs

###
### Antenna Operations Costs Per Observation Year, which is primarily about staffing
###
def calculate_operations_costs(cost_config, sites, const):
    """
    Calculate the cost of operating the sites for a year, which is mostly about staffing.
    Uses both per-obeserving-night plus costs of some full-time staff.
    """
    array_stats = {}

    obs_per_year = cost_config.observations_per_year
    obs_days_per_year = cost_config.days_per_observation

    site_costs = pd.DataFrame(index=['Antenna operations'])

    operation_costs = pd.DataFrame(index=['total_non_local_labor_observation',
                                        'total_labor_needed_to_travel_observation',
                                        'total_local_labor_observation',
                                    #   'total_nonlocal_labor_monitoring',
                                    #   'total_local_labor_monitoring',
                                        'total_nonlocal_labor_maintenance',
                                        'total_local_labor_mainenance'])

    for siteindex, site in enumerate(sites):
        #
        # Antenna Operations costs
        # todo - don't we have operations costs for existing sites too?
        #
        operation_costs.loc[:, siteindex] = 0
        autonomy_scenario = cost_config.autonomy_of_operations
        site_region = site.region

        if not site.eht:
            # Antenna operations - total non-local labor during observations
            # eht_and_dedicated_obs_days_per_year = campaigns_per_year * campaign_duration

            labor_needed_to_travel = const['autonomy_mode_values_table']\
                .loc[autonomy_scenario, 'travel_campaign']
            remote_labor = const['autonomy_mode_values_table']\
                .loc[autonomy_scenario, 'remote_campaign_perday']

            # todo in the spreadsheet this is hardwired to NA labor, not by site region.
            na_remote_labor_cost_day = const['labor_cost_values_table'].at['science_salary',
                                                                        'N. America'] / 365

            total_non_local_labor_observation = obs_days_per_year * \
                (labor_needed_to_travel + remote_labor) * na_remote_labor_cost_day
            operation_costs.at['total_non_local_labor_observation',
                                siteindex] = total_non_local_labor_observation

            # Antenna operations - total travel during observations

            travel_cost = const['travel_cost_values_table']\
                .loc[:,site_region].loc['round_trip']
            per_diem = const['travel_cost_values_table']\
                .loc[:,site_region].loc['per_diem']

            operation_costs.at['total_labor_needed_to_travel_observation', siteindex] = \
                (labor_needed_to_travel * \
                    (obs_per_year * travel_cost) + (obs_days_per_year * per_diem))

            # Antenna operations - total local labor during observations
            local_labor = const['autonomy_mode_values_table']\
                .at[autonomy_scenario,'onsite_campaign']
            technician_cost_day = const['labor_cost_values_table']\
                .loc[:,site_region].loc['technician_salary'] / 365

            total_local_labor_observation = \
                obs_days_per_year * local_labor * technician_cost_day
            operation_costs\
                .at['total_local_labor_observation',siteindex] = total_local_labor_observation

            # # Antenna operations - total non-local labor during monitoring
            # nonlocal_labor_onsite_monitoring = const['autonomy_mode_values_table']\
            #     .loc[autonomy_scenario,'nonlocal_onsite_monitoring']
            # remote_labor_cost_day = const['labor_cost_values_table']\
            #     .at['science_salary',site_region] / 365
            # total_nonlocal_labor_monitoring = \
            #     monitoring_days_per_year * nonlocal_labor_onsite_monitoring * remote_labor_cost_day
            # operation_costs\
            #     .at['total_nonlocal_labor_monitoring',siteindex] = total_nonlocal_labor_monitoring

            # # Antenna operations - total local labor during monitoring
            # local_labor_onsite_monitoring = const['autonomy_mode_values_table']\
            #     .at[autonomy_scenario,'local_onsite_monitoring']

            # total_local_labor_monitoring = \
            #     monitoring_days_per_year * local_labor_onsite_monitoring * technician_cost_day
            # operation_costs\
            #     .at['total_local_labor_monitoring',siteindex] = total_local_labor_monitoring

            # Antenna operations - total non-local labor needed for maintenance
            nonlocal_labor_remote_maintenance = const['autonomy_mode_values_table']\
                .loc[autonomy_scenario,'nonlocal_remote_maint']
            scientist_cost_year = const['labor_cost_values_table']\
                .loc[:,site_region].loc['science_salary']

            total_nonlocal_labor_maintenance = \
                nonlocal_labor_remote_maintenance * scientist_cost_year
            operation_costs\
                .at['total_nonlocal_labor_maintenance',siteindex] = \
                    total_nonlocal_labor_maintenance

        # Antenna operations - total local labor needed for maintenance
        local_labor_remote_maintenance = const['autonomy_mode_values_table']\
            .loc[autonomy_scenario,'local_onsite_maint']
        technician_cost_year = const['labor_cost_values_table']\
            .loc[:,site_region].loc['technician_salary']

        total_local_labor_maintenance = local_labor_remote_maintenance * technician_cost_year
        operation_costs\
            .at['total_local_labor_maintenance',siteindex] = total_local_labor_maintenance

        # add 'em up and plug into the site costs
        site_costs.at['Antenna operations',
                        siteindex] = operation_costs.loc[:, siteindex].sum()

    total_site_costs = site_costs.sum(axis=1)
    
    new_sites = [i for i,x in enumerate(sites) if not x.eht]
    new_site_costs = \
        site_costs[site_costs.columns.intersection(new_sites)].sum(axis=1)

    # assume we have a full-time staff of 10 people to coordinate operations
    cost_of_fulltime_staff = \
        3 * const['labor_cost_values_table'].loc[:,'N. America'].loc['science_salary'] + \
        4 * const['labor_cost_values_table'].loc[:,'N. America'].loc['engineering_salary'] + \
        3 * const['labor_cost_values_table'].loc[:,'N. America'].loc['technician_salary']

    total_site_costs['Fulltime staff'] = cost_of_fulltime_staff
    new_site_costs['Fulltime staff'] = cost_of_fulltime_staff

    return total_site_costs, new_site_costs


##
## Data Management Costs
##
def calculate_data_costs(cost_config, sites_count, total_pb_per_year, collecting_days_per_year, \
    const):

    #
    # calculate data management costs
    #
    data_management_costs = pd.Series(dtype='float')
    # row to hold the category title
    data_management_costs['DATA MANAGEMENT'] = ''

    data_management_strategy = cost_config.data_management

    # data center capex
    data_management_costs['Cluster Build Cost'] = \
        const['data_management_option_values_table'].at[data_management_strategy, 'build_cost']

    # data center opex - personnel, data storage, computation costs

    # personnel costs
    data_management_costs['Personnel'] = \
        const['data_management_option_values_table']\
            .loc[data_management_strategy,'fte_required'] * \
                const['data_management_values_table'].at['FTE cost', 'Value']

    # costs to hold data in cold storage while we wait for it all to trickle in
    # if we're in Cloud mode, need to pay for 12 month minimum for cold storage
    months_to_hold = 12 if data_management_strategy == 'Cloud' else const[
        'data_management_values_table'].at['Months for holding data', 'Value']
    data_management_costs['Holding Data Storage Costs'] = \
        const['data_management_option_values_table']\
            .at[data_management_strategy,'holding_storage_perPB'] * \
                months_to_hold * \
                    total_pb_per_year

    # fast data storage cost, while we're processing
    data_management_costs['Fast Data Storage Costs'] = \
        const['data_management_option_values_table']\
            .loc[data_management_strategy,'fast_storage_perPB'] * \
                const['data_management_values_table']\
                    .at['Months for processing', 'Value'] * total_pb_per_year

    # cost to transfer data from one class of storage to another
    data_management_costs['Transfer Costs'] = const['data_management_option_values_table']\
        .at[data_management_strategy,'data_xfer_perPB'] * total_pb_per_year

    # computation costs
    data_management_costs['Computation Costs'] = const['data_management_option_values_table']\
        .at[data_management_strategy, 'compute_fixed'] + \
            const['data_management_option_values_table']\
                .at[data_management_strategy,'compute_perPB'] * total_pb_per_year

    # station capex - recorders and media

    # cost for recorders - one per station
    data_management_costs['Site Recorders'] = sites_count * \
        const['data_management_values_table'].at['Recorder Cost', 'Value']

    # media cost
    max_nights_media = const['data_management_values_table']\
        .at['Max nights of media on-hand', 'Value']
    nights_of_media = min(max_nights_media, collecting_days_per_year)
    total_pb_per_year_per_site = (total_pb_per_year / sites_count) if sites_count else 0
    pb_of_media_per_site = nights_of_media * (total_pb_per_year_per_site / collecting_days_per_year)
    data_management_costs['Site Media'] = sites_count * pb_of_media_per_site * \
        const['data_management_values_table'].at['Media Cost / PB', 'Value']

    # station opex - cost to ship the data
    data_management_costs['Data Shipping'] = const['data_management_option_values_table']\
        .at[data_management_strategy,'shipping_perPB'] * total_pb_per_year

    return data_management_costs
