# ngeht-util - Utilities for ngEHT

*ngeht-util* is a library of python modules to help in the design, development, and analysis of the
ngEHT VLBI telescope. It consists of four models: station, source, target, and cost.

## Installation

The library is installed using pip, and it is recommended to use a virtual environment. The library
is installed directly from github. To install the latest plus its dependencies:

    pip install git+https://github.com/ngeht/ngeht-util.git

## Station Module

The Statiopn module contains models and functions to manage the definition of VLBI arrays and stations.

### Usage

    from ngehtutil.station import *

This library provides the following functions:

*get_array_list()* - returns a dict in which keys are strings listing array configurations known by the library. Each value is a list of strings identifying the telescope installations that are part of the array.

    >>> al = arrays.get_array_list()
    >>> al.keys()
    dict_keys(['eht2017', 'eht2022', 'ngeht_ref1', 'ngeht_ref1_4', 'ngeht_ref1_6', 'ngeht_ref1_8', 'ngeht_ref1_10'])
    >>> al['eht2017']
    ['IRAM-30m', 'SMT', 'SMA', 'LMT', 'ALMA', 'SPT', 'APEX', 'JCMT']

*get_station_list(array=None)* - returns a list of stations. If no array is given, will return all of the stations known to the module. If an array is given, returns the station list for that array.

    >>> arrays.get_station_list()
    ['ALMA', 'APEX', 'BAJA', 'BAN', 'BAR', 'BGA', 'BGK', 'BLDR', 'BMAC', 'BOL', 'BRZ', 'CAS', 'CAT', 'CNI', 'Dome A', 'Dome C', 'Dome F', 'ERB', 'FAIR', 'FUJI', 'GAM', 'GARS', 'GLT', 'GLT-S', 'HAN', 'HAY', 'HOP', 'IRAM-30m', 'JCMT', 'JELM', 'KEN', 'KILI', 'KP', 'KVNYS', 'LAS', 'LLA', 'LMT', 'LOS', 'NOB', 'NOEMA', 'NOR', 'NZ', 'ORG', 'OVRO', 'PAR', 'PIKE', 'SAN', 'SGO', 'SMA', 'SMT', 'SOC', 'SPT', 'SPX', 'SUF', 'YAN', 'YBG']
    >>> arrays.get_station_list('eht2017')
    ['ALMA', 'APEX', 'IRAM-30m', 'JCMT', 'LMT', 'SMA', 'SMT', 'SPT']

*get_station_info(stations=None)* - returns information about stations. Arguments can be None, in which case a dict is returned with keys for each station known to the module, with values containin station info; a list of station identifiers in which case a dict is returns with keys for each of the stations; or a single station identifier in which case the info is returned directly. Station info is an object with attributes including known and derived information about station location, configuration, data rate, etc.

    >>> alma = arrays.get_station_info('Alma')

Station objects have the following attributes:

* name: name of station (required parameter)
* pwv: array of average pwv measurements, one for each month of the year
* country: country location of station
* locality: locality within country of station
* latitude: position
* longitude: position
* elevation: position
* site_or_region: whether "station" indicates a specific installation or a region
* owner: institution operating the station
* antenna_count: number of dishes at the site (if preexisting, 1 otherwise by default)
* dish_size: size of each dish at the station, in meters (6 by default)
* rms_surf_error: surface error (0 by default)
* region: which continent
* polar_nonpolar: is the station in a polar region or non-polar
* eht: 1 if the station is currently part of the eht array
* existing_infrastructure: information about the state of the site
* site_acquisition: whether or not the site needs to be acquired to build a station there
* radiometer_testing: whether or not the site has had radiometer testing to measure PWV
* uv_M87: whether the station can contribute to observation of M87
* uv_SgrA: whether the station can contribute to observation of SgrA*
* recording_bandwidth: bandwidth of each sideband (default: 8)
* recording_frequencies: number of simultaneous recording frequencies (default: 2)
* polarizations: number of polarizations captured (default: 2)
* sidebands: number of sidebands captured (default: 2)
* bit_depth: number of bits per sample (default: 2)

Any parameter can be set as keyword arguments when instantiating a Station.

    >>> x = Station(name='newstation', sidebands=2)

Station objects have the following methods:

