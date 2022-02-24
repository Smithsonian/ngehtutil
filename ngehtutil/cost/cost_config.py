#
# CostConfig object defines a bunch of attributes that affect cost calculations. Instantiate
# this object and override defaults in the constructor if desired
#
#   dish_size:              Size for new dishes - must be 4, 6, 8, 10
#   recording_nights:       Number of nights per year the system will record. This is optional;
#                             can instead include operational_scenario
#   autonomy_of_operations:	One of the modes from the AutonomyModeValues tab in
#                             cost_constants.xlsx
#   data_management:    	One of the data management schemes from the
#                             DataManagementOptionValues tab in cost_constants.xlsx
#   start_building:         Year we start construction
#   fully_operational:      Year we complete construction and start operating
#   inflation_rate:         Rate at which cCosts go up over time (e.g. 0.02)
#   active_lifetime:    	Expected life of system in years
#   recording_bandwidth:    Bandwidth of recording (e.g. 8 for 8GHz)
#   recording_frequencies:  Number of frequencies being recorded simultaneously
#   campaigns_per_year      Number of discrete "campaigns" every year
#   event_duration_hours    Expected duration of each campaign event in hours
#   monitoring_days_per_year Number of individual days for monitoring

class CostConfig:
    dish_size = 6
    autonomy_of_operations = 'Manual'
    data_management = 'Own Cluster'
    recording_bandwidth = 8
    recording_frequencies = 2
    start_building = 2025
    fully_operational = 2030
    inflation_rate = 0.02
    active_lifetime = 10
    observations_per_year = 1
    days_per_observation = 3
    hours_per_observation = 30

    def __init__(self, **kwargs):
        """
        Pass in values to override defaults
        """
        for k,v in kwargs.items():
            if not hasattr(self, k):
                raise KeyError(f'no configuration key "{k}"')
            setattr(self, k, v)
