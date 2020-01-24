import pandas as pd 
import numpy as np
from matplotlib import pyplot as plt, ticker
import matplotlib as mpl
import datetime as dt
import os
from mintpy.defaults.plot import *
from mintpy.utils import ptime, readfile, utils as ut, plot as pp
from mintpy.objects import sensor, timeseries, ifgramStack
from mintpy import view
import subprocess


# Read me first ===============================================================
# Use conda env mintpy source ~/.mintpy


# [1] Choose option(s) to run
get_ts_of_ls = False # both figs and csv files
save_fig = False
#work_dir = os.path.expanduser('/scratch/hpham/insar/insar_pahrump/P173_F_470/TOPSTACK/mintpy/geo')
work_dir = os.path.expanduser('/scratch/hpham/insar/las2agu_new/pahrump_sen1/TOPSTACK/mintpy/geo_no_ref_v21')
#ifile_loc='/scratch/hpham/insar/las2agu_new/pahrump_sen1/TOPSTACK/mintpy/loc_20_wells.csv'
ifile_loc='/scratch/hpham/insar/las2agu_new/pahrump_sen1/TOPSTACK/mintpy/loc_gwwells.csv'
#ifile_loc='/scratch/hpham/insar/las2agu_new/pahrump_sen1/TOPSTACK/mintpy/all_locs.csv' # all points: gw, gps, well_logs

geo_box = (-116.184, 36.388, -115.802, 36.007)    # Small Pahrump



# [2]
plot_ls_vs_gps = False  # Old, hpham's code, not using now.
plot_temporal_corehence = False
check_result_diff_ref_points = False # Check ts of ls for 3 sces of ref_loc vs GPS data
#ref_sta = 'ASHM'

ref_sta = '_no_ref_v21'
# Specify some input files
ts_file = 'timeseries_ERA5_ramp_demErr.h5'
#vel_file = 'geo' + ref_sta + '/geo_velocity.h5'
vel_file = 'velocity.h5'
dem_file    = '/scratch/hpham/insar/las2agu_new/pahrump_sen1/ISCE/demLat_N35_N38_Lon_W117_W113.dem.wgs84'
ifgram_file = 'inputs/ifgramStack.h5'
geom_file   = 'inputs/geometryRadar.h5'  
temp_coh_file = 'temporalCoherence.h5'  


# [3] Compare with GPS data ===================================================
# https://nbviewer.jupyter.org/github/geodesymiami/Yunjun_et_al-2019-MintPy/blob/master/Fig_08_S06_InSAR_vs_GPS.ipynb
compare_gps = True # Code from Junjun

# Provide GPS stations [Name, lat, long]
#site_names = ['GV{:02d}'.format(i) for i in [1] + np.arange(3,11).tolist()]
#site_names = ['ASHM','NOPE','UNR1','CLV1','CLV2','CLV3','NVCA','NVLV','NVBM','JEAN','VFSP']
site_names = ['ASHM','NOPE','UNR1','CLV1','CLV2','CLV3'] # both Pahrump and LAS
#site_names = ['ASHM','NOPE','UNR1'] # 

gps_dir = os.path.expanduser('/scratch/hpham/insar/raw_data') # To save GPS data? 
ref_site = 'ASHM'

#
curr_geo_dir = 'geo' + ref_sta + '/'
dem_file    = '/scratch/hpham/insar/las2agu_new/pahrump_sen1/ISCE/demLat_N35_N38_Lon_W117_W113.dem.wgs84'
work_dir = os.path.expanduser('/scratch/hpham/insar/las2agu_new/pahrump_sen1/TOPSTACK/mintpy/')
proj_dir = work_dir
ts_file = work_dir + 'timeseries_ERA5_ramp_demErr.h5'
vel_file = work_dir + curr_geo_dir + 'geo_velocity.h5'
mask_file = work_dir + curr_geo_dir +  'geo_maskTempCoh.h5'
temp_coh_file = work_dir + 'temporalCoherence.h5'
geom_file = work_dir + 'inputs/geometryRadar.h5'

