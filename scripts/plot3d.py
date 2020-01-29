import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from func4mapping import *

mpl.rcParams['legend.fontsize'] = 10

# Load data
ifile = '../output/dfmeta_added.csv'  # run process_well_logs to get this fle
df = pd.read_csv(ifile)

# Define the model domain
# x_min, x_max, y_min, y_max = [-116.215, -115.567, 35.861, 36.47]  # Full Pahrump
x_min, x_max, y_min, y_max = [-116.21, -115.85, 36.1, 36.47]  # Full Pahrump
domain = [x_min, x_max, y_min, y_max]
var2plot = ['th_all', 'th_sand', 'th_clay']  # th_all, th_sand, or th_clay
for var in var2plot:
    ofile = '../output/' + var + '.png'
    MapPlotPV(domain_coor=domain, showbg=True, show_wsb=False, df=df, var=var,
              ofile=ofile, vmin=0, vmax=1200, legend_name=var)


'''
fig = plt.figure()
ax = fig.gca(projection='3d')
theta = np.linspace(-4 * np.pi, 4 * np.pi, 100)
z = np.linspace(-2, 2, 100)
r = z**2 + 1
x = r * np.sin(theta)
y = r * np.cos(theta)
ax.plot(x, y, z, label='parametric curve', color='red')
ax.legend()
'''


# plt.show()
