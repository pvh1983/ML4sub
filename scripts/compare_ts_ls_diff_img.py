import pandas as pd
import matplotlib.pyplot as plt
import os

'''
Compare the results from diffent runs/satellits: (1) ALOS, (2) SENTINEL-1 ascending/descending paths

'''

# cd c:\Users\hpham\Documents\P31 Maki\ML4sub\scripts\


def read_input_file(ifile, sampling_freq):
    #ifile1 = r'../input/ts_ls_at_well_logs/ts_ls_at_well_logs_sen_dsc.csv'
    df = pd.read_csv(ifile)
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.resample(sampling_freq, on='Date').mean()
    df = df.reset_index()
    df['Date'] = pd.to_datetime(df['Date'])
    return df


def get_list_of_points(p0):
    p0 = 'p046_074'
    irow = int(p0[1:4])
    icol = int(p0[5:8])
    # Get four points around p0
    id_rows = [irow-1, irow, irow+1]
    id_cols = [icol-1, icol, icol+1]
    pname = []
    for j in id_cols:
        pname_cur = 'p'+str(irow).rjust(3, '0') + '_' + str(j).rjust(3, '0')
        if pname_cur not in pname:
            pname.append(pname_cur)
    for i in id_rows:
        pname_cur = 'p'+str(i).rjust(3, '0') + '_' + str(icol).rjust(3, '0')
        if pname_cur not in pname:
            pname.append(pname_cur)
    return pname


    # Define several input parameters
sampling_freq = 'M'

ifile = [
    r'../input/ts_ls_at_well_logs/v02_02202020/ts_ls_at_well_logs_sen_asc_run4_NOPE.csv',
    r'../input/ts_ls_at_well_logs/v02_02202020/ts_ls_at_well_logs_sen_asc_run5_ASHM.csv',
    #         r'../input/ts_ls_at_well_logs/v02_02202020/ts_ls_at_well_logs_sen_dsc_run1.csv',
    r'../input/ts_ls_at_well_logs/v02_02202020/ts_ls_at_well_logs_sen_dsc_ASHM_run4.csv',
]


# Make a new dir
odir = '../output/compare_ls_ts_freq_' + sampling_freq + '/'
if not os.path.exists(odir):  # Make a new directory if not exist
    os.makedirs(odir)
    print(f'\nCreated directory {odir}\n')


df = read_input_file(ifile[0], sampling_freq)
wname = list(df.columns)
wname.remove('Date')

wname = [{'LaComb Irrigation Well': 'p046_074'},
         {'Ruins Well': 'p044_069'}]

cur_point = wname[1]['Ruins Well']
list_of_points = get_list_of_points(cur_point)
for i, wn in enumerate(wname[:300]):
    fig, ax = plt.subplots()
    fig.set_size_inches(6, 4)
    plt.grid(color='#e6e6e6', linestyle='-', linewidth=0.5, axis='both')
    for j, f in enumerate(ifile):
        df = read_input_file(f, sampling_freq)

        # Plot 1
        cols = ['Date', wn]
        dfi = df[cols]
        dfi = dfi.dropna(subset=cols)
        y1 = dfi[wn]
        x1 = dfi['Date']
        p1 = ax.plot(x1, y1, '-o', MarkerSize=1.5, alpha=0.8)
    ax.set_ylabel('LOS Displacement (cm)', color='k')
    ax.set_ylim([-5, 5])
    ax.legend([
        #           'Ascending run 2',
        'Asc4 NOPE',
        'Asc5 ASHM',
        #           #               'Descending run 1',
        'Dsc4 ASHM',
    ])
    plt.title(wn)
    ofile = odir + str(i+1).rjust(4, '0') + '_' + wn + '.png'
    fig.savefig(ofile, dpi=150, transparent=False, bbox_inches='tight')
    plt.close("all")
