#
# Code to manage site weather derived from MERRA-2 data
#

import requests
import os
from pathlib import Path
import shutil

def load_site(sitename, months=None):
    """ Makes sure we have the data for a site for the given months, which is
        a list of month numbers 1-12, or None which means all. """
    
    if not months:
        months = list(range(1,13))
    else:
        if type(months) is int:
            months=[months]
        if not all(x >= 1 and x <= 12 for x in months):
            raise ValueError('Months must be between 1 and 12')

    print(f'loading weather data for site "{sitename}" for months {months}')
    
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

    urlbase = 'https://raw.githubusercontent.com/Smithsonian/ngeht-weather/main/weather_data'
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

    # make sure the target directory is here
    homepath=str(Path(__file__).parent) + '/weather_data'
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
                raise ValueError('no such weather data file for {sitename} {monthmap[m]}')
            open(f'{homepath}/{sitename}/{monthmap[m]}/{f}','w').write(r.content.decode("utf-8"))


def delete_sites():
    homepath=str(Path(__file__).parent) + '/weather_data'
    try:
        shutil.rmtree(homepath)
    except OSError as e:
        print("Error: %s : %s" % (homepath, e.strerror))