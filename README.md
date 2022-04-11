# ngeht-util - Utilities for ngEHT

*ngeht-util* is a library of python modules to help in the design, development, and analysis of the
ngEHT VLBI telescope. It consists of four models: station, source, target, and cost.

One purpose of the system is to maintain a database of known sites, array definitions, source
models, and sky locations. By using a single library for all of our tools, we can be certain that
we're all talking about the same thing when we say "the reference array" or "OVRO." When the library
loaded, the database of these known items is loaded and ready for use.

## Installation

The library is installed using pip, and it is recommended to use a virtual environment. The library
is installed directly from github. To install the latest plus its dependencies:

    pip install git+https://github.com/ngeht/ngeht-util.git

## Architecture

![plot](./doc/ngeht-util.png)

The library consists of objects representing various components of a VLBI array that work together 
represent a complete system. These are:

* Array: represents a set of stations
* Station: represents a location with receiver capabilities, a set of dishes, and weather info
* Dish: represents a dish in terms of diameter, surface error, pointing model
* Weather: represents information needed to calculate atmospheric effects for a site
* Target: represents a place in the sky to point an array
* Source: represents an object to be observed, as a model (e.g. fits file)
* Schedule: represents timing of an observation: duration of an observation event; events per year
* Campaign: represents a combination of Target, Source, and Schedule
* Program: represents a combination of a specific array and a specific set of campaigns

## Use Example

For this example, we construct an array, pick a source, and calculate the costs to observe for 5 days, with 24 hours of observation total, once/year. The library has many defaults baked in for the various elements that can be overridden.

    >>> from ngehtutil import *
    >>> t = Target.get_default() # one of the targets the library knows about
    >>> t
    Target M87
    >>> s = Source.get_default() # one of the sources the library knows about
    >>> s
    Source M87
    >>> sch = Schedule(obs_per_year=1, obs_days=5, obs_hours=24)
    >>> sch
    Schedule(1, 5, 24)
    >>> c = Campaign(t,s,sch)
    >>> c
    Source M87 @ Target M87 for Schedule: 1 obs per year; 5 days per obs; 24 hours per obs
    >>> array = Array.from_name('ngEHT Ref. Array 1.1A')
    >>> array
    Array ngEHT Ref. Array 1.1A
    >>> array.stations()
    [station OVRO, station BAR, station BAJA, station HAY, station CNI, station SGO, station CAT, station GAM, station GARS, station NZ]
    >>> p = Program(array, c)
    >>> costs = Program(array, c).calculate_costs(dish_size=6) # use 6m as the size of new dishes that need to be constructed for this array
    >>> import pprint
    >>> pprint.pprint(costs,sort_dicts=False)
    {'ARRAY STATS': '',
    'New Sites Count': 10,
    'EHT Sites Count': 0,
    'Total Sites Count': 10,
    'Data Per Observation Per Station': 1.3824,
    'Data Per Year - Full Array (PB)': 14.0,
    'SITE COSTS': '',
    'Design NRE': 3982500.0,
    'Site acquisition / leasing': 0.0,
    'Infrastructure': 33000000.0,
    'Antenna construction': 24674770.54058225,
    'Antenna commissioning': 4500000.0,
    'Backend costs': 18000000.0,
    'Antenna operations': 7985023.972602739,
    'DATA MANAGEMENT': '',
    'Cluster Build Cost': 6000000,
    'Personnel': 500000,
    'Holding Data Storage Costs': 0.0,
    'Fast Data Storage Costs': 0.0,
    'Transfer Costs': 0.0,
    'Computation Costs': 442461.0,
    'Site Recorders': 300000,
    'Site Media': 1400000.0,
    'Data Shipping': 3733.3333333333335,
    'NEW SITE AVG COSTS': '',
    'New Site Avg Design NRE': 398250.0,
    'New Site Avg Site acquisition / leasing': 0.0,
    'New Site Avg Infrastructure': 3300000.0,
    'New Site Avg Antenna construction': 2467477.054058225,
    'New Site Avg Antenna commissioning': 450000.0,
    'New Site Avg Backend costs': 1800000.0,
    'New Site Avg Antenna operations': 798502.3972602739,
    'New Site Avg Site Recorders': 30000.0,
    'New Site Avg Site Media': 140000.0,
    'New Site Total CAPEX': 6785727.054058225,
    'TOTAL COSTS': '',
    'TOTAL CAPEX': 91857270.54058225,
    'ANNUAL OPEX': 8931218.305936072}

