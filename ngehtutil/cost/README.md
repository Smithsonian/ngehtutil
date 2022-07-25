# ngEHT Cost Model
The ngEHT Cost Model takes into account many aspects of building and operating a radio telescope array and calculates the capital and operational costs
for a given system.

## Configuring The Model
### The Array
To calculate costs, the model requires a list of Site objects that represent the sites to build. This is documented in the ngEHT-util documentation.

### The CostConfig object
When calculating system costs, a CostConfig object is created to specific aspects of the system under analysis. These are shown here with their defaults:

- dish_size = 6 # Size for new dishes - must be 4, 6, 8, 10
- autonomy_of_operations = 'Manual' # one of 'Manual' 'Somewhat Autonomous' 'Semi-Autonomous' or 'Fully Autonomous'
- data_management = 'Own Cluster' # one of 'Own Cluster' 'Research Cluster' 'Cloud'
- recording_bandwidth = 8 # in GHz
- recording_frequencies = 2
- start_building = 2025
- fully_operational = 2030
- inflation_rate = 0.02
- active_lifetime = 10
- observations_per_year = 1
- days_per_observation = 3
- hours_per_observation = 30
- no_upgrade = [] # list of existing sites to skip when calculating cost of upgrades

### The Cost Constants
The model works by adding up the costs of many elements of an array. These costs are stored in a spreadsheet that is part of the ngEHT-utils library.

## The Calculation

### Basics
`Total Sites Cound` is calculated simply as the number of sites passed in.

`New Sites Count` is calculated as the number of sites that do not have dishes defined.

`EHT Sites Count` is simply the difference: the total sites - the new sites.

### Capital Costs


`Design NRE` (non-recurring engineering) costs include design and prototype development for an antenna. This is calculated by multplying the sample NRE cost from the constants file by a factor described by the level of "autonomy" we expect, with the assumption that a more "autonomous" system will cost more in terms of control systems to develop.

For a new site (that is, one that has no dishes defined):

- `Site acquisition / leasing` comes from the constants tables unless the site doesn't require any acquisition (ie. it's an existing site we're building on).

- `Infrastructure` costs come from multiplying the infrastructure cost constant by a value that describes how much infrastructure already exists on the site. A new site will cost much more than an existing site that already has infrastructure.

- `Antenna construction` comes from multiplying the cost of a single antenna by a value describing whether or not a site is "polar" - polar sites cost much more than non-polar sites.

The cost for a single antenna is calculated using this formula:
    
    antenna_constant + 
    (antenna_factor1 * dish size) + 
    (antenna_factor2 * pow(dish_size, antenna_exp))


This allows for different calculations than the usual *size^2.7*, which, as we get more data from vendors, does not necessarily hold.

- `Antenna transport` comes from the constants table

For an existing site, we don't need to build a dish, so `Site acquisition / leasing`, `Infrastructure`, `Antenna construction`, and `Antenna transport` are all set to zero.

For sites where we need to build a new receiver/back end/maser (that is, sites that are not in the "no upgrade" list):

- receiver cost comes from the constants and is assumed to be dual-band. If the configuration specified three frequencies, the receiver cost is multiplied by a constant from the tables.

- maser cost comes from the constants

- dbe cost comes from the constants mutiplied by the number of frequencies

`Receiver and Backend costs` is then calculated by adding the receiver, maser, and dbe costs and multiplying by the number of dishes at the site. This overestimates because generally, sites with multiple dishes only need one maser; however, they need a more sophisticated distribution system. We are also not planning to upgrade the existing array sites so this is not much of an issue.

`Antenna commissioning` comes from the constants table. For a new site, commissioning costs are multiplied by a factor dependent on whether or not the site is "Polar."

The total capital costs are then the sum of all of the costs for each site. The new site capital costs are the same, but only for sites that are new.

### Operations Costs

Operations costs are highly dependent on utilization. The cost model separates operations costs into those primarily driven by staffing and those driven by data management, which are in their own section below.

There are several sets of labor costs which are included for new sites:

- travel costs to sites
- per diem costs during observations
- technician costs during observations and for maintenance
- "non-local" costs, meaning costs for staff that don't travel to the site

Where appropriate, these labor costs are adjusted for location. The "automation mode" for new sites adjusts certain of the labor costs too - more fully automated sites require less staffing.

In addition, a full-time staff of 10 people is included as part of the ngEHT operations team.

Note that currently the costs for existing "EHT" sites are not calculated.

### Data Management Costs

Data management depends on the strategy configured: "Own Cluster" in which we build a cluster, "Research Cluster" in which we rent time on another cluster, or "Cloud" in which we upload everything to Google.

`Cluster Build Cost` is in the constants file and obviously only matters for the "Own Cluster" case.

`Personnel` takes into account FTEs for data management

Data storage includes both "cold storage" and "fast storage" - since some data may take a long time to arrive, the available data can be held in cheaper storage until it is ready to be used. There is then a set of "transfer costs" accrued when the data is moved from one to the other.

Finally, `Computation Costs` are the costs to actually do the math.

Media costs are calculated using the "media on-hand" constant, which dictates how much storage a site must hold. Since the storage is recycled, this is less than the data actually needed to store.

Finally, the data must be shipped, so `Data Shipping` is used to hold the calculation of shipping per petabyte * number of PB recorded.

# Other Stuff
The project uses tbump for tracking version numbers and github tag synchronizations