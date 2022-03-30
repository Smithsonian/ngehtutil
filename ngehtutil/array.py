"""
Manage things to do with arrays

Originator: Aaron Oppenheimer March 2020
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
    """
    Class to represent an Array, comprising a set of Station objects. The module loads a set
    of known arrays that can be accessed through class methods.
    """
    name = None
    _stations = []

    @staticmethod
    def get_list():
        """ Get the list of arrays in the database as a list of names """
        return list(_THE_ARRAYS.keys())

    @classmethod
    def get_default_array_name(cls):
        """ Returns the name of the first known array in the builtin database """
        return cls.get_list()[0]

    @classmethod
    def get_default(cls):
        """ Returns an Array object representing the default array """
        return cls.from_name(cls.get_default_array_name())

    @classmethod
    def get_station_names(cls, name):
        """ Get list of station names associated with an array """
        return _THE_ARRAYS[name]

    @classmethod
    def from_name(cls, name):
        """
        Returns an Array object from the database by name. Will raise an exception if the
        array name is unknown.
        """
        stations = [Station.from_name(x) for x in _THE_ARRAYS[name]]
        return cls(name, stations)

    def __init__(self, name, stations):
        """Initialize an Array object"""
        self.name = name if name else '[none]'
        self.stations(stations)

    def stations(self, stns = None):
        """ return the stations comprising this array, or set it """
        if stns:
            if not type(stns) is list:
                raise ValueError("Can only add lists of Stations to an array")
            if not sum([1 if type(x) is Station else 0 for x in stns]) == len(stns):
                raise ValueError("Can only add lists of Stations to an array")
            self._stations = stns

        return self._stations

    def __str__(self):
        return f'Array {self.name}'

    def __repr__(self):
        return f'Array {self.name}'