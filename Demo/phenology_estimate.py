# -*- coding: utf-8 -*-
"""
Created on Tue Apr 26 22:11:25 2017

@author: wxf
"""

#comprison of phenology methods

import numpy as np 
import numpy.polynomial.polynomial as poly

def VI_normalize_yearly(vi):
    max_vi = max(vi)
    min_vi = min(vi)
    vi_norm = []
    for i in range(len(vi)):
        vi_norm.append((vi[i]-min_vi)/(max_vi-min_vi))
    
    return vi_norm
    
def Gmax_SOS_EOS(vi_norm,threshold):
    m=max(vi_norm)
    ind = list(vi_norm).index(m)
    
    SOS = -9999
    EOS = -9999
    #get SOS
    i=ind
    while ((vi_norm[i] > threshold) and (i > 1)):
        i=i-1
    
    SOS = i
        
    #get EOS
    i=ind
    while ((vi_norm[i]>threshold) and (i<364)):
        i=i+1
    EOS = i    
    return SOS,EOS

def dbl_logistic_model ( p, doys ):
    """A double logistic model, as in Sobrino and Juliean, or Zhang et al"""
    y= p[0] + p[1]* ( 1./(1+np.exp(p[2]*(doys-p[3]))) + 1./(1+np.exp(-p[4]*(doys-p[5])) ))#+ \
                        #  1./(1+np.exp(-p[4]*(agdd-p[5])))  - 1 )
    #y=-y
    return y
                              
def mismatch_function ( p, pheno_func, ndvi, days):
    """The NDVI/Phenology model mismatch function. This can be a multi-year
    function that will be minimised wrt to the VI observations. This function
    will take different phenology models, and NDVI and AGDD datasets. """

    # output stores the predictions    
    output = []
    
    # define funciton using lambda structure
    fitness = lambda p, ndvi_in, days: ndvi_in - pheno_func ( p, days )
    oot = fitness ( p, ndvi, days )            
    [ output.append ( x ) for x in oot ]
        
    return np.array(output).squeeze()                              
 

def fit_phenology_model_double_logistic ( ndvi_all, t_axis, pheno_func, xinit=None ):
    """This function fits a phenology model of choice for a given location and
    time period. The user can also modify the base and maximum temperature for
    AGDD calculations, as well as the number of harmonics used by the Fourier
    phenology model."""
    from scipy.optimize import leastsq
    # Find the number of parameters and a pointer to the phenology model func.
    
    pheno_func = dbl_logistic_model
    n_params = 6 # 6 terms
    if xinit is None:        
        # The user hasn't provided a starting guess
        xinit = [.5,] * n_params
        # Dbl_logistic might require sensible starting point  
        xinit[0] = ndvi_all.min()
        xinit[1] = ndvi_all.max() - ndvi_all.min()
        xinit[2] = 0.19
        xinit[3] = 120
        xinit[4] = 0.13
        xinit[5] = 260
            
    ( xsol, msg ) = leastsq ( mismatch_function, xinit, \
                args=( pheno_func, ndvi_all, t_axis ), maxfev=1000000 )
    #print msg
    ax = pheno_func ( xsol, np.arange(1, 366))
    
        
    return ( xsol, msg,ax )        

def get_phen_date_model_double_logistic(daily_ndvi,days):
    import numpy as np
    try:
        daily_ndvi = daily_ndvi.tolist()
        max_ndvi= max(daily_ndvi)
        ind_max = daily_ndvi.index(max_ndvi)
        sep_day = days[ind_max]
        
        days = np.asarray(days)
        daily_ndvi = np.asarray(daily_ndvi)
        first_half_ind = days < sep_day
        
        #spr_days = days[first_half_ind]
        spr_ndvi = daily_ndvi[first_half_ind]
        
        second_half_ind = days > sep_day
        
        #fall_days = days[second_half_ind]
        fall_ndvi = daily_ndvi[second_half_ind]
        
        
        spr_first_der = np.diff(spr_ndvi)
        doy_onset = np.diff(spr_first_der).argmax()
        # I get 297 for this
        # Onset of greenness is the minimum of the derivative
        fall_first_der = np.diff(fall_ndvi)
        doy_dormacy = np.diff(fall_first_der).argmax() + sep_day
        # I get 109 for my example
        
        return (doy_onset,doy_dormacy)
    except:
        return (-9999,-9999)

