"""
Copyright (c) 2022 Center for Astrophysics | Harvard & Smithsonian

This software is licensed for use as described in the LICENSE file in
the root directory of this distribution.

Classes to describe VLBI campaigns

Originator: Aaron Oppenheimer March 2020
"""


class Schedule():
    """
    Describes an observation schedule in terms of number of events per year,
    duration of event in days, and data captured by hours observed.
    """
    obs_per_year = None  # number of observations in a year
    obs_days = None  # number of days for each observation
    obs_hours = None  # total number of hours per observation

    def __init__(self, obs_per_year=1, obs_days=5, obs_hours=15):
        """ Initialize a schedule """
        self.obs_per_year = obs_per_year
        self.obs_days = obs_days
        self.obs_hours = obs_hours

    def __repr__(self):
        return 'Schedule({0}, {1}, {2})'.format(
            self.obs_per_year, self.obs_days, self.obs_hours
        )

    def __str__(self):
        return 'Schedule: {0} obs/year; {1} days/obs; {2} hours/obs'.format(
            self.obs_per_year,
            self.obs_days,
            self.obs_hours
        )

    # THIS DOESN'T DO THE RIGHT THING - For 1,2,3 + 1,2,3 we should not
    # end up with 2 4-day events
    #
    # def __add__(self, value):
    #     """ Combine two schedules into a single schedule """

    #     if not type(value) is Schedule:
    #         raise TypeError

    #     return Schedule(obs_per_year =
    #                       self.obs_per_year + value.obs_per_year,
    #                     obs_days = self.obs_days + value.obs_days,
    #                     obs_hours = self.obs_hours + value.obs_hours)


class Campaign:
    """
    Class to describe a "campaign" which comprises a target in the sky,
    a source to observe, and a schedule for the observation.
    """
    schedule = None
    target = None
    source = None

    def __init__(self, target, source, schedule):
        self.schedule = schedule
        self.target = target
        self.source = source

    def __str__(self):
        return f'{self.source} @ {self.target} for {self.schedule}'

    def __repr__(self):
        return f'{self.source} @ {self.target} for {self.schedule}'
