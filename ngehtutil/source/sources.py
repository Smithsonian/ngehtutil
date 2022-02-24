"""
Manage things to do with sources
"""
from pathlib import Path
import pandas as pd
from PIL import Image
import os

THE_SOURCES = None

 ## Helper functions

def _init_sources():
    """ do the initial setup on sources """
    global THE_SOURCES
    if THE_SOURCES is None:
        path=str(Path(__file__).parent) + '/config'
        srcs = pd.read_csv(f'{path}/sources.csv', index_col=0)
        THE_SOURCES = srcs

_init_sources()

def get_source_list():
    return list(THE_SOURCES.index)


def get_default_source():
    return list(get_source_list())[0]


def get_source_info(source):
    return dict(THE_SOURCES.loc[source])


def get_source_description(source):
    return THE_SOURCES.loc[source,'DESCRIPTION']


def get_source_freq_list(source):
    the_list=[]
    for freq in [86, 230, 345, 480, 690]:
        if type(THE_SOURCES.loc[source][f'{freq}_DATA']) is str:
            the_list.append(freq)
    return the_list


def get_source_image(source, frequency):
    """ load the image file for a given source and frequency """
    file_name = THE_SOURCES.loc[source][f'{int(frequency)}_IMAGE']
    if file_name:
        path = os.path.abspath(__file__)
        dir_path = os.path.dirname(path)
        im = Image.open(f'{dir_path}/models/{file_name}')
        return im
    else:
        return None


def get_source_data_file(source, frequency):
    """ return the data file for a given source and frequency """
    file_name = THE_SOURCES.loc[source][f'{int(frequency)}_DATA']
    if file_name:
        path = os.path.abspath(__file__)
        dir_path = os.path.dirname(path)
        data = f'{dir_path}/models/{file_name}'
        return data
    else:
        return None