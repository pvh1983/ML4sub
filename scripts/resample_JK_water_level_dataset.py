import pandas as pd
import datetime as dt
from datetime import datetime
import os

'''
JK gave data in format of Name, Date, and Water level.
This code resample the data in format of Date (monthly, quarterly, or yearly)
 and gwlevels at each well (one col one well)

'''

ifile = r'../input/new_gwlevel_2019_from_JK_hpham_edited.csv'
df = pd.read_csv(ifile)

# [] Create a new folder to save the figures
odir = '../output/raw_gwlevels/'
if not os.path.exists(odir):  # Make a new directory if not exist
    os.makedirs(odir)
    print(f'\nCreated directory {odir}\n')

wname = df['Well Name'].drop_duplicates()
for i, wn in enumerate(wname):
    print(f'i={i}, wn={wn} \n')
    df_new = df[df['Well Name'] == str(wn)]
    ofile = odir + wn + '.csv'
    df_new.to_csv(ofile, index=False)
