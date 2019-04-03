# -*- coding: utf-8 -*-
"""
Created on Tue May 30 15:52:21 2017

@author: wxf
"""
import os
import glob
import pandas as pd
import numpy as np
import calendar
import matplotlib.pyplot as plt
import scipy.stats as stat
import MK_trend as MK

def cm2inch(*tupl):
    inch = 2.54
    if isinstance(tupl[0], tuple):
        return tuple(i/inch for i in tupl[0])
    else:
        return tuple(i/inch for i in tupl) 
        
def plot_scatter(var,var_QC,phen,phen_QC,xname,yname,plotname,out_fig):
    if(len(phen_QC)<3):
        return(-9999, -9999, -9999, -9999, -9999)
    phen = np.asarray(phen)
    phen_QC = np.asarray(phen_QC)
    var = np.asarray(var)
    var_QC = np.asarray(var_QC)
    
    ind_phen_QC = phen_QC==1
    ind_phen = phen > 0.75
    ind_var_QC = var_QC > 0.75
    ind_var = var > -9999
    
    ind_good = ind_phen_QC & ind_phen & ind_var_QC & ind_var
    fig=plt.figure(figsize=cm2inch(8, 8))
    phen_good = phen[ind_good]
    var_good = var[ind_good]
    if(len(phen_good)>=5):
        plt.plot(var_good,phen_good,'o',markerfacecolor='none')
        
        slp_phen, intp_phen, r_phen, p_phen, std_phen = stat.linregress(var_good,phen_good)
        lin_x = np.asarray([np.nanmin(var_good),np.nanmax(var_good)])
        lin_y = lin_x*slp_phen + intp_phen
        
        
        plt.plot(lin_x,lin_y,'r-')
        plt.text(1.1*np.min(var_good),0.9*np.max(phen_good),'y=%3.2f*x+%4.2f\n$R^2$=%3.2f n=%d' %(slp_phen,intp_phen,r_phen*r_phen,len(phen_good)))
        
        min_x = np.min(var_good) 
        max_x = np.max(var_good)
        plt.xlim([0.9*min_x, 1.1*max_x])
    
        plt.xlabel(xname)
        plt.ylabel(yname)
        plt.title(plotname)
        plt.savefig(out_fig,format='png',dpi=300,bbox_inches='tight')
        plt.show()
        return(slp_phen, intp_phen, r_phen, p_phen, std_phen)
    else:
        return(-9999, -9999, -9999, -9999, -9999)

def plot_scatter_flux(phen,phen_QC,var,var_QC,xname,yname,plotname,out_fig):
    if(len(phen_QC)<3):
        return(-9999, -9999, -9999, -9999, -9999)
    phen = np.asarray(phen)
    phen_QC = np.asarray(phen_QC)
    var = np.asarray(var)
    var_QC = np.asarray(var_QC)
    
    ind_phen_QC = phen_QC==1
    ind_phen = phen > 0
    ind_var_QC = var_QC > 0.75
    ind_var = var > -9999
    
    ind_good = ind_phen_QC & ind_phen & ind_var_QC & ind_var
    fig=plt.figure(figsize=cm2inch(8, 8))
    phen_good = phen[ind_good]
    var_good = var[ind_good]
    if(len(phen_good)>=5):
        plt.plot(phen_good,var_good,'o',markerfacecolor='none')
        
        slp_phen, intp_phen, r_phen, p_phen, std_phen = stat.linregress(phen_good,var_good)
        lin_x = np.asarray([np.nanmin(phen_good),np.nanmax(phen_good)])
        lin_y = lin_x*slp_phen + intp_phen
        
        
        plt.plot(lin_x,lin_y,'r-')
        plt.text(1.1*np.min(phen_good),0.9*np.max(var_good),'y=%3.2f*x+%4.2f\n$R^2$=%3.2f n=%d' %(slp_phen,intp_phen,r_phen*r_phen,len(phen_good)))
        
        min_x = np.min(phen_good) 
        max_x = np.max(phen_good)
        plt.xlim([0.9*min_x, 1.1*max_x])
    
        plt.xlabel(xname)
        plt.ylabel(yname)
        plt.title(plotname)
        plt.savefig(out_fig,format='png',dpi=300,bbox_inches='tight')
        plt.show()
        return(slp_phen, intp_phen, r_phen, p_phen, std_phen)
    else:
        return(-9999, -9999, -9999, -9999, -9999)
    
def get_mean_std_phen(phen,phen_QC):
    if(len(phen_QC)<=4):
        return (-9999, -9999)
        
    phen_QC = np.asarray(phen_QC)
    phen = np.asarray(phen)
    ind = (phen_QC == 1) & (phen>0)
    phen_ok = phen[ind]
    if (len(phen_ok)>6):
        avg = np.nanmean(phen_ok)
        std = np.nanstd(phen_ok)
    else:
        avg = -9999
        std = -9999
    
    return (avg, std)
    
def get_mean_std_var(var,var_QC):
    if(len(var_QC)<=4):
        return (-9999, -9999)
    var_QC = np.asarray(var_QC)
    var = np.asarray(var)
    ind = (var_QC  > 0.75) & (var > -300)
    var_ok = var[ind]
    if (len(var_ok)>6):
        avg = np.nanmean(var_ok)
        std = np.nanstd(var_ok)
    else:
        avg = -9999
        std = -9999
    
    return (avg, std)    

def Trend_phen(years,phen,phen_QC):
    if(len(phen_QC)<=6):
        return (-9999, -9999,-9999)
    phen_QC = np.asarray(phen_QC)
    phen = np.asarray(phen)
    years = np.asarray(years)
    ind = (phen_QC  > 0.75) & (phen > 0)
    phen_ok = phen[ind]
    years_ok = years[ind]
    if (len(phen_ok)>6):
        h, trend, intp, p_value, z = MK.mk_trend(phen_ok,years_ok,0.05)
    else:
        trend = -9999
        intp = -9999
        p_value = -9999
    
    return trend, intp, p_value

def Trend_var(years,var,var_QC):
    if(len(var_QC)<=6):
        return (-9999, -9999,-9999)
    var_QC = np.asarray(var_QC)
    var = np.asarray(var)
    years = np.asarray(years)
    ind = (var_QC  > 0.75) & (var > -9999)
    var_ok = var[ind]
    years_ok = years[ind]
    if (len(var_ok)>6):
        h, trend, intp, p_value, z = MK.mk_trend(var_ok,years_ok,0.05)
    else:
        trend = -9999
        intp = -9999
        p_value = -9999
    
    return trend, intp, p_value

############################################################################
############## main program start here #####################################
############################################################################
SOS_env_slp = []
EOS_env_slp = []
GSL_env_slp = []

SOS_env_R2 = []
EOS_env_R2 = []
GSL_env_R2 = []
SOS_env_P = []
EOS_env_P = []
GSL_env_P = []

SOS_avg_std = []
EOS_avg_std = []
GSL_avg_std = []

SOS_env_MK_trend_slp = []
SOS_env_MK_trend_intp = []
SOS_env_MK_trend_P = []

EOS_env_MK_trend_slp = []
EOS_env_MK_trend_intp = []
EOS_env_MK_trend_P = []

GSL_env_MK_trend_slp = []
GSL_env_MK_trend_intp = []
GSL_env_MK_trend_P = []

##### seasonal FLUXNET carbon fluxes and meteorological files path ############
in_path = 'D:/3.UNH_visiting/fluxnet_analyze_v2/FluxnetData_season_ver3'

##### MK trend, R2, P output path  ############################################
out_R2_path = 'D:/3.UNH_visiting/Phenology_from_fluxnet/phen_vs_envir_factors_seasons20190302'

##### input path for the phenology estiamted from FLUXNET data  ###############
inpath_phen = 'D:/3.UNH_visiting/Phenology_from_fluxnet/output_phen_ver3_20171023/over_7years_20171023'

os.chdir(inpath_phen)
phen_files = glob.glob('*.csv')


phen_sites = []
start_year = []
end_year = []

for f in phen_files:
    if(f[0:2] == 'MF'):
        phen_sites.append(f[7:13])
        start_year.append(int(f[14:18]))
        end_year.append(int(f[19:23]))
    else:
        phen_sites.append(f[8:14])
        start_year.append(int(f[15:19]))
        end_year.append(int(f[20:24]))
    