#ts_file       = os.path.join(proj_dir, 'mintpy/timeseries_ECMWF_ramp_demErr.h5')
#geom_file     = os.path.join(proj_dir, 'mintpy/inputs/geometryRadar.h5')
#temp_coh_file = os.path.join(proj_dir, 'mintpy/temporalCoherence.h5')




# Create a new directory
odir = '/scratch/hpham/insar/las2agu_new/pahrump_sen1/TOPSTACK/mintpy/outputs/compare_ls_ref_sta_' + ref_sta
if not os.path.exists(odir):  # Make a new directory if not exist
    os.makedirs(odir)
    print(f'Created directory {odir}')

odir2 = '/scratch/hpham/insar/las2agu_new/pahrump_sen1/TOPSTACK/mintpy/outputs/ls_at_a_sta_' + ref_sta
if not os.path.exists(odir2):  # Make a new directory if not exist
    os.makedirs(odir2)
    print(f'Created directory {odir2}')

odir3 = '/scratch/hpham/insar/las2agu_new/pahrump_sen1/TOPSTACK/mintpy/outputs/compare_results_diff_ref_points_' + ref_sta
if not os.path.exists(odir3):  # Make a new directory if not exist
    os.makedirs(odir3)
    print(f'Created directory {odir3}')


  

#ref_lat, ref_lon = 36.3459,-116.1394  
#lat, lon = 36.3459,-116.1394  


#[1] calculate subsidence at given points from 06/14/2015 to 03/25/2019
#ifile_ts_ls = '/scratch/hpham/insar/insar_pahrump/P173_F_470/TOPSTACK/mintpy/geo/ts_ls_all_points.csv'
#dfls = pd.read_csv(ifile_ts_ls)



#[2] GPS data http://geodesy.unr.edu
# Run code download_gps_data.py to get raw data
path_to_gps_data = '/scratch/hpham/insar/raw_data/'
ifile_gps= path_to_gps_data + 'daily_gps_data_in_cm.csv'
df_gps = pd.read_csv(ifile_gps) # Daily data
df_gps.Date=pd.to_datetime(df_gps.Date)
df_gps = df_gps.resample('M', on='Date').mean()  # Monthly data
df_gps.reset_index(inplace=True)

gps_sta_name=list(df_gps.columns)
gps_sta_name.remove('Date')

sta_list = gps_sta_name
n_sta = len(gps_sta_name)
offset = [75]*n_sta
#os.chdir(path_to_gps_data)
#print(f'Current dir: {path_to_gps_data}')
df2_gps=pd.DataFrame({'Date':df_gps.Date})


