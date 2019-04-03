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



inpath = 'D:/3.UNH_visiting/Phenology_from_fluxnet/Paper Writing/global_warming_hiatus/CRUTEM.4/CRUTEM4.02_grid0.5deg/seasonal_average_tifs'
outpath = 'D:/3.UNH_visiting/Phenology_from_fluxnet/Paper Writing/global_warming_hiatus/CRUTEM.4/CRUTEM4.02_grid0.5deg/CRUTEM4_05deg_spatial_MK_trend'


refer_tif_file_CRUTEM4 = "tmp_geo_reference.tif"
[GeoT, Proj] = Geotiff_RW.GetGeoInfo(refer_tif_file_CRUTEM4)

################# calculate the MK trend during 1982~1998 ####################
start_yr = 1982
end_yr = 1998

for yr in range(start_yr, end_yr + 1):
    infile_temp_spr = '%s/CRUTEM4v_05deg_spr_%d.tif' %(inpath,yr)
    data_temp_spr, Ysize, Xsize = Geotiff_RW.ReadGeoTiff(infile_temp_spr)
    data_temp_spr = np.asarray(data_temp_spr)
    #print(np.nanmin(data_temp_spr))
    ind = data_temp_spr == -9999.0
    data_temp_spr[ind] = np.nan
    data_temp_spr = np.reshape(data_temp_spr,[1,Ysize*Xsize]).squeeze()
    
    infile_temp_aut = '%s/CRUTEM4v_05deg_aut_%d.tif' %(inpath,yr)
    data_temp_aut, Ysize, Xsize = Geotiff_RW.ReadGeoTiff(infile_temp_aut)
    data_temp_aut = np.asarray(data_temp_aut)
    #print(np.nanmin(data_temp_aut))
    ind = data_temp_aut == -9999.0
    data_temp_aut[ind] = np.nan
    data_temp_aut = np.reshape(data_temp_aut,[1,Ysize*Xsize]).squeeze()
    
    infile_temp_yr = '%s/CRUTEM4v_05deg_year_%d.tif' %(inpath,yr)
    data_temp_yr, Ysize, Xsize = Geotiff_RW.ReadGeoTiff(infile_temp_yr)
    data_temp_yr = np.asarray(data_temp_yr)
    #print(np.nanmin(data_temp_yr))
    ind = data_temp_yr == -9999.0
    data_temp_yr[ind] = np.nan
    data_temp_yr = np.reshape(data_temp_yr,[1,Ysize*Xsize]).squeeze()
    
    
    
    #print(np.nanmin(data_EOS_md0))
    
    if (yr == start_yr):
        all_data_temp_spr = data_temp_spr
        all_data_temp_aut = data_temp_aut
        all_data_temp_yr = data_temp_yr
    else:
        all_data_temp_spr = np.vstack((all_data_temp_spr, data_temp_spr))
        all_data_temp_aut = np.vstack((all_data_temp_aut, data_temp_aut))
        all_data_temp_yr = np.vstack((all_data_temp_yr, data_temp_yr))
        

rows,cols =  np.shape(all_data_temp_spr)

temp_spr_slp = []
temp_spr_p = []
temp_aut_slp = []
temp_aut_p = []
temp_yr_slp = []
temp_yr_p = []


