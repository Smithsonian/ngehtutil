"""
Manage things to do with arrays
"""
from .station import Station
from pathlib import Path
import csv
import pandas as pd
import numpy as np

THE_ARRAYS = None
THE_STATIONS = {}

SITE_FILE_NAME = 'Telescope_Site_Matrix_20220126.xlsx'

def site_file_path():
    path=str(Path(__file__).parent) + '/config'
    return f'{path}/{SITE_FILE_NAME}'

def _init_arrays():
    """ do the initial setup on arrays """
    global THE_ARRAYS, THE_STATIONS
    if THE_ARRAYS is None:

        # set up the arrays, which are just lists of station codes
        THE_ARRAYS = {}
        path=str(Path(__file__).parent) + '/config'
        with open(f'{path}/arrays.csv', newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            for row in reader:
                THE_ARRAYS[row[0]] = [x for x in row[1:] if x]


        # set up the stations
        THE_STATIONS = {}
        sites_data = pd.read_excel(site_file_path(), index_col=0, \
            sheet_name='Basic Site Data')
        pwv_data = pd.read_excel(site_file_path(), index_col=0, \
            sheet_name='PWV')
        for s in sites_data.index:
            d = sites_data.loc[s]
            pwv = list(pwv_data.loc[s])
            stn = Station(name=s, pwv=pwv, **dict(d))
            THE_STATIONS[s] = stn

_init_arrays()


def get_array_list():
    return THE_ARRAYS


def get_default_array():
    return list(get_array_list().keys())[0]


def get_station_list(array=None):
    if array is None:
        return sorted(list(THE_STATIONS.keys()))
    else:
        try:
            return sorted(THE_ARRAYS[array])
        except:
            raise ValueError(f"Can't get stations for array [{array}]")


def get_station_info(stations=None):
    ''' turn a list of station names into a Station object '''
    if stations is None:
        return THE_STATIONS
    else:
        if type(stations) == list:
            the_stns = [THE_STATIONS[x] for x in list(stations)]
            return the_stns
        else:
            return THE_STATIONS[stations]
