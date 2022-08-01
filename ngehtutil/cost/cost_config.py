"""
Copyright (c) 2022 Center for Astrophysics | Harvard & Smithsonian

This software is licensed for use as described in the LICENSE file in
the root directory of this distribution.

Cost model code

Originator: Aaron Oppenheimer March 2020
"""


class CostConfig:
    # Size for new dishes - must be 4, 6, 8, 10
    dish_size = 6

    # one of 'Manual' 'Somewhat Autonomous' 'Semi-Autonomous'
    # or 'Fully Autonomous'
    autonomy_of_operations = 'Manual'

    # one of 'Own Cluster' 'Research Cluster' 'Cloud'
    data_management = 'Own Cluster'
    recording_bandwidth = 8  # in GHz
    recording_frequencies = 2
    start_building = 2025
    fully_operational = 2030
    inflation_rate = 0.02
    active_lifetime = 10
    observations_per_year = 1
    days_per_observation = 3
    hours_per_observation = 30

    # sites to skip when calculating costs for receiver, backend, etc.
    no_upgrade = []

    def __init__(self, **kwargs):
        """
        Pass in values to override defaults
        """
        for k, v in kwargs.items():
            if not hasattr(self, k):
                raise KeyError(f'no configuration key "{k}"')
            setattr(self, k, v)