for i in range(len(phen_sites)):
    ### read data
    infile_sea = '%s/season_all/FLX_%s_season.csv' %(in_path,phen_sites[i])    
    
    infile_phen = '%s/%s' %(inpath_phen,phen_files[i])
    
    data_sea = pd.read_csv(infile_sea)

    phen_data = pd.read_csv(infile_phen)
    
    years_phen = np.asarray(phen_data['Unnamed: 0'])
    SOS = np.asarray(phen_data['SOS_15%_GA_GP_NT'])
    EOS = np.asarray(phen_data['EOS_15%_GA_GP_NT'])
    phen_QC = np.asarray(phen_data['QC_flag'])
    
    years = np.asarray(data_sea['Year'])
    TA_spr = np.asarray(data_sea['TA_F_spr'])
    TA_spr_QC = np.asarray(data_sea['TA_F_QC_spr'])
    P_spr = np.asarray(data_sea['P_F_spr'])
    P_spr_QC = np.asarray(data_sea['P_F_QC_spr'])    
    SW_IN_spr	 = np.asarray(data_sea['SW_IN_F_spr'])
    SW_IN_spr_QC = np.asarray(data_sea['SW_IN_F_QC_spr'])
    VPD_spr	 = np.asarray(data_sea['VPD_F_spr'])
    VPD_spr_QC = np.asarray(data_sea['VPD_F_QC_spr'])
    TS_MDS_1_spr	 = np.asarray(data_sea['TS_F_MDS_1_spr'])
    TS_MDS_1_spr_QC = np.asarray(data_sea['TS_F_MDS_1_QC_spr'])
    TS_MDS_2_spr	 = np.asarray(data_sea['TS_F_MDS_2_spr'])
    TS_MDS_2_spr_QC = np.asarray(data_sea['TS_F_MDS_2_QC_spr'])
    SWC_MDS_1_spr	 = np.asarray(data_sea['SWC_F_MDS_1_spr'])
    SWC_MDS_1_spr_QC = np.asarray(data_sea['SWC_F_MDS_1_QC_spr'])
    SWC_MDS_2_spr	 = np.asarray(data_sea['SWC_F_MDS_2_spr'])
    SWC_MDS_2_spr_QC = np.asarray(data_sea['SWC_F_MDS_2_QC_spr'])    
    NEE_VUT_REF_spr	 = np.asarray(data_sea['NEE_VUT_REF_spr'])*92
    NEE_VUT_REF_QC_spr = np.asarray(data_sea['NEE_VUT_REF_QC_spr'])
    GPP_NT_VUT_REF_spr	 = np.asarray(data_sea['GPP_NT_VUT_REF_spr'])*92
    RECO_NT_VUT_REF_spr	 = np.asarray(data_sea['RECO_NT_VUT_REF_spr'])*92
    LE_F_MDS_spr	 = np.asarray(data_sea['LE_F_MDS_spr'])
    LE_F_MDS_QC_spr	 = np.asarray(data_sea['LE_F_MDS_QC_spr'])
    
    
    TA_smr = np.asarray(data_sea['TA_F_sum'])
    TA_smr_QC = np.asarray(data_sea['TA_F_QC_sum'])
    P_smr = np.asarray(data_sea['P_F_sum'])
    P_smr_QC = np.asarray(data_sea['P_F_QC_sum'])    
    SW_IN_smr	 = np.asarray(data_sea['SW_IN_F_sum'])
    SW_IN_smr_QC = np.asarray(data_sea['SW_IN_F_QC_sum'])
    VPD_smr	 = np.asarray(data_sea['VPD_F_sum'])
    VPD_smr_QC = np.asarray(data_sea['VPD_F_QC_sum'])
    TS_MDS_1_smr	 = np.asarray(data_sea['TS_F_MDS_1_sum'])
    TS_MDS_1_smr_QC = np.asarray(data_sea['TS_F_MDS_1_QC_sum'])
    TS_MDS_2_smr	 = np.asarray(data_sea['TS_F_MDS_2_sum'])
    TS_MDS_2_smr_QC = np.asarray(data_sea['TS_F_MDS_2_QC_sum'])
    SWC_MDS_1_smr	 = np.asarray(data_sea['SWC_F_MDS_1_sum'])
    SWC_MDS_1_smr_QC = np.asarray(data_sea['SWC_F_MDS_1_QC_sum'])
    SWC_MDS_2_smr	 = np.asarray(data_sea['SWC_F_MDS_2_sum'])
    SWC_MDS_2_smr_QC = np.asarray(data_sea['SWC_F_MDS_2_QC_sum'])    
    NEE_VUT_REF_smr	 = np.asarray(data_sea['NEE_VUT_REF_sum'])*92
    NEE_VUT_REF_QC_smr = np.asarray(data_sea['NEE_VUT_REF_QC_sum'])
    GPP_NT_VUT_REF_smr	 = np.asarray(data_sea['GPP_NT_VUT_REF_sum'])*92
    RECO_NT_VUT_REF_smr	 = np.asarray(data_sea['RECO_NT_VUT_REF_sum'])*92
    LE_F_MDS_smr	 = np.asarray(data_sea['LE_F_MDS_sum'])
    LE_F_MDS_QC_smr	 = np.asarray(data_sea['LE_F_MDS_QC_sum'])
    
    
    TA_aut = np.asarray(data_sea['TA_F_aut'])
    TA_aut_QC = np.asarray(data_sea['TA_F_QC_aut'])
    P_aut = np.asarray(data_sea['P_F_aut'])
    P_aut_QC = np.asarray(data_sea['P_F_QC_aut'])    
    SW_IN_aut	 = np.asarray(data_sea['SW_IN_F_aut'])
    SW_IN_aut_QC = np.asarray(data_sea['SW_IN_F_QC_aut'])
    VPD_aut	 = np.asarray(data_sea['VPD_F_aut'])
    VPD_aut_QC = np.asarray(data_sea['VPD_F_QC_aut'])
    TS_MDS_1_aut	 = np.asarray(data_sea['TS_F_MDS_1_aut'])
    TS_MDS_1_aut_QC = np.asarray(data_sea['TS_F_MDS_1_QC_aut'])
    TS_MDS_2_aut	 = np.asarray(data_sea['TS_F_MDS_2_aut'])
    TS_MDS_2_aut_QC = np.asarray(data_sea['TS_F_MDS_2_QC_aut'])
    SWC_MDS_1_aut	 = np.asarray(data_sea['SWC_F_MDS_1_aut'])
    SWC_MDS_1_aut_QC = np.asarray(data_sea['SWC_F_MDS_1_QC_aut'])
    SWC_MDS_2_aut	 = np.asarray(data_sea['SWC_F_MDS_2_aut'])
    SWC_MDS_2_aut_QC = np.asarray(data_sea['SWC_F_MDS_2_QC_aut'])    
    NEE_VUT_REF_aut	 = np.asarray(data_sea['NEE_VUT_REF_aut'])*91
    NEE_VUT_REF_QC_aut = np.asarray(data_sea['NEE_VUT_REF_QC_aut'])
    GPP_NT_VUT_REF_aut	 = np.asarray(data_sea['GPP_NT_VUT_REF_aut'])*91
    RECO_NT_VUT_REF_aut	 = np.asarray(data_sea['RECO_NT_VUT_REF_aut'])*91
    LE_F_MDS_aut	 = np.asarray(data_sea['LE_F_MDS_aut'])
    LE_F_MDS_QC_aut	 = np.asarray(data_sea['LE_F_MDS_QC_aut'])
    
    
    TA_wit = np.asarray(data_sea['TA_F_wit'])
    TA_wit_QC = np.asarray(data_sea['TA_F_QC_wit'])
    P_wit = np.asarray(data_sea['P_F_wit'])
    P_wit_QC = np.asarray(data_sea['P_F_QC_wit'])    
    SW_IN_wit	 = np.asarray(data_sea['SW_IN_F_wit'])
    SW_IN_wit_QC = np.asarray(data_sea['SW_IN_F_QC_wit'])
    VPD_wit	 = np.asarray(data_sea['VPD_F_wit'])
    VPD_wit_QC = np.asarray(data_sea['VPD_F_QC_wit'])
    TS_MDS_1_wit	 = np.asarray(data_sea['TS_F_MDS_1_wit'])
    TS_MDS_1_wit_QC = np.asarray(data_sea['TS_F_MDS_1_QC_wit'])
    TS_MDS_2_wit	 = np.asarray(data_sea['TS_F_MDS_2_wit'])
    TS_MDS_2_wit_QC = np.asarray(data_sea['TS_F_MDS_2_QC_wit'])
    SWC_MDS_1_wit	 = np.asarray(data_sea['SWC_F_MDS_1_wit'])
    SWC_MDS_1_wit_QC = np.asarray(data_sea['SWC_F_MDS_1_QC_wit'])
    SWC_MDS_2_wit	 = np.asarray(data_sea['SWC_F_MDS_2_wit'])
    SWC_MDS_2_wit_QC = np.asarray(data_sea['SWC_F_MDS_2_QC_wit'])    
    NEE_VUT_REF_wit	 = np.asarray(data_sea['NEE_VUT_REF_wit'])*90
    NEE_VUT_REF_QC_wit = np.asarray(data_sea['NEE_VUT_REF_QC_wit'])
    GPP_NT_VUT_REF_wit	 = np.asarray(data_sea['GPP_NT_VUT_REF_wit'])*90
    RECO_NT_VUT_REF_wit	 = np.asarray(data_sea['RECO_NT_VUT_REF_wit'])*90
    LE_F_MDS_wit	 = np.asarray(data_sea['LE_F_MDS_wit'])
    LE_F_MDS_QC_wit	 = np.asarray(data_sea['LE_F_MDS_QC_wit'])
    
    TA_gs = np.asarray(data_sea['TA_F_gs'])
    TA_gs_QC = np.asarray(data_sea['TA_F_QC_gs'])
    P_gs = np.asarray(data_sea['P_F_gs'])
    P_gs_QC = np.asarray(data_sea['P_F_QC_gs'])    
    SW_IN_gs	 = np.asarray(data_sea['SW_IN_F_gs'])
    SW_IN_gs_QC = np.asarray(data_sea['SW_IN_F_QC_gs'])
    VPD_gs	 = np.asarray(data_sea['VPD_F_gs'])
    VPD_gs_QC = np.asarray(data_sea['VPD_F_QC_gs'])
    TS_MDS_1_gs	 = np.asarray(data_sea['TS_F_MDS_1_gs'])
    TS_MDS_1_gs_QC = np.asarray(data_sea['TS_F_MDS_1_QC_gs'])
    TS_MDS_2_gs	 = np.asarray(data_sea['TS_F_MDS_2_gs'])
    TS_MDS_2_gs_QC = np.asarray(data_sea['TS_F_MDS_2_QC_gs'])
    SWC_MDS_1_gs	 = np.asarray(data_sea['SWC_F_MDS_1_gs'])
    SWC_MDS_1_gs_QC = np.asarray(data_sea['SWC_F_MDS_1_QC_gs'])
    SWC_MDS_2_gs	 = np.asarray(data_sea['SWC_F_MDS_2_gs'])
    SWC_MDS_2_gs_QC = np.asarray(data_sea['SWC_F_MDS_2_QC_gs'])    
    NEE_VUT_REF_gs	 = np.asarray(data_sea['NEE_VUT_REF_gs'])*275
    NEE_VUT_REF_QC_gs = np.asarray(data_sea['NEE_VUT_REF_QC_gs'])
    GPP_NT_VUT_REF_gs	 = np.asarray(data_sea['GPP_NT_VUT_REF_gs'])*275
    RECO_NT_VUT_REF_gs	 = np.asarray(data_sea['RECO_NT_VUT_REF_gs'])*275
    LE_F_MDS_gs	 = np.asarray(data_sea['LE_F_MDS_gs'])
    LE_F_MDS_QC_gs	 = np.asarray(data_sea['LE_F_MDS_QC_gs'])
    
    
    
    TA_yr = np.asarray(data_sea['TA_F_yr'])
    TA_yr_QC = np.asarray(data_sea['TA_F_QC_yr'])
    P_yr = np.asarray(data_sea['P_F_yr'])
    P_yr_QC = np.asarray(data_sea['P_F_QC_yr'])    
    SW_IN_yr	 = np.asarray(data_sea['SW_IN_F_yr'])
    SW_IN_yr_QC = np.asarray(data_sea['SW_IN_F_QC_yr'])
    VPD_yr	 = np.asarray(data_sea['VPD_F_yr'])
    VPD_yr_QC = np.asarray(data_sea['VPD_F_QC_yr'])
    TS_MDS_1_yr	 = np.asarray(data_sea['TS_F_MDS_1_yr'])
    TS_MDS_1_yr_QC = np.asarray(data_sea['TS_F_MDS_1_QC_yr'])
    TS_MDS_2_yr	 = np.asarray(data_sea['TS_F_MDS_2_yr'])
    TS_MDS_2_yr_QC = np.asarray(data_sea['TS_F_MDS_2_QC_yr'])
    SWC_MDS_1_yr	 = np.asarray(data_sea['SWC_F_MDS_1_yr'])
    SWC_MDS_1_yr_QC = np.asarray(data_sea['SWC_F_MDS_1_QC_yr'])
    SWC_MDS_2_yr	 = np.asarray(data_sea['SWC_F_MDS_2_yr'])
    SWC_MDS_2_yr_QC = np.asarray(data_sea['SWC_F_MDS_2_QC_yr'])    
    NEE_VUT_REF_yr	 = np.asarray(data_sea['NEE_VUT_REF_yr'])*365
    NEE_VUT_REF_QC_yr = np.asarray(data_sea['NEE_VUT_REF_QC_yr'])
    GPP_NT_VUT_REF_yr	 = np.asarray(data_sea['GPP_NT_VUT_REF_yr'])*365
    RECO_NT_VUT_REF_yr	 = np.asarray(data_sea['RECO_NT_VUT_REF_yr'])*365
    LE_F_MDS_yr	 = np.asarray(data_sea['LE_F_MDS_yr'])
    LE_F_MDS_QC_yr	 = np.asarray(data_sea['LE_F_MDS_QC_yr'])
    

    ##############################################################################
    ### SOS vs temperature #########################
    #### SOS vs temp spring ##################
    out_fig = '%s/%s_SOS_vs_TA_spr_20170527.png' %(out_R2_path,phen_files[i][0:-4])
    plotname = 'SOS_Ta_spr'
    
    slp_SOS_Ta_spr, intp_SOS_Ta_spr, r_SOS_Ta_spr, p_SOS_Ta_spr, std_SOS_Ta_spr \
           = plot_scatter(TA_spr,TA_spr_QC, SOS, phen_QC, "TA_spr","SOS",plotname,out_fig)
    
    SOS_env_slp.append(slp_SOS_Ta_spr)       
    SOS_env_R2.append(r_SOS_Ta_spr)
    SOS_env_P.append(p_SOS_Ta_spr)
    
    #### SOS vs temp winter ##################
    out_fig = '%s/%s_SOS_vs_TA_wit_20170527.png' %(out_R2_path,phen_files[i][0:-4])
    plotname = 'SOS_Ta_wit'
    
    slp_SOS_Ta_wit, intp_SOS_Ta_wit, r_SOS_Ta_wit, p_SOS_Ta_wit, std_SOS_Ta_wit \
           = plot_scatter(TA_wit,TA_wit_QC, SOS, phen_QC, "TA_wit","SOS",plotname,out_fig)
    
    SOS_env_slp.append(slp_SOS_Ta_wit)        
    SOS_env_R2.append(r_SOS_Ta_wit)
    SOS_env_P.append(p_SOS_Ta_wit)
    
    
    #### SOS vs VPD spring ##################
    out_fig = '%s/%s_SOS_vs_VPD_spr_20170527.png' %(out_R2_path,phen_files[i][0:-4])
    plotname = 'SOS_VPD_spr'
    
    slp_SOS_VPD_spr, intp_SOS_VPD_spr, r_SOS_VPD_spr, p_SOS_VPD_spr, std_SOS_VPD_spr \
           = plot_scatter(VPD_spr,VPD_spr_QC, SOS, phen_QC, "VPD_spr","SOS",plotname,out_fig)
    
    SOS_env_slp.append(slp_SOS_VPD_spr)
    SOS_env_R2.append(r_SOS_VPD_spr)
    SOS_env_P.append(p_SOS_VPD_spr)
    #### SOS vs VPD winter ##################
    out_fig = '%s/%s_SOS_vs_VPD_wit_20170527.png' %(out_R2_path,phen_files[i][0:-4])
    plotname = 'SOS_VPD_wit'
    
    slp_SOS_VPD_wit, intp_SOS_VPD_wit, r_SOS_VPD_wit, p_SOS_VPD_wit, std_SOS_VPD_wit \
           = plot_scatter(VPD_wit, VPD_wit_QC, SOS, phen_QC, "VPD_wit","SOS",plotname,out_fig)
    
    SOS_env_slp.append(slp_SOS_VPD_wit)       
    SOS_env_R2.append(r_SOS_VPD_wit)
    SOS_env_P.append(p_SOS_VPD_wit)
    
    
    
    #### SOS vs prec spring ##################
    out_fig = '%s/%s_SOS_vs_P_spr_20170527.png' %(out_R2_path,phen_files[i][0:-4])
    plotname = 'SOS_P_spr'

    slp_SOS_P_spr, intp_SOS_P_spr,r_SOS_P_spr,p_SOS_P_spr,std_SOS_P_spr \
           = plot_scatter(P_spr,P_spr_QC, SOS, phen_QC, "P_spr","SOS",plotname,out_fig)
    
    SOS_env_slp.append(slp_SOS_P_spr)              
    SOS_env_R2.append(r_SOS_P_spr)
    SOS_env_P.append(p_SOS_P_spr)
    
    #### SOS vs prec winter ##################
    out_fig = '%s/%s_SOS_vs_P_wit_20170527.png' %(out_R2_path,phen_files[i][0:-4])
    plotname = 'SOS_P_wit'

    slp_SOS_P_wit, intp_SOS_P_wit,r_SOS_P_wit,p_SOS_P_wit,std_SOS_P_wit \
           = plot_scatter(P_wit,P_wit_QC, SOS, phen_QC, "P_wit","SOS",plotname,out_fig)
    
    SOS_env_slp.append(slp_SOS_P_wit)          
    SOS_env_R2.append(r_SOS_P_wit)
    SOS_env_P.append(p_SOS_P_wit)
    
    
    #### SOS vs SW_IN spring ##################
    out_fig = '%s/%s_SOS_vs_SW_IN_spring_20170527.png' %(out_R2_path,phen_files[i][0:-4])
    plotname = 'SOS_SW_IN_spr'

    
    slp_SOS_SW_IN_spr, intp_SOS_SW_IN_spr,r_SOS_SW_IN_spr,p_SOS_SW_IN_spr,std_SOS_SW_IN_spr \
           = plot_scatter(SW_IN_spr, SW_IN_spr_QC, SOS, phen_QC, "SW_IN_spr","SOS",plotname,out_fig)
    
    SOS_env_slp.append(slp_SOS_SW_IN_spr)          
    SOS_env_R2.append(r_SOS_SW_IN_spr)
    SOS_env_P.append(p_SOS_SW_IN_spr)
    
    
    #### SOS vs SW_IN winter ##################
    out_fig = '%s/%s_SOS_vs_SW_IN_wit_20170527.png' %(out_R2_path,phen_files[i][0:-4])
    plotname = 'SOS_SW_IN_wit'

    
    slp_SOS_SW_IN_wit, intp_SOS_SW_IN_wit,r_SOS_SW_IN_wit,p_SOS_SW_IN_wit,std_SOS_SW_IN_wit \
           = plot_scatter(SW_IN_wit, SW_IN_wit_QC, SOS, phen_QC, "SW_IN_wit","SOS",plotname,out_fig)
    
    SOS_env_slp.append(slp_SOS_SW_IN_wit)         
    SOS_env_R2.append(r_SOS_SW_IN_wit)
    SOS_env_P.append(p_SOS_SW_IN_wit)
    
    #### SOS vs TS_MDS_1 spring ##################
    out_fig = '%s/%s_SOS_vs_TS_MDS_1_spr_20170527.png' %(out_R2_path,phen_files[i][0:-4])
    plotname = 'SOS_TS_MDS_1_spr'

    
    slp_SOS_TS_MDS_1_spr, intp_SOS_TS_MDS_1_spr,r_SOS_TS_MDS_1_spr,p_SOS_TS_MDS_1_spr,std_SOS_TS_MDS_1_spr \
           = plot_scatter(TS_MDS_1_spr, TS_MDS_1_spr_QC, SOS, phen_QC, "TS_MDS_1_spr","SOS",plotname,out_fig)
    
    SOS_env_slp.append(slp_SOS_TS_MDS_1_spr)           
    SOS_env_R2.append(r_SOS_TS_MDS_1_spr)
    SOS_env_P.append(p_SOS_TS_MDS_1_spr)
    
    #### SOS vs TS_MDS_1 winter ##################
    out_fig = '%s/%s_SOS_vs_TS_MDS_1_wit_20170527.png' %(out_R2_path,phen_files[i][0:-4])
    plotname = 'SOS_TS_MDS_1_wit'

    
    slp_SOS_TS_MDS_1_wit, intp_SOS_TS_MDS_1_wit,r_SOS_TS_MDS_1_wit,p_SOS_TS_MDS_1_wit,std_SOS_TS_MDS_1_wit \
           = plot_scatter(TS_MDS_1_wit, TS_MDS_1_wit_QC, SOS, phen_QC, "TS_MDS_1_wit","SOS",plotname,out_fig)
    
    SOS_env_slp.append(slp_SOS_TS_MDS_1_wit)        
    SOS_env_R2.append(r_SOS_TS_MDS_1_wit)
    SOS_env_P.append(p_SOS_TS_MDS_1_wit)
    
    #### SOS vs TS_MDS_2 spring ##################
    out_fig = '%s/%s_SOS_vs_TS_MDS_2_spr_20170527.png' %(out_R2_path,phen_files[i][0:-4])
    plotname = 'SOS_TS_MDS_2_spr'

    
    slp_SOS_TS_MDS_2_spr, intp_SOS_TS_MDS_2_spr,r_SOS_TS_MDS_2_spr,p_SOS_TS_MDS_2_spr,std_SOS_TS_MDS_2_spr \
           = plot_scatter(TS_MDS_2_spr, TS_MDS_2_spr_QC, SOS, phen_QC, "TS_MDS_2_spr","SOS",plotname,out_fig)
    
    SOS_env_slp.append(slp_SOS_TS_MDS_2_spr)             
    SOS_env_R2.append(r_SOS_TS_MDS_2_spr)
    SOS_env_P.append(p_SOS_TS_MDS_2_spr)
    
    #### SOS vs TS_MDS_2 winter ##################
    out_fig = '%s/%s_SOS_vs_TS_MDS_2_wit_20170527.png' %(out_R2_path,phen_files[i][0:-4])
    plotname = 'SOS_TS_MDS_2_wit'

    
    slp_SOS_TS_MDS_2_wit, intp_SOS_TS_MDS_2_wit,r_SOS_TS_MDS_2_wit,p_SOS_TS_MDS_2_wit,std_SOS_TS_MDS_2_wit \
           = plot_scatter(TS_MDS_2_wit, TS_MDS_2_wit_QC, SOS, phen_QC, "TS_MDS_2_wit","SOS",plotname,out_fig)
    
    SOS_env_slp.append(slp_SOS_TS_MDS_2_wit)          
    SOS_env_R2.append(r_SOS_TS_MDS_2_wit)
    SOS_env_P.append(p_SOS_TS_MDS_2_wit)
    
    #### SOS vs SWC_MDS_1 spring ##################
    out_fig = '%s/%s_SOS_vs_SWC_MDS_1_spr_20170527.png' %(out_R2_path,phen_files[i][0:-4])
    plotname = 'SOS_SWC_MDS_1_spr'

    
    slp_SOS_SWC_MDS_1_spr, intp_SOS_SWC_MDS_1_spr,r_SOS_SWC_MDS_1_spr,p_SOS_SWC_MDS_1_spr,std_SOS_SWC_MDS_1_spr \
           = plot_scatter(SWC_MDS_1_spr, SWC_MDS_1_spr_QC, SOS, phen_QC, "SWC_MDS_1_spr","SOS",plotname,out_fig)
    
    SOS_env_slp.append(slp_SOS_SWC_MDS_1_spr)          
    SOS_env_R2.append(r_SOS_SWC_MDS_1_spr)
    SOS_env_P.append(p_SOS_SWC_MDS_1_spr)
    
    #### SOS vs SWC_MDS_1 winter ##################
    out_fig = '%s/%s_SOS_vs_SWC_MDS_1_wit_20170527.png' %(out_R2_path,phen_files[i][0:-4])
    plotname = 'SOS_SWC_MDS_1_wit'

    
    slp_SOS_SWC_MDS_1_wit, intp_SOS_SWC_MDS_1_wit,r_SOS_SWC_MDS_1_wit,p_SOS_SWC_MDS_1_wit,std_SOS_SWC_MDS_1_wit \
           = plot_scatter(SWC_MDS_1_wit, SWC_MDS_1_wit_QC, SOS, phen_QC, "SWC_MDS_1_wit","SOS",plotname,out_fig)
    
    SOS_env_slp.append(slp_SOS_SWC_MDS_1_wit)          
    SOS_env_R2.append(r_SOS_SWC_MDS_1_wit)
    SOS_env_P.append(p_SOS_SWC_MDS_1_wit)
    
    #### SOS vs SWC_MDS_2 spring ##################
    out_fig = '%s/%s_SOS_vs_SWC_MDS_2_spr_20170527.png' %(out_R2_path,phen_files[i][0:-4])
    plotname = 'SOS_SWC_MDS_2_spr'

    
    slp_SOS_SWC_MDS_2_spr, intp_SOS_SWC_MDS_2_spr,r_SOS_SWC_MDS_2_spr,p_SOS_SWC_MDS_2_spr,std_SOS_SWC_MDS_2_spr \
           = plot_scatter(SWC_MDS_2_spr, SWC_MDS_2_spr_QC, SOS, phen_QC, "SWC_MDS_2_spr","SOS",plotname,out_fig)
    
    SOS_env_slp.append(slp_SOS_SWC_MDS_2_spr)          
    SOS_env_R2.append(r_SOS_SWC_MDS_2_spr)
    SOS_env_P.append(p_SOS_SWC_MDS_2_spr)
    
    #### SOS vs SWC_MDS_2 winter ##################
    out_fig = '%s/%s_SOS_vs_SWC_MDS_2_wit_20170527.png' %(out_R2_path,phen_files[i][0:-4])
    plotname = 'SOS_SWC_MDS_2_wit'

    
    slp_SOS_SWC_MDS_2_wit, intp_SOS_SWC_MDS_2_wit,r_SOS_SWC_MDS_2_wit,p_SOS_SWC_MDS_2_wit,std_SOS_SWC_MDS_2_wit \
           = plot_scatter(SWC_MDS_2_wit, SWC_MDS_2_wit_QC, SOS, phen_QC, "SWC_MDS_2_wit","SOS",plotname,out_fig)
    
    SOS_env_slp.append(slp_SOS_SWC_MDS_2_wit)       
    SOS_env_R2.append(r_SOS_SWC_MDS_2_wit)
    SOS_env_P.append(p_SOS_SWC_MDS_2_wit)
    
    #### SOS vs NEE_VUT_REF spring ##################
    out_fig = '%s/%s_SOS_vs_NEE_VUT_REF_spr_20170527.png' %(out_R2_path,phen_files[i][0:-4])
    plotname = 'SOS_NEE_VUT_REF_spr'

    
    slp_SOS_NEE_VUT_REF_spr, intp_SOS_NEE_VUT_REF_spr,r_SOS_NEE_VUT_REF_spr,p_SOS_NEE_VUT_REF_spr,std_SOS_NEE_VUT_REF_spr \
           = plot_scatter_flux(SOS, phen_QC, NEE_VUT_REF_spr, NEE_VUT_REF_QC_spr,"SOS","NEE_VUT_REF_spr",plotname,out_fig)
    
    SOS_env_slp.append(slp_SOS_NEE_VUT_REF_spr)            
    SOS_env_R2.append(r_SOS_NEE_VUT_REF_spr)
    SOS_env_P.append(p_SOS_NEE_VUT_REF_spr)
    
    #### SOS vs NEE_VUT_REF year ##################
    out_fig = '%s/%s_SOS_vs_NEE_VUT_REF_wit_20170527.png' %(out_R2_path,phen_files[i][0:-4])
    plotname = 'SOS_NEE_VUT_REF_yr'

    
    slp_SOS_NEE_VUT_REF_yr, intp_SOS_NEE_VUT_REF_yr,r_SOS_NEE_VUT_REF_yr,p_SOS_NEE_VUT_REF_yr,std_SOS_NEE_VUT_REF_yr \
           = plot_scatter_flux(SOS, phen_QC, NEE_VUT_REF_yr, NEE_VUT_REF_QC_yr,"SOS","NEE_VUT_REF_yr",plotname,out_fig)
    
    SOS_env_slp.append(slp_SOS_NEE_VUT_REF_yr)        
    SOS_env_R2.append(r_SOS_NEE_VUT_REF_yr)
    SOS_env_P.append(p_SOS_NEE_VUT_REF_yr)
    
    
    #### SOS vs GPP_NT_VUT_REF spring ##################
    out_fig = '%s/%s_SOS_vs_GPP_NT_VUT_REF_spr_20170527.png' %(out_R2_path,phen_files[i][0:-4])
    plotname = 'SOS_GPP_NT_VUT_REF_spr'

    
    slp_SOS_GPP_NT_VUT_REF_spr, intp_SOS_GPP_NT_VUT_REF_spr,r_SOS_GPP_NT_VUT_REF_spr,p_SOS_GPP_NT_VUT_REF_spr,std_SOS_GPP_NT_VUT_REF_spr \
           = plot_scatter_flux(SOS, phen_QC, GPP_NT_VUT_REF_spr, NEE_VUT_REF_QC_spr,"SOS","GPP_NT_VUT_REF_spr",plotname,out_fig)
    
    SOS_env_slp.append(slp_SOS_GPP_NT_VUT_REF_spr)        
    SOS_env_R2.append(r_SOS_GPP_NT_VUT_REF_spr)
    SOS_env_P.append(p_SOS_GPP_NT_VUT_REF_spr)
    
    #### SOS vs GPP_NT_VUT_REF year ##################
    out_fig = '%s/%s_SOS_vs_GPP_NT_VUT_REF_yr_20170527.png' %(out_R2_path,phen_files[i][0:-4])
    plotname = 'SOS_GPP_NT_VUT_REF_yr'

    
    slp_SOS_GPP_NT_VUT_REF_yr, intp_SOS_GPP_NT_VUT_REF_yr,r_SOS_GPP_NT_VUT_REF_yr,p_SOS_GPP_NT_VUT_REF_yr,std_SOS_GPP_NT_VUT_REF_yr \
           = plot_scatter_flux(SOS, phen_QC, GPP_NT_VUT_REF_yr, NEE_VUT_REF_QC_yr,"SOS","GPP_NT_VUT_REF_yr",plotname,out_fig)
    
    SOS_env_slp.append(slp_SOS_GPP_NT_VUT_REF_yr)           
    SOS_env_R2.append(r_SOS_GPP_NT_VUT_REF_yr)
    SOS_env_P.append(p_SOS_GPP_NT_VUT_REF_yr)
    
    #### SOS vs RECO_NT_VUT_REF spring ##################
    out_fig = '%s/%s_SOS_vs_RECO_NT_VUT_REF_spr_20170527.png' %(out_R2_path,phen_files[i][0:-4])
    plotname = 'SOS_RECO_NT_VUT_REF_spr'

    
    slp_SOS_RECO_NT_VUT_REF_spr, intp_SOS_RECO_NT_VUT_REF_spr,r_SOS_RECO_NT_VUT_REF_spr,p_SOS_RECO_NT_VUT_REF_spr,std_SOS_RECO_NT_VUT_REF_spr \
           = plot_scatter_flux(SOS, phen_QC, RECO_NT_VUT_REF_spr, NEE_VUT_REF_QC_spr,"SOS","RECO_NT_VUT_REF_spr",plotname,out_fig)
    
    SOS_env_slp.append(slp_SOS_RECO_NT_VUT_REF_spr)       
    SOS_env_R2.append(r_SOS_RECO_NT_VUT_REF_spr)
    SOS_env_P.append(p_SOS_RECO_NT_VUT_REF_spr)
    
    #### SOS vs RECO_NT_VUT_REF year ##################
    out_fig = '%s/%s_SOS_vs_RECO_NT_VUT_REF_yr_20170527.png' %(out_R2_path,phen_files[i][0:-4])
    plotname = 'SOS_RECO_NT_VUT_REF_yr'

    
    slp_SOS_RECO_NT_VUT_REF_yr, intp_SOS_RECO_NT_VUT_REF_yr,r_SOS_RECO_NT_VUT_REF_yr,p_SOS_RECO_NT_VUT_REF_yr,std_SOS_RECO_NT_VUT_REF_yr \
           = plot_scatter_flux(SOS, phen_QC, RECO_NT_VUT_REF_yr, NEE_VUT_REF_QC_yr,"SOS","RECO_NT_VUT_REF_wit",plotname,out_fig)
    
    SOS_env_slp.append(slp_SOS_RECO_NT_VUT_REF_yr)       
    SOS_env_R2.append(r_SOS_RECO_NT_VUT_REF_yr)
    SOS_env_P.append(p_SOS_RECO_NT_VUT_REF_yr)
    
    #### SOS vs LE_F_MDS_spr spring ##################
    out_fig = '%s/%s_SOS_vs_LE_F_MDS_spr_20170527.png' %(out_R2_path,phen_files[i][0:-4])
    plotname = 'SOS_LE_F_MDS_spr'

    
    slp_SOS_LE_F_MDS_spr, intp_SOS_LE_F_MDS_spr,r_SOS_LE_F_MDS_spr,p_SOS_LE_F_MDS_spr,std_SOS_LE_F_MDS_spr \
           = plot_scatter_flux(SOS, phen_QC, LE_F_MDS_spr, LE_F_MDS_QC_spr,"SOS","LE_F_MDS_spr",plotname,out_fig)
    
    SOS_env_slp.append(slp_SOS_LE_F_MDS_spr)              
    SOS_env_R2.append(r_SOS_LE_F_MDS_spr)
    SOS_env_P.append(p_SOS_LE_F_MDS_spr)
    
    #### SOS vs LE_F_MDS winter ##################
    out_fig = '%s/%s_SOS_vs_LE_F_MDS_wit_20170527.png' %(out_R2_path,phen_files[i][0:-4])
    plotname = 'SOS_LE_F_MDS_wit'

    
    slp_SOS_LE_F_MDS_wit, intp_SOS_LE_F_MDS_wit,r_SOS_LE_F_MDS_wit,p_SOS_LE_F_MDS_wit,std_SOS_LE_F_MDS_wit \
           = plot_scatter_flux(SOS, phen_QC, LE_F_MDS_wit, LE_F_MDS_QC_wit,"SOS","LE_F_MDS_wit",plotname,out_fig)
    
    SOS_env_slp.append(slp_SOS_LE_F_MDS_wit)           
    SOS_env_R2.append(r_SOS_LE_F_MDS_wit)
    SOS_env_P.append(p_SOS_LE_F_MDS_wit)
    


    
    ### get average and std for SOS ##############
    avg, std = get_mean_std_phen(SOS, phen_QC)
    SOS_avg_std.append(avg)
    SOS_avg_std.append(std)
    
    # temperature
    avg, std = get_mean_std_var(TA_spr,TA_spr_QC)
    SOS_avg_std.append(avg)
    SOS_avg_std.append(std)
    
    avg, std = get_mean_std_var(TA_wit,TA_wit_QC)
    SOS_avg_std.append(avg)
    SOS_avg_std.append(std)

    
    # VPD
    avg, std = get_mean_std_var(VPD_spr,VPD_spr_QC)
    SOS_avg_std.append(avg)
    SOS_avg_std.append(std)
    
    avg, std = get_mean_std_var(VPD_wit,VPD_wit_QC)
    SOS_avg_std.append(avg)
    SOS_avg_std.append(std)
    
    
    # precipitation
    avg, std = get_mean_std_var(P_spr,P_spr_QC)
    SOS_avg_std.append(avg)
    SOS_avg_std.append(std)
    
    avg, std = get_mean_std_var(P_wit,P_wit_QC)
    SOS_avg_std.append(avg)
    SOS_avg_std.append(std)
    
    
    # SW_IN
    avg, std = get_mean_std_var(SW_IN_spr, SW_IN_spr_QC)
    SOS_avg_std.append(avg)
    SOS_avg_std.append(std)
    
    avg, std = get_mean_std_var(SW_IN_wit, SW_IN_wit_QC)
    SOS_avg_std.append(avg)
    SOS_avg_std.append(std)
    
    # TS_MDS_1
    avg, std = get_mean_std_var(TS_MDS_1_spr, TS_MDS_1_spr_QC)
    SOS_avg_std.append(avg)
    SOS_avg_std.append(std)
    
    avg, std = get_mean_std_var(TS_MDS_1_wit, TS_MDS_1_wit_QC)
    SOS_avg_std.append(avg)
    SOS_avg_std.append(std)
    
    # TS_MDS_2
    avg, std = get_mean_std_var(TS_MDS_2_spr, TS_MDS_2_spr_QC)
    SOS_avg_std.append(avg)
    SOS_avg_std.append(std)
    
    avg, std = get_mean_std_var(TS_MDS_2_wit, TS_MDS_2_wit_QC)
    SOS_avg_std.append(avg)
    SOS_avg_std.append(std)
    
    # SWC_MDS_1
    avg, std = get_mean_std_var(SWC_MDS_1_spr, SWC_MDS_1_spr_QC)
    SOS_avg_std.append(avg)
    SOS_avg_std.append(std)
    
    avg, std = get_mean_std_var(SWC_MDS_1_wit, SWC_MDS_1_wit_QC)
    SOS_avg_std.append(avg)
    SOS_avg_std.append(std)
    
    # SWC_MDS_2
    avg, std = get_mean_std_var(SWC_MDS_2_spr, SWC_MDS_2_spr_QC)
    SOS_avg_std.append(avg)
    SOS_avg_std.append(std)
    
    avg, std = get_mean_std_var(SWC_MDS_2_wit, SWC_MDS_2_wit_QC)
    SOS_avg_std.append(avg)
    SOS_avg_std.append(std)
    
    # NEE_VUT_REF
    avg, std = get_mean_std_var(NEE_VUT_REF_spr, NEE_VUT_REF_QC_spr)
    SOS_avg_std.append(avg)
    SOS_avg_std.append(std)
    
    avg, std = get_mean_std_var(NEE_VUT_REF_wit, NEE_VUT_REF_QC_wit)
    SOS_avg_std.append(avg)
    SOS_avg_std.append(std)
    
    # GPP_NT_VUT_REF
    avg, std = get_mean_std_var(GPP_NT_VUT_REF_spr, NEE_VUT_REF_QC_spr)
    SOS_avg_std.append(avg)
    SOS_avg_std.append(std)
    
    avg, std = get_mean_std_var(GPP_NT_VUT_REF_wit, NEE_VUT_REF_QC_wit)
    SOS_avg_std.append(avg)
    SOS_avg_std.append(std)
    
    # RECO_NT_VUT_REF
    avg, std = get_mean_std_var(RECO_NT_VUT_REF_spr, NEE_VUT_REF_QC_spr)
    SOS_avg_std.append(avg)
    SOS_avg_std.append(std)
    
    avg, std = get_mean_std_var(RECO_NT_VUT_REF_wit, NEE_VUT_REF_QC_wit)
    SOS_avg_std.append(avg)
    SOS_avg_std.append(std)
    
    # LE_F_MDS
    avg, std = get_mean_std_var(LE_F_MDS_spr, LE_F_MDS_QC_spr)
    SOS_avg_std.append(avg)
    SOS_avg_std.append(std)
    
    avg, std = get_mean_std_var(LE_F_MDS_wit, LE_F_MDS_QC_wit)
    SOS_avg_std.append(avg)
    SOS_avg_std.append(std)
 

    
    ### get MK trend of phen and envr factors ##############
    ### SOS  ########
    slp, intp, P_value = Trend_phen(years,SOS, phen_QC)
    SOS_env_MK_trend_slp.append(slp)
    SOS_env_MK_trend_intp.append(intp)
    SOS_env_MK_trend_P.append(P_value)
    
    # temperature
    slp, intp, P_value = Trend_var(years,TA_spr,TA_spr_QC)
    SOS_env_MK_trend_slp.append(slp)
    SOS_env_MK_trend_intp.append(intp)
    SOS_env_MK_trend_P.append(P_value)
    
    slp, intp, P_value = Trend_var(years,TA_wit,TA_wit_QC)
    SOS_env_MK_trend_slp.append(slp)
    SOS_env_MK_trend_intp.append(intp)
    SOS_env_MK_trend_P.append(P_value)
    
    
    # VPD
    slp, intp, P_value = Trend_var(years,VPD_spr,VPD_spr_QC)
    SOS_env_MK_trend_slp.append(slp)
    SOS_env_MK_trend_intp.append(intp)
    SOS_env_MK_trend_P.append(P_value)
    
    slp, intp, P_value = Trend_var(years,VPD_wit,VPD_wit_QC)
    SOS_env_MK_trend_slp.append(slp)
    SOS_env_MK_trend_intp.append(intp)
    SOS_env_MK_trend_P.append(P_value)
    
    # precipitation
    slp, intp, P_value = Trend_var(years,P_spr,P_spr_QC)
    SOS_env_MK_trend_slp.append(slp)
    SOS_env_MK_trend_intp.append(intp)
    SOS_env_MK_trend_P.append(P_value)
    
    slp, intp, P_value = Trend_var(years,P_wit,P_wit_QC)
    SOS_env_MK_trend_slp.append(slp)
    SOS_env_MK_trend_intp.append(intp)
    SOS_env_MK_trend_P.append(P_value)
    
    # SW_IN
    slp, intp, P_value = Trend_var(years,SW_IN_spr, SW_IN_spr_QC)
    SOS_env_MK_trend_slp.append(slp)
    SOS_env_MK_trend_intp.append(intp)
    SOS_env_MK_trend_P.append(P_value)
    
    slp, intp, P_value = Trend_var(years,SW_IN_wit, SW_IN_wit_QC)
    SOS_env_MK_trend_slp.append(slp)
    SOS_env_MK_trend_intp.append(intp)
    SOS_env_MK_trend_P.append(P_value)
    
    # TS_MDS_1
    slp, intp, P_value = Trend_var(years,TS_MDS_1_spr, TS_MDS_1_spr_QC)
    SOS_env_MK_trend_slp.append(slp)
    SOS_env_MK_trend_intp.append(intp)
    SOS_env_MK_trend_P.append(P_value)
    
    slp, intp, P_value = Trend_var(years,TS_MDS_1_wit, TS_MDS_1_wit_QC)
    SOS_env_MK_trend_slp.append(slp)
    SOS_env_MK_trend_intp.append(intp)
    SOS_env_MK_trend_P.append(P_value)
    
    
    # TS_MDS_2
    slp, intp, P_value = Trend_var(years,TS_MDS_2_spr, TS_MDS_2_spr_QC)
    SOS_env_MK_trend_slp.append(slp)
    SOS_env_MK_trend_intp.append(intp)
    SOS_env_MK_trend_P.append(P_value)
    
    slp, intp, P_value = Trend_var(years,TS_MDS_2_wit, TS_MDS_2_wit_QC)
    SOS_env_MK_trend_slp.append(slp)
    SOS_env_MK_trend_intp.append(intp)
    SOS_env_MK_trend_P.append(P_value)
    
    
    # SWC_MDS_1
    slp, intp, P_value = Trend_var(years,SWC_MDS_1_spr, SWC_MDS_1_spr_QC)
    SOS_env_MK_trend_slp.append(slp)
    SOS_env_MK_trend_intp.append(intp)
    SOS_env_MK_trend_P.append(P_value)
    
    slp, intp, P_value = Trend_var(years,SWC_MDS_1_wit, SWC_MDS_1_wit_QC)
    SOS_env_MK_trend_slp.append(slp)
    SOS_env_MK_trend_intp.append(intp)
    SOS_env_MK_trend_P.append(P_value)

    
    # SWC_MDS_2
    slp, intp, P_value = Trend_var(years,SWC_MDS_2_spr, SWC_MDS_2_spr_QC)
    SOS_env_MK_trend_slp.append(slp)
    SOS_env_MK_trend_intp.append(intp)
    SOS_env_MK_trend_P.append(P_value)
    
    slp, intp, P_value = Trend_var(years,SWC_MDS_2_wit, SWC_MDS_2_wit_QC)
    SOS_env_MK_trend_slp.append(slp)
    SOS_env_MK_trend_intp.append(intp)
    SOS_env_MK_trend_P.append(P_value)
    
    
    # NEE_VUT_REF
    slp, intp, P_value = Trend_var(years,NEE_VUT_REF_spr, NEE_VUT_REF_QC_spr)
    SOS_env_MK_trend_slp.append(slp)
    SOS_env_MK_trend_intp.append(intp)
    SOS_env_MK_trend_P.append(P_value)
    
    slp, intp, P_value = Trend_var(years,NEE_VUT_REF_wit, NEE_VUT_REF_QC_wit)
    SOS_env_MK_trend_slp.append(slp)
    SOS_env_MK_trend_intp.append(intp)
    SOS_env_MK_trend_P.append(P_value)
    
        
    # GPP_NT_VUT_REF
    slp, intp, P_value = Trend_var(years,GPP_NT_VUT_REF_spr, NEE_VUT_REF_QC_spr)
    SOS_env_MK_trend_slp.append(slp)
    SOS_env_MK_trend_intp.append(intp)
    SOS_env_MK_trend_P.append(P_value)
    
    slp, intp, P_value = Trend_var(years,GPP_NT_VUT_REF_wit, NEE_VUT_REF_QC_wit)
    SOS_env_MK_trend_slp.append(slp)
    SOS_env_MK_trend_intp.append(intp)
    SOS_env_MK_trend_P.append(P_value)
    
    
    # RECO_NT_VUT_REF
    slp, intp, P_value = Trend_var(years,RECO_NT_VUT_REF_spr, NEE_VUT_REF_QC_spr)
    SOS_env_MK_trend_slp.append(slp)
    SOS_env_MK_trend_intp.append(intp)
    SOS_env_MK_trend_P.append(P_value)
    
    slp, intp, P_value = Trend_var(years,RECO_NT_VUT_REF_wit, NEE_VUT_REF_QC_wit)
    SOS_env_MK_trend_slp.append(slp)
    SOS_env_MK_trend_intp.append(intp)
    SOS_env_MK_trend_P.append(P_value)
    
    
    # LE_F_MDS
    slp, intp, P_value = Trend_var(years,LE_F_MDS_spr, LE_F_MDS_QC_spr)
    SOS_env_MK_trend_slp.append(slp)
    SOS_env_MK_trend_intp.append(intp)
    SOS_env_MK_trend_P.append(P_value)
    
    slp, intp, P_value = Trend_var(years,LE_F_MDS_wit, LE_F_MDS_QC_wit)
    SOS_env_MK_trend_slp.append(slp)
    SOS_env_MK_trend_intp.append(intp)
    SOS_env_MK_trend_P.append(P_value)
    
    
    ##############################################################################
    ### EOS vs temperature #########################
    
    #### EOS vs temp summer ##################
    out_fig = '%s/%s_EOS_vs_TA_smr_20170527.png' %(out_R2_path,phen_files[i][0:-4])
    plotname = 'EOS_Ta_smr'
    
    slp_EOS_Ta_smr, intp_EOS_Ta_smr, r_EOS_Ta_smr, p_EOS_Ta_smr, std_EOS_Ta_smr \
           = plot_scatter(TA_smr,TA_smr_QC, EOS, phen_QC, "TA_smr","EOS",plotname,out_fig)
    
    EOS_env_slp.append(slp_EOS_Ta_smr)       
    EOS_env_R2.append(r_EOS_Ta_smr)
    EOS_env_P.append(p_EOS_Ta_smr)
    
    #### EOS vs temp autumn ##################
    out_fig = '%s/%s_EOS_vs_TA_aut_20170527.png' %(out_R2_path,phen_files[i][0:-4])
    plotname = 'EOS_Ta_aut'
    
    slp_EOS_Ta_aut, intp_EOS_Ta_aut, r_EOS_Ta_aut, p_EOS_Ta_aut, std_EOS_Ta_aut \
           = plot_scatter(TA_aut, TA_aut_QC, EOS, phen_QC,"TA_aut", "EOS",plotname,out_fig)
    
    EOS_env_slp.append(slp_EOS_Ta_aut)             
    EOS_env_R2.append(r_EOS_Ta_aut)
    EOS_env_P.append(p_EOS_Ta_aut)
    
        
    #### EOS vs VPD summer ##################
    out_fig = '%s/%s_EOS_vs_VPD_smr_20170527.png' %(out_R2_path,phen_files[i][0:-4])
    plotname = 'EOS_VPD_smr'
    
    slp_EOS_VPD_smr, intp_EOS_VPD_smr,r_EOS_VPD_smr,p_EOS_VPD_smr,std_EOS_VPD_smr \
           = plot_scatter(VPD_smr, VPD_smr_QC, EOS, phen_QC, "VPD_smr","EOS",plotname,out_fig)
    
    EOS_env_slp.append(slp_EOS_VPD_smr)    
    EOS_env_R2.append(r_EOS_VPD_smr)
    EOS_env_P.append(p_EOS_VPD_smr)
    
    #### EOS vs VPD autumn ##################
    out_fig = '%s/%s_EOS_vs_VPD_aut_20170527.png' %(out_R2_path,phen_files[i][0:-4])
    plotname = 'EOS_VPD_aut'
    
    slp_EOS_VPD_aut, intp_EOS_VPD_aut,r_EOS_VPD_aut,p_EOS_VPD_aut,std_EOS_VPD_aut \
           = plot_scatter(VPD_aut, VPD_aut_QC, EOS, phen_QC, "VPD_aut","EOS",plotname,out_fig)
           
    EOS_env_slp.append(slp_EOS_VPD_aut)    
    EOS_env_R2.append(r_EOS_VPD_aut)
    EOS_env_P.append(p_EOS_VPD_aut)
    
        
    #### EOS vs prec summer ##################
    out_fig = '%s/%s_EOS_vs_P_smr_20170527.png' %(out_R2_path,phen_files[i][0:-4])
    plotname = 'EOS_P_smr'

    slp_EOS_P_smr, intp_EOS_P_smr,r_EOS_P_smr,p_EOS_P_smr,std_EOS_P_smr \
           = plot_scatter(P_smr, P_smr_QC, EOS, phen_QC, "P_smr","EOS",plotname,out_fig)
    
    EOS_env_slp.append(slp_EOS_P_smr)           
    EOS_env_R2.append(r_EOS_P_smr)
    EOS_env_P.append(p_EOS_P_smr)
    
    #### EOS vs prec autumn ##################
    out_fig = '%s/%s_EOS_vs_P_aut_20170527.png' %(out_R2_path,phen_files[i][0:-4])
    plotname = 'EOS_P_aut'

    slp_EOS_P_aut, intp_EOS_P_aut,r_EOS_P_aut,p_EOS_P_aut,std_EOS_P_aut \
           = plot_scatter(P_aut, P_aut_QC, EOS, phen_QC, "P_aut","EOS",plotname,out_fig)
    
    EOS_env_slp.append(slp_EOS_P_aut)       
    EOS_env_R2.append(r_EOS_P_aut)
    EOS_env_P.append(p_EOS_P_aut)
    
    
    #### EOS vs SW_IN summer ##################
    out_fig = '%s/%s_EOS_vs_SW_IN_smr_20170527.png' %(out_R2_path,phen_files[i][0:-4])
    plotname = 'EOS_SW_IN_smr'

    
    slp_EOS_SW_IN_smr, intp_EOS_SW_IN_smr,r_EOS_SW_IN_smr,p_EOS_SW_IN_smr,std_EOS_SW_IN_smr \
           = plot_scatter(SW_IN_smr, SW_IN_smr_QC, EOS, phen_QC, "SW_IN_smr","EOS",plotname,out_fig)
    
    EOS_env_slp.append(slp_EOS_SW_IN_smr)        
    EOS_env_R2.append(r_EOS_SW_IN_smr)
    EOS_env_P.append(p_EOS_SW_IN_smr)
    
    #### EOS vs SW_IN autumn ##################
    out_fig = '%s/%s_EOS_vs_SW_IN_aut_20170527.png' %(out_R2_path,phen_files[i][0:-4])
    plotname = 'EOS_SW_IN_aut'

    
    slp_EOS_SW_IN_aut, intp_EOS_SW_IN_aut,r_EOS_SW_IN_aut,p_EOS_SW_IN_aut,std_EOS_SW_IN_aut \
           = plot_scatter(SW_IN_aut, SW_IN_aut_QC, EOS, phen_QC,"SW_IN_aut", "EOS",plotname,out_fig)
    
    EOS_env_slp.append(slp_EOS_SW_IN_aut)       
    EOS_env_R2.append(r_EOS_SW_IN_aut)
    EOS_env_P.append(p_EOS_SW_IN_aut)
    
    #### EOS vs TS_MDS_1 summer ##################
    out_fig = '%s/%s_EOS_vs_TS_MDS_1_smr_20170527.png' %(out_R2_path,phen_files[i][0:-4])
    plotname = 'EOS_TS_MDS_1_smr'

    
    slp_EOS_TS_MDS_1_smr, intp_EOS_TS_MDS_1_smr,r_EOS_TS_MDS_1_smr,p_EOS_TS_MDS_1_smr,std_EOS_TS_MDS_1_smr \
           = plot_scatter(TS_MDS_1_smr, TS_MDS_1_smr_QC, EOS, phen_QC, "TS_MDS_1_smr", "EOS",plotname,out_fig)
    
    EOS_env_slp.append(slp_EOS_TS_MDS_1_smr)           
    EOS_env_R2.append(r_EOS_TS_MDS_1_smr)
    EOS_env_P.append(p_EOS_TS_MDS_1_smr)
    
    #### EOS vs TS_MDS_1 autumn ##################
    out_fig = '%s/%s_EOS_vs_TS_MDS_1_aut_20170527.png' %(out_R2_path,phen_files[i][0:-4])
    plotname = 'EOS_TS_MDS_1_aut'

    
    slp_EOS_TS_MDS_1_aut, intp_EOS_TS_MDS_1_aut,r_EOS_TS_MDS_1_aut,p_EOS_TS_MDS_1_aut,std_EOS_TS_MDS_1_aut \
           = plot_scatter(TS_MDS_1_aut, TS_MDS_1_aut_QC, EOS, phen_QC, "TS_MDS_1_aut", "EOS",plotname,out_fig)
    
    EOS_env_slp.append(slp_EOS_TS_MDS_1_aut)       
    EOS_env_R2.append(r_EOS_TS_MDS_1_aut)
    EOS_env_P.append(p_EOS_TS_MDS_1_aut)
    
    #### EOS vs TS_MDS_2 summer ##################
    out_fig = '%s/%s_EOS_vs_TS_MDS_2_smr_20170527.png' %(out_R2_path,phen_files[i][0:-4])
    plotname = 'EOS_TS_MDS_2_smr'

    
    slp_EOS_TS_MDS_2_smr, intp_EOS_TS_MDS_2_smr,r_EOS_TS_MDS_2_smr,p_EOS_TS_MDS_2_smr,std_EOS_TS_MDS_2_smr \
           = plot_scatter(TS_MDS_2_smr, TS_MDS_2_smr_QC, EOS, phen_QC, "TS_MDS_2_smr","EOS",plotname,out_fig)
    
    EOS_env_slp.append(slp_EOS_TS_MDS_2_smr)        
    EOS_env_R2.append(r_EOS_TS_MDS_2_smr)
    EOS_env_P.append(p_EOS_TS_MDS_2_smr)
    
    #### EOS vs TS_MDS_2 autumn ##################
    out_fig = '%s/%s_EOS_vs_TS_MDS_2_aut_20170527.png' %(out_R2_path,phen_files[i][0:-4])
    plotname = 'EOS_TS_MDS_2_aut'

    
    slp_EOS_TS_MDS_2_aut, intp_EOS_TS_MDS_2_aut,r_EOS_TS_MDS_2_aut,p_EOS_TS_MDS_2_aut,std_EOS_TS_MDS_2_aut \
           = plot_scatter(TS_MDS_2_aut, TS_MDS_2_aut_QC, EOS, phen_QC, "TS_MDS_2_aut","EOS",plotname,out_fig)
    
    EOS_env_slp.append(slp_EOS_TS_MDS_2_aut)        
    EOS_env_R2.append(r_EOS_TS_MDS_2_aut)
    EOS_env_P.append(p_EOS_TS_MDS_2_aut)
    
    #### EOS vs SWC_MDS_1 summer ##################
    out_fig = '%s/%s_EOS_vs_SWC_MDS_1_smr_20170527.png' %(out_R2_path,phen_files[i][0:-4])
    plotname = 'EOS_SWC_MDS_1_smr'

    
    slp_EOS_SWC_MDS_1_smr, intp_EOS_SWC_MDS_1_smr,r_EOS_SWC_MDS_1_smr,p_EOS_SWC_MDS_1_smr,std_EOS_SWC_MDS_1_smr \
           = plot_scatter(SWC_MDS_1_smr, SWC_MDS_1_smr_QC, EOS, phen_QC,"SWC_MDS_1_aut", "EOS",plotname,out_fig)
    
    EOS_env_slp.append(slp_EOS_SWC_MDS_1_smr)              
    EOS_env_R2.append(r_EOS_SWC_MDS_1_smr)
    EOS_env_P.append(p_EOS_SWC_MDS_1_smr)
    
    #### EOS vs SWC_MDS_1 autumn ##################
    out_fig = '%s/%s_EOS_vs_SWC_MDS_1_aut_20170527.png' %(out_R2_path,phen_files[i][0:-4])
    plotname = 'EOS_SWC_MDS_1_aut'

    
    slp_EOS_SWC_MDS_1_aut, intp_EOS_SWC_MDS_1_aut,r_EOS_SWC_MDS_1_aut,p_EOS_SWC_MDS_1_aut,std_EOS_SWC_MDS_1_aut \
           = plot_scatter(SWC_MDS_1_aut, SWC_MDS_1_aut_QC, EOS, phen_QC, "SWC_MDS_1_aut","EOS",plotname,out_fig)
    
    EOS_env_slp.append(slp_EOS_SWC_MDS_1_aut)       
    EOS_env_R2.append(r_EOS_SWC_MDS_1_aut)
    EOS_env_P.append(p_EOS_SWC_MDS_1_aut)
    
    #### EOS vs SWC_MDS_2 summer ##################
    out_fig = '%s/%s_EOS_vs_SWC_MDS_2_smr_20170527.png' %(out_R2_path,phen_files[i][0:-4])
    plotname = 'EOS_SWC_MDS_2_smr'

    
    slp_EOS_SWC_MDS_2_smr, intp_EOS_SWC_MDS_2_smr,r_EOS_SWC_MDS_2_smr,p_EOS_SWC_MDS_2_smr,std_EOS_SWC_MDS_2_smr \
           = plot_scatter(SWC_MDS_2_smr, SWC_MDS_2_smr_QC, EOS, phen_QC, "SWC_MDS_2_smr", "EOS",plotname,out_fig)
    
    EOS_env_slp.append(slp_EOS_SWC_MDS_2_smr)        
    EOS_env_R2.append(r_EOS_SWC_MDS_2_smr)
    EOS_env_P.append(p_EOS_SWC_MDS_2_smr)
    
    #### EOS vs SWC_MDS_2 autumn ##################
    out_fig = '%s/%s_EOS_vs_SWC_MDS_2_aut_20170527.png' %(out_R2_path,phen_files[i][0:-4])
    plotname = 'EOS_SWC_MDS_2_aut'

    
    slp_EOS_SWC_MDS_2_aut, intp_EOS_SWC_MDS_2_aut,r_EOS_SWC_MDS_2_aut,p_EOS_SWC_MDS_2_aut,std_EOS_SWC_MDS_2_aut \
           = plot_scatter(SWC_MDS_2_aut, SWC_MDS_2_aut_QC, EOS, phen_QC, "SWC_MDS_2_aut", "EOS",plotname,out_fig)
    
    EOS_env_slp.append(slp_EOS_SWC_MDS_2_aut)           
    EOS_env_R2.append(r_EOS_SWC_MDS_2_aut)
    EOS_env_P.append(p_EOS_SWC_MDS_2_aut)
    
    
    #### EOS vs NEE_VUT_REF autumn ##################
    out_fig = '%s/%s_EOS_vs_NEE_VUT_REF_aut_20170527.png' %(out_R2_path,phen_files[i][0:-4])
    plotname = 'EOS_NEE_VUT_REF_aut'

    
    slp_EOS_NEE_VUT_REF_aut, intp_EOS_NEE_VUT_REF_aut,r_EOS_NEE_VUT_REF_aut,p_EOS_NEE_VUT_REF_aut,std_EOS_NEE_VUT_REF_aut \
           = plot_scatter_flux(EOS, phen_QC, NEE_VUT_REF_aut, NEE_VUT_REF_QC_aut,"EOS","NEE_VUT_REF_aut",plotname,out_fig)
    
    EOS_env_slp.append(slp_EOS_NEE_VUT_REF_aut)       
    EOS_env_R2.append(r_EOS_NEE_VUT_REF_aut)
    EOS_env_P.append(p_EOS_NEE_VUT_REF_aut)
    
    #### EOS vs NEE_VUT_REF year ##################
    out_fig = '%s/%s_EOS_vs_NEE_VUT_REF_yr_20170527.png' %(out_R2_path,phen_files[i][0:-4])
    plotname = 'EOS_NEE_VUT_REF_yr'

    
    slp_EOS_NEE_VUT_REF_yr, intp_EOS_NEE_VUT_REF_yr,r_EOS_NEE_VUT_REF_yr,p_EOS_NEE_VUT_REF_yr,std_EOS_NEE_VUT_REF_yr \
           = plot_scatter_flux(EOS, phen_QC, NEE_VUT_REF_yr, NEE_VUT_REF_QC_yr,"EOS","NEE_VUT_REF_yr",plotname,out_fig)
    
    EOS_env_slp.append(slp_EOS_NEE_VUT_REF_yr)        
    EOS_env_R2.append(r_EOS_NEE_VUT_REF_yr)
    EOS_env_P.append(p_EOS_NEE_VUT_REF_yr)
    
    
    #### EOS vs GPP_NT_VUT_REF autumn ##################
    out_fig = '%s/%s_EOS_vs_GPP_NT_VUT_REF_aut_20170527.png' %(out_R2_path,phen_files[i][0:-4])
    plotname = 'EOS_GPP_NT_VUT_REF_aut'

    
    slp_EOS_GPP_NT_VUT_REF_aut, intp_EOS_GPP_NT_VUT_REF_aut,r_EOS_GPP_NT_VUT_REF_aut,p_EOS_GPP_NT_VUT_REF_aut,std_EOS_GPP_NT_VUT_REF_aut \
           = plot_scatter_flux(EOS, phen_QC, GPP_NT_VUT_REF_aut, NEE_VUT_REF_QC_aut,"EOS","GPP_NT_VUT_REF_aut",plotname,out_fig)
    
    EOS_env_slp.append(slp_EOS_GPP_NT_VUT_REF_aut)       
    EOS_env_R2.append(r_EOS_GPP_NT_VUT_REF_aut)
    EOS_env_P.append(p_EOS_GPP_NT_VUT_REF_aut)
    
    #### EOS vs GPP_NT_VUT_REF year ##################
    out_fig = '%s/%s_EOS_vs_GPP_NT_VUT_REF_yr_20170527.png' %(out_R2_path,phen_files[i][0:-4])
    plotname = 'EOS_GPP_NT_VUT_REF_yr'

    
    slp_EOS_GPP_NT_VUT_REF_yr, intp_EOS_GPP_NT_VUT_REF_yr,r_EOS_GPP_NT_VUT_REF_yr,p_EOS_GPP_NT_VUT_REF_yr,std_EOS_GPP_NT_VUT_REF_yr \
           = plot_scatter_flux(EOS, phen_QC, GPP_NT_VUT_REF_yr, NEE_VUT_REF_QC_yr,"EOS","GPP_NT_VUT_REF_yr",plotname,out_fig)
    
    EOS_env_slp.append(slp_EOS_GPP_NT_VUT_REF_yr)       
    EOS_env_R2.append(r_EOS_GPP_NT_VUT_REF_yr)
    EOS_env_P.append(p_EOS_GPP_NT_VUT_REF_yr)
    
    
    #### EOS vs RECO_NT_VUT_REF autumn ##################
    out_fig = '%s/%s_EOS_vs_RECO_NT_VUT_REF_aut_20170527.png' %(out_R2_path,phen_files[i][0:-4])
    plotname = 'EOS_RECO_NT_VUT_REF_aut'

    
    slp_EOS_RECO_NT_VUT_REF_aut, intp_EOS_RECO_NT_VUT_REF_aut,r_EOS_RECO_NT_VUT_REF_aut,p_EOS_RECO_NT_VUT_REF_aut,std_EOS_RECO_NT_VUT_REF_aut \
           = plot_scatter_flux(EOS, phen_QC, RECO_NT_VUT_REF_aut, NEE_VUT_REF_QC_aut,"EOS","RECO_NT_VUT_REF_aut",plotname,out_fig)
    
    EOS_env_slp.append(slp_EOS_RECO_NT_VUT_REF_aut)        
    EOS_env_R2.append(r_EOS_RECO_NT_VUT_REF_aut)
    EOS_env_P.append(p_EOS_RECO_NT_VUT_REF_aut)
    
    #### EOS vs RECO_NT_VUT_REF year ##################
    out_fig = '%s/%s_EOS_vs_RECO_NT_VUT_REF_yr_20170527.png' %(out_R2_path,phen_files[i][0:-4])
    plotname = 'EOS_RECO_NT_VUT_REF_yr'

    
    slp_EOS_RECO_NT_VUT_REF_yr, intp_EOS_RECO_NT_VUT_REF_yr,r_EOS_RECO_NT_VUT_REF_yr,p_EOS_RECO_NT_VUT_REF_yr,std_EOS_RECO_NT_VUT_REF_yr \
           = plot_scatter_flux(EOS, phen_QC, RECO_NT_VUT_REF_yr, NEE_VUT_REF_QC_yr,"EOS","RECO_NT_VUT_REF_yr",plotname,out_fig)
    
    EOS_env_slp.append(slp_EOS_RECO_NT_VUT_REF_yr)       
    EOS_env_R2.append(r_EOS_RECO_NT_VUT_REF_yr)
    EOS_env_P.append(p_EOS_RECO_NT_VUT_REF_yr)
    
    #### EOS vs LE_F_MDS autumn ##################
    out_fig = '%s/%s_EOS_vs_LE_F_MDS_aut_20170527.png' %(out_R2_path,phen_files[i][0:-4])
    plotname = 'SOS_LE_F_MDS_aut'

    
    slp_EOS_LE_F_MDS_aut, intp_EOS_LE_F_MDS_aut,r_EOS_LE_F_MDS_aut,p_EOS_LE_F_MDS_aut,std_EOS_LE_F_MDS_aut \
           = plot_scatter_flux(EOS, phen_QC, LE_F_MDS_aut, LE_F_MDS_QC_aut,"EOS","LE_F_MDS_aut",plotname,out_fig)
    
    EOS_env_slp.append(slp_EOS_LE_F_MDS_aut)       
    EOS_env_R2.append(r_EOS_LE_F_MDS_aut)
    EOS_env_P.append(p_EOS_LE_F_MDS_aut)
    
    
    #### EOS vs LE_F_MDS_smr year ##################
    out_fig = '%s/%s_EOS_vs_LE_F_MDS_smr_20170527.png' %(out_R2_path,phen_files[i][0:-4])
    plotname = 'EOS_LE_F_MDS_smr'

    
    slp_EOS_LE_F_MDS_smr, intp_EOS_LE_F_MDS_smr,r_EOS_LE_F_MDS_smr,p_EOS_LE_F_MDS_smr,std_EOS_LE_F_MDS_smr \
           = plot_scatter_flux(EOS, phen_QC, LE_F_MDS_smr, LE_F_MDS_QC_smr,"EOS","LE_F_MDS_smr",plotname,out_fig)
    
    EOS_env_slp.append(slp_EOS_RECO_NT_VUT_REF_aut)       
    EOS_env_R2.append(r_EOS_LE_F_MDS_smr)
    EOS_env_P.append(p_EOS_LE_F_MDS_smr)
    
    ### get average and std for EOS ##############
    avg, std = get_mean_std_phen(EOS, phen_QC)
    EOS_avg_std.append(avg)
    EOS_avg_std.append(std)
    
    # temperature
    avg, std = get_mean_std_var(TA_smr,TA_smr_QC)
    EOS_avg_std.append(avg)
    EOS_avg_std.append(std)
    
    avg, std = get_mean_std_var(TA_aut,TA_aut_QC)
    EOS_avg_std.append(avg)
    EOS_avg_std.append(std)
   
    
    # VPD
    avg, std = get_mean_std_var(VPD_smr,VPD_smr_QC)
    EOS_avg_std.append(avg)
    EOS_avg_std.append(std)
    
    avg, std = get_mean_std_var(VPD_aut,VPD_aut_QC)
    EOS_avg_std.append(avg)
    EOS_avg_std.append(std)
    
    
    # precipitation
    avg, std = get_mean_std_var(P_smr,P_smr_QC)
    EOS_avg_std.append(avg)
    EOS_avg_std.append(std)
    
    avg, std = get_mean_std_var(P_aut,P_aut_QC)
    EOS_avg_std.append(avg)
    EOS_avg_std.append(std)
    
    
    # SW_IN
    avg, std = get_mean_std_var(SW_IN_smr, SW_IN_smr_QC)
    EOS_avg_std.append(avg)
    EOS_avg_std.append(std)
    
    avg, std = get_mean_std_var(SW_IN_aut, SW_IN_aut_QC)
    EOS_avg_std.append(avg)
    EOS_avg_std.append(std)
    
    # TS_MDS_1
    avg, std = get_mean_std_var(TS_MDS_1_smr, TS_MDS_1_smr_QC)
    EOS_avg_std.append(avg)
    EOS_avg_std.append(std)
    
    avg, std = get_mean_std_var(TS_MDS_1_aut, TS_MDS_1_aut_QC)
    EOS_avg_std.append(avg)
    EOS_avg_std.append(std)
    
    # TS_MDS_2
    avg, std = get_mean_std_var(TS_MDS_2_smr, TS_MDS_2_smr_QC)
    EOS_avg_std.append(avg)
    EOS_avg_std.append(std)
    
    avg, std = get_mean_std_var(TS_MDS_2_aut, TS_MDS_2_aut_QC)
    EOS_avg_std.append(avg)
    EOS_avg_std.append(std)
    
    # SWC_MDS_1
    avg, std = get_mean_std_var(SWC_MDS_1_smr, SWC_MDS_1_smr_QC)
    EOS_avg_std.append(avg)
    EOS_avg_std.append(std)
    
    avg, std = get_mean_std_var(SWC_MDS_1_aut, SWC_MDS_1_aut_QC)
    EOS_avg_std.append(avg)
    EOS_avg_std.append(std)
    
    # SWC_MDS_2
    avg, std = get_mean_std_var(SWC_MDS_2_smr, SWC_MDS_2_smr_QC)
    EOS_avg_std.append(avg)
    EOS_avg_std.append(std)
    
    avg, std = get_mean_std_var(SWC_MDS_2_aut, SWC_MDS_2_aut_QC)
    EOS_avg_std.append(avg)
    EOS_avg_std.append(std)
    
    # NEE_VUT_REF
    avg, std = get_mean_std_var(NEE_VUT_REF_smr, NEE_VUT_REF_QC_smr)
    EOS_avg_std.append(avg)
    EOS_avg_std.append(std)
    
    avg, std = get_mean_std_var(NEE_VUT_REF_aut, NEE_VUT_REF_QC_aut)
    EOS_avg_std.append(avg)
    EOS_avg_std.append(std)
    
    # GPP_NT_VUT_REF
    avg, std = get_mean_std_var(GPP_NT_VUT_REF_smr, NEE_VUT_REF_QC_smr)
    EOS_avg_std.append(avg)
    EOS_avg_std.append(std)
    
    avg, std = get_mean_std_var(GPP_NT_VUT_REF_aut, NEE_VUT_REF_QC_aut)
    EOS_avg_std.append(avg)
    EOS_avg_std.append(std)
    
    # RECO_NT_VUT_REF
    avg, std = get_mean_std_var(RECO_NT_VUT_REF_smr, NEE_VUT_REF_QC_smr)
    EOS_avg_std.append(avg)
    EOS_avg_std.append(std)
    
    avg, std = get_mean_std_var(RECO_NT_VUT_REF_aut, NEE_VUT_REF_QC_aut)
    EOS_avg_std.append(avg)
    EOS_avg_std.append(std)
    
    # LE_F_MDS
    avg, std = get_mean_std_var(LE_F_MDS_smr, LE_F_MDS_QC_smr)
    EOS_avg_std.append(avg)
    EOS_avg_std.append(std)
    
    avg, std = get_mean_std_var(LE_F_MDS_aut, LE_F_MDS_QC_aut)
    EOS_avg_std.append(avg)
    EOS_avg_std.append(std)
   
    
    
    ### get MK trend of EOS and envir factors ##############
    ### EOS ##########
    slp, intp, P_value = Trend_phen(years, EOS, phen_QC)
    EOS_env_MK_trend_slp.append(slp)
    EOS_env_MK_trend_intp.append(intp)
    EOS_env_MK_trend_P.append(P_value)
    
    # temperature
    slp, intp, P_value = Trend_var(years, TA_smr,TA_smr_QC)
    EOS_env_MK_trend_slp.append(slp)
    EOS_env_MK_trend_intp.append(intp)
    EOS_env_MK_trend_P.append(P_value)
    
    slp, intp, P_value = Trend_var(years, TA_aut,TA_aut_QC)
    EOS_env_MK_trend_slp.append(slp)
    EOS_env_MK_trend_intp.append(intp)
    EOS_env_MK_trend_P.append(P_value)
    
    # VPD   
    slp, intp, P_value = Trend_var(years, VPD_smr,VPD_smr_QC)
    EOS_env_MK_trend_slp.append(slp)
    EOS_env_MK_trend_intp.append(intp)
    EOS_env_MK_trend_P.append(P_value)
    
    slp, intp, P_value = Trend_var(years, VPD_aut,VPD_aut_QC)
    EOS_env_MK_trend_slp.append(slp)
    EOS_env_MK_trend_intp.append(intp)
    EOS_env_MK_trend_P.append(P_value)
    
    # precipitation   
    slp, intp, P_value = Trend_var(years, P_smr,P_smr_QC)
    EOS_env_MK_trend_slp.append(slp)
    EOS_env_MK_trend_intp.append(intp)
    EOS_env_MK_trend_P.append(P_value)
    
    slp, intp, P_value = Trend_var(years, P_aut,P_aut_QC)
    EOS_env_MK_trend_slp.append(slp)
    EOS_env_MK_trend_intp.append(intp)
    EOS_env_MK_trend_P.append(P_value)

    
    # SW_IN    
    slp, intp, P_value = Trend_var(years, SW_IN_smr, SW_IN_smr_QC)
    EOS_env_MK_trend_slp.append(slp)
    EOS_env_MK_trend_intp.append(intp)
    EOS_env_MK_trend_P.append(P_value)
    
    slp, intp, P_value = Trend_var(years, SW_IN_aut, SW_IN_aut_QC)
    EOS_env_MK_trend_slp.append(slp)
    EOS_env_MK_trend_intp.append(intp)
    EOS_env_MK_trend_P.append(P_value)
    
    # TS_MDS_1
    slp, intp, P_value = Trend_var(years, TS_MDS_1_smr, TS_MDS_1_smr_QC)
    EOS_env_MK_trend_slp.append(slp)
    EOS_env_MK_trend_intp.append(intp)
    EOS_env_MK_trend_P.append(P_value)
    
    slp, intp, P_value = Trend_var(years, TS_MDS_1_aut, TS_MDS_1_aut_QC)
    EOS_env_MK_trend_slp.append(slp)
    EOS_env_MK_trend_intp.append(intp)
    EOS_env_MK_trend_P.append(P_value)
    
    
    # TS_MDS_2
    slp, intp, P_value = Trend_var(years, TS_MDS_2_smr, TS_MDS_2_smr_QC)
    EOS_env_MK_trend_slp.append(slp)
    EOS_env_MK_trend_intp.append(intp)
    EOS_env_MK_trend_P.append(P_value)
    
    slp, intp, P_value = Trend_var(years, TS_MDS_2_aut, TS_MDS_2_aut_QC)
    EOS_env_MK_trend_slp.append(slp)
    EOS_env_MK_trend_intp.append(intp)
    EOS_env_MK_trend_P.append(P_value)
    
    # SWC_MDS_1
    slp, intp, P_value = Trend_var(years, SWC_MDS_1_smr, SWC_MDS_1_smr_QC)
    EOS_env_MK_trend_slp.append(slp)
    EOS_env_MK_trend_intp.append(intp)
    EOS_env_MK_trend_P.append(P_value)
    
    slp, intp, P_value = Trend_var(years, SWC_MDS_1_aut, SWC_MDS_1_aut_QC)
    EOS_env_MK_trend_slp.append(slp)
    EOS_env_MK_trend_intp.append(intp)
    EOS_env_MK_trend_P.append(P_value)
    
    
    # SWC_MDS_2
    slp, intp, P_value = Trend_var(years, SWC_MDS_2_smr, SWC_MDS_2_smr_QC)
    EOS_env_MK_trend_slp.append(slp)
    EOS_env_MK_trend_intp.append(intp)
    EOS_env_MK_trend_P.append(P_value)
    
    slp, intp, P_value = Trend_var(years, SWC_MDS_2_aut, SWC_MDS_2_aut_QC)
    EOS_env_MK_trend_slp.append(slp)
    EOS_env_MK_trend_intp.append(intp)
    EOS_env_MK_trend_P.append(P_value)
    
    
    # NEE_VUT_REF
    slp, intp, P_value = Trend_var(years, NEE_VUT_REF_smr, NEE_VUT_REF_QC_smr)
    EOS_env_MK_trend_slp.append(slp)
    EOS_env_MK_trend_intp.append(intp)
    EOS_env_MK_trend_P.append(P_value)
    
    slp, intp, P_value = Trend_var(years, NEE_VUT_REF_aut, NEE_VUT_REF_QC_aut)
    EOS_env_MK_trend_slp.append(slp)
    EOS_env_MK_trend_intp.append(intp)
    EOS_env_MK_trend_P.append(P_value)
    
    
    # GPP_NT_VUT_REF
    slp, intp, P_value = Trend_var(years, GPP_NT_VUT_REF_smr, NEE_VUT_REF_QC_smr)
    EOS_env_MK_trend_slp.append(slp)
    EOS_env_MK_trend_intp.append(intp)
    EOS_env_MK_trend_P.append(P_value)
    
    slp, intp, P_value = Trend_var(years, GPP_NT_VUT_REF_aut, NEE_VUT_REF_QC_aut)
    EOS_env_MK_trend_slp.append(slp)
    EOS_env_MK_trend_intp.append(intp)
    EOS_env_MK_trend_P.append(P_value)
    
    
    # RECO_NT_VUT_REF
    slp, intp, P_value = Trend_var(years, RECO_NT_VUT_REF_smr, NEE_VUT_REF_QC_smr)
    EOS_env_MK_trend_slp.append(slp)
    EOS_env_MK_trend_intp.append(intp)
    EOS_env_MK_trend_P.append(P_value)
    
    slp, intp, P_value = Trend_var(years, RECO_NT_VUT_REF_aut, NEE_VUT_REF_QC_aut)
    EOS_env_MK_trend_slp.append(slp)
    EOS_env_MK_trend_intp.append(intp)
    EOS_env_MK_trend_P.append(P_value)
    
    
    # LE_F_MDS
    slp, intp, P_value = Trend_var(years, LE_F_MDS_smr, LE_F_MDS_QC_smr)
    EOS_env_MK_trend_slp.append(slp)
    EOS_env_MK_trend_intp.append(intp)
    EOS_env_MK_trend_P.append(P_value)
    
    slp, intp, P_value = Trend_var(years, LE_F_MDS_aut, LE_F_MDS_QC_aut)
    EOS_env_MK_trend_slp.append(slp)
    EOS_env_MK_trend_intp.append(intp)
    EOS_env_MK_trend_P.append(P_value)
    
    