* rate = data_rate() - returns the data rate produced by the station in Gbps
* (x, y, z) = xyz() - return station location in XYZ
* s = SEFD(freq, elev, filled=0.7, month=5) - calculates SEFD given parameters

## Source Model

The Source module contains functions and models to help manage observation sources.

### Usage

from ngehtutil.source import *

The Source model provides the following functions:

*get_source_list()* - Returns a list of sources known by the util library.

    >>> get_source_list()
    ['M87', 'SgrA*']

*get_source_description(s)* - Returns a string describing the image, for instance including the source of the data.

    >>> get_source_desctiption('M87')
    'Chael M87'

*get_source_freq_list(s)* - Returns a list of frequencies for which native data is available for a source.

    >>> get_source_freq_list('M87')
    [86, 230, 345]

*get_source_image(s, frequency)* - Returns a Python Image Library Image object containing a png image of the source at the given frequency

    >>> get_source_image('M87',230)
    <PIL.PngImagePlugin.PngImageFile image mode=RGBA size=413x319 at 0x7FCC68552070>

*get_source_data_file(s, freqency)* - Returns a path to a file containing the data describing the source at a given frequency.

    >>> get_source_data_file('M87',230)
    '/Users/aoppenheimer/src/ngeht-util/ngehtutil/source/models/M87_230GHz_Chael.fits'

# README below this point still in progress!


## Target Model

## Cost Model

### To use

This repo is a module that exposes two functions that are used to calculate cost information for an array configuration:

* calculate_costs takes a cost_configuration, which specified things like size of new dishes, when construction starts, etc. It also takes a description of an array as a set of structures describing the antennas in the array. It returns a dict with a lot of cost information.
* calculate_costs_over_time takes the cost information and returns a schedule of capex and opex payments over time.

### Requirements

* Python (written under 3.9 but will probably work for earlier)

  _Note: Use of a virtual python environment (`python -m venv` _venvdir_) is **highly recommended**_
* pip
* Additional dependencies installed via `pip install -r requirements.txt` or `python -m pip install -r requirements.txt`

  _Note: On Windows, some dependencies require MS VC++ tools from
  [Visual Studio Build Tools](https://visualstudio.microsoft.com/thank-you-downloading-visual-studio/?sku=BuildTools&rel=16) be present.
  They need to be installed prior to running the command above; be sure to select C++ in the installation option)._

### Example

Cost.py is simple application to exercise the calculate_cost and calculate_cost_over_time functions.

```
usage: python cost.py [--help] [--const_file CONST_FILE] [--setup_file SETUP_FILE]
                      [--new_site_config CONFIG_COLUMN] [--array ARRAY_COLUMN]
                      [--output_file OUTPUT_FILE] [--verbose]
```

Relies on three input files:

* *CONST_FILE* contains all of the constants governing the cost calculations: information about sites, costs for construction and data, etc. The default const_constants.xlsx is provided as part of the module and shouldn't be touched unless you're really updating it. cost.py will pull in the default file if you don't specify another.
* *SETUP_FILE* contains both the array configurations to be costed (first tab) and specific lists of sites to be evaluated (second tab). Use the default as the template, and add as many configurations and arrays as desired. The default array_setup.xlsx is pulled in if you don't specify another.
* *CONFIG_COLUMN* specifies the configuration to use for new sites when calculating for different array site configurations (defaults to first column in the SETUP_FILE)
* *ARRAY_COLUMN* specified the array site configuration to use when calculating for different new site configurations (defaults to first column in the SETUP_FILE)
* *SITE_FILE* contains information about the sites - location, etc.

and

* *OUTPUT_FILE* tells the code where to dump the data. Should be a .xlsx - will use cost_output.xlsx if unspecified
  &nbsp;
  &nbsp;

### Another Example

Exercise.py takes a number of options for configuration parameters and runs the cost model against all of the permutations.

```
usage: python exercise.py
```

Records output to exercise_out.xlsx
&nbsp;
&nbsp;

### Even More Fun

Exercise_vis.py uses the exercise_out.xlsx file generated by exercise.py to provide a dynamic UI that allows changing the configuration and seeing the cost data points. It requires plotly (pip install plotly), and, if you're running on windows, may require you to enable local web serving. (Control panel -> Turn windows features on or off -> Internet Information Services -> turn on Web Management Tools and World Wide Web Serivces)

```
usage: python exercise_vis.py
```
