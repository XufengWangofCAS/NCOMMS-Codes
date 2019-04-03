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



inpath = 'E:/GIMMS3g_v1_phen_result_20180717/merge_phen'

#start_rows = [0,200,250,300,350,400,450,500,550,600,650,700,750]
#end_rows = [199,249,299,349,399,449,499,549,599,649,699,749,799]
methods = ['dbl_1st','dbl_2rd','Gmax20','Gmax50','poly']

outpath = 'E:/GIMMS3g_v1_phen_result_20180717'

outpath_tif_30_90 = 'E:/GIMMS3g_v1_phen_result_20180717/merge_phen_30_90'

refer_tif_file_gimms3g= 'GIMMS_NH.tif'

[GeoT, Proj] = Geotiff_RW.GetGeoInfo(refer_tif_file_gimms3g)

SOS_avg_all = []
EOS_avg_all = []


SOS_avg_all_30_90 = []
EOS_avg_all_30_90 = []
SOS_avg_all_30_60 = []
EOS_avg_all_30_60 = []
SOS_avg_all_60_90 = []
EOS_avg_all_60_90 = []
    
for md in methods:
    SOS_flag = np.zeros(1080*4320)
    SOS_flag = np.asarray(np.reshape(SOS_flag,[1080,4320]))
    EOS_flag = np.zeros(1080*4320)
    EOS_flag = np.asarray(np.reshape(EOS_flag,[1080,4320]))
    
    #loop to get common area
    for yr in range(1982,2015):
        print yr, md
        infile_SOS = '%s/GIMMS_SOS_%d_%s.tif' %(inpath,yr,md)
        infile_EOS = '%s/GIMMS_EOS_%d_%s.tif' %(inpath,yr,md)
        SOS_data, Ysize, Xsize = Geotiff_RW.ReadGeoTiff(infile_SOS)
        EOS_data, Ysize, Xsize = Geotiff_RW.ReadGeoTiff(infile_EOS)
        
        SOS_data = np.asarray(SOS_data)*1.0
        EOS_data = np.asarray(EOS_data)*1.0        
        
        nodata = np.min(SOS_data)
        print nodata
        '''
        nodata_ind = SOS_data==nodata
        SOS_data[nodata_ind] = np.nan
        '''
        
        nodata = np.min(EOS_data)
        print nodata
        '''
        nodata_ind = EOS_data==nodata
        EOS_data[nodata_ind] = np.nan
        '''
        SOS_ind = (SOS_data>0) & (SOS_data < 200)
        EOS_ind = (EOS_data>200) & (EOS_data < 365)
        
        SOS_flag[SOS_ind] = SOS_flag[SOS_ind] + 1
        EOS_flag[EOS_ind] = EOS_flag[EOS_ind] + 1
        
    SOS_ind = SOS_flag != 33 #some year data missing in the area
    EOS_ind = EOS_flag != 33 #some year data missing in the area 
    
    for yr in range(1982,2015):
        infile_SOS = '%s/GIMMS_SOS_%d_%s.tif' %(inpath,yr,md)
        infile_EOS = '%s/GIMMS_EOS_%d_%s.tif' %(inpath,yr,md)
        SOS_data, Ysize, Xsize = Geotiff_RW.ReadGeoTiff(infile_SOS)
        EOS_data, Ysize, Xsize = Geotiff_RW.ReadGeoTiff(infile_EOS)
        
        SOS_data = np.asarray(SOS_data)*1.0
        EOS_data = np.asarray(EOS_data)*1.0  
        
        SOS_data[SOS_ind] = np.nan
        EOS_data[EOS_ind] = np.nan
        
        #average between 60 and 90 degree
        SOS_avg_all_60_90.append(np.nanmean(SOS_data[0:360,:]))
        EOS_avg_all_60_90.append(np.nanmean(EOS_data[0:360,:]))
        
        #average between 30 and 60 degree
        SOS_avg_all_30_60.append(np.nanmean(SOS_data[360:720,:]))
        EOS_avg_all_30_60.append(np.nanmean(EOS_data[360:720,:]))
        
        #average between 30 and 90 degree
        SOS_avg_all_30_90.append(np.nanmean(SOS_data[0:720,:]))
        EOS_avg_all_30_90.append(np.nanmean(EOS_data[0:720,:]))
        
        ## save lat 30-90 to geotif files
        out_file_SOS_30_90 = '%s/GIMMS3g_v1_SOS_%d_%s_30_90_spatial_uniform' %(outpath_tif_30_90,yr,md)
        out_file_EOS_30_90 = '%s/GIMMS3g_v1_EOS_%d_%s_30_90_spatial_uniform' %(outpath_tif_30_90,yr,md)
        SOS_data[720:1080,:] = np.nan
        EOS_data[720:1080,:] = np.nan
        
        SOS_data[np.isnan(SOS_data)] = -9999
        EOS_data[np.isnan(EOS_data)] = -9999
        NoData_value = -9999
        Geotiff_RW.CreateGeoTiff(out_file_SOS_30_90, SOS_data, Xsize, Ysize, GeoT, Proj, NoData_value)
        
        Geotiff_RW.CreateGeoTiff(out_file_EOS_30_90, EOS_data, Xsize, Ysize, GeoT, Proj, NoData_value)
               