#### output R2 ##############################################            
fld_SOS = ['SOS_Ta_spr','SOS_Ta_wit',\
           'SOS_VPD_spr','SOS_VPD_wit',\
           'SOS_P_spr','SOS_P_wit',\
           'SOS_SW_IN_spr','SOS_SW_IN_wit',\
           'SOS_TS_MDS_1_spr','SOS_TS_MDS_1_wit',\
           'SOS_TS_MDS_2_spr','SOS_TS_MDS_2_wit',\
           'SOS_SWC_MDS_1_spr','SOS_SWC_MDS_1_wit',\
           'SOS_SWC_MDS_2_spr','SOS_SWC_MDS_2_wit',\
           'SOS_NEE_spr','SOS_NEE_yr',\
           'SOS_GPP_spr','SOS_GPP_yr',\
           'SOS_RECO_spr','SOS_RECO_yr',\
           'SOS_LE_spr','SOS_LE_wit']

fld_SOS_all = []
paras = ['R','P','slp']
for n in range(len(paras)):
    for i in range(len(fld_SOS)):
        str = '%s_%s' %(fld_SOS[i],paras[n])
        fld_SOS_all.append(str)
    
SOS_env_R2 = np.reshape(SOS_env_R2,[len(SOS_env_R2)/len(fld_SOS),len(fld_SOS)])
SOS_env_slp = np.reshape(SOS_env_slp,[len(SOS_env_slp)/len(fld_SOS),len(fld_SOS)])
SOS_env_P = np.reshape(SOS_env_P,[len(SOS_env_P)/len(fld_SOS),len(fld_SOS)])   

