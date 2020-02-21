import pandas as pd
import matplotlib.pyplot as plt
import os

'''
Compare the results from two runs for the descending path and the ascending path

'''


def read_input_file(ifile, sampling_freq):
    #ifile1 = r'../input/ts_ls_at_well_logs/ts_ls_at_well_logs_sen_dsc.csv'
    df = pd.read_csv(ifile)
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.resample(sampling_freq, on='Date').mean()
    df = df.reset_index()
    df['Date'] = pd.to_datetime(df['Date'])
    return df


# Define several input parameters
sampling_freq = 'Q'

ifile = [r'../input/ts_ls_at_well_logs/ts_ls_at_well_logs_sen_dsc.csv',
         r'../input/ts_ls_at_well_logs/ts_ls_at_well_logs_sen_dsc.csv']

'''
ifile1 = r'../input/ts_ls_at_well_logs/ts_ls_at_well_logs_sen_dsc.csv'
df1 = read_input_file(ifile1, sampling_freq)

ifile2 = r'../input/ts_ls_at_well_logs/ts_ls_at_well_logs_sen_dsc.csv'
df2 = read_input_file(ifile2, sampling_freq)

ifile1 = r'../input/ts_ls_at_well_logs/ts_ls_at_well_logs_sen_dsc.csv'
df1 = pd.read_csv(ifile1)
df1['Date'] = pd.to_datetime(df1['Date'])
df1 = df1.resample(sampling_freq, on='Date').mean()
df1 = df1.reset_index()
df1['Date'] = pd.to_datetime(df1['Date'])


ifile2 = r'../input/ts_ls_at_well_logs/ts_ls_at_well_logs_sen_asc.csv'
df2 = pd.read_csv(ifile2)
df2['Date'] = pd.to_datetime(df2['Date'])
df2 = df2.resample(sampling_freq, on='Date').mean()
df2 = df2.reset_index()
df2['Date'] = pd.to_datetime(df2['Date'])
'''

for i, f in enumerate(ifile):

    wname = list(df2.columns)
    wname.remove('Date')

    # Make a new dir
    odir = '../output/compare_ls_ts/'
    if not os.path.exists(odir):  # Make a new directory if not exist
        os.makedirs(odir)
        print(f'\nCreated directory {odir}\n')

    for i, wn in enumerate(wname):
        # Compare the time series of subsidence for diff data sets (asc vs dsc)
        fig, ax = plt.subplots()
        fig.set_size_inches(8, 6.5)

        # Plot 1
        y1 = df1[wn]
        x1 = df1['Date']
        p1 = ax.plot(x1, y1, '-o')

        # Plot 2
        y2 = df2[wn]
        x2 = df2['Date']
        p2 = ax.plot(x2, y2, '-s')
        ax.legend(['Ascending', 'Descending'])

        plt.title(wn)
        ofile = odir + str(i+1).rjust(4, '0') + '_' + wn + '.png'
        fig.savefig(ofile, dpi=100, transparent=False, bbox_inches='tight')
        plt.close("all")
