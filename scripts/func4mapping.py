import pandas as pd
#import math
import os
#import subprocess
import numpy as np
import matplotlib.pyplot as plt
#import seaborn as sns
#import statistics as stat
from mpl_toolkits.basemap import Basemap


def MapPlotPV(domain_coor='', showbg=False, show_wsb=False, df='',
              var='', ofile='', vmin=0, vmax=10, legend_name=''):
    xmin, xmax, ymin, ymax = domain_coor  # NV
    s_size = 12
    s_edgewidth = 0.1
    cmap = 'rainbow'

    # Create the figure and basemap object
    fig, ax = plt.subplots()
    #fig = plt.gcf()
    fig.set_size_inches(8, 6.5)
    #    m = Basemap(projection='robin', lon_0=0, resolution='c')
    m = Basemap(llcrnrlon=xmin, llcrnrlat=ymin, urcrnrlon=xmax,
                urcrnrlat=ymax, projection='npstere',
                resolution='l', lon_0=-115, lat_0=36, epsg=4269)
    #    m = Basemap(llcrnrlon=xmin, llcrnrlat=ymin, urcrnrlon=xmax, urcrnrlat=ymax, projection='robin',
    #                resolution='l', lon_0=-115, lat_0=36)

    #

    # m.bluemarble(scale=0.2)   # full scale will be overkill
    # Plot BACKGROUND =========================================================

    if showbg == True:
        # World_Shaded_Relief, ESRI_Imagery_World_2D, World_Imagery,
        m.arcgisimage(service='World_Shaded_Relief',
                      xpixels=1500, dpi=300, verbose=True, alpha=0.25)  # Background
        # More maps at http://server.arcgisonline.com/arcgis/rest/services
    # Watershed
    show_wsb = True
    if show_wsb:
        m.readshapefile('../input/shp/WBDHU12', name='NAME',
                        color='#bfbfbf', linewidth=0.25, drawbounds=True)

    # road layer
    show_road = True
    if show_road:
        m.readshapefile('../input/shp/tl_2016_us_primaryroads',
                        name='NAME', color='#a52a2a', linewidth=0.5, drawbounds=True)

    # Plot well_depth =========================================================
    #x, y = [df["Lon"].values, df["Lat"].values]
    z_value = df[var]
    #vmin = min(z_value)
    #vmax = max(z_value)

    # transform coordinates
    x, y = m(df["longitude"].values, df["latitude"].values)

    plt1 = plt.scatter(x, y, c=z_value, vmin=vmin, vmax=vmax,
                       edgecolors='k', s=z_value/25,
                       linewidth=s_edgewidth, cmap=cmap, alpha=1)

    # Legend
    # fig.colorbar(plt1)
    #cbar_ax = fig.add_axes([0.1, 0.1, 0.25, 0.01])
    cbar_ax = fig.add_axes([0.2, 0.18, 0.25, 0.01])
    #cbar_ax = fig.add_axes([0.2, 0.08, 0.2, 0.01])
    cbar = fig.colorbar(plt1, orientation='horizontal',
                        extend='both', extendfrac='auto', cax=cbar_ax)
    cbar.set_label(legend_name, labelpad=0, y=0.08, rotation=0)

#    ax.set_title('One standard deviation of simulated heads')
    # m.drawcountries(linewidth=1.0)
    # m.drawcoastlines(linewidth=.5)

    fig.savefig(ofile, dpi=300, transparent=False, bbox_inches='tight')
    # plt.show()


