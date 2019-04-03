This is Instruction for codes supporting the results in "No trends in spring and autumn phenology during the global warming hiatus period"

All the code was wrote in Python

environment reguirement:
the code was tested in Anaconda2-4.5, Python2.7, GDAL-2.1 package is also required for process geotiff format.


Code files:
Cal_phenology_from_NDVI.py: the main program to extact SOS and EOS from NDVI data;
phenology_estimate.py: this file include functions for different NDVI based phenology methods, and they are called in Cal_phenology_from_NDVI.py;
savitzky_golay.py: savitzky-golay model to smooth NDVI data to eliminate the noises in NDVI data.
Geotiff_read_write.py: functions to read and write geotiff format in Python.
estimate_phenology_date_from_daily_GPP.py: the main program to extract SOS and EOS from daily GPP file;
GPP_smooth_func.py: functions to smooth daily GPP, and these functions are called in estimate_phenology_date_from_daily_GPP.py.

Example:
A NDVI example was provided in the input folder(GIMMS_NDVI.csv) to test Cal_phenology_from_NDVI.py. The result will be put in output folder.
Daily GPP at US-UMB site was provided input folder to test the estimate_phenology_date_from_daily_GPP.py. The result will be put in output folder, and the plot of each year was also generated in output\figures
