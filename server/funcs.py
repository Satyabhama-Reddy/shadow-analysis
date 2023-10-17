from src_code.solarposition import *
from src_code.shadowingfunction_wallheight_13 import shadowingfunction_wallheight_13
import pandas as pd
import numpy as np
import db

# dsm is a map that reprents elevation information 
dsm = np.load('./dsm_local_array.npy') # TODO
dsm = np.nan_to_num(dsm, nan=0)

def shadow_analysis(timestamp):
    
    lon = -95.30052 # TODO
    lat = 29.73463
    utc_offset= -6

    timestamps = pd.DatetimeIndex([timestamp])

    # Create a DataFrame using the timestamps as a column
    df_solar_data = pd.DataFrame({'TimeStamp': timestamps})

    # UTC time
    df_solar_data['TimeStamp'] = pd.DatetimeIndex(df_solar_data['TimeStamp']) - pd.DateOffset(hours=utc_offset)

    # To_Datetime
    df_solar_data["TimeStamp"] = df_solar_data["TimeStamp"].apply(pd.to_datetime)
    df_solar_data.set_index("TimeStamp", inplace = True)

    # Add time index
    df_solar_data["TimeStamp"] = df_solar_data.index

    # Get_sun's position df
    df_solar = get_solarposition(df_solar_data.index, lat, lon)

    # Add time index
    df_solar['TimeStamp'] = pd.DatetimeIndex(df_solar.index) + pd.DateOffset(hours=utc_offset)

    df_solar = df_solar[['TimeStamp', 'apparent_zenith', 'zenith', 'apparent_elevation', 'elevation',
                    'azimuth', 'equation_of_time']]

    # To_Datetime
    df_solar["TimeStamp"] = df_solar["TimeStamp"].apply(pd.to_datetime)
    df_solar.set_index("TimeStamp", inplace = True)

    df_solar["TimeStamp"] = df_solar.index
    df_solar = df_solar[['TimeStamp', 'elevation', 'zenith', 'azimuth']]

    df_solar = df_solar.rename(columns={"elevation": "Elevation","azimuth": "Azimuth", "zenith": "Zenith"})

    # Temporally !
    scale = 1
    walls = np.zeros((dsm.shape[0], dsm.shape[1]))
    dirwalls = np.zeros((dsm.shape[0], dsm.shape[1])) # TODO

    i = 0
    altitude = df_solar['Elevation'].iloc[i]
    azimuth = df_solar['Azimuth'].iloc[i]

    hour = df_solar.index[i].hour
    minute = df_solar.index[i].minute

    print(hour, minute)

    sh, wallsh, wallsun, facesh, facesun = shadowingfunction_wallheight_13(dsm, azimuth, altitude, scale, walls, dirwalls * np.pi / 180.)
    shadow_matrix = sh.tolist()
    record = db.insert(timestamp, shadow_matrix)
    return record
