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


#########  set directory for GIMMS3g subregion txt format phenology  ###########
inpath = 'E:/phen_result_20180717'

start_rows = [0,200,250,300,350,400,450,500,550,600,650,700,750]
end_rows = [199,249,299,349,399,449,499,549,599,649,699,749,799]
methods = ['dbl_1st','dbl_2rd','Gmax20','Gmax50','poly']

#########  set directory for merged north Hemisphere geotiff phenology  ###########
outpath = 'E:/phen_result_20180717/merge_phen'


refer_tif_file_gimms3g= 'GIMMS_NH.tif'

[GeoT, Proj] = Geotiff_RW.GetGeoInfo(refer_tif_file_gimms3g)

SOS_avg_all = []
EOS_avg_all = []

for yr in range(1982,2016):
    for md in methods:
        print yr, md
        for i in range(len(start_rows)):
            infile_SOS = '%s/r%03d_%d/GIMMS_%d_NDVI_SOS_%s_sr_%d.txt' %(inpath,start_rows[i],end_rows[i],yr,md,start_rows[i])
            infile_EOS = '%s/r%03d_%d/GIMMS_%d_NDVI_EOS_%s_sr_%d.txt' %(inpath,start_rows[i],end_rows[i],yr,md,start_rows[i])
            SOS_data = np.genfromtxt(infile_SOS,delimiter = ',')
            EOS_data = np.genfromtxt(infile_EOS,delimiter = ',')
            if (i==0):
                all_SOS = SOS_data
                all_EOS = EOS_data
            else:
                all_SOS = np.vstack((all_SOS,SOS_data))
                all_EOS = np.vstack((all_EOS,EOS_data))
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

            
SOS_avg_all = np.reshape(SOS_avg_all,[34,len(methods)])
EOS_avg_all = np.reshape(EOS_avg_all,[34,len(methods)])
out_df = pd.DataFrame(data = SOS_avg_all,columns = methods,index=range(1982,2016))
out_df.to_csv('E:/phen_result_20180717/NH30_SOS.csv',index_label = 'Year')
out_df = pd.DataFrame(data = EOS_avg_all,columns = methods,index=range(1982,2016))
out_df.to_csv('E:/phen_result_20180717/NH30_EOS.csv',index_label = 'Year')