for c in range(cols):
    print("%d in %d" %(c,cols))
    temp_spr_vector = np.asarray(all_data_temp_spr[:,c])
    temp_spr_years = np.arange(start_yr, end_yr + 1)
    
    ind = ~np.isnan(temp_spr_vector)
    temp_spr_vector_ok = temp_spr_vector[ind]
    temp_spr_years_ok = temp_spr_years[ind]
    
    if(len(temp_spr_vector_ok) > (end_yr-start_yr)*0.7):
        h_bf98_temp_spr, trend_bf98_temp_spr, intp_bf98_temp_spr, p_value_bf98_temp_spr, z_bf98_temp_spr = MK.mk_trend(temp_spr_vector_ok, temp_spr_years_ok, 0.05)
        temp_spr_slp.append(trend_bf98_temp_spr)
        temp_spr_p.append(p_value_bf98_temp_spr)
    else:
        temp_spr_slp.append(-9999)
        temp_spr_p.append(-9999)
    
    
    temp_aut_vector = np.asarray(all_data_temp_aut[:,c])
    temp_aut_years = np.arange(start_yr, end_yr + 1)
    
    ind = ~np.isnan(temp_aut_vector)
    temp_aut_vector_ok = temp_aut_vector[ind]
    temp_aut_years_ok = temp_aut_years[ind]
    
    if(len(temp_aut_vector_ok) > (end_yr-start_yr)*0.7):
        h_bf98_temp_aut, trend_bf98_temp_aut, intp_bf98_temp_aut, p_value_bf98_temp_aut, z_bf98_temp_aut = MK.mk_trend(temp_aut_vector_ok, temp_aut_years_ok, 0.05)
        temp_aut_slp.append(trend_bf98_temp_aut)
        temp_aut_p.append(p_value_bf98_temp_aut)
    else:
        temp_aut_slp.append(-9999)
        temp_aut_p.append(-9999)
    
    
    temp_yr_vector = np.asarray(all_data_temp_yr[:,c])
    temp_yr_years = np.arange(start_yr, end_yr + 1)
    
    ind = ~np.isnan(temp_yr_vector)
    temp_yr_vector_ok = temp_yr_vector[ind]
    temp_yr_years_ok = temp_yr_years[ind]
    
    if(len(temp_yr_vector_ok) > (end_yr-start_yr)*0.7):
        h_bf98_temp_yr, trend_bf98_temp_yr, intp_bf98_temp_yr, p_value_bf98_temp_yr, z_bf98_temp_yr = MK.mk_trend(temp_yr_vector_ok, temp_yr_years_ok, 0.05)
        temp_yr_slp.append(trend_bf98_temp_yr)
        temp_yr_p.append(p_value_bf98_temp_yr)
    else:
        temp_yr_slp.append(-9999)
        temp_yr_p.append(-9999)

    
temp_spr_slp = np.reshape(temp_spr_slp,[Ysize,Xsize])
temp_spr_p = np.reshape(temp_spr_p,[Ysize,Xsize])

temp_aut_slp = np.reshape(temp_aut_slp,[Ysize,Xsize])
temp_aut_p = np.reshape(temp_aut_p,[Ysize,Xsize])    

temp_yr_slp = np.reshape(temp_yr_slp,[Ysize,Xsize])
temp_yr_p = np.reshape(temp_yr_p,[Ysize,Xsize]) 

NoData_value = -9999.0


outfile_temp_spr_slp = '%s/CRUTEM4_05deg_spr_%d_%d_slp' %(outpath,start_yr,end_yr)
Geotiff_RW.CreateGeoTiff(outfile_temp_spr_slp, temp_spr_slp, Xsize, Ysize, GeoT, Proj, NoData_value)

outfile_temp_spr_p = '%s/CRUTEM4_05deg_spr_%d_%d_p' %(outpath,start_yr,end_yr)
Geotiff_RW.CreateGeoTiff(outfile_temp_spr_p, temp_spr_p, Xsize, Ysize, GeoT, Proj, NoData_value)

outfile_temp_aut_slp = '%s/CRUTEM4_05deg_aut_%d_%d_slp' %(outpath,start_yr,end_yr)
Geotiff_RW.CreateGeoTiff(outfile_temp_aut_slp, temp_aut_slp, Xsize, Ysize, GeoT, Proj, NoData_value)

outfile_temp_aut_p = '%s/CRUTEM4_05deg_aut_%d_%d_p' %(outpath,start_yr,end_yr)
Geotiff_RW.CreateGeoTiff(outfile_temp_aut_p, temp_aut_p, Xsize, Ysize, GeoT, Proj, NoData_value)

outfile_temp_yr_slp = '%s/CRUTEM4_05deg_yr_%d_%d_slp' %(outpath,start_yr,end_yr)
Geotiff_RW.CreateGeoTiff(outfile_temp_yr_slp, temp_yr_slp, Xsize, Ysize, GeoT, Proj, NoData_value)

