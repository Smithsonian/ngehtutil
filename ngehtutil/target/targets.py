"""
Manage things to do with targets
"""
from pathlib import Path
import csv
import pandas as pd
import numpy as np

THE_TARGETS = None

 ## Helper functions

def _init_targets():
    """ do the initial setup on arrays """
    global THE_TARGETS
    if THE_TARGETS is None:
        path=str(Path(__file__).parent) + '/config'
        targs = pd.read_csv(f'{path}/targets.csv', index_col=0)

        def convert_ra_dec(site):
            ra = site['RA_hr']+site['RA_min']/60.0+site['RA_sec']/3600.
            dec = (np.sign(site['Dec_deg'])*(np.abs(site['Dec_deg'])+site['Dec_arcmin']/60.0+site['Dec_arcsec']/3600.))
            return [ra, dec]

        targs[['RA','Dec']] = targs.apply(convert_ra_dec, axis=1, result_type='expand')
        THE_TARGETS = targs[['RA','Dec']]

_init_targets()

def get_target_list():
    return list(THE_TARGETS.index)

def get_target_info(target=None):
    if target is None:
        return THE_TARGETS.to_dict(orient='index')

    if not target in THE_TARGETS.index:
        raise ValueError(f'No information on target {target}')

    return THE_TARGETS.loc[target].to_dict()