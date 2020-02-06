import requests
import pandas as pd
import os
import datetime as dt


download_data = True
process_data = True
shift_gps_data = False

#
min_gps_obs = 20  # Keep stations that have at least 1 obs
resample_option = 'M'  # Resample gps data by D, M, Y?
ofile_gps = resample_option + '_gps_data_in_cm_short_list.csv'
start_yr = 2007
end_yr = 2020

# Testing some functions


def conv_dec_year_to_date(df):
    nrows = df.shape[0]
    df_new = pd.DataFrame(columns=['Date'])
    for i in range(nrows):
        start = df.iloc[i]
        year = int(start)
        rem = start - year
        base = dt.datetime(year, 1, 1)
        result = base + \
            dt.timedelta(seconds=(base.replace(
                year=base.year + 1) - base).total_seconds() * rem)
        df_new.at[i, 'Date'] = result
    return df_new


if download_data:
    os.chdir(r'/scratch/hpham/insar/raw_data')
    sta = pd.read_csv(r'/scratch/hpham/insar/raw_data/GPS_points_PV1_LAS.csv')
    nsta = sta.shape[0]

    for i, sname in enumerate(sta.Name):
        url = ' http://geodesy.unr.edu/gps_timeseries/tenv3/IGS08/' + sname + '.IGS08.tenv3'
        print(f'url: {url}')
        r = requests.get(url)
        ofile = sname + '.csv'
        open(ofile, 'wb').write(r.content)
    # geodesy.unr.edu/gps_timeseries/tenv3/IGS08/UNR1.IGS08.tenv3

if process_data:
    # Create datetime series
    start_date = dt.date(start_yr, 1, 1)
    end_date = dt.date(end_yr, 12, 31)
    df_dt = pd.DataFrame({'Date': [start_date, end_date], 'Val': [999, 999]})
    df_dt['Date'] = pd.to_datetime(df_dt['Date'])
    # resample by M: month; D: Day; Y: year
    df_date = df_dt.resample(resample_option, on='Date').mean()
    df_date = df_date.reset_index()
    df_date = df_date.drop('Val', 1)
    df_date.reset_index(inplace=True)

    path_to_gps_data = '/scratch/hpham/insar/raw_data/'
    ifile_gps_loc = path_to_gps_data + 'GPS_points_PV1_LAS.csv'
    df_gps_loc = pd.read_csv(ifile_gps_loc)
    sta_list = df_gps_loc.Name
    n_sta = int(sta_list.shape[0])
    df_new = pd.DataFrame({'Date': df_date.Date})
    for i, sname in enumerate(sta_list):
        # Process GPS data
        ifile_gps = path_to_gps_data + sname + '.csv'
        print(f'i={i}, Reading file: {ifile_gps}')
        dfgps = pd.read_csv(ifile_gps, delim_whitespace=True)

        col_keep = ['yyyy.yyyy', '____up(m)']

        dfgps = dfgps[col_keep]
        df_tmp = conv_dec_year_to_date(dfgps['yyyy.yyyy'])
        dfgps['Date'] = conv_dec_year_to_date(dfgps['yyyy.yyyy'])
        #dfgps['Date']  = pd.to_datetime(dfgps.YYMMMDD, yearfirst=True)

        #dfgps.drop('YYMMMDD',axis=1, inplace=True)
        #df2 = dfgps.resample('D', on='Date').mean()   #
        df2 = dfgps.resample(resample_option, on='Date').mean()   #
        df2.reset_index(inplace=True)
        n_gps_obs = df2['____up(m)'].count()  # Count NOT NaN
        print(f'i={i}, n_gps_obs: {n_gps_obs}')
        if n_gps_obs >= min_gps_obs:
            df_new[sname] = df2['____up(m)']*100  # convert to cm
print(f'N gps stations: {df_new.shape[1]-1}')
print(f'N rows: {df_new.shape[0]}')
df_new.to_csv(ofile_gps, index=None)


if shift_gps_data:
    df = pd.read_csv(ofile_gps)
