"""
Classes to describe VLBI program
"""
from ngehtutil import calculate_costs, CostConfig, Campaign, Array

class Program:
    array = None
    campaigns = []

    def __init__(self, array=None, campaigns=None):
        self.array = array
        if type(campaigns) == Campaign:
            self.campaigns = [campaigns]
        else:
            self.campaigns = campaigns


    def calculate_costs(self):
        """ use the cost model to figure out what an array and campaigns cost """

        if type(self.array) is not Array:
            raise ValueError("Program not configured with an Array")

        if not self.campaigns:
            raise ValueError("Program not configured with Campaigns")

        config = CostConfig()
        config.observations_per_year = self.campaigns[0].schedule.obs_per_year
        config.days_per_observation = self.campaigns[0].schedule.obs_days
        config.hours_per_observation = self.campaigns[0].schedule.obs_hours
        config.recording_frequencies = 1
        
        costs = calculate_costs(config, self.array.stations())
        return costs