#
if get_ts_of_ls:
    
    
    #work_dir = os.path.expanduser('/scratch/hpham/insar/las2agu_new/pahrump_sen1/TOPSTACK/mintpy/geo_no_ref_v21')
    print(f'Work directory is {work_dir}\n')
    os.chdir(work_dir)
    print('Go to directory: '+ work_dir)

    #ts_file = 'geo_timeseries_ECMWF_ramp_demErr.h5'
    ts_file = work_dir + curr_geo_dir + 'geo_timeseries_ERA5_ramp_demErr.h5'
    vel_file = work_dir + curr_geo_dir + 'geo_velocity.h5'

    #dem_file = 'dem.h5'
    dem_file    = '/scratch/hpham/insar/las2agu_new/pahrump_sen1/ISCE/demLat_N35_N38_Lon_W117_W113.dem.wgs84'

    #mask_file = 'maskTempCohFernandina.h5'
    mask_file = work_dir + curr_geo_dir + 'geo_maskTempCoh.h5'

    #geo_box = (-116.749489, 37.818520, -113.520241, 35.510933)    # W, N, E, S
    #geo_box = (-116.5, 36.5, -115.25, 35.5)    # large Pahrump only
    #geo_box = (-116.75, 38.0, -113.5, 35.5)    # Pahrump and Vegas
    
    
    proj_name = 'pv1_las_sen1A'

    atr = readfile.read_attribute(ts_file)
    coord = ut.coordinate(atr)
    pix_box = coord.box_geo2pixel(geo_box)

    ## Fig.7 - call view.py to plot
    cmd = 'view.py {} -m {} '.format(ts_file, mask_file)
    cmd += ' --sub-lon {w} {e} --sub-lat {s} {n} '.format(w=geo_box[0], n=geo_box[1],
                                                        e=geo_box[2], s=geo_box[3])
    cmd += ' --wrap --wrap-range -5 5 '
    cmd += ' -c bwr -v -2.5 2.5 '
    cmd += ' --ncols 10 --nrows 10 --figsize 8 9 --fontsize 8 --notick --nocbar --dpi 600 --no-tight-layout '
    cmd += ' --noaxis  --nodisplay  -o {}_TS.png'.format(proj_name)
    #!{cmd}
    subprocess.call(cmd, shell=True)


    # Fig.7 - colorbar
    fig = plt.figure(figsize=(2, 0.1))
    ax = fig.add_axes([0.05, 0.05, 0.9, 0.9])
    cbar = mpl.colorbar.ColorbarBase(ax, cmap=plt.get_cmap('bwr'), orientation='horizontal', ticks=[0, 0.5, 1], extend='both')
    cbar.ax.set_xticklabels(['-10', '0', '10'])
    cbar.ax.tick_params(which='both', direction='out', labelsize=font_size)
    cbar.set_label('LOS Displacement [cm]', fontsize=font_size)
    if save_fig:
        plt.savefig('{}_TS_cbar.png'.format(proj_name), bbox_inches='tight', transparent=True, dpi=fig_dpi)
    #plt.show()

    # Backup - Plot Velocity with POI displacement timeseries

    # read ts data
    # load coordinates of observed wells
    #ll = pd.read_csv('/scratch/hpham/insar/insar_pahrump/GPS_points_PV1.csv') # only gps sta
    #ll = pd.read_csv('/scratch/hpham/insar/insar_pahrump/GPS_points_PV1_full.csv') # 
    print(f'Reading ifile_loc {ifile_loc} \n')
    ll = pd.read_csv(ifile_loc) # 
    

    obj = timeseries(ts_file)
    obj.open()
    dates = ptime.date_list2vector(obj.dateList)[0]
    df=pd.DataFrame({'Date':dates})
    for i in range(ll.shape[0]):
        cur_point = str(ll['Name'][i])
        lat, lon = ll['Latitude'][i], ll['Longitude'][i]
        print(f'\nName={cur_point}, lat={lat}, lon={lon}')
        y, x = coord.geo2radar(lat, lon)[0:2]
        print(f'x={x}, y={y}')
        print('y/x: {}/{}'.format(y, x))
        d_ts = np.squeeze(readfile.read(ts_file, box=(x, y, x+1, y+1))[0]) * 100.
        
        
        #d_ts = d_ts/
        #(Unw_Phase * wavelength in cm) / (-4 * PI * cos(rad(incident_angle)))
        #https://forum.step.esa.int/t/subswath-iw2-sentinel-1a/4322/4

        df[cur_point]=d_ts
        if save_fig:        
            fig, ax = plt.subplots(nrows=1, ncols=2, figsize=[8, 3])

            # read vel data
            cmd = 'view.py {} velocity --mask {} '.format(vel_file, mask_file)
            cmd += ' --sub-lon {w} {e} --sub-lat {s} {n} '.format(w=geo_box[0], n=geo_box[1], e=geo_box[2], s=geo_box[3])
            cmd += ' -c bwr -v -2.5 2.5 --cbar-loc bottom --cbar-nbins 5 --cbar-ext both --cbar-size 5% '
            cmd += ' --dem {} --dem-nocontour '.format(dem_file)
            cmd += ' --lalo-step 0.2 --lalo-loc 1 0 1 0 --scalebar 0.3 0.80 0.05 --notitle --fontsize 12 '
            cmd += ' --noverbose'
            d_v, atr ,inps = view.prep_slice(cmd)
            ax[0], inps, im, cbar = view.plot_slice(ax[0], d_v, atr, inps)

            ax[0].plot(lon, lat, "k^", mfc='none', mew=1., ms=6)  #point of interest
            cbar.set_label("LOS Velocity [cm/yr]", fontsize=font_size)


            ax[1].scatter(dates, d_ts, marker='o', s=4**2) #, color='k')
            pp.auto_adjust_xaxis_date(ax[1], obj.yearList, fontsize=font_size)
            ax[1].set_xlabel('Time [years]', fontsize=font_size)
            ax[1].set_ylabel('LOS Displacement [cm]', fontsize=font_size)
            ax[1].yaxis.set_minor_locator(ticker.AutoMinorLocator())
            ax[1].tick_params(which='both', direction='in', labelsize=font_size,
                            bottom=True, top=True, left=True, right=True)
            ax[1].set_title(cur_point, fontsize=font_size)

            fig.subplots_adjust(wspace=-0.4)
            fig.tight_layout()
            #plt.savefig('{}_POI.png'.format(proj_name), bbox_inches='tight', transparent=True, dpi=fig_dpi)
            ofilename = odir2 + '/' + str(cur_point) + '.png'
            print(f'Point: {ofilename}')
            plt.savefig(ofilename, bbox_inches='tight', transparent=True, dpi=fig_dpi)
    #plt.show()
    ofile = 'ts_ls_all_points.csv'
    df.to_csv(ofile, index=None)
    print(f'Saving LS ts to {ofile}')






