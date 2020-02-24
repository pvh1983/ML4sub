import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime as dt
from datetime import datetime
import os
import plotly.express as px
from func4stat import *

'''
# Notes: Using conda env irp on local PC
# Plot time series of ls and gwlevels

# input data ------------------------------------------------------------------
# [1] A DataFrame of time series subsidence velocity at given points (i.e., 
#     gwlevel observation locations). Run main_sar.py after done mintpy
# [2] A DataFrame of time series gwlevels at observation locations

'''

# cd c:\Users\hpham\Documents\P31 Maki\ML4sub\scripts\

# Run options
opt_plot_ls_vs_head = True
opt_cal_trend = False

# Define domain and satellite
domain = 'pv_las'    # 'pv' or 'las' or 'pv_las' (for sentinel)
sat = 'sen'   # 'alos' or 'sen'

# Specify the time to plot
cur_dir = os.getcwd()  # get the current working directory
sampling_freq = 'M'    # Note: Check freq of gwlevel at line 48
start_date = pd.Timestamp(dt.date(2005, 1, 1))
end_date = pd.Timestamp(dt.date(2020, 2, 28))
df_date = gen_date_time_series(start_date, end_date, sampling_freq)


# [1] LOAD DATA ===============================================================
# [1.1] Specify an input file that has the time series of subsidence velocity
# at groundwater level observation wells
# ifile_ls = r'../input/ts_ls_at_well_logs/ts_ls_at_well_logs_' + \
#    sat + '_' + domain + '.csv'


# [1] calculate subsidence at given points from 06/14/2015 to 03/25/2019
ifile_ts_ls_alos = 'c:/Users/hpham/Documents/P31 Maki/ML4sub/input/ts_ls_at_well_logs/v02_02202020/ts_ls_at_well_logs_alos_pv.csv'
print(f'Reading file {ifile_ts_ls_alos}\n')
#dfls_alos = pd.read_csv(ifile_ts_ls_alos)
#dfls_alos['Date'] = pd.to_datetime(dfls_alos['Date'])

ifile_ts_ls_sen = 'c:/Users/hpham/Documents/P31 Maki/ML4sub/input/ts_ls_at_well_logs/v02_02202020/ts_ls_at_well_logs_sen_asc_run4.csv'
print(f'Reading file {ifile_ts_ls_sen}\n')
#dfls_sen = pd.read_csv(ifile_ts_ls_sen)
#dfls_sen['Date'] = pd.to_datetime(dfls_sen['Date'])


# [1.2] Specify the path to time series groundwater level data
# (csv files, one file for one well) - Combine to one file later
ifile_gwlevel = r'../input/gwlevels__freq_M.csv'

# [1.3] Load data and resampling
dfls_alos, dfgw = read_input(ifile_ts_ls_alos, ifile_gwlevel,
                             sampling_freq, start_date)
dfls_sen, dfgw = read_input(ifile_ts_ls_sen, ifile_gwlevel,
                            sampling_freq, start_date)

print(dfls_alos.shape)
print(dfls_sen.shape)


# [] Create a new folder to save the figures
odir = '../output/head_vs_ls_' + sat + '_' + domain + '_' + sampling_freq + '/'
if not os.path.exists(odir):  # Make a new directory if not exist
    os.makedirs(odir)
    print(f'\nCreated directory {odir}\n')

# [] Plot ls vs.hed
if opt_plot_ls_vs_head:
    plot_ls_vs_hed(dfls_alos, dfls_sen, dfgw, start_date, end_date, odir)

# [] Calculate trends
if opt_cal_trend:
    wname = list(dfs.columns)
    wname.remove('Date')
    dfout = pd.DataFrame(columns=['Name', 'trend', 'up', 'lo'])
    dfout['Name'] = wname
    dfout = EstimateTrend(dfs, dfout, wname)
    dfout.to_csv('../output/trend.csv', index=False)
