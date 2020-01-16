import pandas as pd
import datetime as dt
from datetime import datetime
import os


'''
Notes: Using conda env irp on local PC

input data ------------------------------------------------------------------
[1] Multiple time series files of gwlevels at observation locations

output ----------------------------------------------------------------------
[1] A csv DataFrame that has gwlevels at all obswell [row: time, col: obswell]

Some options to consider ----------------------------------------------------
[1] Choosing a sampling_freq: Daily (D) or Monthly (M) or Quarterly (Q)
'''


# Main code -------------------------------------------------------------------
cur_dir = os.getcwd()  # get the current working directory

# Specify the path to time series groundwater level data
# (csv files, one file for one well)
path_gw = r'c:/Users/hpham/Documents/P25_InSAR_Pahrump/gwlevels/'
# Get the list of groundwater level observation wells
logs = os.listdir(path_gw)

# Specify the time to plot
start_date = pd.Timestamp(dt.date(2005, 1, 1))
end_date = pd.Timestamp(dt.date(2019, 12, 31))
sampling_freq = 'M'
df_dt = pd.DataFrame({'Date': [start_date, end_date], 'Val': [999, 999]})
df_dt['Date'] = pd.to_datetime(df_dt['Date'])
df_date = df_dt.resample(sampling_freq, on='Date').mean()   # resample by month
df_date = df_date.reset_index()
df_date = df_date.drop('Val', 1)

df_final = df_date.copy()
for f in logs:  # logs[0:1]:
    line = f.split('.')
    loc_name = str(line[0])  # well name
    print(f'Name = {loc_name} \n')
    ifile_gw = path_gw + loc_name + '.csv'

    # Read a csv file to get gwlevel data
    dfgw = pd.read_csv(ifile_gw)
    dfgw['Date'] = pd.to_datetime(dfgw['Date'])

    dfgw = dfgw.rename(columns={'hobs ': loc_name})
    # resample to monthly/quaterly data
    dfgw = dfgw.resample(sampling_freq, on='Date').mean()
    dfgw = dfgw.reset_index()
    df_merge = pd.merge(df_date, dfgw, how='left', on=['Date'])
    df_merge.reset_index()
    df_final[loc_name] = df_merge[loc_name]

    '''
    # Trim the dataframe
    #dfgw['Date'] = pd.to_datetime(df['Date'])
    dfgw = dfgw[dfgw['Date'] > start_date]

    print(f'size dfgw = {dfgw.shape}')

#    row_to_drop = range(0, 117, 1)
#    dfgw = dfgw.drop(row_to_drop)
    dfgw = dfgw.reset_index()
    dfgw['Date'] = pd.to_datetime(dfgw['Date'])
    '''

ofile = '../data/' + 'gwlevels_' + '_freq_' + sampling_freq + '.csv'
df_final.to_csv(ofile, index=False)
print(f'The output dataframe was saved at {ofile} \n')