outfile_temp_yr_p = '%s/CRUTEM4_05deg_yr_%d_%d_p' %(outpath,start_yr,end_yr)
Geotiff_RW.CreateGeoTiff(outfile_temp_yr_p, temp_yr_p, Xsize, Ysize, GeoT, Proj, NoData_value)

######################################################################################

################# calculate the MK trend during 1998~2014 ####################
start_yr = 1998
end_yr = 2014

for yr in range(start_yr, end_yr + 1):
    infile_temp_spr = '%s/CRUTEM4v_05deg_spr_%d.tif' %(inpath,yr)
    data_temp_spr, Ysize, Xsize = Geotiff_RW.ReadGeoTiff(infile_temp_spr)
    data_temp_spr = np.asarray(data_temp_spr)
    #print(np.nanmin(data_temp_spr))
    ind = data_temp_spr == -9999.0
    data_temp_spr[ind] = np.nan
    data_temp_spr = np.reshape(data_temp_spr,[1,Ysize*Xsize]).squeeze()
    
    infile_temp_aut = '%s/CRUTEM4v_05deg_aut_%d.tif' %(inpath,yr)
    data_temp_aut, Ysize, Xsize = Geotiff_RW.ReadGeoTiff(infile_temp_aut)
    data_temp_aut = np.asarray(data_temp_aut)
    #print(np.nanmin(data_temp_aut))
    ind = data_temp_aut == -9999.0
    data_temp_aut[ind] = np.nan
    data_temp_aut = np.reshape(data_temp_aut,[1,Ysize*Xsize]).squeeze()
    
    infile_temp_yr = '%s/CRUTEM4v_05deg_year_%d.tif' %(inpath,yr)
    data_temp_yr, Ysize, Xsize = Geotiff_RW.ReadGeoTiff(infile_temp_yr)
    data_temp_yr = np.asarray(data_temp_yr)
    #print(np.nanmin(data_temp_yr))
    ind = data_temp_yr == -9999.0
    data_temp_yr[ind] = np.nan
    data_temp_yr = np.reshape(data_temp_yr,[1,Ysize*Xsize]).squeeze()
    
    
    
    #print(np.nanmin(data_EOS_md0))
    
    if (yr == start_yr):
        all_data_temp_spr = data_temp_spr
        all_data_temp_aut = data_temp_aut
        all_data_temp_yr = data_temp_yr
    else:
        all_data_temp_spr = np.vstack((all_data_temp_spr, data_temp_spr))
        all_data_temp_aut = np.vstack((all_data_temp_aut, data_temp_aut))
        all_data_temp_yr = np.vstack((all_data_temp_yr, data_temp_yr))
        

rows,cols =  np.shape(all_data_temp_spr)

temp_spr_slp = []
temp_spr_p = []
temp_aut_slp = []
temp_aut_p = []
temp_yr_slp = []
temp_yr_p = []