SOS_outdata = np.hstack((SOS_env_R2,SOS_env_P,SOS_env_slp)) 

out_df = pd.DataFrame(data = SOS_outdata,columns=fld_SOS_all,index = phen_files)
outfile = '%s/STAT/SOS_vs_env_R2_P_slp_season_20190302.csv' %(out_R2_path)
out_df.to_csv(outfile,index_label = 'site')


   
fld_EOS = ['EOS_Ta_smr','EOS_Ta_aut',\
           'EOS_VPD_smr','EOS_VPD_aut',\
           'EOS_P_smr','EOS_P_aut',\
           'EOS_SW_IN_smr','EOS_SW_IN_aut',\
           'EOS_TS_MDS_1_smr','EOS_TS_MDS_1_aut',\
           'EOS_TS_MDS_2_smr','EOS_TS_MDS_2_aut',\
           'EOS_SWC_MDS_1_smr','EOS_SWC_MDS_1_aut',\
           'EOS_SWC_MDS_2_smr','EOS_SWC_MDS_2_aut',\
           'EOS_NEE_aut','EOS_NEE_yr',\
           'EOS_GPP_aut','EOS_GPP_yr',\
           'EOS_RECO_aut','EOS_RECO_yr',\
           'EOS_LE_aut','EOS_LE_yr']

