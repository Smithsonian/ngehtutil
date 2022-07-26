[![](https://img.shields.io/pypi/v/ngehtutil.svg)](https://pypi.org/project/ngehtutil/)
[![](https://github.com/smithsonian/ngehtutil/workflows/Testing/badge.svg)](https://github.com/smithsonian/ngehtutil/actions)

# ngehtutil - Utilities for ngEHT

*ngehtutil* is a library of python modules to help in the design, development, and analysis of the
ngEHT VLBI telescope. It consists of four models: station, source, target, and cost.

One purpose of the system is to maintain a database of known sites, array definitions, source
models, and sky locations. By using a single library for all of our tools, we can be certain that
we're all talking about the same thing when we say "the reference array" or "OVRO." When the library
loaded, the database of these known items is loaded and ready for use.

## Installation

The library is installed using pip, and it is recommended to use a virtual environment. The library
is installed from pypi. To install the latest plus its dependencies:

    pip install ngehtutil
    
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

---

## Array: a set of stations

Class to represent an Array, comprising a set of Station objects. The module loads a set
of known arrays that can be accessed through class methods.

### Class / Static Methods

    Array.get_list()
    # Get the list of arrays in the database as a list of names

    Array.from_name(name)
    # Returns an Array object from the database by name. Will raise an exception 
    # if the array name is unknown.

    Array.get_default()
    # Returns an Array object representing the default array

    Array.get_default_array_name()
    # Returns the name of the first known array in the builtin database

    Array.get_station_names(name)
    # Get list of station names associated with an array name

### Instance Methods

    a = Array(name, stations)
    # Initializes an Array object from a name and a list of Station objects

    a.stations()
    # Return the stations comprising this array
 
    a.stations(stations)
    # Set the list of stations comprising this array

---

## Station: a location with receiver capabilities, a set of dishes, and weather info

Class to represent a Station, comprising attributes of the receiver, a set of Dish objects, and
(coming soon) information about weather at the site. The module loads a set of known stations that
can be accessed through class methods.

### Class / Static Methods

    Station.get_list()
    # Get the list of stations in the database as a list of names

    Station.from_name(name)
    # Returns a Station object from the database by name. Will raise an exception
    # if the station name is unknown.

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

    s.set_diameter(diameter)
    # sets the diameter of all dishes at the station to [diameter]. If the station does not have
    # any dishes, creates a single dish with diameter [diameter] and default parameters for other
    # dish attributes.

    w = s.get_weather(type, year, month, day)
    # returns information about weather at the site, derived from MERRA-2 data.
    # type is one of the supported data, currently 'RH', 'SEFD_info_230', 'SEFD_info_345',
    #   'mean_RH', 'mean_SEFD_info_230', 'mean_SEFD_info_345', 'mean_wind_speed', 'wind_speed'
    #
    # The returned weather data is a dict:
    # d = {
    #    'index': ['segment','tau','Tb'], # description of each field in the returned data
    #    'data': [(0, 2.9, 271),          # list of data that meets the specification
    #             (1, 2.5, 261),
    #             ...
    #            ]
    #   }
    #
    # Note that accessing this data causes a bunch of files to be downloaded from a repository
    # holding all the data: https://github.com/Smithsonian/ngeht-weather
    #
    # These files can be cleared from the system using a function:
    #
    # >> from ngehtutil.station_weather import delete_sites
    # >> delete_sites()



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

---

## Dish: a single radio antenna at a site

Class to represent a Dish. A Station has a list of Dish objects.

### Instance Methods

    d = Dish(size=6, surface_error=0, pointing_model=None)
    # Returns a Dish object with the given attributes. Size is diameter of the dish in meters;
    # surface_error is the rms error in microns; the pointing model is under development

---

## Weather: a model of weather at the site

Under construction

---

## Target: a place in the sky to point an array

Class to represent a place in the sky to point the array. The module loads a set of
common targets that can be accessed through class methods.

### Class / Static Methods

    Target.get_list()
    # Returns the list of targets in the database as a list of names

    Target.from_name(name)
    # Returns a Target object from the database by name. Will raise an exception
    # if the array name is unknown

    Target.get_default()
    # Returns the name of the first known target in the builtin database

### Attributes

    # Target objects have these attributes:
    [
        'name', # common name for the target, e.g. 'M87'
        'RA',   # RA as a float
        'RA_hr',# RA hours only
        'RA_min',# RA minutes only
        'RA_sec',# RA seconds only
        'Dec',  # Dec as a float
        'Dec_deg', # Dec degrees only
        'Dec_arcmin', # Dec arcmin only
        'Dec_arcsec' # Dec arcsec only
    ]

---

## Source: an object in the sky to be observed

Class to represent an object that can be observed. The module has several built-in source
models that can be accessed through class methods.

### Class / Static Methods

    Source.get_list()
    # Returns the list of sources in the database as a list of names

    Source.from_name(name)
    # Returns a Source objsect from the database by name. Will raise an exception if the source
    # name is unknown.

    Source.get_default()
    # Returns the name of the first known target in the builtin database

### Instance Methods

    s = Source(name, **kwargs)
    # initializes a new source from a name and set of keyword attributes

    s.freq_list()
    # returns a list of frequencies for which the Source has available data

    s.picture(frequency)
    # returns a python imaging library Image object containing a picture of the source at the
    # given frequency. Raises an exception if there is no data for the given frequency.

    s.fits(frequency)
    # returns a path to a fits file containing data for the source at the given frequency. Raises
    # an exception if there is no data for the given frequency.


---

## Schedule: timing of an observation

Class to represent a set of observations. An observation is a (possibly multi-day) event to collect
a certain number of hours of data. The observation many happen multiple times per year.

### Instance Methods

    sch =  Schedule(obs_per_year=1, obs_days=5, obs_hours=15)
    # initializes a Schedule object with number of events per year, number of days per event, and
    # number of hours of data collection per event.

### Attributes

    # Schedule objects have these attributes:
    sch.obs_per_year # number of observations in a year
    sch.obs_days # number of days for each observation
    sch.obs_hours # number of hours to observe per observation

---

## Campaign: a combination of Target, Source, and Schedule

Class to describe a "campaign" which comprises a target in the sky, a source to observe,
and a schedule for the observation.

# Instance Methods

    cmp = Campaign(target, source, schedule)
    # initializes a Campaign object with a target, source, and schedule

### Attributes

    # Campaign objects have these attributes:
    cmp.schedule # schedule object
    cmp.target # target object
    cmp.source # source object

---

## Program: a combination of a specific array and a set of campaigns

Class to describe a VLBI program: the array and the campaigns. With this defined we can calclate
costs and other attributes of the entire system.

### Instance Methods

    prg = Program(array, campaign)
    # initializes a Program object from an Array object and a Campaign object

    c = prg.calculate_costs(**kwargs)
    # runs the integrated cost model, which can be configured using keyword arguments to override
    # defaults in the CostConfig object used to set up the cost model. Returns a dict of relevant
    # cost information for the system.

---

## CostConfig: a set of configurations for calculating costs

Class to hold configuration information used by the cost model.

### Instance Methods

    cc = CostConfig(**kwargs)
    # initializes a CostConfig object, which has default values for its attributes that can be
    # overridden by keyword arguments.

### Attributes

    # the following attributes can be overriden as keyword arguments when initializing
    dish_size = 6 # Size for new dishes - must be 4, 6, 8, 10
    autonomy_of_operations = 'Manual' # one of 'Manual' 'Somewhat Autonomous' 'Semi-Autonomous'
                                      # or 'Fully Autonomous'
    data_management = 'Own Cluster' # one of 'Own Cluster' 'Research Cluster' 'Cloud'
    recording_bandwidth = 8 # in GHz
    recording_frequencies = 2
    start_building = 2025
    fully_operational = 2030
    inflation_rate = 0.02
    active_lifetime = 10
    observations_per_year = 1 # will be defined by Schedule when calling prg.calculate_costs
    days_per_observation = 3 # will be defined by Schedule when calling prg.calculate_costs
    hours_per_observation = 30 # will be defined by Schedule when calling prg.calculate_costs
    no_upgrade = [] # sites that should not get an upgraded receiver or back end, by name

---

## Cost module convenience functions

The cost module has a few functions to calculate costs:

    costs, site_costs = calculate_costs(cost_config, stations, cost_constants=None)
    # returns a dict of cost items including capital, operating, data handling, and average costs;
    # also returns a dict of costs indexed by site name
    #
    # cost_constants can be left None in which case the module will use constants stored in-memory
    # if you need a deep copy (for instance, for cluster computing) use get_cost_constants()

    total, new = calculate_capital_costs(cost_config, stations, cost_constants)
    # returns a pandas series containing only the capital costs for stations. Total is for all of
    # the stations; new only includes stations for which a dish must be built.
    #
    # to get a sum of the costs, use sum=total[1:].sum()

    total, new = calculate_operating_costs(cost_config, stations, cost_constants)
    # returns a pandas series containing only the operating costs for stations. Total is for all of
    # the stations; new only includes stations for which a dish must be built.

---

# Versioning scheme

ngehtutil uses a semantic versioning as described [here](https://semver.org/): MAJOR.MINOR.PATCH. We use [tbump](https://pypi.org/project/tbump/) to manage this. `tbump X.Y.Z` will do the following:

- change the version hardcoded in version.py
- commit the change
- create a new tag called 'vX.Y.Z'
- push to github

The [github repository](https://github.com/Smithsonian/ngehtutil) has an action that detects a new tag. This action will push the new version of the code to [pypi](https://pypi.org/project/ngehtutil/) where it can be installed using pip.

From within any code that imports ngehtutil, the current version can be accessed at ngehtutil.version.VERSION .
