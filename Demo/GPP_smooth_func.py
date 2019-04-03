# -*- coding: utf-8 -*-
"""
Created on Mon Jan 16 17:32:12 2017

@author: wxf
"""

import numpy as np
from scipy.interpolate import UnivariateSpline
from scipy.signal import gaussian
from scipy.ndimage import filters


def Gauss_func(x, y):
    b = gaussian(39, 10)
    #ga = filtfilt(b/b.sum(), [1.0], y)
    ga = filters.convolve1d(y, b/b.sum())
    return ga
    
def move_window_15day(year_flux_data):
    l = len(year_flux_data)
    out_flux = np.zeros(l)
    for i in range(6,l-6):
        out_flux[i] = np.nanmean(year_flux_data[i-6:i+6+1])
    return out_flux

def get_thredhold_p15(multi_year_GPP,multi_year_data_QC):
    multi_year_data_QC = np.asarray(multi_year_data_QC)
    multi_year_GPP = np.asarray(multi_year_GPP)
    multi_year_GPP = move_window_15day(multi_year_GPP)
    ind = multi_year_data_QC > 0.9
    multi_year_GPP_good = multi_year_GPP[ind]
    thred_p15 = 0.15*np.nanmax(multi_year_GPP_good)
    if(thred_p15> 2):
        thred_p15 = 2
    if(thred_p15<1.0):
        thred_p15 = 1.0
    return thred_p15


#### fixed threshold across all years,     
def get_phen_date_fixed_per15(doy,year_flux_data,func,thrd15):
    sm_flux_data = func(doy,year_flux_data)
    max_flux = np.nanmax(sm_flux_data)
    sep = list(sm_flux_data).index(max_flux)
         
    # initial
    SOS_p15 = -99
    EOS_p15 = -99
    
    if ((sep == 0) or (sep == len(year_flux_data)-1)):
        return SOS_p15,  EOS_p15, sm_flux_data
        
    flag15 = 0
    for i  in range(1,sep-10):
        if ((sm_flux_data[i-1] < thrd15) and (sm_flux_data[i] > thrd15) and \
           (np.nanmin(sm_flux_data[i:i+20]) > thrd15) and (flag15 == 0)):
            flag15 = 1
            SOS_p15 = doy[i]
        

    flag15 = 0
    for i  in range(len(sm_flux_data)-1, sep, -1):
        if ((sm_flux_data[i] < thrd15) and (sm_flux_data[i-1] > thrd15) and \
            (np.nanmin(sm_flux_data[i-20:i-1]) > thrd15) and (flag15 == 0)):
            flag15 = 1
            EOS_p15 = doy[i]
            
    return  SOS_p15,  EOS_p15, sm_flux_data
    
def Cflux_Qualit_assess(Cflux_QC):
    if (np.nanmean(Cflux_QC) < 0.75):
        return 0
    else:
        return 1

    
