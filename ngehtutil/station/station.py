#
# object to describe a station
#
import numpy as np

class Station:
    name = None
    dish_size = 6
    number_dishes = 1
    autonomy_of_operations = 'Manual'
    recording_bandwidth = 8
    recording_frequencies = 2
    polarizations = 2
    sidebands = 2
    bit_depth = 2
    pwv = [0] * 12
    rms_surf_err = 0

    def __init__(self, name, **kwargs):

        self.name = name

        # these are the labels in the excel file that defines stations, mapped to the attribute
        # names we really want
        attribute_map = {
            'ID':'id',
            'Locality':'locality',
            'Country':'country',
            'Latitude':'latitude',
            'Longitude':'longitude',
            'Elevation':'elevation',
            'Site or Region':'site_or_region',
            'Owner':'owner',
            'Antenna Count':'antenna_count',
            'Region':'region',
            'Polar/Non-polar':'polar_nonpolar',
            'EHT':'eht',
            'Existing Infrastructure':'existing_infrastructure',
            'Site Acquisition':'site_acquisition',
            'Radiometer Testing':'radiometer_testing',
            'uv_M87':'uv_M87',
            'uv_SgrA*':'uv_SgrA',
            'Antenna Count':'antenna_count',
            'RMS surf err':'rms_surf_error',
            'pwv':'pwv',
            'Dish Dia.':'dish_size',
        }

        for k,v in kwargs.items():
            # convert column headings in spreadsheet to our attribute names
            # todo - we skip some that might be helpful
            if k in attribute_map:
                mapkey = attribute_map[k]
                setattr(self, mapkey, v)
            else:
                raise ValueError(f'bad attribute for station: {k}')

        # stn['lat'] = np.arcsin( stn['z']/np.sqrt(stn['x']**2+stn['y']**2+stn['z']**2) ) * 180./np.pi
        # stn['lon'] = np.arctan2( stn['y'], stn['x'] ) * 180.0/np.pi
        self.data_rate = self.recording_bandwidth * self.recording_frequencies * \
                        self.polarizations * self.sidebands * self.bit_depth * 2 # nyquist


    def xyz(self):
        """
        # convert latitude longitude and altitude into ECEF X Y Z coordinates
        # tewt tyoubg
        # x = ECEF X-coordinate (m)
        # y = ECEF Y-coordinate (m)
        # z = ECEF Z-coordinate (m)
        # lat = geodetic latitude (radians)
        # lon = longitude (radians)
        # alt = height above WGS84 ellipsoid (m)
        #
        % Notes: This function assumes the WGS84 model.
        %        Latitude is customary geodetic (not geocentric).
        %
        % Source: "Department of Defense World Geodetic System 1984"
        %         Page 4-4
        %         National Imagery and Mapping Agency
        %         Last updated June, 2004
        %         NIMA TR8350.2
        %
        % Michael Kleder, July 2005
        """
        # Convert Lat and Lon to radians
        lat = np.deg2rad(self.latitude)
        lon = np.deg2rad(self.longitude)
        alt = self.elevation
        # WGS84 ellipsoid constants:
        a = 6378137   
        e = 8.1819190842622e-2
        # intermediate calculation
        # (prime vertical radius of curvature)
        N = a / (1 - e**2 * np.sin(lat)**2)**0.5
        
        # results:
        x = (N+alt) * np.cos(lat) * np.cos(lon)
        y = (N+alt) * np.cos(lat)* np.sin(lon)
        z = ((1-e**2) * N + alt) * np.sin(lat)
        return [x, y, z]


    def SEFD(self, freq, elev, filled=0.7, month=5):
        """
        %
        % SEFD is the System Equivalent Flux Density
        %   freq is the measurement frequency (GHz)
        %   elev is the elevation angle of the telescope in degrees (0 to 90)

        %   filled is the geometric filling factor (unobscured telescope fraction)
        %   month is the observation month (1-12)

        %   Trx is the receiver temperature (K) - removed from arg list but could be back!

        % Get coefficients for PWV -> tau_0 based on frequency

        """

        N = self.antenna_count
        D = self.dish_size
        RMS = self.rms_surf_err
        PWV = self.pwv[month-1]

        if freq == 86:
            a = 0.0157; b = 0.00686
            Trx = 60 * 2/3
        elif freq == 230:
            a = 0.0107; b = 0.0431
            Trx = 136 * 2/3
        elif freq == 345:
            a = 0.0192; b = 0.152
            Trx = 219 * 2/3
        elif freq == 480:
            a = 0.123; b = 0.810
            Trx = 292 * 2/3
        elif freq == 690:
            a = 0.0664; b = 1.14
            Trx = 261 * 2/3
        else:
            print('Frequency fit for tau not known at this frequency')
            print('Available frequencies are 86, 225, 345, 480, 690 GHz')
            return 0

        # Calculate the aperture loss including Ruze loss due to roughness
        eta_A = filled * np.exp(-((4.0 * np.pi * RMS/3e5 * freq)**2))

        # DPFU is the "Degrees per Flux density Unit" which converts System
        # Temperature to flux density units
        DPFU = eta_A * N * (np.pi * (D/2)**2)/(2 * 1380)

        # Convert the Precipitable Water Vapor to Zenith Opacity (LB fits)
        tau_0 = a + b * PWV
        AM = 1/np.sin(np.deg2rad(elev))

        #Calculate the corrected System Temperature
        Tsys_star = np.exp(tau_0 * AM) * (Trx + (1 - np.exp(-tau_0 * AM)) * 290)

        # Calculate the SEFD
        the_SEFD = Tsys_star/DPFU
        return the_SEFD