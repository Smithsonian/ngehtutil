# arraymodel

Code to manage definitions of arrays and sites for other ngEHT tools.

### Features

This library provides the following functions:

*get_array_list()* - returns a dict in which keys are strings listing array configurations known by the library. Each value is a list of strings identifying the telescope installations that are part of the array. For example:

    >>> al = arrays.get_array_list()
    >>> al.keys()
    dict_keys(['eht2017', 'eht2022', 'ngeht_ref1', 'ngeht_ref1_4', 'ngeht_ref1_6', 'ngeht_ref1_8', 'ngeht_ref1_10'])
    >>> al['eht2017']
    ['PV', 'AZ', 'SM', 'LM', 'AA', 'SP', 'AP', 'JC']

*get_station_list(array=None)* - returns a list of stations. If no array is given, will return all of the stations known to the module. If an array is given, returns the station list for that array.

    >>> arrays.get_station_list()
    ['AA', 'AP', 'AZ', 'BA', 'BR', 'CI', 'CT', 'GB', 'GL', 'GR', 'HA', 'JC', 'KP', 'LM', 'NZ', 'OV', 'PB', 'PV', 'SG', 'SM', 'SP']
    >>> arrays.get_station_list('eht2017')
    ['PV', 'AZ', 'SM', 'LM', 'AA', 'SP', 'AP', 'JC']

*get_station_info(stations=None)* - returns information about stations. Arguments can be None, in which case a dict is returned with keys for each station known to the module, with values containin station info; a list of station identifiers in which case a dict is returns with keys for each of the stations; or a single station identifier in which case the info is returned directly. Station info is a dict including known and derived information about station location, configuration, data rate, etc.

    >>> arrays.get_station_info('AA')
    {'name': 'AA', 'location': None, 'region': None, 'polar': False, 'x': 2225061.164, 'y': -5440057.37, 'z': -2481681.15, 'sefd': [], 'dish_size': 6, 'autonomy_of_operations': 'Manual', 'recording_bandwidth': 8, 'recording_frequencies': 2, 'polarizations': 2, 'sidebands': 2, 'bit_depth': 2, 'lat': -22.891096902887742, 'lon': -67.75473738818759, 'data rate': 256}

### Usage

Include the module in your PYTHONPATH or install it as a submodule in another project.

    >>> from arraymodel import *
    >>> get_station_list()
    ['AA', 'AP', 'AZ', 'BA', 'BR', 'CI', 'CT', 'GB', 'GL', 'GR', 'HA', 'JC', 'KP', 'LM', 'NZ', 'OV', 'PB', 'PV', 'SG', 'SM', 'SP']