def get_phen_date_model_double_logistic_first_derive(daily_ndvi,days):
    import numpy as np
    try:
        daily_ndvi = daily_ndvi.tolist()
        max_ndvi= max(daily_ndvi)
        ind_max = daily_ndvi.index(max_ndvi)
        sep_day = days[ind_max]
        
        days = np.asarray(days)
        daily_ndvi = np.asarray(daily_ndvi)
        
        doy_onset = np.diff(daily_ndvi).argmax()
        doy_dormacy = np.diff(daily_ndvi).argmin()
        
        if(doy_onset<1 or doy_onset>365):
            doy_onset=-9999
        if(doy_dormacy<1 or doy_dormacy>365):
            doy_dormacy=-9999
        
        return (doy_onset,doy_dormacy)
    except:
        return (-9999,-9999)      
        

def get_onset_dormancy_ndvi(NDVI_data,ndata_year):
    nyear = len(NDVI_data)/ndata_year
    NDVI_data = np.reshape(NDVI_data,[nyear,ndata_year])
    years_avg_ndvi = np.nanmean(NDVI_data,axis=0) # get the mean of each column
    
    if(np.nanmean(years_avg_ndvi)>0.1):
        ndvi_ratio = []
        for i in range(ndata_year-1):
            ndvi_ratio.append((years_avg_ndvi[i+1]-years_avg_ndvi[i])/years_avg_ndvi[i])
        
        max_ratio = np.nanmax(ndvi_ratio) 
        min_ratio = np.nanmin(ndvi_ratio)
        
        ind_onset = ndvi_ratio.index(max_ratio)
        ind_dormancy = ndvi_ratio.index(min_ratio) + 1
        
        onset_ndvi = years_avg_ndvi[ind_onset]
        dormancy_ndvi = years_avg_ndvi[ind_dormancy]
    else:
        onset_ndvi = -9.999
        dormancy_ndvi = -9.999
    return [onset_ndvi, dormancy_ndvi]
    
    
def fit_phenology_model_poly (ndvi_pixel, doys,onset_ndvi,dormacy_ndvi):
    SOS = -9999
    EOS = -9999
    #divide the data into two parts
    # spring part data
    # fitting the curve
    doys = np.asarray(doys)
    ind_spr = doys < 256
    spr_doy=doys[ind_spr]
    spr_ndvi=ndvi_pixel[ind_spr]
    p_spr=poly.polyfit(spr_doy,spr_ndvi,6)
    
    # get the phenology date
    
    first_half_days=np.arange(1,210)
    ndvi_first_half=poly.polyval(first_half_days,p_spr)
    
    ndvi_first_half = ndvi_first_half.tolist()
    max_ind = ndvi_first_half.index(np.nanmax(ndvi_first_half))
    max_ndvi_day_sec_first = first_half_days[max_ind]
    
    if(onset_ndvi>0 ): # and onset_ndvi<1  # whether onset_ndvi is valid           
        for d in range(max_ndvi_day_sec_first,50,-1):
            ind_d = d -1 -1
            if(ndvi_first_half[ind_d]<=onset_ndvi):
                SOS=d
                break    
    else:
        SOS = -9999
    
    # fall part data
    # fitting the curve
    
    ind_fall = doys > 180
    fall_doy=doys[ind_fall]
    fall_ndvi=ndvi_pixel[ind_fall]
    p_fall=poly.polyfit(fall_doy,fall_ndvi,6)
    # get the phenology date

    second_half_days=np.arange(181,365)
    ndvi_second_half=poly.polyval(second_half_days,p_fall)
    
    ndvi_second_half = ndvi_second_half.tolist()
    max_ind = ndvi_second_half.index(np.nanmax(ndvi_second_half))
    max_ndvi_day_second = second_half_days[max_ind]    
    
    if(dormacy_ndvi>0): # and dormacy_ndvi<1
        for d in range(max_ndvi_day_second,340):
            ind_d = d-181
            if(ndvi_second_half[ind_d]<=dormacy_ndvi):
                EOS=d
                break    
    else:
        EOS = -9999
        
    return (SOS,EOS,first_half_days,ndvi_first_half,second_half_days,ndvi_second_half)