## Array: a set of stations

Class to represent an Array, comprising a set of Station objects. The module loads a set
of known arrays that can be accessed through class methods.

### Class / Static Methods

    Array.from_name(name)
    # Returns an Array object from the database by name. Will raise an exception 
    # if the array name is unknown.

    Array.get_default()
    # Returns an Array object representing the default array

    Array.get_default_array_name()
    # Returns the name of the first known array in the builtin database

    Array.get_station_names(name)
    # Get list of station names associated with an array

    Array.get_list()
    # Get the list of arrays in the database as a list of names

### Instance Methods

    a = Array(name, stations)
    # Initializes an Array object from a name and a list of Station objects

    a.stations()
    # Return the stations comprising this array
 
    a.stations(stations)
    # Set the list of stations comprising this array


## Station: a location with receiver capabilities, a set of dishes, and weather info

Class to represent a Station, comprising attributes of the receiver, a set of Dish objects, and
(coming soon) information about weather at the site. The module loads a set of known stations that
can be accessed through class methods.

### Class / Static Methods

    Station.from_name(name)
    # Returns a Station object from the database by name. Will raise an exception
    # if the station name is unknown.

    Station.get_list()
    # Get the list of stations in the database as a list of names

    Station.get_all()
    # Returns all of the Station objects from the database as a list


### Instance Methods

    s = Station(name, **kwargs)
    # Initializes a Station object from a name and an optional set of keyword arguments. See below
    # for the list of attributes that can be set this way.

    s.to_dict()
    # Returns a dictionary of station attributes

    s.data_rate()
    # Convenience function to calculate the rate at which a station captures data according to
    # its attributes. Since recording_bandwidth is defined in GHz, return is in gigabits/second.
    #               self.recording_bandwidth * self.recording_frequencies * \
    #                    self.polarizations * self.sidebands * self.bit_depth * 2 

    s.xyz()
    # Convenience function to return the location of a site in XYZ coordinates from the lat, lon,
    # elevation attributes of a Station object.

    s.SEFD(freq, elev, filled=0.7, month=5)
    # Convenience function to calculate SEFD for a particular month given various attributes
    # of a site. [UNDER CONSTRUCTION]


### Attributes

    # These attributes of a Station object can be passed in as part of initialization. The site
    # database has these attributes, but they can be overridden or built up from scratch.
    #
    # Shown here are the default values if not initialized:

    s = Station('name',
        id = None # text code for the station. This need not be the same as the name.
        locality = None # where the station is located
        country = None # where the station is located
        latitude = None
        longitude = None
        elevation = None
        site_or_region = None # whether this represents a specific site or an entire 
                            # region (one of 'Site' or 'Region')
        owner = None
        register_converter = None
        polar_nonpolar = None # one of 'Polar' or 'Non-polar'
        existing_infrastructure = None # one of 'Partial' 'Complete' 'Remote'
        site_acquisition = None # 0 if the site does not need to be aqcuired, otherwise 1
        radiometer_testing = None # 'Yes' if the site has been surveryed with radiometer, else 'No'
        uv_M87 = None # 1 if site can contribute to UV plane for M87 observation, else 0
        uv_SgrA = None # 1 if site can contribute to UV plane for SgrA* obs, else 0
        dishes = None # list of Dish objects
        autonomy_of_operations = 'Manual' # one of 'Manual' 'Somewhat Autonomous' 'Semi-Autonomous',
                                        # or 'Fully Autonomous'
        recording_bandwidth = 8 # in GHz
        recording_frequencies = [] # list of frequencies, e.g. [86, 230, 345]
        polarizations = 2 # number of polarizations to receiver
        sidebands = 2 # number of sidebands to capture
        bit_depth = 2 # bit depth to record
        pwv = [0] * 12 # pwv for this site by month
        eht = False # True if the site is part of the EHT observations in 2022
    )

## Dish: a since radio antenna at a site

Class to represent a Dish. A Station has a list of Dish objects.

## Instance Methods

    d = Dish(size=6, surface_error=0, pointing_model=None)
    # Returns a Dish object with the given attributes. Size is diameter of the dish in meters;
    # surface_error is the rms error in microns; the pointing model is under development

## Weather: a model of weather at the site

Under construction

## Target: a place in the sky to point an array

## Source: an object in the sky to be observed

## Schedule: timing of an observation

## Campaign: a combination of Target, Source, and Schedule

## Program: a combination of a specific array and a set of campaigns



# IN PROGRESS BELOW HERE

