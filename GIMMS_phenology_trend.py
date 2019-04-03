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
import MK_trend as MK



inpath = 'E:/GIMMS3g_v1_phen_result_20180717/average_5methods'


methods = ['dbl_1st','dbl_2rd','Gmax20','Gmax50','poly']

outpath = 'E:/GIMMS3g_v1_phen_result_20180717/MK_trend'


refer_tif_file_gimms3g= 'GIMMS_NH.tif'

[GeoT, Proj] = Geotiff_RW.GetGeoInfo(refer_tif_file_gimms3g)

################# calculate the MK trend during 1982~1998 ####################
start_yr = 1982
end_yr = 1998

for yr in range(start_yr, end_yr + 1):
    infile_SOS = '%s/GIMMS_SOS_%d_5methods_avg.tif' %(inpath,yr)
    data_SOS_md0, Ysize, Xsize = Geotiff_RW.ReadGeoTiff(infile_SOS)
    data_SOS_md0 = np.asarray(data_SOS_md0)
    #print(np.nanmin(data_SOS_md0))
    ind = data_SOS_md0 == -9999
    data_SOS_md0[ind] = np.nan
    data_SOS_md0 = np.reshape(data_SOS_md0,[1,Ysize*Xsize]).squeeze()
    
    infile_EOS = '%s/GIMMS_EOS_%d_5methods_avg.tif' %(inpath,yr)
    data_EOS_md0, Ysize, Xsize = Geotiff_RW.ReadGeoTiff(infile_EOS)
    data_EOS_md0 = np.asarray(data_EOS_md0)
    #print(np.nanmin(data_EOS_md0))
    ind = data_EOS_md0 == -9999
    data_EOS_md0[ind] = np.nan
    data_EOS_md0 = np.reshape(data_EOS_md0,[1,Ysize*Xsize]).squeeze()
    
    
    #print(np.nanmin(data_EOS_md0))
    
    if (yr == start_yr):
        all_data_SOS = data_SOS_md0
        all_data_EOS = data_EOS_md0
    else:
        all_data_SOS = np.vstack((all_data_SOS, data_SOS_md0))
        all_data_EOS = np.vstack((all_data_EOS, data_EOS_md0))

rows,cols =  np.shape(all_data_SOS)

SOS_slp = []
SOS_p = []
EOS_slp = []
EOS_p = []


for c in range(cols):
    print("%d in %d" %(c,cols))
    SOS_vector = np.asarray(all_data_SOS[:,c])
    SOS_years = np.arange(start_yr, end_yr + 1)
    
    ind = ~np.isnan(SOS_vector)
    SOS_vector_ok = SOS_vector[ind]
    SOS_years_ok = SOS_years[ind]
    
    if(len(SOS_vector_ok) > (end_yr-start_yr)*0.7):
        h_bf98_SOS, trend_bf98_SOS, intp_bf98_SOS, p_value_bf98_SOS, z_bf98_SOS = MK.mk_trend(SOS_vector_ok, SOS_years_ok, 0.05)
        SOS_slp.append(trend_bf98_SOS)
        SOS_p.append(p_value_bf98_SOS)
    else:
        SOS_slp.append(-9999)
        SOS_p.append(-9999)
    
    
    EOS_vector = np.asarray(all_data_EOS[:,c])
    EOS_years = np.arange(start_yr, end_yr + 1)
    
    ind = ~np.isnan(EOS_vector)
    EOS_vector_ok = EOS_vector[ind]
    EOS_years_ok = EOS_years[ind]
    if(len(SOS_vector_ok) > (end_yr-start_yr)*0.7):
        h_bf98_EOS, trend_bf98_EOS, intp_bf98_EOS, p_value_bf98_EOS, z_bf98_EOS = MK.mk_trend(EOS_vector_ok, EOS_years_ok, 0.05)
        EOS_slp.append(trend_bf98_EOS)
        EOS_p.append(p_value_bf98_EOS)
    else:
        EOS_slp.append(-9999)
        EOS_p.append(-9999)

    
