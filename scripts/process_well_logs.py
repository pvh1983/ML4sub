import pandas as pd
import os

'''
NOTES: 
    + Code to process the well log data (Create a dataframe for all logs)

'''
# cd c:\\Users\\hpham\\Documents\\P31 Maki\\ML4sub\\scripts

generate_init_dataframe = True  # Create an init dataframe
thre_segment = 1  # (=1 mean no threshold; other: yes, consider)

process_init_data_frame = True


path_to_file = r'..//input/well_log_interpretations/'
list_of_file = os.listdir(path_to_file)
nwells = len(list_of_file)
wname = ['Depth_ft'] + [list_of_file[i][:-4] for i in range(len(list_of_file))]
df_out = pd.DataFrame(columns=wname)
well_depth = range(1, 1200+1, 1)  # 1000 feet
df_out['Depth_ft'] = well_depth

# Load well meta file to add more information
mfile = r'../input/top1wells_final_100percent.csv'
dfmeta = pd.read_csv(mfile)
col_keep = ['well_log', 'latitude', 'longitude', 'well_finish_date',
            'depth_drilled', 'depth_cased', 'csng_diameter', 'top_perf', 'bottom_perf',
            'static_wl']
# skip 'date_log_rcvd', 'utm_x', 'utm_y'
dfmeta = dfmeta[col_keep]
dfmeta['well_log'] = dfmeta['well_log'].astype(str)

dfmeta_inuse = dfmeta.loc[dfmeta['well_log'].isin(wname)]

# Open a file to record the run log and important information
ifile_out = '../output/logs_processing_well_logs.txt'
f = open(ifile_out, 'w')


if generate_init_dataframe:
    count = 0
    for i, wlog_file in enumerate(list_of_file):
        print(
            f'i={i}/{nwells} ({round(100*i/nwells,1)} %) (Reading {wlog_file}) \n')
        ifile = path_to_file + wlog_file
        wname = wlog_file[:-4]
        df = pd.read_csv(ifile)
        n_segment = df.shape[0]
        if n_segment >= thre_segment:
            for j in range(n_segment):
                from_ft = int(df['from_feet'].iloc[j])
                to_ft = int(df['to_feet'].iloc[j])
                if (j == 0 and from_ft > 0):
                    df_out[wname].iloc[0:to_ft] = 0
                    print(
                        f'Well {wname}, starting deep: {from_ft} (ft), may be a deepen well -> assigned SAND (1). \n', file=f)
                    count += 1
                else:
                    df_out[wname].iloc[from_ft:to_ft] = df['binary'].iloc[j]
        else:
            print(f'n_segment = {n_segment}. Skip this well log. \n', file=f)
            count += 1

    print(
        f'Skipped {count} boreholes that have problems. \n', file=f)

    ofile = '../output/df_litho.csv'
    df_out.to_csv(ofile, index=False)
    print(f'The ouput was saved at {ofile} \n')
    f.close()

if process_init_data_frame:
    ifile = '../output/df_litho.csv'
    df = pd.read_csv(ifile)
    th_all = df.count()
    th_sand = df.sum()
    th_clay = th_all - th_sand

    df2 = pd.DataFrame(
        {'th_all': th_all, 'th_sand': th_sand, 'th_clay': th_clay})
    df2.reset_index(inplace=True)
    df2.rename(columns={'index': 'well_log'}, inplace=True)

    # Combine the two dataframe
    df_final = pd.merge(dfmeta_inuse, df2, how='left', on='well_log')
    ofile = '../output/dfmeta_added.csv'
    df_final.to_csv(ofile, index=False)
    print(f'The ouput was saved at {ofile} \n')

'''
# OTHER NOTES:
    + Skip if only one row of record.

'''

# DELETED: 61326.csv,