## Station: represents a location with receiver capabilities, a set of dishes, and weather info
## Dish: represents a dish in terms of diameter, surface error, pointing model
## Weather: represents information needed to calculate atmospheric effects for a site
## Target: represents a place in the sky to point an array
## Source: represents an object to be observed, as a model (e.g. fits file)
## Schedule: represents timing of an observation: duration of an observation event; events per year
## Campaign: represents a combination of Target, Source, and Schedule
## Program: represents a combination of a specific array and a specific set of campaigns


# OLD STUFF BELOW HERE

## Station Module

The Statiopn module contains models and functions to manage the definition of VLBI arrays and stations.

### Usage

    >>> from ngehtutil.station import *

This library provides the following functions:

*get_array_list()* - returns a dict in which keys are strings listing array configurations known by the library. Each value is a list of strings identifying the telescope installations that are part of the array.

    >>> al = arrays.get_array_list()
    >>> al.keys()
    dict_keys(['eht2017', 'eht2022', 'ngeht_ref1', 'ngeht_ref1_4', 'ngeht_ref1_6', 'ngeht_ref1_8', 'ngeht_ref1_10'])
    >>> al['eht2017']
    ['IRAM-30m', 'SMT', 'SMA', 'LMT', 'ALMA', 'SPT', 'APEX', 'JCMT']

*get_list(array=None)* - returns a list of stations. If no array is given, will return all of the stations known to the module. If an array is given, returns the station list for that array.

    >>> arrays.get_list()
    ['ALMA', 'APEX', 'BAJA', 'BAN', 'BAR', 'BGA', 'BGK', 'BLDR', 'BMAC', 'BOL', 'BRZ', 'CAS', 'CAT', 'CNI', 'Dome A', 'Dome C', 'Dome F', 'ERB', 'FAIR', 'FUJI', 'GAM', 'GARS', 'GLT', 'GLT-S', 'HAN', 'HAY', 'HOP', 'IRAM-30m', 'JCMT', 'JELM', 'KEN', 'KILI', 'KP', 'KVNYS', 'LAS', 'LLA', 'LMT', 'LOS', 'NOB', 'NOEMA', 'NOR', 'NZ', 'ORG', 'OVRO', 'PAR', 'PIKE', 'SAN', 'SGO', 'SMA', 'SMT', 'SOC', 'SPT', 'SPX', 'SUF', 'YAN', 'YBG']
    >>> arrays.get_list('eht2017')
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

## Source Module

The Source module contains functions and models to help manage observation sources.

### Usage

    >>> from ngehtutil.source import *

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


## Target Module

The Target module contains some tools for managing useful sky targets

### Usage

    >>> from ngehtutil.target import *

The Target model provides the following functions:

*get_target_list()* - returns a list of known targets

    >>> get_target_list()
    ['M87', 'Sgr A*', 'M31', 'Cen A', 'OJ 287', '3C 279']

*get_target_info(target)* - returns a dict of location information about a target.

    >>> get_target_info('M87')
    {'RA_hr': 12.0, 'RA_min': 30.0, 'RA_sec': 49.42338, 'Dec_deg': 12.0, 'Dec_arcmin': 23.0, 'Dec_arcsec': 28.0439, 'RA': 12.513728716666666, 'Dec': 12.391123305555555}

# README below this point still in progress!


## Cost Module

The Cost module calculates the cost of an array given a list of stations, a set of configuration information for new sites to construct, and a set of configuration information about observation plans.

### Usage

    >>> from ngehtutil.cost import *

The Cost module provides the CostConfig object, which is used to describe the use of an array. CostConfig objects have the following attributes:

* dish_size: size of new dishes in meters (default: 6)
* autonomy_of_operations: description of level of automation at new sites ('Manual')
* data_management: plan for compute resources ('Own Cluster')
* recording_bandwidth: Recording bandwidth in GHz (8)
* recording_frequencies: Number of simaltaneous recording frequencies (2)
* start_building: Year of start construction (2025)
* fully_operational: Year entire array is built (2030)
* inflation_rate: Annual inflation rate (0.02)
* active_lifetime: Lifetime of entire array once it is complete (10)
* observations_per_year: Number of observations each year (1)
* days_per_observation: Number of observing days in an observation (3)
* hours_per_observation: Total number of hours in an observation (30)

Any parameter can be set as keyword arguments when instantiating a Station.

    >>> x = CostConfig(recording_bandwidth=12, inflation_rate=0.03)
    >>> x.recording_bandwidth
    12


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
