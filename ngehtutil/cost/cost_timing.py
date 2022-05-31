"""
Copyright (c) 2022 Center for Astrophysics | Harvard & Smithsonian

This software is licensed for use as described in the LICENSE file in
the root directory of this distribution.

Cost model code

Originator: Aaron Oppenheimer March 2020
"""
from math import floor
import pandas as pd
import logging

def calculate_costs_over_time(cost_config, array_costs):
    """ Do the calculation of array costs for each of the arrays described in array_data """
    costs_over_time = pd.DataFrame(dtype=float)

    years_advance_spend = 3 # years before we break ground that we start spending capex
    calculation_start = 2020

    logging.info(f'calculating costs over time')

    years_to_build = cost_config.fully_operational - cost_config.start_building + years_advance_spend
    year_first_build = cost_config.start_building - years_advance_spend
    final_year = cost_config.fully_operational + cost_config.active_lifetime
    inflation = 1 + cost_config.inflation_rate
    average_annual_capex = array_costs.loc['TOTAL CAPEX'] / years_to_build
    average_annual_opex = array_costs.loc['ANNUAL OPEX'] / array_costs.loc['Total Sites Count']

    existing_stations = array_costs.loc['EHT Sites Count']
    stations_to_build = array_costs.loc['New Sites Count']
    stations_built_per_year = stations_to_build / years_to_build
    stations_built = 0
    for year in range(calculation_start, final_year+1):
        building_in_progress = year >= year_first_build and year <= cost_config.fully_operational
        stations_operating = year >= cost_config.start_building

        cap_spend = (average_annual_capex * pow(inflation, year-calculation_start)) \
            if building_in_progress else 0

        stations_built += stations_built_per_year \
            if building_in_progress and year < cost_config.fully_operational else 0

        stations_available = existing_stations + floor(stations_built)

        op_spend = (stations_available * average_annual_opex * \
                    pow(inflation, year - calculation_start)) \
                        if stations_operating else 0

        costs_over_time.loc[year,'CAPEX'] = float(cap_spend)
        costs_over_time.loc[year,'OPEX'] = float(op_spend)

    return costs_over_time
