"""
Manage things to do with arrays
"""
import csv
from pathlib import Path
from .station import Station

_THE_ARRAYS = None

def _init_arrays():
    """ do the initial setup on arrays """
    global _THE_ARRAYS
    if _THE_ARRAYS is None:

        # set up the arrays, which are just lists of station codes
        _THE_ARRAYS = {}
        path=str(Path(__file__).parent) + '/config'
        with open(f'{path}/arrays.csv', newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            for row in reader:
                _THE_ARRAYS[row[0]] = [x for x in row[1:] if x]
_init_arrays()

class Array:
    name = None
    _stations = []

    # Static methods t get the list of possible items and to get the actual objects

    @staticmethod
    def get_list():
        """get the list of array names we have in the database"""
        return list(_THE_ARRAYS.keys())

    @classmethod
    def get_default_array_name(cls):
        return cls.get_list()[0]

    @classmethod
    def get_station_names(cls, name):
        """ get list of station names associated with an array """
        return _THE_ARRAYS[name]

    # @staticmethod
    # def get_station_names(array):
    #     return _THE_ARRAYS[array]

    def __init__(self, name, stations):
        self.name = name if name else '[none]'
        self._stations = stations

    @classmethod
    def from_name(cls, name):
        stations = [Station.from_name(x) for x in _THE_ARRAYS[name]]
        return cls(name, stations)

    def stations(self):
        """ return the stations comprising this array """
        return self._stations

    def __str__(self):
        return f'Array {self.name}'

    def __repr__(self):
        return f'Array {self.name}'
