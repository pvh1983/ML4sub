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