if plot_ls_vs_gps:

    for i,sname in enumerate(sta_list):
        fig, ax = plt.subplots(nrows=1, ncols=1, figsize  = (8, 5))   
        #print(f'Reading file: {ifile_gps}')

        df2[sname] = df_gps[sname] - offset[i] # convert to cm and lower down
        #df2.plot(ax=ax, x='Date', y=sname,legend=False, style='o--', linewidth=1, markersize=3, label='GPS')
        #df2.plot(ax=ax, x='Date', y=sname, style='o--', label='GPS')
        df2.plot(ax=ax, x='Date', y=sname,legend=False, style='o:', linewidth=0.25, markersize=3, label='GPS')
        
        # 
        dfls.Date=pd.to_datetime(dfls.Date, yearfirst=True)
        dfls = dfls.resample('M', on='Date').mean()   #
        dfls.reset_index(inplace=True)
        dfls[sname] = dfls[sname]
        dfls.plot(ax=ax, x='Date', y=sname,legend=False, style='x-', linewidth=1, markersize=6, label='InSAR')
        
        ax.set_ylabel('Up (cm)')
        ax.set_title(sname)
        ax.legend()
        #ax.set_xlim(dt.date(2015, 1, 1), dt.date(2019, 12, 31))
        ax.grid(linewidth=0.25, alpha=0.5)    
        ofile = odir + '/' + sname + '.png'
        print(f'{i}: Saving file: {ofile}')
        fig.savefig(ofile, dpi=300, transparent=False, bbox_inches='tight')
        
    #plt.show()



