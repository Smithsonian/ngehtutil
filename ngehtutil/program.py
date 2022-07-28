"""
Classes to describe VLBI program
"""
from ngehtutil import calculate_costs, CostConfig, Campaign, Array


class Program:
    array = None
    campaign = None

    def __init__(self, array=None, campaign=None):
        if type(array) is not Array:
            raise TypeError
        self.array = array

        if type(campaign) is not Campaign:
            raise TypeError
        self.campaign = campaign

    def calculate_costs(self, **kwargs):
        """
        Use the cost model to figure out what an array and
        campaigns cost.

        Pass in CostConfig attributes to override them.
        """

        if type(self.array) is not Array:
            raise ValueError("Program not configured with an Array")

        if not self.campaign:
            raise ValueError("Program not configured with Campaigns")

        config = CostConfig()
        config.observations_per_year = self.campaign.schedule.obs_per_year
        config.days_per_observation = self.campaign.schedule.obs_days
        config.hours_per_observation = self.campaign.schedule.obs_hours
        config.recording_frequencies = 1

        for k, v in kwargs.items():
            setattr(config, k, v)

        costs, site_costs = calculate_costs(config, self.array.stations())
        return costs, site_costs
