"""
Copyright (c) 2022 Center for Astrophysics | Harvard & Smithsonian

This software is licensed for use as described in the LICENSE file in
the root directory of this distribution.

Manage things to do with sources

Originator: Aaron Oppenheimer March 2020
"""
from pathlib import Path
import pandas as pd
from PIL import Image
import os

_THE_SOURCES = None


class Source:

    name = None

    @staticmethod
    def get_list():
        return list(_THE_SOURCES.keys())

    @staticmethod
    def from_name(name):
        return _THE_SOURCES[name]

    @staticmethod
    def reinit_sources():
        global _THE_SOURCES
        _THE_SOURCES = None
        _init_sources()

    @staticmethod
    def add_source(name, **kwargs):
        global _THE_SOURCES
        _THE_SOURCES[name] = Source(name=name, **kwargs)

    @classmethod
    def get_default(cls):
        return cls.from_name(cls.get_list()[0])

    def __init__(self, name, **kwargs):
        self.name = name
        for k, v in kwargs.items():
            if v != '':
                setattr(self, k.lower(), v)

    def freq_list(self):
        the_list = []
        for freq in [86, 230, 345, 480, 690]:
            if type(getattr(self, f'{freq}_data', None)) is str:
                the_list.append(freq)
        return the_list

    def picture(self, frequency):
        """ load the image file for a given source and frequency """

        if frequency not in self.freq_list():
            raise ValueError(f'No frequency {0} for source {1}'.format(
                frequency, self.name))

        try:
            file_name = getattr(self, f'{int(frequency)}_image')
        except AttributeError:
            return None

        if file_name:
            path = os.path.abspath(__file__)
            dir_path = os.path.dirname(path)
            im = Image.open(f'{dir_path}/models/{file_name}')
            return im
        else:
            return None

    def fits(self, frequency):
        """ return the data file for a given source and frequency """
        if frequency not in self.freq_list():
            raise ValueError(f'No frequency {0} for source {1}'.format(
                frequency, self.name))

        try:
            file_name = getattr(self, f'{int(frequency)}_data')
        except AttributeError:
            return None

        if file_name:
            if file_name[0] != '/':
                path = os.path.abspath(__file__)
                dir_path = os.path.dirname(path)
                data = f'{dir_path}/models/{file_name}'
            else:
                data = file_name
            return data
        else:
            return None

    def __str__(self):
        return f'Source {self.name}'

    def __repr__(self):
        return f'Source {self.name}'

# Helper functions


def _init_sources():
    """ do the initial setup on sources """
    global _THE_SOURCES
    if _THE_SOURCES is None:
        _THE_SOURCES = {}
        path = str(Path(__file__).parent) + '/config'
        srcs = pd.read_csv(f'{path}/sources.csv', index_col=0)
        for x in srcs.index:
            Source.add_source(name=x, **(srcs.loc[x].to_dict()))


_init_sources()
