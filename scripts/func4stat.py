import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats


def gen_date_time_series(start_date, end_date, sampling_freq):
    df_dt = pd.DataFrame({'Date': [start_date, end_date], 'Val': [999, 999]})
    df_dt['Date'] = pd.to_datetime(df_dt['Date'])
    df_date = df_dt.resample(
        sampling_freq, on='Date').mean()   # resample by month
    df_date = df_date.reset_index()
    df_date = df_date.drop('Val', 1)
    return df_date


def read_input(ifile, sampling_freq, start_date, opt_del_empty_cell):
    print(f'Reading time-series file for LS: {ifile}\n')
    '''
    df0 = pd.read_csv(ifile_ts_ls)
    df0['Date'] = pd.to_datetime(df0['Date'])
    # resample to monthly data
    df0 = df0.resample(sampling_freq, on='Date').mean()
    df0 = df0.reset_index()
    df0['Date'] = pd.to_datetime(df0['Date'])

    print(f'Reading time-series file for GWLevel: {ifile}\n')
    '''
    df = pd.read_csv(ifile)
    df['Date'] = pd.to_datetime(df['Date'])
    # resample to monthly data
    df = df.resample(sampling_freq, on='Date').mean()
    df = df.reset_index()

    df = df[df['Date'] > start_date]
#    row_to_drop = range(0, 117, 1)
#    df = df.drop(row_to_drop)
    df = df.reset_index()
    df['Date'] = pd.to_datetime(df['Date'])
    if opt_del_empty_cell:
        df['Date'] = pd.to_datetime(df['Date'])

    print(f'Done reading the imput files and resampling data \n')
    return df


def EstimateTrend(df, dfout, wname, npoints):
    xm = pd.to_datetime(df['Date'])
#    print(f'xm={xm}')
    #wname = list(df.columns)
    # wname.remove('Date')
    for id, wn in enumerate(wname):     # id is count, s is wname
        cols = ['Date', wn]
        df_new = df[cols]
        df_new = df_new.dropna(subset=cols)
        print(f'df_new size = {df_new.shape}')
        if df_new.empty:
            print('Datafram is empty. Skipped. \n')
            # break
        else:
            if df_new.shape[0] > npoints:
                print(f'df_new size={df_new.shape} \n')
                xm = df_new['Date'].dt.year
                ym = df_new[wn]
                modelm = stats.theilslopes(ym, xm, 0.95)
                dfout.loc[id, 'trend'] = modelm[0]
                dfout.loc[id, 'up'] = modelm[2]
                dfout.loc[id, 'lo'] = modelm[3]
                dfout.loc[id, 'start_date'] = xm.min()
                dfout.loc[id, 'end_date'] = xm.max()
                dfout.loc[id, 'nobs'] = df_new.shape[0]
                print(
                    f'{id}: Well: {wn}, nobs=[{len(xm)}, {len(ym)}], trend = { modelm[0]}')
    return dfout
