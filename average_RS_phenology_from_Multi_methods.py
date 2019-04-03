#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Jul  7 13:21:25 2018

@author: wangxufeng
"""


import matplotlib.pyplot as plt
import numpy as np
from glob import glob
import os
import pandas as pd
import Geotiff_read_write as Geotiff_RW


###################### set path for RS phenology from 5 mehtods ##############
inpath = 'E:/GIMMS3g_v1_phen_result_20180717/merge_phen_30_90_spatial_extent_uniform'

methods = ['dbl_1st','dbl_2rd','Gmax20','Gmax50','poly']

###################### set path for output ###################################
outpath = 'E:/GIMMS3g_v1_phen_result_20180717/average_5methods_spatial_extent_uniform'


#### set geotiff file with specified georeference to output ##################
refer_tif_file_gimms3g= 'GIMMS_NH.tif'

[GeoT, Proj] = Geotiff_RW.GetGeoInfo(refer_tif_file_gimms3g)

SOS_avg_all = []
EOS_avg_all = []

for yr in range(1982,2016):
    
    for md in methods:
        infile = '%s/GIMMS3g_v1_SOS_%d_%s_30_90_spatial_uniform.tif' %(inpath,yr,md)
        data_SOS_md0, Ysize, Xsize = Geotiff_RW.ReadGeoTiff(infile)
        data_SOS_md0 = np.asarray(data_SOS_md0)
        ind = data_SOS_md0 == -9999
        data_SOS_md0[ind] = np.nan
        data_SOS_md0 = np.reshape(data_SOS_md0,[1,Ysize*Xsize]).squeeze()
        
        infile = '%s/GIMMS3g_v1_EOS_%d_%s_30_90_spatial_uniform.tif' %(inpath,yr,md)
        data_EOS_md0, Ysize, Xsize = Geotiff_RW.ReadGeoTiff(infile)
        data_EOS_md0 = np.asarray(data_EOS_md0)
        ind = data_EOS_md0 == -9999
        data_EOS_md0[ind] = np.nan
        data_EOS_md0 = np.reshape(data_EOS_md0,[1,Ysize*Xsize]).squeeze()
        
        if (md == methods[0]):
            all_data_SOS = data_SOS_md0
            all_data_EOS = data_EOS_md0
        else:
            all_data_SOS = np.vstack((all_data_SOS, data_SOS_md0))
            all_data_EOS = np.vstack((all_data_EOS, data_EOS_md0))
            
    
    all_data_SOS_mean = np.nanmean(all_data_SOS,axis=0)
    all_data_SOS_mean = np.reshape(all_data_SOS_mean,[Ysize, Xsize])
    
    all_data_EOS_mean = np.nanmean(all_data_EOS,axis=0)
    all_data_EOS_mean = np.reshape(all_data_EOS_mean,[Ysize, Xsize])
    
    
    
    outfile_SOS = '%s/GIMMS3g_v1_SOS_%d_5methods_avg_30_90_spatial_uniform' %(outpath,yr)
    outfile_EOS = '%s/GIMMS3g_v1_EOS_%d_5methods_avg_30_90_spatial_uniform' %(outpath,yr)
    
    all_data_SOS_mean[np.isnan(all_data_SOS_mean)] = -9999.0
    NoData_value = -9999.0
    Geotiff_RW.CreateGeoTiff(outfile_SOS, all_data_SOS_mean, Xsize, Ysize, GeoT, Proj, NoData_value)
    
    all_data_EOS_mean[np.isnan(all_data_EOS_mean)] = -9999.0
    NoData_value = -9999.0
    Geotiff_RW.CreateGeoTiff(outfile_EOS, all_data_EOS_mean, Xsize, Ysize, GeoT, Proj, NoData_value)