fld_EOS_all = []
paras = ['R','P','slp']
for n in range(len(paras)):
    for i in range(len(fld_EOS)):
        str = '%s_%s' %(fld_EOS[i],paras[n])
        fld_EOS_all.append(str)
        
EOS_env_R2 = np.reshape(EOS_env_R2,[len(EOS_env_R2)/len(fld_EOS),len(fld_EOS)])
EOS_env_P = np.reshape(EOS_env_P,[len(EOS_env_P)/len(fld_EOS),len(fld_EOS)])  
EOS_env_slp = np.reshape(EOS_env_slp,[len(EOS_env_slp)/len(fld_EOS),len(fld_EOS)])

EOS_outdata = np.hstack((EOS_env_R2,EOS_env_P,EOS_env_slp)) 

out_df = pd.DataFrame(data = EOS_outdata,columns=fld_EOS_all,index = phen_files)
outfile = '%s/STAT/EOS_vs_env_R2_P_slp_season_20190302.csv' %(out_R2_path)
out_df.to_csv(outfile,index_label = 'site')


   
fld_GSL = ['GSL_Ta_gs','GSL_Ta_yr',\
           'GSL_VPD_gs','GSL_VPD_yr',\
           'GSL_P_gs','GSL_P_yr',\
           'GSL_SW_IN_gs','GSL_SW_IN_yr',\
           'GSL_TS_MDS_1_gs','GSL_TS_MDS_1_yr',\
           'GSL_TS_MDS_2_gs','GSL_TS_MDS_2_yr',\
           'GSL_SWC_MDS_1_gs','GSL_SWC_MDS_1_yr',\
           'GSL_SWC_MDS_2_gs','GSL_SWC_MDS_2_yr',\
           'GSL_NEE_gs','GSL_NEE_yr',\
           'GSL_GPP_gs','GSL_GPP_yr',\
           'GSL_RECO_gs','GSL_RECO_yr',\
           'GSL_LE_gs','GSL_LE_yr']