if plot_temporal_corehence:
    work_dir = os.path.expanduser('/scratch/hpham/insar/insar_pahrump/P173_F_470/TOPSTACK/mintpy/')
    os.chdir(work_dir)
    print('Go to directory', work_dir)
    proj_name = sensor.project_name2sensor_name(work_dir)[1]

    # spatialCoh vs tempCoh
    spatial_coh_file = 'avgSpatialCoherence.h5'
    temp_coh_file = 'UNW_COR/tempCoh_unwrapPhase.h5'     #'temporalCoherence.h5' with unw err cor
    water_mask_file = 'waterMask.h5'

    # lava flow
    #ts_file  = 'geo/geo_timeseries_ECMWF_ramp_demErr.h5'
    #vel_file = 'geo/geo_velocity.h5'
    ts_file = 'geo/geo_timeseries_ERA5_ramp_demErr.h5'
    vel_file = 'geo/geo_velocity.h5'
    
    dem_file    = '/scratch/hpham/insar/insar_pahrump/P173_F_470/ISCE/demLat_N35_N38_Lon_W117_W113.dem.wgs84'
    ifgram_file = 'inputs/ifgramStack.h5'
    geom_file   = 'inputs/geometryRadar.h5'    
    ref_lat, ref_lon = 36.3459,-116.1394  

    lat, lon = 36.3459,-116.1394     

    # read data
    dates, dis = ut.read_timeseries_lalo(lat, lon, ts_file, lookup_file=geom_file, ref_lat=ref_lat, ref_lon=ref_lon)

    # Fig. 15b - Displacement time-series of the lava flow
    fig, ax = plt.subplots(figsize=[6, 1.5])
    ax.scatter(dates, dis*100., marker='^', s=6**2, facecolors='none', edgecolors='k', linewidth=1.)
    # axis format
    pp.auto_adjust_xaxis_date(ax, dates[2:-1], fontsize=font_size)
    ax.set_xlabel('Time [years]', fontsize=font_size)
    #ax.set_ylabel('LOS displacement [cm]', fontsize=font_size)
    ax.yaxis.tick_right()
    ax.yaxis.set_label_position("right")
    ax.yaxis.set_minor_locator(ticker.AutoMinorLocator())
    ax.set_ylim([-11, 4])
    ax.tick_params(which='both', direction='in', labelsize=font_size, bottom=True, top=True, left=True, right=True)

    # save
    out_file = 'ASHM_ts.png'
    plt.savefig(out_file, bbox_inches='tight', transparent=True, dpi=fig_dpi)
    print('save to file', os.path.join(os.getcwd(), out_file))
    plt.show()
    # read data

    # 
    obj = ifgramStack(ifgram_file)
    obj.open(print_msg=False)
    coord = ut.coordinate(obj.metadata, geom_file)
    y, x = coord.geo2radar(lat, lon)[0:2]
    box = (x, y, x+1, y+1)
    coh = np.squeeze(readfile.read(ifgram_file, datasetName='coherence', box=box, print_msg=False)[0])

    # Fig. 15c - Coherence matrix of the lava flow
    fig, ax = plt.subplots(figsize=[6, 1])
    ax, im = pp.plot_rotate_diag_coherence_matrix(ax, coh.tolist(), obj.date12List, cmap='RdBu', disp_min=0.0)
    # save
    out_file = 'ASHM_cohMat.png'
    plt.savefig(out_file, bbox_inches='tight', transparent=True, dpi=fig_dpi)
    print('save to file: '+out_file)
    plt.show()

    # [] Backup - LOS velocity of the lava flow
    print_msg = False
    fig, ax = plt.subplots(figsize=(3, 2))
    ## plot velocity
    cmd  = 'view.py {} velocity -d {} '.format(vel_file, dem_file)
    cmd += '--sub-lat 36.2459 36.5459 --sub-lon -116.2394 -116.0394 --wrap --wrap-range -2 2 --ref-lalo {} {} '.format(ref_lat, ref_lon)
    cmd += '--notitle --notick --nocbar --ref-size 2 --fontsize 12 -c RdBu_r '
    cmd += '--lalo-label --lalo-step 0.04 --lalo-loc 1 0 1 0 --scalebar 0.2 0.6 0.08 --scalebar-pad 0.1 '
    d_v, atr, inps = view.prep_slice(cmd)
    ax, inps, im, cbar = view.plot_slice(ax, d_v, atr, inps)
    # plot POI
    ax.plot(lon, lat, '^', ms=6, mec='k', mfc='w', mew=1.)
    # plot colorbar
    #cax = fig.add_axes([0.3, 0.05, 0.4, 0.025])
    cax = fig.add_axes([0.75, 0.23, 0.02, 0.35])
    cbar = plt.colorbar(im, cax=cax, ticks=[-2, 2])
    cbar.ax.tick_params(labelsize=font_size)
    cbar.set_label('cm/yr', fontsize=font_size, labelpad=-16)

    #save
    out_file = 'ASHM_vel.png'
    plt.savefig(out_file, bbox_inches='tight', transparent=True, dpi=fig_dpi)
    print('save to file: '+out_file)
    plt.show()

