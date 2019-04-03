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


##############  set GIMMS3g phenology directory ###############################
inpath = 'E:/phen_result_20180717/merge_phen'


methods = ['dbl_1st','dbl_2rd','Gmax20','Gmax50','poly']

##############  set output directory ###############################
outpath = 'E:/phen_result_20180717'



SOS_avg_all = []
EOS_avg_all = []


SOS_avg_all_30_90 = []
EOS_avg_all_30_90 = []
SOS_avg_all_30_60 = []
EOS_avg_all_30_60 = []
SOS_avg_all_60_90 = []
EOS_avg_all_60_90 = []

for yr in range(1982,2016):
    for md in methods:
        print yr, md
        infile_SOS = '%s/GIMMS_SOS_%d_%s.tif' %(inpath,yr,md)
        infile_EOS = '%s/GIMMS_EOS_%d_%s.tif' %(inpath,yr,md)
        SOS_data, Ysize, Xsize = Geotiff_RW.ReadGeoTiff(infile_SOS)
        EOS_data, Ysize, Xsize = Geotiff_RW.ReadGeoTiff(infile_EOS)
        
        SOS_data = np.asarray(SOS_data)*1.0
        EOS_data = np.asarray(EOS_data)*1.0
        
        nodata = np.min(SOS_data)
        nodata_ind = SOS_data==nodata
        SOS_data[nodata_ind] = np.nan
        print nodata
        
        nodata = np.min(EOS_data)
        nodata_ind = EOS_data==nodata
        EOS_data[nodata_ind] = np.nan
        print nodata
        
        '''
        #average between 60 and 90 degree
        SOS_avg_all_60_90.append(np.nanmean(SOS_data[0:360,:]))
        EOS_avg_all_60_90.append(np.nanmean(EOS_data[0:360,:]))
        
        #average between 30 and 60 degree
        SOS_avg_all_30_60.append(np.nanmean(SOS_data[360:720,:]))
        EOS_avg_all_30_60.append(np.nanmean(EOS_data[360:720,:]))
        '''
        
        #average between 30 and 90 degree
        SOS_avg_all_30_90.append(np.nanmean(SOS_data[0:720,:]))
        EOS_avg_all_30_90.append(np.nanmean(EOS_data[0:720,:]))
        

'''            
SOS_avg_all_60_90 = np.reshape(SOS_avg_all_60_90,[34,len(methods)])
EOS_avg_all_60_90 = np.reshape(EOS_avg_all_60_90,[34,len(methods)])
out_df = pd.DataFrame(data = SOS_avg_all_60_90,columns = methods,index=range(1982,2016))
out_df.to_csv('E:/phen_result_20180717/NH60_90_SOS.csv',index_label = 'Year')
out_df = pd.DataFrame(data = EOS_avg_all_60_90,columns = methods,index=range(1982,2016))
out_df.to_csv('E:/phen_result_20180717/NH60_90_EOS.csv',index_label = 'Year')

SOS_avg_all_30_60 = np.reshape(SOS_avg_all_30_60,[34,len(methods)])
EOS_avg_all_30_60 = np.reshape(EOS_avg_all_30_60,[34,len(methods)])
out_df = pd.DataFrame(data = SOS_avg_all_30_60,columns = methods,index=range(1982,2016))
out_df.to_csv('E:/phen_result_20180717/NH30_60_SOS.csv',index_label = 'Year')
out_df = pd.DataFrame(data = EOS_avg_all_30_60,columns = methods,index=range(1982,2016))
out_df.to_csv('E:/phen_result_20180717/NH30_60_EOS.csv',index_label = 'Year')
'''

SOS_avg_all_30_90 = np.reshape(SOS_avg_all_30_90,[34,len(methods)])
EOS_avg_all_30_90 = np.reshape(EOS_avg_all_30_90,[34,len(methods)])
out_df = pd.DataFrame(data = SOS_avg_all_30_90,columns = methods,index=range(1982,2016))
out_df.to_csv('E:/phen_result_20180717/NH30_90_SOS.csv',index_label = 'Year')
out_df = pd.DataFrame(data = EOS_avg_all_30_60,columns = methods,index=range(1982,2016))
out_df.to_csv('E:/phen_result_20180717/NH30_90_EOS.csv',index_label = 'Year')