fld_GSL_all = []
paras = ['R','P','slp']
for n in range(len(paras)):
    for i in range(len(fld_GSL)):
        str = '%s_%s' %(fld_GSL[i],paras[n])
        fld_GSL_all.append(str)

GSL_env_R2 = np.reshape(GSL_env_R2,[len(GSL_env_R2)/len(fld_GSL),len(fld_GSL)])
GSL_env_P = np.reshape(GSL_env_P,[len(GSL_env_P)/len(fld_GSL),len(fld_GSL)])  
GSL_env_slp = np.reshape(GSL_env_slp,[len(GSL_env_slp)/len(fld_GSL),len(fld_GSL)]) 

GSL_outdata = np.hstack((GSL_env_R2, GSL_env_P, GSL_env_slp)) 

out_df = pd.DataFrame(data = GSL_outdata, columns=fld_GSL_all, index = phen_files)
outfile = '%s/STAT/GSL_vs_env_R2_P_slp_season_20190302.csv' %(out_R2_path)
out_df.to_csv(outfile,index_label = 'site')


####### output the avg and std of SOS EOS and GSL  ################
fld_avg = []
fld_avg.append('SOS_avg')
fld_avg.append('SOS_std')
for i in range(len(fld_SOS)):
    fld_avg.append('%s_avg' %(fld_SOS[i]))
    fld_avg.append('%s_std' %(fld_SOS[i]))