def MapPlotLS(filepath, ts, date_aqui, years, gps_file, domain_coor, vmin, vmax, c_map, ti):

    x_min, x_max, y_min, y_max = domain_coor  # NV
    s_size = 12
    s_width = 0.05
    s_gps_color = '#bfbfbf'

    # Read the data and metadata
    print(f'Opening file {filepath}')
    ds = gdal.Open(filepath)

    data = ds.ReadAsArray()
    gt = ds.GetGeoTransform()
    proj = ds.GetProjection()

    xres = gt[1]
    yres = gt[5]

    # get the edge coordinates and add half the resolution
    # to go to center coordinates
    xmin = gt[0] + xres * 0.5
    xmax = gt[0] + (xres * ds.RasterXSize) - xres * 0.5
    ymin = gt[3] + (yres * ds.RasterYSize) + yres * 0.5
    ymax = gt[3] - yres * 0.5

    ds = None

    # create a grid of xy coordinates in the original projection
    xy_source = np.mgrid[xmin:xmax+xres:xres, ymax+yres:ymin:yres]

    # Create the figure and basemap object
    fig, ax = plt.subplots()
    fig.set_size_inches(8, 6.5)
    #    m = Basemap(projection='robin', lon_0=0, resolution='c')
    m = Basemap(llcrnrlon=xmin, llcrnrlat=ymin, urcrnrlon=xmax, urcrnrlat=ymax, projection='lcc',
                resolution='l', lon_0=-115, lat_0=36, epsg=4269)
    #    m = Basemap(llcrnrlon=xmin, llcrnrlat=ymin, urcrnrlon=xmax, urcrnrlat=ymax, projection='robin',
    #                resolution='l', lon_0=-115, lat_0=36)

    # Create the projection objects for the convertion
    # original (Albers)
    #    inproj = osr.SpatialReference()
    #    inproj.ImportFromWkt(proj)

    # Get the target projection from the basemap object
    #    outproj = osr.SpatialReference()
    #    outproj.ImportFromProj4(m.proj4string)

    # Convert from source projection to basemap projection
    # xx, yy = convertXY(xy_source, inproj, outproj)

    # Plot BACKGROUND =========================================================
    showbg = False
    if showbg == True:
        #        m.arcgisimage(service='ESRI_Imagery_World_2D',
        #                      xpixels=1500, ypixel=None, dpi=300, verbose=True, alpha=1)  # Background
        m.arcgisimage(service='World_Shaded_Relief',
                      xpixels=1500, dpi=300, verbose=True, alpha=0.25)  # Background

    # Show GPS locations ==================================================
    plot_gps_locations = True
    if plot_gps_locations == True:
        df = pd.read_csv(gps_file)
        print(f'GPS location input file is {gps_file}')
        # print(df.head())
        x, y = [df["Long"].values, df["Lat"].values]
    #    x, y = map(df["Lat"], df["Long"])
    #    print(f'x={x}, y={y}')
        plt.scatter(x, y, edgecolors=s_gps_color, color='k',
                    s=s_size, linewidth=s_width, alpha=1)
        #
#    m.readshapefile('SHP/WBDHU6', name='NAME', color='#bfbfbf',
#                    linewidth=1, drawbounds=True)

    # plot LS the data (first layer) ==========================================
    plot_ls = True
    if plot_ls == True:
        xx, yy = xy_source
#        print(f'xx={xx}, yy={yy}')

        data = ma.masked_where(data == -9999, data)
        # shading='gouraud',
        im1 = ax.pcolormesh(xx, yy, data.T, cmap=c_map,
                            vmin=vmin, vmax=vmax, alpha=0.5)
        cbar_ax = fig.add_axes([0.32, 0.08, 0.25, 0.01])
        cbar = fig.colorbar(im1, orientation='horizontal',
                            extend='both', extendfrac='auto', cax=cbar_ax)
        cbar.set_label(ti,
                       labelpad=0, y=0.08, rotation=0)
#        ax.set_facecolor('xkcd:salmon')

    ax.set_title(
        f'Acquisition date: {date_aqui}, Cumulative time: {str(round(years,2))} (years)')
    # annotate
    # m.drawcountries(linewidth=1.0)
    # m.drawcoastlines(linewidth=.5)
    # str("{:04}".format(years))
    ofile = 'LS_' + 'TS' + str(ts).rjust(2, '0') + '.png'
    print(f'TS={ts}, date: {date_aqui}, years: {years}, file out: {ofile}')
    fig.savefig(ofile, dpi=100, transparent=False, bbox_inches='tight')
    # plt.show()


def gen_ani(indir, ofile):

    frames = []
    # Load each file into a list
#    for root, dirs, filenames in os.walk(indir):
#    for filenames in os.listdir(indir):
    for filename in sorted(os.listdir(indir)):
        frames.append(imageio.imread(indir + "/" + filename))
    print(f'List of png files: {sorted(os.listdir(indir))}')
    # Save them as frames into a gif
    # kargs = {'duration': 2}
    kargs = {'fps': 0.5}
    imageio.mimsave(ofile, frames, 'GIF', **kargs)

    # shutil.move('fire_in_each_year_USA_png.gif', 'C:\Users\hpham\Dropbox\HPham-PLe\IRP2019\03_Codes\output')


