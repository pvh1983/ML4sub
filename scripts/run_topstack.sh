#!/bin/bash
#$ -V
#$ -S /bin/bash
#$ -N hp_test
#$ -j n
#$ -o r06.out
#$ -e r06.err
#$ -cwd
#$ -pe FillUp 40
#$ -M Hai.Pham@dri.edu
#$ -m abe

#ulimit -s unlimited
#ulimit -l unlimited

export OMP_NUM_THREADS=8
source /home/hpham/.isce2
which python
whereis InSARFlowStack.py

#[2] Download DEM and fix DEM (SRTM30m)
#mkdir DEM
#dem.py -a stitch -b 35 38 -117 -113 -r -s 1 -c
#rm demLat*.dem demLat*.dem.xml demLat*.dem.vrt
#(use source ~/.isce) conda env
### wbd.py 35 37 -117 -115
# fixImageXml.py -f -i demLat_*.dem.wgs84

### Run this to get the run_files folder
#stackSentinel.py -s ../SLCs/ -d ../DEM/demLat_N35_N38_Lon_W117_W113.dem.wgs84 -b '35.746 36.3367 -116.1571  -114.9307' -a ../AUXILIARY/ -o ../POEORB/ -c 2

###POLYGON((-116.1571 35.746,-114.9307 35.746,-114.9307 36.3367,-116.1571 36.3367,-116.1571 35.746))
### Using this box, got 117 images

logfile='filelogs.txt'

cd run_files
chmod +x run_*
echo -e $(date '+%d/%m/%Y %H:%M:%S') | tee -a "$logfile"

#echo -e "Running run_1_unpack_slc_topo_master" | tee -a "$logfile"
#mpirun -np 10 InSARFlowStack.py -i run_1_unpack_slc_topo_master

#echo -e "Running run_2_average_baseline" | tee -a "$logfile"
#mpirun -np 10 InSARFlowStack.py -i run_2_average_baseline

#echo -e "Running run_3_extract_burst_overlaps" | tee -a "$logfile"
#./run_3_extract_burst_overlaps

#echo -e "Running run_4_overlap_geo2rdr_resample" | tee -a "$logfile"
#mpirun -np 10 InSARFlowStack.py -i run_4_overlap_geo2rdr_resample

#echo -e "Running run_5_pairs_misreg" | tee -a "$logfile"
#mpirun -np 10 InSARFlowStack.py -i run_5_pairs_misreg

echo -e "Running run_6_timeseries_misreg" | tee -a "$logfile"
mpirun -np 10 InSARFlowStack.py -i run_6_timeseries_misreg

#echo -e "Running run_7_geo2rdr_resample" | tee -a "$logfile"
#mpirun -np 10 InSARFlowStack.py -i run_7_geo2rdr_resample

#echo -e "Running run_8_extract_stack_valid_region" | tee -a "$logfile"
#./run_8_extract_stack_valid_region

#echo -e "Running run_9_merge_burst_igram" | tee -a "$logfile"
#mpirun -np 10 InSARFlowStack.py -i run_9_merge_burst_igram

#echo -e "Running run_10_filter_coherence" | tee -a "$logfile"
#mpirun -np 10 InSARFlowStack.py -i run_10_filter_coherence

#echo -e "Running run_11_unwrap" | tee -a "$logfile"
#mpirun -np 10 InSARFlowStack.py -i run_11_unwrap

#echo -e "Running run_12_merge_master_slave_slc" | tee -a "$logfile"
#mpirun -np 10 InSARFlowStack.py -i run_12_merge_master_slave_slc

echo -e $(date '+%d/%m/%Y %H:%M:%S') | tee -a "$logfile"
cd ..