SOS_avg_std = np.reshape(SOS_avg_std,[len(SOS_avg_std)/len(fld_avg),len(fld_avg)])
out_df = pd.DataFrame(data = SOS_avg_std,columns=fld_avg,index = phen_files)
outfile = '%s/STAT/SOS_avg_std_season_20190302.csv' %(out_R2_path)
out_df.to_csv(outfile,index_label = 'site')


fld_avg = []
fld_avg.append('EOS_avg')
fld_avg.append('EOS_std')
for i in range(len(fld_EOS)):
    fld_avg.append('%s_avg' %(fld_EOS[i]))
    fld_avg.append('%s_std' %(fld_EOS[i]))
    
EOS_avg_std = np.reshape(EOS_avg_std,[len(EOS_avg_std)/len(fld_avg),len(fld_avg)])
out_df = pd.DataFrame(data = EOS_avg_std,columns=fld_avg,index = phen_files)
outfile = '%s/STAT/EOS_avg_std_season_20190302.csv' %(out_R2_path)
out_df.to_csv(outfile,index_label = 'site')

fld_avg = []
fld_avg.append('GSL_avg')
fld_avg.append('GSL_std')
for i in range(len(fld_GSL)):
    fld_avg.append('%s_avg' %(fld_GSL[i]))
    fld_avg.append('%s_std' %(fld_GSL[i]))
    