def plot_2D_LS(if1, if2, dtime_ifile, lb):
    date = pd.read_csv(dtime_ifile)
    x = date['Time']
    msize = 24
    gw_line_width = 0.25

    df1 = pd.read_csv(if1)
    df2 = pd.read_csv(if2)
    print(f'Opening file {if1}')
    print(f'Opening file {if2}')
    nstations = df1.shape[0]
    for sta in df1.columns:
        y1 = df1[sta]
        y2 = df2[sta] - df2[sta][0]

        # LINE PLOTs
        fig, ax1 = plt.subplots(figsize=(5, 4))

        plt.grid(color='#e6e6e6', linestyle='-', linewidth=0.5, axis='both')
        # linestyle='dotted',
    #    ax1.scatter(x, y1, color='b', marker='o', linestyle=':',
    #                s=msize, edgecolors='k', linewidth=gw_line_width, alpha=0.5, label='SBAS')

        plt.plot(x, y1, '-ob', linewidth=gw_line_width, alpha=1, label=lb[0])
        plt.plot(x, y2, '-sr', linewidth=gw_line_width, alpha=1, label=lb[1])

        ax1.set_ylabel('Cumulative displacement (mm)')
        # Make the y-axis label, ticks and tick labels match the line color.
        ax1.set_xlabel('Time in years', color='b')
        # ax1.set_xlim([-1, 1])
        # ax1.set_ylim([-1, 1])
        ax1.set_title(f"Location: {sta}")
        ofile = 'LS_2D_' + sta + '.png'
        ax1.legend(loc='upper right')
        print(f'Saving {ofile}')
        fig.savefig(ofile, dpi=150, transparent=False, bbox_inches='tight')


def plot_ls_vs_hed(dfls_alos, dfls_sen, dfgw, start_date, end_date, odir):
    # [.] Define some plotting parameters
    font_size = 14
    msize = 6
    lwidth = 0.75
    # [] Get the list of groundwater level observation wells
    logs = list(dfgw.columns)
    logs.remove('Date')

    for loc_name in logs:  # logs[0:1]:
        #print(f'loc_name: {loc_name}, size dfgw = {dfgw.shape}')
        fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(8, 3))

        # Plot 1 LOS displacement -------------------------------------------------
        #col_keep = ['Date', loc_name]
        #df = dfs[col_keep]
        #df['Date'] = pd.to_datetime(df['Date'])

        plt.grid(color='#e6e6e6', linestyle='-', linewidth=0.5, axis='both')

    #    df = df[['Date', loc_name]]
    #    df['Date'] = pd.to_datetime(df['Date'])
    #    df = df.set_index(df['Date'])
    #    df = df[[loc_name]]
    #    df.plot(ax=ax, markersize=msize, linewidth=0.5, style='o:')
    #    print(f'dfsize = {df.shape} ')
    #    plt.show()

        try:
            x = dfls_alos.Date
            y = dfls_alos[loc_name]
            #print(x, y)
            p1 = ax.plot(x, y, 'o', markersize=msize, markeredgecolor=None,
                         linewidth=lwidth, alpha=0.75, label='ALOS')
            #
            x2 = dfls_sen.Date
            #new_x = datetime.datestr2num(x)
            #new_x = datetime.fromisoformat(x).timestamp()
            y2 = dfls_sen[loc_name]
            p2 = ax.plot(x2, y2, 'o', markersize=msize, markeredgecolor=None,
                         linewidth=lwidth, alpha=0.75, label='SENTINEL-1')

            ax.set_ylim(-5, 10)
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

            # plot 3: gwlevels ---------------------------------------------------------
            ax2 = ax.twinx()
            print(f'logname:{loc_name} \n')
            dfgw_cur = dfgw[['Date', loc_name]]
            # print(df_alos)
            dfgw_cur = dfgw_cur.dropna(subset=['Date', loc_name])

            x3 = dfgw_cur.Date
            y3 = dfgw_cur[loc_name]
            y3_mean = round(y3.mean(), 0)
            print(y3_mean)

            p3 = ax2.plot(x3, y3, '--or', markersize=msize-3, markeredgecolor=None,
                          linewidth=1.25, alpha=0.5, label='GW Levels')  # linecolor='#D3D3D3',
        #    dfgw = dfgw[['Date', loc_name]]
        #    dfgw = dfgw.set_index(dfgw['Date'])
        #    dfgw = dfgw[[loc_name]]

        #    dfgw.plot(ax=ax, markersize=msize, linewidth=0.5, style='o')
        #    print(f'dfgw size = {dfgw.shape} ')
            #ax2.set_ylim(min(y2), max(y2))

            ax2.set_xlim(start_date, end_date)
            ax2.set_ylim(y3_mean-30, y3_mean+10)
            ax2.tick_params(axis='y', colors='red')
            ax2.set_ylabel(
                'Groundwater Level [m]', fontsize=font_size, color='r')

            ax.set_title(loc_name, fontsize=font_size+2)
            ax.set_xlabel('Time [years]', fontsize=font_size)
            ax.set_ylabel('LOS Displacement [cm]', fontsize=font_size)

            p = p1 + p2 + p3
            labs = [l.get_label() for l in p]
            ax.legend(p, labs)  # loc="upper right"

            ofile = odir + loc_name + '.png'
            #print(f'Saving map to ... {ofile[-60:]} \n')
            fig.savefig(ofile, dpi=150, transparent=False, bbox_inches='tight')
            # plt.show()

        except:
            print(f'WARNING: Something went wrong for well {loc_name}\n')


