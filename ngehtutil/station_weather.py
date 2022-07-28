"""
Copyright (c) 2022 Center for Astrophysics | Harvard & Smithsonian

This software is licensed for use as described in the LICENSE file in
the root directory of this distribution.

Code to manage site weather derived from MERRA-2 data

Originator: Aaron Oppenheimer March 2020
"""

import requests
import os
from pathlib import Path
import shutil
import pandas as pd


monthmap = {
    1: '01Jan',
    2: '02Feb',
    3: '03Mar',
    4: '04Apr',
    5: '05May',
    6: '06Jun',
    7: '07Jul',
    8: '08Aug',
    9: '09Sep',
    10: '10Oct',
    11: '11Nov',
    12: '12Dec'
}

urlbase = 'https://raw.githubusercontent.com/Smithsonian/ngeht-weather/main/weather_data'  # noqa: E501
filenames = [
            'RH.csv',
            'SEFD_info_230.csv',
            'SEFD_info_345.csv',
            'mean_RH.csv',
            'mean_SEFD_info_230.csv',
            'mean_SEFD_info_345.csv',
            'mean_wind_speed.csv',
            'wind_speed.csv',
        ]

homepath = str(Path(__file__).parent) + '/weather_data'


def load_site(sitename, months=None):
    """ Makes sure we have the data for a site for the given months, which is
        a list of month numbers 1-12, or None which means all. """

    if not months:
        months = list(range(1, 13))
    else:
        if type(months) is int:
            months = [months]
        if not all(x >= 1 and x <= 12 for x in months):
            raise ValueError('Months must be between 1 and 12')

    fetched = 0

    months = \
        [x for x in months if not
            os.path.exists(f'{homepath}/{sitename}/{monthmap[x]}/RH.csv')]
    if len(months) == 0:
        return 0  # nothing to load

    # make sure the target directory is here
    if not os.path.isdir(homepath):
        # create the homepath
        os.mkdir(homepath)
    if not os.path.isdir(f'{homepath}/{sitename}'):
        os.mkdir(f'{homepath}/{sitename}')

    for m in months:
        if not os.path.isdir(f'{homepath}/{sitename}/{monthmap[m]}'):
            os.mkdir(f'{homepath}/{sitename}/{monthmap[m]}')
        for f in filenames:
            urlpath = f'{urlbase}/{sitename}/{monthmap[m]}/{f}'
            r = requests.get(urlpath, allow_redirects=True)
            if r.status_code == 404:
                raise ValueError(
                    'no such weather data file for {sitename} {monthmap[m]}')
            fp = open(f'{homepath}/{sitename}/{monthmap[m]}/{f}', 'w')
            fp.write(r.content.decode("utf-8"))
            fetched = fetched + 1

    return fetched


def delete_sites():
    """ get rid of any downloaded weather files """
    try:
        shutil.rmtree(homepath)
    except FileNotFoundError:
        pass


def get_weather_data(site, type, year, month, day):
    """ return specific information from the weather data """

    # make sure we have the files
    load_site(site, month)

    # get the data
    file = f'{homepath}/{site}/{monthmap[month]}/{type}.csv'
    data = pd.read_csv(file, comment='#')

    ret_data = list((data[(data.loc[:, 'year'] == year) &
        (data.loc[:, 'day']==day)].iloc[:, 3:]).itertuples(name=None, index=False))  # noqa E128

    ret = {'index': list(data.columns[3:]),
           'data': ret_data if ret_data else None
           }
    return ret
    # return ret[0] if len(ret)==1 else None if len(ret)==0 else ret