GSL_avg_std = np.reshape(GSL_avg_std,[len(GSL_avg_std)/len(fld_avg),len(fld_avg)])
out_df = pd.DataFrame(data = GSL_avg_std,columns=fld_avg,index = phen_files)
outfile = '%s/STAT/GSL_avg_std_season_20190302.csv' %(out_R2_path)
out_df.to_csv(outfile,index_label = 'site')

####### output the MK trend slp, intp, P of envir vars for SOS, EOS and GSL ################
fld_sos_var = ['phen_NT', 'Ta_spr','Ta_wit',\
                'VPD_spr','VPD_wit',\
                'P_spr','P_wit', 'SW_IN_spr','SW_IN_wit',\
                'TS_MDS_1_spr','TS_MDS_1_wit',\
                'TS_MDS_2_spr','TS_MDS_2_wit',\
                'SWC_MDS_1_spr','SWC_MDS_1_wit',\
                'SWC_MDS_2_spr','SWC_MDS_2_wit',\
                'NEE_spr','NEE_wit',\
                'GPP_spr','GPP_wit',\
                'RECO_spr','RECO_wit',\
                'LE_MDS_spr','LE_MDS_wit']

fld_eos_var = ['phen_NT', 'Ta_smr','Ta_aut',\
                'VPD_smr','VPD_aut',\
                'P_smr','P_aut', 'SW_IN_smr','SW_IN_aut',\
                'TS_MDS_1_smr','TS_MDS_1_aut',\
                'TS_MDS_2_smr','TS_MDS_2_aut',\
                'SWC_MDS_1_smr','SWC_MDS_1_aut',\
                'SWC_MDS_2_smr','SWC_MDS_2_aut',\
                'NEE_smr','NEE_aut',\
                'GPP_smr','GPP_aut',\
                'RECO_smr','RECO_aut',\
                'LE_MDS_smr','LE_MDS_aut']


###  SOS vars trends

date_str = '2017_12_03'
fld_sos_var_all = []
paras = ['MK_slp','MK_P','MK_intp']
for n in range(len(paras)):
    for i in range(len(fld_sos_var)):
        str = '%s_%s' %(fld_sos_var[i],paras[n])
        fld_sos_var_all.append(str)
        
SOS_env_MK_trend_slp = np.reshape(SOS_env_MK_trend_slp,[len(SOS_env_MK_trend_slp)/len(fld_sos_var),len(fld_sos_var)])
SOS_env_MK_trend_intp = np.reshape(SOS_env_MK_trend_intp,[len(SOS_env_MK_trend_intp)/len(fld_sos_var),len(fld_sos_var)])
SOS_env_MK_trend_P = np.reshape(SOS_env_MK_trend_P,[len(SOS_env_MK_trend_P)/len(fld_sos_var),len(fld_sos_var)])

SOS_all_MK_data = np.hstack((SOS_env_MK_trend_slp, SOS_env_MK_trend_P, SOS_env_MK_trend_intp)) 
out_df = pd.DataFrame(data = SOS_all_MK_data, columns=fld_sos_var_all, index = phen_files)
outfile1 = '%s/STAT/SOS_envir_var_MK_slp_P_intp_season_%s_20190302.csv' %(out_R2_path,date_str)
out_df.to_csv(outfile1,index_label = 'site')



###  EOS vars trends

fld_eos_var_all = []
paras = ['MK_slp','MK_P','MK_intp']
for n in range(len(paras)):
    for i in range(len(fld_eos_var)):
        str = '%s_%s' %(fld_eos_var[i],paras[n])
        fld_eos_var_all.append(str)
        
EOS_env_MK_trend_slp = np.reshape(EOS_env_MK_trend_slp,[len(EOS_env_MK_trend_slp)/len(fld_sos_var),len(fld_sos_var)])
EOS_env_MK_trend_intp = np.reshape(EOS_env_MK_trend_intp,[len(EOS_env_MK_trend_intp)/len(fld_sos_var),len(fld_sos_var)])
EOS_env_MK_trend_P = np.reshape(EOS_env_MK_trend_P,[len(EOS_env_MK_trend_P)/len(fld_sos_var),len(fld_sos_var)])

EOS_all_MK_data = np.hstack((EOS_env_MK_trend_slp, EOS_env_MK_trend_P, EOS_env_MK_trend_intp)) 

out_df = pd.DataFrame(data = EOS_all_MK_data, columns = fld_eos_var_all, index = phen_files)
outfile1 = '%s/STAT/EOS_envir_var_MK_slp_P_intp_season_%s_20190302.csv' %(out_R2_path,date_str)
out_df.to_csv(outfile1,index_label = 'site')


