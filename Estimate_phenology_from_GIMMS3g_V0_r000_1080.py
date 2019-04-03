#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Jul  7 13:21:25 2018

@author: wangxufeng
"""

#from netCDF4 import Dataset as NCfile
import matplotlib.pyplot as plt
import numpy as np
from glob import glob
import os
import pandas as pd

import  savitzky_golay
from scipy.interpolate import interp1d
import phenology_estimate as Phen_Est

import Geotiff_read_write as geotif_RW   

############### set the path for GIMMS3g v0 geotiff format ##########################
inpath = '/home/wangxufeng/wxf1/GIMMS3g_V0_phen/NDVI_GIMMS_3g_1982_2013/AVHRR_3g_tiff'
os.chdir(inpath)
start_row = 000
end_row = 1080

start_year = 1982
end_year = 2013

for yr in range(start_year,end_year+1):
    for m in range(1,13):
        infile_a = "%s/GIMMS3g_NDVI_%d_%02d_1.tif" %(inpath, yr,m)
        infile_b = "%s/GIMMS3g_NDVI_%d_%02d_2.tif" %(inpath, yr,m)
        print(infile_a)
        
        NDVI_a,Ysize, Xsize = geotif_RW.ReadGeoTiff(infile_a)
        NDVI_b,Ysize, Xsize = geotif_RW.ReadGeoTiff(infile_b)
        
        NDVI_a = NDVI_a[start_row:end_row,:]
        NDVI_b = NDVI_b[start_row:end_row,:]
        
        rows,cols = np.shape(NDVI_a)
        
        NDVI_a = np.reshape(NDVI_a,[1,rows,cols])
        NDVI_b = np.reshape(NDVI_b,[1,rows,cols])
        
        NDVI_yr = np.vstack((NDVI_a,NDVI_b))
        
        if((yr == 1982) and (m==1)):
            NDVI_all = NDVI_yr
        else:
            NDVI_all = np.vstack((NDVI_all,NDVI_yr))


SOS_dbl_2rd=[]
EOS_dbl_2rd=[]              
SOS_Gmax20 = []
EOS_Gmax20 = []        
SOS_Gmax50 = []
EOS_Gmax50 = []        
SOS_poly = []
EOS_poly = []        
SOS_dbl_1st = []
EOS_dbl_1st = []
        
VI_SOS_dbl_2rd=[]
VI_EOS_dbl_2rd=[]               
VI_SOS_Gmax20 = []
VI_EOS_Gmax20 = []        
VI_SOS_Gmax50 = []
VI_EOS_Gmax50 = []        
VI_SOS_poly = []
VI_EOS_poly = []        
VI_SOS_dbl_1st = []
VI_EOS_dbl_1st = []

para_phen = []
ndata_year = 24 # records number for a year
nyears = 34   # years of the data

# start_row,end_row
for r in range(end_row-start_row):
    print r+start_row
    for c in range(4320):
        multi_year_vi = np.asarray(NDVI_all[:,r,c])/10000.0
        # exclude non vegetated area
        ind = multi_year_vi<0
        
        ### no NDVI pixels ##########################
        if(len(multi_year_vi[ind])>(len(multi_year_vi)/2)):
            for yr in range(start_year,end_year+1):
                SOS_dbl_2rd.append(-9999)
                EOS_dbl_2rd.append(-9999)
                SOS_Gmax20.append(-9999)
                EOS_Gmax20.append(-9999)    
                SOS_Gmax50.append(-9999)
                EOS_Gmax50.append(-9999)       
                SOS_poly.append(-9999)
                EOS_poly.append(-9999)       
                SOS_dbl_1st.append(-9999)
                EOS_dbl_1st.append(-9999)
            continue
        
        ### replace negative NDVIS 
        multi_year_vi[ind] = np.min(multi_year_vi[~ind])
        multi_year_vi_sg=savitzky_golay.savitzky_golay(multi_year_vi,15,4)
        
        # multiyear average NDVI and gs NDVI/ nongs NDVI
        avg_multi = np.nanmean(np.reshape(multi_year_vi_sg,[len(multi_year_vi_sg)/24,24]),axis=0)
        avg_vi = np.nanmean(avg_multi)
        gs_avg_vi = np.nanmean(avg_multi[6:18])
        nongs_avg_vi = (np.nanmean(avg_multi[0:6])+np.nanmean(avg_multi[18:24]))/2
        if((avg_vi>0.1) and (gs_avg_vi > (nongs_avg_vi + 0.1))):
            if(~np.isnan(np.sum(multi_year_vi_sg))):
                [onset_ndvi,dormacy_ndvi] = Phen_Est.get_onset_dormancy_ndvi(multi_year_vi_sg,ndata_year)
            else:
                onset_ndvi = np.nan
                dormacy_ndvi = np.nan
                
            multi_year_vi_sg = np.squeeze(multi_year_vi_sg)
            
            '''
            plt.plot(multi_year_vi_sg)
            plt.show()
            '''
            doy = np.arange(8,365,15)
            print r+start_row,onset_ndvi,dormacy_ndvi
            
            
            for yr in range(start_year,end_year+1):
                t_axis=np.asarray(doy)
                start_ind=(yr-start_year)*ndata_year
                end_ind=(yr-start_year+1)*ndata_year
                ndvi_1year=multi_year_vi_sg[start_ind:end_ind]
                
                avg_vi_1year = np.nanmean(ndvi_1year)
                gs_avg_vi_1year = np.nanmean(ndvi_1year[6:18])
                nongs_avg_vi_1year = (np.nanmean(ndvi_1year[0:6])+np.nanmean(ndvi_1year[18:24]))/2
                
                if((avg_vi_1year>0.1) and (gs_avg_vi_1year>nongs_avg_vi_1year+0.1)  and ~np.isnan(dormacy_ndvi) and ~np.isnan(onset_ndvi)):
                    t_axis= t_axis[~np.isnan(ndvi_1year)]
                    ndvi_1year = ndvi_1year[~np.isnan(ndvi_1year)]
                    
                    # using polynomial function to fit
                    [sos_poly, eos_poly,spr_days,spr_ndvi,fall_days,fall_ndvi] = \
                             Phen_Est.fit_phenology_model_poly (ndvi_1year, t_axis,onset_ndvi,dormacy_ndvi)
                    
                    SOS_poly.append(sos_poly)
                    EOS_poly.append(eos_poly) 
                    # using logistic function to fit
                    xinit=None
                    pheno_model="dbl_logistic"
                    #### raw NDVI data
                    [para, msg, result]=Phen_Est.fit_phenology_model_double_logistic( ndvi_1year, t_axis, pheno_model, xinit )
                    
                    para_phen.append(para[3])
                    para_phen.append(para[5])
                    
                    
                    doys = range(1,len(result)+1)   
                    [s_sos, s_eos] = Phen_Est.get_phen_date_model_double_logistic(result,doys)
                    
                    SOS_dbl_2rd.append(s_sos)
                    EOS_dbl_2rd.append(s_eos)    
                    ####  Gmax20 to get SOS and EOS ########################
                    ndvi_norm = Phen_Est.VI_normalize_yearly(result)
                    SOS20,EOS20 = Phen_Est.Gmax_SOS_EOS(ndvi_norm,0.2)
                    
                    SOS_Gmax20.append(SOS20)
                    EOS_Gmax20.append(EOS20)
                    
                    ####  Gmax50 to get SOS and EOS ########################
                    SOS50,EOS50 = Phen_Est.Gmax_SOS_EOS(ndvi_norm,0.5)
                    
                    SOS_Gmax50.append(SOS50)
                    EOS_Gmax50.append(EOS50)
                    
                    ####  first derive SOS and EOS ########################
                    [s_sos_slog, s_eos_slog] = Phen_Est.get_phen_date_model_double_logistic_first_derive(result,doys)
                    SOS_dbl_1st.append(s_sos_slog)
                    EOS_dbl_1st.append(s_eos_slog) 
                    
                    ####  using Dbl_log Zhang to get SOS and EOS ####################
                    
                    '''
                    plt.plot(doys,result)
                    plt.plot([s_sos,s_sos],[0,1],'r-',label='dbl_log')
                    plt.plot([s_eos,s_eos],[0,1],'r-',label='dbl_log')
                    
                    plt.plot([SOS20,SOS20],[0,1],'g-',label='p20')
                    plt.plot([EOS20,EOS20],[0,1],'g-',label='p20')
                    
                    plt.plot([SOS50,SOS50],[0,1],'y-',label='p50')
                    plt.plot([EOS50,EOS50],[0,1],'y-',label='p50')
                    
                    plt.plot([sos_poly,sos_poly],[0,1],'k-',label='poly')
                    plt.plot([eos_poly,eos_poly],[0,1],'k-',label='poly')
                    plt.show()
                    '''
                    
                else:
                    SOS_dbl_2rd.append(-9999)
                    EOS_dbl_2rd.append(-9999) 
                    SOS_Gmax20.append(-9999)
                    EOS_Gmax20.append(-9999)    
                    SOS_Gmax50.append(-9999)
                    EOS_Gmax50.append(-9999)       
                    SOS_poly.append(-9999)
                    EOS_poly.append(-9999)       
                    SOS_dbl_1st.append(-9999)
                    EOS_dbl_1st.append(-9999)

        else:
            for yr in range(start_year,end_year+1):
                SOS_dbl_2rd.append(-9999)
                EOS_dbl_2rd.append(-9999)
                SOS_Gmax20.append(-9999)
                EOS_Gmax20.append(-9999)    
                SOS_Gmax50.append(-9999)
                EOS_Gmax50.append(-9999)       
                SOS_poly.append(-9999)
                EOS_poly.append(-9999)       
                SOS_dbl_1st.append(-9999)
                EOS_dbl_1st.append(-9999)

            
cols = (end_row - start_row)*4320          
### output results ###################################
SOS_dbl_2rd = np.reshape(SOS_dbl_2rd,[cols,32])
EOS_dbl_2rd = np.reshape(EOS_dbl_2rd,[cols,32])
SOS_Gmax20 = np.reshape(SOS_Gmax20,[cols,32])
EOS_Gmax20 = np.reshape(EOS_Gmax20,[cols,32])       
SOS_Gmax50 = np.reshape(SOS_Gmax50,[cols,32])
EOS_Gmax50 = np.reshape(EOS_Gmax50,[cols,32])       
SOS_poly = np.reshape(SOS_poly,[cols,32])       
EOS_poly = np.reshape(EOS_poly,[cols,32])              
SOS_dbl_1st = np.reshape(SOS_dbl_1st,[cols,32])       
EOS_dbl_1st = np.reshape(EOS_dbl_1st,[cols,32])       
    
######## set the path for output the remote sensing phenology results #########
outpath = '/home/wangxufeng/wxf1/GIMMS3g_V0_phen/NDVI_GIMMS_3g_1982_2013/phen_v0_out/r%03d_%03d_v0' %(start_row,end_row-1)

Ysize = end_row-start_row
Xsize = 4320    
vi='NDVI'
for n in range(end_year-start_year+1):
    # output dbl_2rd result
    outdata = SOS_dbl_2rd[:,n]
    outdata = np.reshape(outdata,[Ysize,Xsize])
    year = start_year+n
    outfile = '%s/GIMMS_%d_%s_SOS_dbl_2rd_sr_%d.txt' %(outpath,year,vi,start_row)        
    NoData_value = -9999
    np.savetxt(outfile,outdata, delimiter = ',',fmt='%7d')
        
    outdata = EOS_dbl_2rd[:,n]
    outdata = np.reshape(outdata,[Ysize,Xsize])
    year = start_year+n
    outfile = '%s/GIMMS_%d_%s_EOS_dbl_2rd_sr_%d.txt' %(outpath,year,vi,start_row)        
    NoData_value = -9999
    np.savetxt(outfile,outdata, delimiter = ',',fmt='%7d')
    
        
    # output GMAX20 result
    outdata = SOS_Gmax20[:,n]
    outdata = np.reshape(outdata,[Ysize,Xsize])
    year = start_year+n
    outfile = '%s/GIMMS_%d_%s_SOS_Gmax20_sr_%d.txt' %(outpath,year,vi,start_row)        
    NoData_value = -9999
    np.savetxt(outfile,outdata, delimiter = ',',fmt='%7d')
    
    
    
    outdata = EOS_Gmax20[:,n]
    outdata = np.reshape(outdata,[Ysize,Xsize])
    year = start_year+n
    outfile = '%s/GIMMS_%d_%s_EOS_Gmax20_sr_%d.txt' %(outpath,year,vi,start_row)        
    NoData_value = -9999
    np.savetxt(outfile,outdata, delimiter = ',',fmt='%7d')
    
      
    # output GMAX50 result
    outdata = SOS_Gmax50[:,n]
    outdata = np.reshape(outdata,[Ysize,Xsize])
    year = start_year+n
    outfile = '%s/GIMMS_%d_%s_SOS_Gmax50_sr_%d.txt' %(outpath,year,vi,start_row)        
    NoData_value = -9999
    np.savetxt(outfile,outdata, delimiter = ',',fmt='%7d')
    
    outdata = EOS_Gmax50[:,n]
    outdata = np.reshape(outdata,[Ysize,Xsize])
    year = start_year+n
    outfile = '%s/GIMMS_%d_%s_EOS_Gmax50_sr_%d.txt' %(outpath,year,vi,start_row)        
    NoData_value = -9999
    np.savetxt(outfile,outdata, delimiter = ',',fmt='%7d')
    
    
    # output poly result
    outdata = SOS_poly[:,n]
    outdata = np.reshape(outdata,[Ysize,Xsize])
    year = start_year+n
    outfile = '%s/GIMMS_%d_%s_SOS_poly_sr_%d.txt' %(outpath,year,vi,start_row)        
    NoData_value = -9999
    np.savetxt(outfile,outdata, delimiter = ',',fmt='%7d')
    
    outdata = EOS_poly[:,n]
    outdata = np.reshape(outdata,[Ysize,Xsize])
    year = start_year+n
    outfile = '%s/GIMMS_%d_%s_EOS_poly_sr_%d.txt' %(outpath,year,vi,start_row)        
    NoData_value = -9999
    np.savetxt(outfile,outdata, delimiter = ',',fmt='%7d')
    
    
    # output dbl_1st result
    outdata = SOS_dbl_1st[:,n]
    outdata = np.reshape(outdata,[Ysize,Xsize])
    year = start_year+n
    outfile = '%s/GIMMS_%d_%s_SOS_dbl_1st_sr_%d.txt' %(outpath,year,vi,start_row)        
    NoData_value = -9999
    np.savetxt(outfile,outdata, delimiter = ',',fmt='%7d')
    
    outdata = EOS_dbl_1st[:,n]
    outdata = np.reshape(outdata,[Ysize,Xsize])
    year = start_year+n
    outfile = '%s/GIMMS_%d_%s_EOS_dbl_1st_sr_%d.txt' %(outpath,year,vi,start_row)        
    NoData_value = -9999
    np.savetxt(outfile,outdata, delimiter = ',',fmt='%7d')