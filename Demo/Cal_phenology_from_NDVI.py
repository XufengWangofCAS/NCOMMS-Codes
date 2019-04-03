#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Jul  7 13:21:25 2018

@author: wangxufeng
"""

#from netCDF4 import Dataset as NCfile
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import savitzky_golay
import phenology_estimate as Phen_Est

#import Geotiff_read_write as geotif_RW   

inpath_NDVI_file = 'input/GIMMS_NDVI.csv'

NDVI = pd.read_csv(inpath_NDVI_file)

NDVI_all = np.asarray(NDVI["NDVI"])

start_year = 1982
end_year = 2014


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
nyears = 33   # years of the data

# start_row,end_row
multi_year_vi = np.asarray(NDVI_all)
# exclude non vegetated area
ind = multi_year_vi<0

### no NDVI pixels ##########################
multi_year_vi_sg=savitzky_golay.savitzky_golay(multi_year_vi,15,4)
# multiyear average NDVI and gs NDVI/ nongs NDVI
avg_multi = np.nanmean(np.reshape(multi_year_vi_sg,[len(multi_year_vi_sg)/24,24]),axis=0)
[onset_ndvi,dormacy_ndvi] = Phen_Est.get_onset_dormancy_ndvi(multi_year_vi_sg,ndata_year)
doy = np.arange(8,365,15)
print onset_ndvi,dormacy_ndvi
for yr in range(start_year,end_year+1):
    t_axis=np.asarray(doy)
    start_ind=(yr-start_year)*ndata_year
    end_ind=(yr-start_year+1)*ndata_year
    ndvi_1year=multi_year_vi_sg[start_ind:end_ind]
    
    
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
    
    
### output results ###################################

outpath = 'output' 

vi='NDVI'


start_year = 1982
end_year = 2014
years = range(start_year, end_year+1)

SOS_outdata = np.vstack((SOS_dbl_2rd,SOS_dbl_1st,SOS_Gmax20,SOS_Gmax50,SOS_poly))
SOS_outdata = np.transpose(SOS_outdata)
col_flds = ['SOS_dbl_2rd','SOS_dbl_1st','SOS_Gmax20','SOS_Gmax50','SOS_poly']
df_out_SOS = pd.DataFrame(data=SOS_outdata,columns = col_flds,index = years)
outfile_SOS = '%s/GIMMS_%d_%d_%s_SOS.csv' %(outpath,start_year,end_year,vi)
df_out_SOS.to_csv(outfile_SOS,index_label="Year")

EOS_outdata = np.vstack((EOS_dbl_2rd,EOS_dbl_1st,EOS_Gmax20,EOS_Gmax50,EOS_poly))
EOS_outdata = np.transpose(EOS_outdata)
col_flds = ['EOS_dbl_2rd','EOS_dbl_1st','EOS_Gmax20','EOS_Gmax50','EOS_poly']
df_out_EOS = pd.DataFrame(data=EOS_outdata,columns = col_flds,index = years)
outfile_EOS = '%s/GIMMS_%d_%d_%s_EOS.csv' %(outpath,start_year,end_year,vi)
df_out_EOS.to_csv(outfile_EOS,index_label="Year")

