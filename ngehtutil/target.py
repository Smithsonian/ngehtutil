"""
Copyright (c) 2022 Center for Astrophysics | Harvard & Smithsonian

This software is licensed for use as described in the LICENSE file in
the root directory of this distribution.

Code to manage targets

Originator: Aaron Oppenheimer March 2020
"""
from pathlib import Path
import pandas as pd
import numpy as np

THE_TARGETS = None


class Target:
    name = None

    @staticmethod
    def get_list():
        return list(THE_TARGETS.keys())

    @staticmethod
    def from_name(name):
        return THE_TARGETS[name]

    @classmethod
    def get_default(cls):
        return cls.from_name(cls.get_list()[0])

    def __init__(self, name, **kwargs):
        self.name = name
        for k, v in kwargs.items():
            setattr(self, k, v)

    def __str__(self):
        return f'Target {self.name}'

    def __repr__(self):
        return f'Target {self.name}'

# Helper functions


def _init_targets():
    """ do the initial setup on arrays """
    global THE_TARGETS
    if THE_TARGETS is None:
        path = str(Path(__file__).parent) + '/config'
        targs = pd.read_csv(f'{path}/targets.csv', index_col=0)

        def convert_ra_dec(site):
            ra = site['RA_hr']+site['RA_min']/60.0+site['RA_sec']/3600.
            dec = np.sign(site['Dec_deg']) * \
                (np.abs(site['Dec_deg']) +
                 site['Dec_arcmin']/60.0+site['Dec_arcsec']/3600.)
            return [ra, dec]

        targs[['RA', 'Dec']] = \
            targs.apply(convert_ra_dec, axis=1, result_type='expand')
        THE_TARGETS = {x: Target(name=x, **(targs.loc[x].to_dict()))
                       for x in targs.index}


_init_targets()