for c in range(cols):
    print("%d in %d" %(c,cols))
    temp_spr_vector = np.asarray(all_data_temp_spr[:,c])
    temp_spr_years = np.arange(start_yr, end_yr + 1)
    
    ind = ~np.isnan(temp_spr_vector)
    temp_spr_vector_ok = temp_spr_vector[ind]
    temp_spr_years_ok = temp_spr_years[ind]
    
    if(len(temp_spr_vector_ok) > (end_yr-start_yr)*0.7):
        h_bf98_temp_spr, trend_bf98_temp_spr, intp_bf98_temp_spr, p_value_bf98_temp_spr, z_bf98_temp_spr = MK.mk_trend(temp_spr_vector_ok, temp_spr_years_ok, 0.05)
        temp_spr_slp.append(trend_bf98_temp_spr)
        temp_spr_p.append(p_value_bf98_temp_spr)
    else:
        temp_spr_slp.append(-9999)
        temp_spr_p.append(-9999)
    
    
    temp_aut_vector = np.asarray(all_data_temp_aut[:,c])
    temp_aut_years = np.arange(start_yr, end_yr + 1)
    
    ind = ~np.isnan(temp_aut_vector)
    temp_aut_vector_ok = temp_aut_vector[ind]
    temp_aut_years_ok = temp_aut_years[ind]
    
    if(len(temp_aut_vector_ok) > (end_yr-start_yr)*0.7):
        h_bf98_temp_aut, trend_bf98_temp_aut, intp_bf98_temp_aut, p_value_bf98_temp_aut, z_bf98_temp_aut = MK.mk_trend(temp_aut_vector_ok, temp_aut_years_ok, 0.05)
        temp_aut_slp.append(trend_bf98_temp_aut)
        temp_aut_p.append(p_value_bf98_temp_aut)
    else:
        temp_aut_slp.append(-9999)
        temp_aut_p.append(-9999)
    
    
    temp_yr_vector = np.asarray(all_data_temp_yr[:,c])
    temp_yr_years = np.arange(start_yr, end_yr + 1)
    
    ind = ~np.isnan(temp_yr_vector)
    temp_yr_vector_ok = temp_yr_vector[ind]
    temp_yr_years_ok = temp_yr_years[ind]
    
    if(len(temp_yr_vector_ok) > (end_yr-start_yr)*0.7):
        h_bf98_temp_yr, trend_bf98_temp_yr, intp_bf98_temp_yr, p_value_bf98_temp_yr, z_bf98_temp_yr = MK.mk_trend(temp_yr_vector_ok, temp_yr_years_ok, 0.05)
        temp_yr_slp.append(trend_bf98_temp_yr)
        temp_yr_p.append(p_value_bf98_temp_yr)
    else:
        temp_yr_slp.append(-9999)
        temp_yr_p.append(-9999)

    
temp_spr_slp = np.reshape(temp_spr_slp,[Ysize,Xsize])
temp_spr_p = np.reshape(temp_spr_p,[Ysize,Xsize])

temp_aut_slp = np.reshape(temp_aut_slp,[Ysize,Xsize])
temp_aut_p = np.reshape(temp_aut_p,[Ysize,Xsize])    

temp_yr_slp = np.reshape(temp_yr_slp,[Ysize,Xsize])
temp_yr_p = np.reshape(temp_yr_p,[Ysize,Xsize]) 

NoData_value = -9999.0


outfile_temp_spr_slp = '%s/CRUTEM4_05deg_spr_%d_%d_slp' %(outpath,start_yr,end_yr)
Geotiff_RW.CreateGeoTiff(outfile_temp_spr_slp, temp_spr_slp, Xsize, Ysize, GeoT, Proj, NoData_value)

outfile_temp_spr_p = '%s/CRUTEM4_05deg_spr_%d_%d_p' %(outpath,start_yr,end_yr)
Geotiff_RW.CreateGeoTiff(outfile_temp_spr_p, temp_spr_p, Xsize, Ysize, GeoT, Proj, NoData_value)

outfile_temp_aut_slp = '%s/CRUTEM4_05deg_aut_%d_%d_slp' %(outpath,start_yr,end_yr)
Geotiff_RW.CreateGeoTiff(outfile_temp_aut_slp, temp_aut_slp, Xsize, Ysize, GeoT, Proj, NoData_value)

outfile_temp_aut_p = '%s/CRUTEM4_05deg_aut_%d_%d_p' %(outpath,start_yr,end_yr)
Geotiff_RW.CreateGeoTiff(outfile_temp_aut_p, temp_aut_p, Xsize, Ysize, GeoT, Proj, NoData_value)

outfile_temp_yr_slp = '%s/CRUTEM4_05deg_yr_%d_%d_slp' %(outpath,start_yr,end_yr)
Geotiff_RW.CreateGeoTiff(outfile_temp_yr_slp, temp_yr_slp, Xsize, Ysize, GeoT, Proj, NoData_value)

outfile_temp_yr_p = '%s/CRUTEM4_05deg_yr_%d_%d_p' %(outpath,start_yr,end_yr)
Geotiff_RW.CreateGeoTiff(outfile_temp_yr_p, temp_yr_p, Xsize, Ysize, GeoT, Proj, NoData_value)

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