SOS_slp = np.reshape(SOS_slp,[Ysize,Xsize])
SOS_p = np.reshape(SOS_p,[Ysize,Xsize])    

EOS_slp = np.reshape(EOS_slp,[Ysize,Xsize])
EOS_p = np.reshape(EOS_p,[Ysize,Xsize])    
NoData_value = -9999.0

outfile_SOS_slp = '%s/GIMMS_SOS_%d_%d_slp' %(outpath,start_yr,end_yr)
Geotiff_RW.CreateGeoTiff(outfile_SOS_slp, SOS_slp, Xsize, Ysize, GeoT, Proj, NoData_value)


outfile_SOS_p = '%s/GIMMS_SOS_%d_%d_p' %(outpath,start_yr,end_yr)
Geotiff_RW.CreateGeoTiff(outfile_SOS_p, SOS_p, Xsize, Ysize, GeoT, Proj, NoData_value)


outfile_EOS_slp = '%s/GIMMS_EOS_%d_%d_slp' %(outpath,start_yr,end_yr)
Geotiff_RW.CreateGeoTiff(outfile_EOS_slp, EOS_slp, Xsize, Ysize, GeoT, Proj, NoData_value)


outfile_EOS_p = '%s/GIMMS_EOS_%d_%d_p' %(outpath,start_yr,end_yr)
Geotiff_RW.CreateGeoTiff(outfile_EOS_p, EOS_p, Xsize, Ysize, GeoT, Proj, NoData_value)

######################################################################################

################# calculate the MK trend during 1998~2014 ####################
start_yr = 1998
end_yr = 2014

for yr in range(start_yr, end_yr + 1):
    infile_SOS = '%s/GIMMS_SOS_%d_5methods_avg.tif' %(inpath,yr)
    data_SOS_md0, Ysize, Xsize = Geotiff_RW.ReadGeoTiff(infile_SOS)
    data_SOS_md0 = np.asarray(data_SOS_md0)
    #print(np.nanmin(data_SOS_md0))
    ind = data_SOS_md0 == -9999
    data_SOS_md0[ind] = np.nan
    data_SOS_md0 = np.reshape(data_SOS_md0,[1,Ysize*Xsize]).squeeze()
    
    infile_EOS = '%s/GIMMS_EOS_%d_5methods_avg.tif' %(inpath,yr)
    data_EOS_md0, Ysize, Xsize = Geotiff_RW.ReadGeoTiff(infile_EOS)
    data_EOS_md0 = np.asarray(data_EOS_md0)
    #print(np.nanmin(data_EOS_md0))
    ind = data_EOS_md0 == -9999
    data_EOS_md0[ind] = np.nan
    data_EOS_md0 = np.reshape(data_EOS_md0,[1,Ysize*Xsize]).squeeze()
    
    
    #print(np.nanmin(data_EOS_md0))
    
    if (yr == start_yr):
        all_data_SOS = data_SOS_md0
        all_data_EOS = data_EOS_md0
    else:
        all_data_SOS = np.vstack((all_data_SOS, data_SOS_md0))
        all_data_EOS = np.vstack((all_data_EOS, data_EOS_md0))

rows,cols =  np.shape(all_data_SOS)

SOS_slp = []
SOS_p = []
EOS_slp = []
EOS_p = []