if check_result_diff_ref_points:
    sce = ['geo_no_ref', 'geo_ref_UNR1','geo_ref_ASHM', 'geo_no_ref_NEW']
    ifile = '/scratch/hpham/insar/insar_pahrump/P173_F_470/TOPSTACK/mintpy/geo_no_ref/ts_ls_all_points.csv'
    df1=pd.read_csv(ifile)
    ifile = '/scratch/hpham/insar/insar_pahrump/P173_F_470/TOPSTACK/mintpy/geo_ref_UNR1/ts_ls_all_points.csv'
    df2=pd.read_csv(ifile)
    ifile = '/scratch/hpham/insar/insar_pahrump/P173_F_470/TOPSTACK/mintpy/geo_ref_ASHM/ts_ls_all_points.csv'
    df3=pd.read_csv(ifile)
    ifile = '/scratch/hpham/insar/insar_pahrump/P173_F_470/TOPSTACK/mintpy/geo/ts_ls_all_points.csv'
    df4=pd.read_csv(ifile)
    
    df1.Date = pd.to_datetime(df1.Date)
    df2.Date = pd.to_datetime(df2.Date)
    df3.Date = pd.to_datetime(df3.Date)
    df4.Date = pd.to_datetime(df4.Date)
#    df1 = df1.resample('M', on='Date').mean()   #
#    df2 = df2.resample('M', on='Date').mean()   #
#    df3 = df3.resample('M', on='Date').mean()   #
#    df4 = df4.resample('M', on='Date').mean()   #

    font_size = 8
    sta_name = list(df_gps.columns)
    sta_name.remove('Date')
    #sta_name.remove('NVBR')
    #sta_name.remove('NVCS')
    for i,sname in enumerate(sta_name):
        fig, ax = plt.subplots(figsize=[8, 6])
        

        
        df1.plot(ax=ax, x='Date', y=sname,legend=False, style='o-', linewidth=1, markersize=3, label=sce[0])
    
        df2.plot(ax=ax, x='Date', y=sname,legend=False, style='o-', linewidth=1, markersize=3, label=sce[1])
 
        df3.plot(ax=ax, x='Date', y=sname,legend=False, style='o-', linewidth=1, markersize=3, label=sce[2])
    
        df4.plot(ax=ax, x='Date', y=sname,legend=False, style='o-', linewidth=1, markersize=3, label=sce[3])

        df2_gps[sname] = df_gps[sname] - offset[i] # convert to cm and lower down
        df2_gps.plot(ax=ax, x='Date', y=sname,legend=False, style='o:', linewidth=0.25, markersize=5, label='GPS')
        #ax.plot(df2_gps.Date, df2_gps[sname])




        ax.set_xlabel('Time [years]', fontsize=font_size)
        ax.set_ylabel('LOS displacement [cm]', fontsize=font_size)
        ax.set_title(sname, fontsize=font_size)
#        ax.yaxis.tick_right()
#        ax.yaxis.set_label_position("right")
#        ax.yaxis.set_minor_locator(ticker.AutoMinorLocator())
#        ax.set_ylim([-11, 4])
        ax.tick_params(which='both', direction='in', labelsize=font_size, bottom=True, top=True, left=True, right=True)
        ax.legend()
        ax.grid(linewidth=0.25,alpha=0.6)
        ofile = odir3 + '/' + sname + '.png'
        print(f'{i}: Saving file: {ofile}')
        fig.savefig(ofile, dpi=150, transparent=False, bbox_inches='tight')


