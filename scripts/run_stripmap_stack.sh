#!/bin/bash
#$ -V
#$ -S /bin/bash
#$ -N hp_test
#$ -j n
#$ -o r_00.out
#$ -e r_00.err
#$ -cwd
#$ -pe FillUp 40
#$ -M Hai.Pham@dri.edu
#$ -m abe

#ulimit -s unlimited
#ulimit -l unlimited

export OMP_NUM_THREADS=6
source /home/hpham/.isce2
which python
whereis InSARFlowStack.py

#------------------------------------------------------------------------------
# This script is designed for processing ALOS data using stripmapStack in ISCE. 
#---------------------------------------------------------------------
# Created by Phong Le @VNU-HUS (8/29/2019)
# Modified by Hai Pham (01/28/2020)
#---------------------------------------------------------------------

#echo "PROCESSING ALOS InSAR USING STRIPMAPSTACK IN ISCE ......"
#echo "working directory = "$SLURM_SUBMIT_DIR
#cd $SLURM_SUBMIT_DIR

#-----------------------------------------------------
# 0. SETUP PARAMETERS
#    Select sensor, processing level, path, frame, 
#    and list of orbit
#-----------------------------------------------------
#config='./ALOS_parameters.cfg'
#source $config
#logbash='stack_logs.txt'
#touch $logbash

###SLCdir=SLC
###DEMdir=DEM

# mkdir SLC
# mkdir DEM

### cd $DEMdir
### dem.py -a stitch -b $minLat_int $maxLat_int $minLon_int $maxLon_int -r -c    
# dem.py -a stitch -b 35 37 -116 -114 -r -s 1 -c # LAS VEGAS
# rm demLat*.dem demLat*.dem.xml demLat*.dem.vrt

# wbd.py $minLat_int $maxLat_int $minLon_int $maxLon_int
# wbd.py 35 37 -116 -114
# fixImageXml.py -f -i demLat_*.dem.wgs84
# cd ..

# prepRawALOS.py -i ALOS_zip/ -o SLC -t '' --dual2single
### prepRawSensor.py -i ALOS_zip/ -o SLC # not in use
#[Extract zip files in zipdir]
 
#mpirun -n 4 InSARFlowStack.py -i run_unPackALOS


master=$(ls SLC | head -1)
#stackStripMap.py -s SLC -d DEM/demLat_*.dem.wgs84 -t 1800 -b 2800 -a 20 -r 8 -u snaphu -W interferogram -m $master -f 0.5
# [create run_files folder]

logfile='logs.txt'
cd run_files
chmod +x *

echo -e "Running run_1_master" | tee -a "$logfile"
./run_1_master

echo -e "Running run_2_focus_split" | tee -a "$logfile"
mpirun -n 6 InSARFlowStack.py -i run_2_focus_split

echo -e "Running run_3_geo2rdr_coarseResamp" | tee -a "$logfile"
mpirun -n 6 InSARFlowStack.py -i run_3_geo2rdr_coarseResamp

echo -e "Running run_4_refineSlaveTiming" | tee -a "$logfile"
mpirun -n 6 InSARFlowStack.py -i run_4_refineSlaveTiming

echo -e "Running run_5_invertMisreg" | tee -a "$logfile"
./run_5_invertMisreg

echo -e "Running run_6_fineResamp" | tee -a "$logfile"
mpirun -n 6 InSARFlowStack.py -i run_6_fineResamp

echo -e "Running run_7_grid_baseline" | tee -a "$logfile"
mpirun -n 6 InSARFlowStack.py -i run_7_grid_baseline

echo -e "Running run_8_igram" | tee -a "$logfile"
mpirun -n 6 InSARFlowStack.py -i run_8_igram


cd ..

### Run later. 
#slavedir=$(ls ./coregSLC/Coarse/ | head -1)
#cp -r coregSLC/Coarse/$slavedir/masterShelve .
#./run_multilook_geometry.sh 20 8 # source ~/.isce2
#prep_isce.py -i ./Igrams -m ./masterShelve/data.dat -b ./baselines -g ./geom_master
# Notes: source ~/.mintpy then module load isce and module load basic

#
# cd mintpy
# smallbaselineApp.py pv_alos.txt
# DONE ALL
# source ~/.isce and load only module load isce/202001 (no basic)


# =========================
# FINAL NOTES
# if something went wrong with numpy, try to swicht the module_loading_order (mintpy->basic->isce)

# More References
#https://github.com/insarlab/MintPy/blob/a6387521e47466c3b8b6bc73c0d99c280dd4b417/sh/run_stripmap_stack.sh


#        info.py                    #check HDF5 file structure and metadata
#        view.py                    #2D map view
#        tsview.py                  #1D point time-series (interactive)
#        transect.py                #1D profile (interactive)
#        plot_coherence_matrix.py   #plot coherence matrix for one pixel (interactive)
#        plot_network.py            #plot network configuration of the dataset
#        plot_transection.py        #plot 1D profile along a line of a 2D matrix (interactive)
#        save_kmz.py                #generate Google Earth KMZ file in raster image
#        save_kmz_timeseries.py     #generate Goodle Earth KMZ file in points for time-series (interactive)

# save_kmz.py geo/geo_velocity.h5 -o mean_los_vel -u cm -v -1 1 -c bwr