for c in range(cols):
    print("%d in %d" %(c,cols))
    SOS_vector = np.asarray(all_data_SOS[:,c])
    SOS_years = np.arange(start_yr, end_yr + 1)
    
    ind = ~np.isnan(SOS_vector)
    SOS_vector_ok = SOS_vector[ind]
    SOS_years_ok = SOS_years[ind]
    
    if(len(SOS_vector_ok) > (end_yr-start_yr)*0.7):
        h_bf98_SOS, trend_bf98_SOS, intp_bf98_SOS, p_value_bf98_SOS, z_bf98_SOS = MK.mk_trend(SOS_vector_ok, SOS_years_ok, 0.05)
        SOS_slp.append(trend_bf98_SOS)
        SOS_p.append(p_value_bf98_SOS)
    else:
        SOS_slp.append(-9999)
        SOS_p.append(-9999)
    
    
    EOS_vector = np.asarray(all_data_EOS[:,c])
    EOS_years = np.arange(start_yr, end_yr + 1)
    
    ind = ~np.isnan(EOS_vector)
    EOS_vector_ok = EOS_vector[ind]
    EOS_years_ok = EOS_years[ind]
    if(len(SOS_vector_ok) > (end_yr-start_yr)*0.7):
        h_bf98_EOS, trend_bf98_EOS, intp_bf98_EOS, p_value_bf98_EOS, z_bf98_EOS = MK.mk_trend(EOS_vector_ok, EOS_years_ok, 0.05)
        EOS_slp.append(trend_bf98_EOS)
        EOS_p.append(p_value_bf98_EOS)
    else:
        EOS_slp.append(-9999)
        EOS_p.append(-9999)

    
SOS_slp = np.reshape(SOS_slp,[Ysize,Xsize])
SOS_p = np.reshape(SOS_p,[Ysize,Xsize])    

EOS_slp = np.reshape(EOS_slp,[Ysize,Xsize])
EOS_p = np.reshape(EOS_p,[Ysize,Xsize])    
NoData_value = -9999.0

outfile_SOS_slp = '%s/GIMMS_SOS_%d_%d_slp' %(outpath,start_yr,end_yr)
Geotiff_RW.CreateGeoTiff(outfile_SOS_slp, SOS_slp, Xsize, Ysize, GeoT, Proj, NoData_value)


outfile_SOS_p = '%s/GIMMS_SOS_%d_%d_p' %(outpath,start_yr,end_yr)
Geotiff_RW.CreateGeoTiff(outfile_SOS_p, SOS_p, Xsize, Ysize, GeoT, Proj, NoData_value)


outfile_EOS_slp = '%s/GIMMS_EOS_%d_%d_slp' %(outpath,start_yr,end_yr)
Geotiff_RW.CreateGeoTiff(outfile_EOS_slp, EOS_slp, Xsize, Ysize, GeoT, Proj, NoData_value)


outfile_EOS_p = '%s/GIMMS_EOS_%d_%d_p' %(outpath,start_yr,end_yr)
Geotiff_RW.CreateGeoTiff(outfile_EOS_p, EOS_p, Xsize, Ysize, GeoT, Proj, NoData_value)

######################################################################################
    
'''    
    for md in methods:
        print yr, md
        
        infile = '%s/GIMMS_SOS_%d_%s.tif' %(inpath,yr,md)
        
        
        
        
        end_data = np.ones(4320*280)*(-9999)
        end_data = np.reshape(end_data,[280,4320])
        all_SOS = np.vstack((all_SOS,end_data))
        all_EOS = np.vstack((all_EOS,end_data))
                
        outfile_SOS = '%s/GIMMS_SOS_%d_%s' %(outpath,yr,md)
        outfile_EOS = '%s/GIMMS_EOS_%d_%s' %(outpath,yr,md)
        
        [Ysize, Xsize] = all_SOS.shape
        NoData_value = -9999.0
        Geotiff_RW.CreateGeoTiff(outfile_SOS, all_SOS, Xsize, Ysize, GeoT, Proj, NoData_value)
        
        Geotiff_RW.CreateGeoTiff(outfile_EOS, all_EOS, Xsize, Ysize, GeoT, Proj, NoData_value)
        
        all_SOS = np.asarray(all_SOS)*1.0
        ind = all_SOS == -9999
        all_SOS[ind] = np.nan
        SOS_avg_all.append(np.nanmean(all_SOS))
        
        all_EOS = np.asarray(all_EOS)*1.0
        ind = all_EOS == -9999
        all_EOS[ind] = np.nan
        EOS_avg_all.append(np.nanmean(all_EOS))

'''