if compare_gps:
    # hpham
    import os
    import pickle
    from dateutil.relativedelta import relativedelta
    import numpy as np
    from matplotlib import pyplot as plt, ticker
    from mintpy.defaults.plot import *
    from mintpy.objects import ifgramStack
    from mintpy.utils import readfile, plot as pp, utils as ut, network as pnet
    from mintpy.objects.gps import GPS
    from mintpy.objects.insar_vs_gps import insar_vs_gps
    from mintpy import view


    #work_dir = os.path.expanduser('~/Documents/Paper/2019_MintPy/figs_src/insar_vs_gps')
    #work_dir = os.path.expanduser('/scratch/hpham/insar/insar_pahrump/P173_F_470/TOPSTACK/mintpy/')
    #work_dir = os.path.expanduser('/scratch/hpham/insar/las2agu_new/pahrump_sen1/TOPSTACK/mintpy/')
    
    
    os.chdir(work_dir)
    print(f'Go to directory {work_dir} \n')

    #gps_loc_file = os.path.join(gps_dir, 'loc.txt')
    #gps_loc_file = os.path.join(gps_dir, 'GPS_points_PV1_LAS.csv')
    
    start_date = '20150614' # hpham: Need to update insar_vs_gps.py as well
    end_date = '20201231'
    fig_dpi=300

    # InSAR
#    proj_dir = os.path.expanduser('/scratch/hpham/insar/insar_pahrump/P173_F_470/TOPSTACK/mintpy/')
    out_file = 'mintpy.pickle'
#    ts_file       = os.path.join(proj_dir, 'mintpy/timeseries_ECMWF_ramp_demErr.h5')
#    geom_file     = os.path.join(proj_dir, 'mintpy/inputs/geometryRadar.h5')
#    temp_coh_file = os.path.join(proj_dir, 'mintpy/temporalCoherence.h5')

    if not os.path.isfile(out_file):
        #obj = insar_vs_gps(ts_file, geom_file, temp_coh_file, site_names, gps_dir, ref_site, gps_loc_file=None)
        obj = insar_vs_gps(ts_file, geom_file, temp_coh_file, site_names, gps_dir, ref_site)
        obj.open()
        with open(out_file, 'wb') as f:
            pickle.dump(obj.ds, f)
        print('saved to pickle file {}.'.format(out_file))
        ds = dict(obj.ds)
    else:
        with open(out_file, 'rb') as f:
            ds = pickle.load(f)
        print('read from pickle file {}.'.format(out_file))

    fig, ax = plt.subplots(figsize=(4, 6))
    site2plot = insar_vs_gps.sort_by_velocity(ds)
    for i in range(len(site2plot)):
        site = ds[site2plot[i]]
        ax = insar_vs_gps.plot_one_site(ax, site, offset=0.3*i)
    # axis format
    yr_list = [i.year + (i.timetuple().tm_yday - 1)/365.25 for i in site['insar_datetime']]
    ax, t0, t1 = pp.auto_adjust_xaxis_date(ax, yr_list)
    #ax.set_xlim(t0, t1+relativedelta(months=12))
    ax.yaxis.set_minor_locator(ticker.AutoMinorLocator())
    ax.tick_params(which='both', direction='in', labelsize=font_size, bottom=True, top=True, left=True, right=True)
    ax.set_xlabel('Time [years]', fontsize=font_size)
    ax.set_ylabel('LOS Displacement [m]', fontsize=font_size)
    ax.annotate(r'$RMSE$ / $R^2$ / $\gamma_{temp}$', xy=(1.03, -0.01), xycoords='axes fraction', fontsize=font_size, color='k')
    ax.annotate(' [cm]', xy=(1.03, -0.05), xycoords='axes fraction', fontsize=font_size, color='k')
    # legend
    handles, labels = ax.get_legend_handles_labels()
    ax.legend([handles[-1], handles[0]], ['GPS', 'InSAR'], loc='upper left', bbox_to_anchor=(0.03, 0.93), fontsize=font_size)

    # output
    out_file = os.path.join(os.getcwd(), 'insar_vs_gps_point_ts.png')
    plt.savefig(out_file, bbox_inches='tight', transparent=True, dpi=fig_dpi)
    print('save figure to file', out_file)
    #plt.show()       


