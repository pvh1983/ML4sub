import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime as dt
from datetime import datetime
import os
import plotly.express as px

'''
# Notes: Using conda env irp on local PC

# input data ------------------------------------------------------------------
# [1] A DataFrame of time series subsidence velocity at given points (i.e., 
#     gwlevel observation locations)
# [2] A DataFrame of time series gwlevels at observation locations

'''


cur_dir = os.getcwd()  # get the current working directory

sampling_freq = 'M'

# [1] Specify an input file that has the time series of subsidence velocity
# at groundwater level observation wells
ifile_ls = r'../data/ts_ls_all_points.csv'
df0 = pd.read_csv(ifile_ls)
df0['Date'] = pd.to_datetime(df0['Date'])
# resample to monthly data
dfs = df0.resample(sampling_freq, on='Date').mean()
dfs = df0.reset_index()


# [2] Specify the path to time series groundwater level data
# (csv files, one file for one well) - Combine to one file later
ifile_gwlevel = r'../data/gwlevels__freq_M.csv'
dfgw = pd.read_csv(ifile_gwlevel)
dfgw['Date'] = pd.to_datetime(dfgw['Date'])
# Get the list of groundwater level observation wells
logs = list(dfgw.columns)
logs.remove('Date')


# [3] Define some plotting parameters
font_size = 16
msize = 6
lwidth = 0.75
# Specify the time to plot
start_date = pd.Timestamp(dt.date(2005, 1, 1))
end_date = pd.Timestamp(dt.date(2019, 12, 31))
df_dt = pd.DataFrame({'Date': [start_date, end_date], 'Val': [999, 999]})
df_dt['Date'] = pd.to_datetime(df_dt['Date'])
df_date = df_dt.resample(sampling_freq, on='Date').mean()   # resample by month
df_date = df_date.reset_index()
df_date = df_date.drop('Val', 1)

# [4] Trim data
dfgw = dfgw[dfgw['Date'] > start_date]
#    row_to_drop = range(0, 117, 1)
#    dfgw = dfgw.drop(row_to_drop)
dfgw = dfgw.reset_index()
#

dfgw = dfgw[dfgw['Date'] > start_date]

# [5] Create a new folder to save the figures
odir = '../output/head_vs_ls/'
if not os.path.exists(odir):  # Make a new directory if not exist
    os.makedirs(odir)
    print(f'\nCreated directory {odir}\n')

for loc_name in logs:  # logs[0:1]:
    print(f'size dfgw = {dfgw.shape}')

    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(6, 5))

    # Plot 1 LOS displacement -------------------------------------------------
    col_keep = ['Date', loc_name]
    df = df0[col_keep]
    df['Date'] = pd.to_datetime(df['Date'])

    plt.grid(color='#e6e6e6', linestyle='-', linewidth=0.5, axis='both')

#    df = df[['Date', loc_name]]
#    df['Date'] = pd.to_datetime(df['Date'])
#    df = df.set_index(df['Date'])
#    df = df[[loc_name]]
#    df.plot(ax=ax, markersize=msize, linewidth=0.5, style='o:')
#    print(f'dfsize = {df.shape} ')
#    plt.show()

    x = df.Date
    #new_x = datetime.datestr2num(x)
    #new_x = datetime.fromisoformat(x).timestamp()
    y = df[loc_name]
    p1 = ax.plot(x, y, '-o', markersize=msize, markeredgecolor=None,
                 linewidth=lwidth, alpha=0.5, label='InSAR Displacement')
    ax.set_ylim(-5, 5)
#    tips = px.data.tips()
#    fig = px.scatter(df, x='Date', y=loc_name, trendline="ols")
    # fig.show()

    '''
    # calc the trendline
    xx = range(1, len(x)+1, 1)
    z = np.polyfit(xx, y, 1)
    p = np.poly1d(z)
    ax.plot(x, p(x), "r--")
    # the line equation:
    # print(f'y={z[0]}x+{z[1]}')
    '''

    # plot 2: gwleels ---------------------------------------------------------
    ax2 = ax.twinx()
    x2 = dfgw.Date
    y2 = dfgw[loc_name]

    p2 = ax2.plot(x2, y2, '-ro', markersize=msize, markeredgecolor=None,
                  linewidth=lwidth, alpha=0.75, label='Observed GW Levels')  # linecolor='#D3D3D3',
#    dfgw = dfgw[['Date', loc_name]]
#    dfgw = dfgw.set_index(dfgw['Date'])
#    dfgw = dfgw[[loc_name]]

#    dfgw.plot(ax=ax, markersize=msize, linewidth=0.5, style='o')
#    print(f'dfgw size = {dfgw.shape} ')
    #ax2.set_ylim(min(y2), max(y2))

    ax2.set_xlim(start_date, end_date)
    ax.set_title(loc_name, fontsize=font_size+2)
    ax.set_xlabel('Time [years]', fontsize=font_size)
    ax.set_ylabel('LOS Displacement [cm]', fontsize=font_size)
    ax2.set_ylabel('Groundwater Level [m]', fontsize=font_size)

    p = p1 + p2
    labs = [l.get_label() for l in p]
    ax.legend(p, labs, loc="upper right")

    ofile = odir + 'head_vs_ls_' + loc_name + '.png'
    print(f'Saving map to ... {ofile[-60:]} \n')
    fig.savefig(ofile, dpi=150, transparent=False, bbox_inches='tight')
    # plt.show()
