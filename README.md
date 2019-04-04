Code run environment: Anaconda for Python 2.7. NumPy, SciPy, pandas, matplotlib, netCDF4 and GDAL packages should be installed. 

###########################################################################

Part 1: Instruction to run the code to process GIMMS3g NDVI.

Step 1: 
Data format conversion.
GIMMS_binary2geotiff.py: run this code to convert GIMMS3g V0 binary data to GeoTIFF format. The user needs to specify the input and output directory in the code.

Step 2:
Estimate_phenology_from_GIMMS3g_V0_r000_1080.py:  python code to estimate phenology from step1 converted GIMMS3g V0 GeoTIFF files specified row range.
Estimate_phenology_from_GIMMS3g_V1_r000_1080.py:  python code to estimate phenology from GIMMS3g V1 netcdf files for specified row range.

The user should specify the input/output path, the start row and end row number in the code. The output is in text format. 
The user can parallelly calculate at several regions by setting the start and end row number in the codes.

Step 3:
Run GIMMS3g_phen_merge.py to merge the sub-regions phenology outputted from step2 to the whole northern hemisphere and saved as GeoTIFF. 
The user needs to specify the input/output path in the code file.

Step 4:
Run GIMMS3g_phenology_result_spatial_extent_uniform.py code to make the spatial extent consistent during the period for each method.
The user needs to specify the input/output path in the code file. The input is output from step 3.

Step 5:
Run GIMMS3g_phen_sub_statistic.py to get northern hemisphere spatial average phenology from the output of step 4. 

Step 6:
Run average_RS_phenology_from_Multi_methods.py to get average phenology from different methods in each year. The user needs to specify the input/output path in the code file. The input is output from step 4.

Step 7:
Run GIMMS_phenology_trend.py code to calculate the MK trend in the northern hemisphere. The user needs to specify the input/output path in the code file. The input is output from step 6.



###########################################################################

Part 2: Instruction to run the code to process FLUXNET2015 dataset.

Step 1:
Run estimate_phenology_date_from_daily_GPP.py to estimate SOS and EOS at each site.

Step 2:
Run get_seasonal_meteo_&_carbon_flux20171027.py to get seasonal meteorological data, carbon flux data and quality flag.

Step 3:
Run Cal_Trends_R2_phen_vs_envir_and_var_trend_for_seasons.py to calculate phenology trends, meteorological variables trends, carbon fluxes trends, correlation between phenology and meteorological variables (or carbon fluxes).


###########################################################################

Part 3: Codes to process the CRUTEM data
Temperature_CRUTEM3_Seasonal.py: This code is used to calculate the seasonal average temperature from CRUTEM3 (5 degree resolution) in the northern hemisphere (lat > 30degree). User need to specify the input/output directory in the codes.

Temperature_CRUTEM4_Seasonal.py: This code is used to calculate the seasonal average temperature from CRUTEM4 (5-degree resolution) in the northern hemisphere (lat > 30degree). The user needs to specify the input/output directory in the codes.

Temperature_Berkely_Earth_seasonal_data.py: This code is used to calculate the seasonal average temperature from Berkely Earth temperature dataset in the northern hemisphere (lat > 30degree).

Temperature_GISTEMP_seasonal_data.py: This code is used to calculate the seasonal average temperature from NASA GIS temperature dataset in the northern hemisphere (lat > 30degree).

Temperature_NOAA_seasonal_data.py: This code is used to calculate the seasonal average temperature from NOAA GIS temperature dataset in the northern hemisphere (lat > 30degree).

Temperature_CRUTEM4_seasonal_spatial_05deg_grid.py: This code is used to convert the high resolution (0.5 degree) CRUTEM4 NetCDF files to seasonal GeoTIFF files. The user needs to specify the input/output directory in the codes.

Temperature_CRUTEM4_05deg_grid_trend_spatial_pattern.py: This code is used to calculate the spring (or autumn) temperature trend for each grid. The user needs to specify the input/output directory in the codes.

###########################################################################

Part 4: Results plotting codes, here we only provide the codes for figures in the Main manuscript
Fig1_GIMMS_SOS_EOS_trend_version2.py: Codes used to plot Figure 1 in the manuscript.
Fig2_FLX_phen_spaghetti.py: Codes used to plot Figure 2 in the manuscript.
Fig3_envir_control_SOS_EOS_boxplot.py: Codes used to plot Figure 3 in the manuscript.
Fig4_Temp_spr_aut.py: Codes used to plot Figure 4 in the manuscript.
Fig5_carbon_flux_trend_result_from_phenology_trend.py: Codes used to plot Figure 5 in the manuscript.

FigS3_Get_GPP_threshold_for_phen_extract.py: Codes used to plot Figure S3 in the Support Information.

FigS6_warming_hiatus_sensitivity.py: Codes used to plot Figure S6 in the Support Information.

FigS7_Plot_phen_avg_std_20190401_latitude_sort.py: Codes used to plot Figure S7 in the Support Information.

FigS8_Plot_trends_as_bar_plot_NT_latitude_sort_unsignificant.py: Codes used to plot Figure S8 in the Support Information.

FigS10_FLX_sites_GIMMS_SOS_EOS_trend.py: Codes used to plot Figure S10 in the Support Information.

FigS11_S12_Plot_R2_for_phen_&meteo_season_latitude_sorted_no_display_nosig.py: Codes used to plot Figure S11 and S12 in the Support Information.

FigS13_plot_partial_correlation_boxplot.py: Codes used to plot Figure S13 in the Support Information.

FigS17_plot_correlation_of_2groups.py: Codes used to plot Figure S17 in the Support Information.

FigS18_S19_Plot_R2_for_phen_&carbon_flux_latitude_sorted_display_sig.py: Codes used to plot Figure S18 and S19 in the Support Information.

###########################################################################

Part5: other codes:
phenology_estimate.py: this file include functions for different NDVI based phenology methods, and they are called in Cal_phenology_from_NDVI.py;

savitzky_golay.py: Savitsky-Golay model to smooth NDVI data to eliminate the noises in NDVI data.

Geotiff_read_write.py: functions to read and write GeoTIFF format in Python.

GPP_smooth_func.py: functions to smooth daily GPP, and these functions are called in estimate_phenology_date_from_daily_GPP.py.

MK_trend.py: function to perform Mann-Kendall trend analysis.

perform_start_end_date_sensitivity.py: code to perform result sensitivity to start and end date of warming hiatus.


###########################################################################

Any problems in installation of the codes, please contact Xufeng Wang(wangxufeng@lzb.ac.cn).