SOS_avg_all_60_90 = np.reshape(SOS_avg_all_60_90,[len(methods),33])
EOS_avg_all_60_90 = np.reshape(EOS_avg_all_60_90,[len(methods),33])
SOS_avg_all_60_90 = np.transpose(SOS_avg_all_60_90)
EOS_avg_all_60_90 = np.transpose(EOS_avg_all_60_90)
out_df = pd.DataFrame(data = SOS_avg_all_60_90,columns = methods,index=range(1982,2015))
out_df.to_csv('E:/GIMMS3g_v1_phen_result_20180717/NH60_90_SOS_spatial_uniform.csv',index_label = 'Year')
out_df = pd.DataFrame(data = EOS_avg_all_60_90,columns = methods,index=range(1982,2015))
out_df.to_csv('E:/GIMMS3g_v1_phen_result_20180717/NH60_90_EOS_spatial_uniform.csv',index_label = 'Year')

SOS_avg_all_30_60 = np.reshape(SOS_avg_all_30_60,[len(methods),33])
EOS_avg_all_30_60 = np.reshape(EOS_avg_all_30_60,[len(methods),33])
SOS_avg_all_30_60 = np.transpose(SOS_avg_all_30_60)
EOS_avg_all_30_60 = np.transpose(EOS_avg_all_30_60)
out_df = pd.DataFrame(data = SOS_avg_all_30_60,columns = methods,index=range(1982,2015))
out_df.to_csv('E:/GIMMS3g_v1_phen_result_20180717/NH30_60_SOS_spatial_uniform.csv',index_label = 'Year')
out_df = pd.DataFrame(data = EOS_avg_all_30_60,columns = methods,index=range(1982,2015))
out_df.to_csv('E:/GIMMS3g_v1_phen_result_20180717/NH30_60_EOS_spatial_uniform.csv',index_label = 'Year')

SOS_avg_all_30_90 = np.reshape(SOS_avg_all_30_90,[len(methods),33])
EOS_avg_all_30_90 = np.reshape(EOS_avg_all_30_90,[len(methods),33])
SOS_avg_all_30_90 = np.transpose(SOS_avg_all_30_90)
EOS_avg_all_30_90 = np.transpose(EOS_avg_all_30_90)
out_df = pd.DataFrame(data = SOS_avg_all_30_90,columns = methods,index=range(1982,2015))
out_df.to_csv('E:/GIMMS3g_v1_phen_result_20180717/NH30_90_SOS_spatial_uniform.csv',index_label = 'Year')
out_df = pd.DataFrame(data = EOS_avg_all_30_60,columns = methods,index=range(1982,2015))
out_df.to_csv('E:/GIMMS3g_v1_phen_result_20180717/NH30_90_EOS_spatial_uniform.csv',index_label = 'Year')
