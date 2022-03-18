"""
Classes to describe VLBI campaigns
"""

class Schedule():
    """
    Describes an observation schedule
    """
    obs_per_year = None # number of observations in a year
    obs_days = None # number of days for each observation
    obs_hours = None # total number of hours per observation

    def __init__(self, obs_per_year=1, obs_days=5, obs_hours=15):
        self.obs_per_year = obs_per_year
        self.obs_days = obs_days
        self.obs_hours = obs_hours

    def __repr__(self):
        return f'Schedule({self.obs_per_year}, {self.obs_days}, {self.obs_hours})'

    def __str__(self):
        return f'Schedule: {self.obs_per_year} obs per year; {self.obs_days} days per obs; {self.obs_hours} hours per obs'

    def __add__(self, value):
        if not type(value) is Schedule:
            raise TypeError

        return Schedule(obs_per_year = self.obs_per_year + value.obs_per_year,
                        obs_days = self.obs_days + value.obs_days,
                        obs_hours = self.obs_hours + value.obs_hours)


class Campaign:
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