def subplot_ls_vs_hed(dfls_alos, dfls_sen, dfgw, start_date, end_date, wname, ofile):
    # [.] Define some plotting parameters
    font_size = 7
    msize = 1.5
    lwidth = 1.5
    # [] Get the list of groundwater level observation wells
    logs = list(dfgw.columns)
    logs.remove('Date')
    plt.rc('font', size=font_size)
    fig, axs = plt.subplots(nrows=4, ncols=2, figsize=(8, 10), sharey=True)
    # print(ax_all)

    for i, ax in enumerate(fig.axes):
        # print(ax)
        plt.grid(color='#e6e6e6', linestyle='-', linewidth=0.5, axis='both')
        loc_name = wname[i]
        
        # PLOT ALOS
        x = dfls_alos.Date
        y = dfls_alos[loc_name]
        p1 = ax.plot(x, y, '-o', color='#8da0cb', markersize=msize, markeredgecolor=None,
                     linewidth=lwidth, alpha=1, label='ALOS')
        # PLOT SENTINEL-1
        x2 = dfls_sen.Date
        y2 = dfls_sen[loc_name]
        p2 = ax.plot(x2, y2, '-o', color='#fc8d62', markersize=msize, markeredgecolor=None,
                     linewidth=lwidth, alpha=1, label='SENTINEL-1')

        ax.set_ylim(-5, 10)

        # plot 3: gwlevels ---------------------------------------------------------
        ax2 = ax.twinx()
        print(f'logname:{loc_name} \n')
        dfgw_cur = dfgw[['Date', loc_name]]
        # print(df_alos)
        dfgw_cur = dfgw_cur.dropna(subset=['Date', loc_name])

        x3 = dfgw_cur.Date
        y3 = dfgw_cur[loc_name]
        y3_mean = round(y3.mean(), 0)
        # print(y3_mean)
        p3 = ax2.plot(x3, y3, '-o', color='#66c2a5', markersize=msize,
                      markeredgecolor=None, linewidth=lwidth, alpha=1,
                      label='GW Levels')  # linecolor='#D3D3D3',

        ax2.set_xlim(start_date, end_date)
        ax2.set_ylim(y3_mean-30, y3_mean+10)
        ax2.tick_params(axis='y', colors='#66c2a5')

        if (i == 1 or i == 3 or i == 5 or i == 7):
            ax2.set_ylabel(
                'Groundwater Level [m]', fontsize=font_size, color='r')

        ax.set_title(loc_name, fontsize=font_size+1)
#        ax.set_xlabel('Time [years]', fontsize=font_size)

        if (i == 0 or i == 2 or i == 4 or i == 6):
            ax.set_ylabel('LOS Displacement [cm]', fontsize=font_size)

        p = p1 + p2 + p3
        labs = [l.get_label() for l in p]
        if i == 0:
            ax.legend(p, labs, fontsize=font_size-1)  # loc="upper right"

    fig.savefig(ofile, dpi=150, transparent=False, bbox_inches='tight')
    # plt.show()

# More background map
# https://kbkb-wx-python.blogspot.com/2016/04/python-basemap-background-image-from.html


'''
map_list = [
'ESRI_Imagery_World_2D',    # 0
'ESRI_StreetMap_World_2D',  # 1
'NatGeo_World_Map',         # 2
'NGS_Topo_US_2D',           # 3
#'Ocean_Basemap',            # 4
'USA_Topo_Maps',            # 5
'World_Imagery',            # 6
'World_Physical_Map',       # 7     Still blurry
'World_Shaded_Relief',      # 8
'World_Street_Map',         # 9
'World_Terrain_Base',       # 10
'World_Topo_Map'            # 11
]
'''
