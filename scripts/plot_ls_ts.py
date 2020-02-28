import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime as dt
from datetime import datetime
import os
import plotly.express as px
from func4stat import *
from func4mapping import *

'''
# Notes: Using conda env irp on local PC
# Plot time series of both ls and gwlevels
 
# input data ------------------------------------------------------------------
# [1] A DataFrame of time series subsidence velocity at given points (i.e.,
#     gwlevel observation locations). Run main_sar.py after done mintpy
# [2] A DataFrame of time series gwlevels at observation locations

'''

# cd c:\Users\hpham\Documents\P31 Maki\ML4sub\scripts\

# Run options
opt_plot_ls_vs_head = False
opt_cal_trend_subsidence = False  # Subsidence
opt_cal_trend_gwlevel = False  # GWLevels
# Plot subplot 4x2 for selected wells (for fiel trip)
opt_subplot_ls_vs_head = True

# Define domain and satellite
domain = 'pv_las'    # 'pv' or 'las' or 'pv_las' (for sentinel)
sat = 'sen'   # 'alos' or 'sen'

# Specify the time to plot
cur_dir = os.getcwd()  # get the current working directory
sampling_freq = 'M'    # Note: Check freq of gwlevel at line 48
opt_del_empty_cell = True
start_date = pd.Timestamp(dt.date(2005, 1, 1))
end_date = pd.Timestamp(dt.date(2020, 2, 28))
df_date = gen_date_time_series(start_date, end_date, sampling_freq)


# [1] LOAD DATA ===============================================================
# [1.1] Specify an input file that has the time series of subsidence velocity
# at groundwater level observation wells
# ifile_ls = r'../input/ts_ls_at_well_logs/ts_ls_at_well_logs_' + \
#    sat + '_' + domain + '.csv'


# [1] ALOS subsidence at given points from 06/14/2015 to 03/25/2019
ifile_ts_ls_alos = 'c:/Users/hpham/Documents/P31 Maki/ML4sub/input/ts_ls_at_well_logs/v02_02202020/ts_ls_at_well_logs_alos_pv.csv'
print(f'Reading file {ifile_ts_ls_alos}\n')
# dfls_alos = pd.read_csv(ifile_ts_ls_alos)
# dfls_alos['Date'] = pd.to_datetime(dfls_alos['Date'])

# [2] SENTINEL-1 subsidence
ifile_ts_ls_sen = 'c:/Users/hpham/Documents/P31 Maki/ML4sub/input/ts_ls_at_well_logs/v02_02202020/ts_ls_at_well_logs_sen_dsc_ASHM_run4.csv'
print(f'Reading file {ifile_ts_ls_sen}\n')
# dfls_sen = pd.read_csv(ifile_ts_ls_sen)
# dfls_sen['Date'] = pd.to_datetime(dfls_sen['Date'])


# [1.2] Specify the path to time series groundwater level data
# (csv files, one file for one well) - Combine to one file later
# ifile_gwlevel = r'../input/gwlevels__freq_M.csv' # Old, gwlevels upto 2015
ifile_gwlevel = r'../output/gwlevel_cleanup_M_2019.csv'  # Old, gwlevels upto 2015


# [1.3] Load data and resampling/cleanning
dfls_alos, dfgw = read_input(ifile_ts_ls_alos, ifile_gwlevel,
                             sampling_freq, start_date, opt_del_empty_cell)
dfls_sen, dfgw = read_input(ifile_ts_ls_sen, ifile_gwlevel,
                            sampling_freq, start_date, opt_del_empty_cell)

print(dfls_alos.shape)
print(dfls_sen.shape)

# [1.4] Load metafile (locations of all point of interest)
ifile_meta = '../input/all_locs_at_boreholes.csv'
df_meta = pd.read_csv(ifile_meta)

# [] Create a new folder to save the figures
odir = '../output/head_vs_ls_' + sat + '_' + domain + '_' + sampling_freq + '/'
if not os.path.exists(odir):  # Make a new directory if not exist
    os.makedirs(odir)
    print(f'\nCreated directory {odir}\n')

# [] Plot ls vs.hed
if opt_plot_ls_vs_head:
    plot_ls_vs_hed(dfls_alos, dfls_sen, dfgw, start_date, end_date, odir)

if opt_subplot_ls_vs_head:
    print(f'\nRunning opt_subplot_ls_vs_head\n')
    sce_all = ['day1', 'day2', 'day3']  # day1 or day2 or day 3
    for sce in sce_all:
        if sce == 'day1':
            wname = ['Basin Station', 'Mcdonalds Horse Farm', 'Ruins Well', 'LaComb Irrigation Well',
                     'AW28', 'Hall2', 'Forum Group', 'West Flamingo Fan Well']
        elif sce == 'day2':
            wname = ['Stirrup', 'AW01', 'AW64', 'AW63',
                     'Donna', 'AW46', 'AW66', 'Squaw Valley Well']
        elif sce == 'day3':
            wname = ['BLM Stewart Valley Well', 'Stewart Valley Vacant', 'West Basin Fan Well',
                     'Stewart Valley South', 'West 372 Fan Well', 'West Basin Fan Well', 'Our Bar', 'West Mesquite']

        ofile = '../output/subplot hed vs InSAR ' + sce + '.png'
        subplot_ls_vs_hed(dfls_alos, dfls_sen, dfgw,
                          start_date, end_date, wname, ofile)
    print(f'\n All the outputs were saved at {ofile} \n')
    # [] Calculate trends
if opt_cal_trend_subsidence:
    # Trend ALOS
    npoints = 5
    wname = list(dfls_alos.columns)
    wname.remove('Date')
    dfout = pd.DataFrame(columns=['Name', 'trend', 'up', 'lo'])
    dfout['Name'] = wname
    dfout_alos = EstimateTrend(dfls_alos, dfout, wname, npoints)
    dfout_alos.to_csv('../output/trend_subsidence_2007_2011.csv', index=False)

    # TREND SENTINEL
    wname = list(dfls_sen.columns)
    wname.remove('Date')
    dfout = pd.DataFrame(columns=['Name', 'trend', 'up', 'lo'])
    dfout['Name'] = wname
    dfout_sen = EstimateTrend(dfls_sen, dfout, wname, npoints)
    dfout_sen.to_csv('../output/trend_subsidence_2014_2020.csv', index=False)

if opt_cal_trend_gwlevel:
    dfls_sen, dfgw = read_input(ifile_ts_ls_sen, ifile_gwlevel,
                                'Y', start_date)
    npoints = 2
    wname = list(dfgw.columns)
    wname.remove('Date')
    dfout = pd.DataFrame(
        columns=['Name', 'trend', 'up', 'lo', 'start_date', 'end_date', 'nobs'])
    dfout['Name'] = wname
    dfout = EstimateTrend(dfgw, dfout, wname, npoints)
    # Get location for each well
    df_final = pd.merge(dfout, df_meta, on='Name')
    df_final.to_csv('../output/trend_gwlevels.csv', index=False)
