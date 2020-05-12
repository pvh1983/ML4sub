import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime as dt
from datetime import datetime
import os
import plotly.express as px


# cd c:\Users\hpham\Documents\P31 Maki\ML4sub\scripts\
"""
The main script of ML4sub
[0] Run resample_JK_water_level_dataset.py to process the data from JK. The output is
    gwlevel at each well (one file one well)

[1] Generate a DataFrame for groundwater levels [row: time; col: obswell]
    by running gen_gwlevel_dataframe.py

[2] Visualize the relationship between the gwlevels and subsidence velocity
    using plot_ls_ts.py
[3] Build geologic structures using process_well_logs.py
    - Map boreholes, lithology
    - Build 3-D lithologic models    
[4] Calculate subsidence trends using plot_ls_ts.py

[5] Compare InSAR-derived mean velocity vs. GPS data compare_with_gps.py


OTHER SETUP
[1] Groundwater level plots
# Three quantitative color:['#66c2a5','#fc8d62','#8da0cb'] # [GW, ALOS, SEN]

Ref
### Chooseing best colors http://colorbrewer2.org/#type=qualitative&scheme=Set2&n=3

"""


if __name__ == '__main__':
    print('coming soon ...')
