"""
Manage things to do with sources
"""
from multiprocessing.sharedctypes import Value
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

    @classmethod
    def get_default_source(cls):
        return cls.get(cls.get_source_list()[0])

    def __init__(self, name, **kwargs):
        self.name = name
        for k,v in kwargs.items():
            setattr(self, k.lower(), v)

    def freq_list(self):
        the_list=[]
        for freq in [86, 230, 345, 480, 690]:
            if type(getattr(self,f'{freq}_data',None)) is str:
                the_list.append(freq)
        return the_list


    def picture(self, frequency):
        """ load the image file for a given source and frequency """

        if not frequency in self.freq_list():
            raise ValueError(f'No frequency {frequency} for source {self.name}')

        file_name = getattr(self,f'{int(frequency)}_image')
        if file_name:
            path = os.path.abspath(__file__)
            dir_path = os.path.dirname(path)
            im = Image.open(f'{dir_path}/models/{file_name}')
            return im
        else:
            return None


    def fits(self, frequency):
        """ return the data file for a given source and frequency """
        if not frequency in self.freq_list():
            raise ValueError(f'No frequency {frequency} for source {self.name}')

        file_name = getattr(self, f'{int(frequency)}_data')
        if file_name:
            path = os.path.abspath(__file__)
            dir_path = os.path.dirname(path)
            data = f'{dir_path}/models/{file_name}'
            return data
        else:
            return None

    def __str__(self):
        return f'Source {self.name}'

    def __repr__(self):
        return f'Source {self.name}'



 ## Helper functions

def _init_sources():
    """ do the initial setup on sources """
    global _THE_SOURCES
    if _THE_SOURCES is None:
        path=str(Path(__file__).parent) + '/config'
        srcs = pd.read_csv(f'{path}/sources.csv', index_col=0)
        _THE_SOURCES = {x:Source(name=x, **(srcs.loc[x].to_dict())) for x in srcs.index}

_init_sources()

