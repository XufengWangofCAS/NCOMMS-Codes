# -*- coding: utf-8 -*-
"""
Created on Mon Aug 06 15:29:15 2018

@author: wxf
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import MK_trend as MK

def cm2inch(*tupl):
    inch = 2.54
    if isinstance(tupl[0], tuple):
        return tuple(i/inch for i in tupl[0])
    else:
        return tuple(i/inch for i in tupl) 

infile = "../dataset_code_to_upload/NCOMMS-19-00016-T-SourceDataFile/Figure1.data.xlsx"        

infile_SOS_v1 = pd.read_excel(infile,"Figure1a") #'D:/3.UNH_visiting/Phenology_from_fluxnet/remote_sensing_phenology/GIMMS3g_v1_phen_20180717/NH30_90_SOS.csv'
infile_EOS_v1 = pd.read_excel(infile,"Figure1b") #'D:/3.UNH_visiting/Phenology_from_fluxnet/remote_sensing_phenology/GIMMS3g_v1_phen_20180717/NH30_90_EOS.csv'
infile_TEM_spr = pd.read_excel(infile,"Figure1c") #'D:/3.UNH_visiting/Phenology_from_fluxnet/Paper Writing/global_warming_hiatus/CRUTEM.4/CRU_TEM3_seasonal.xlsx'
infile_TEM_aut = pd.read_excel(infile,"Figure1d") #'D:/3.UNH_visiting/Phenology_from_fluxnet/Paper Writing/global_warming_hiatus/CRUTEM.4/CRU_TEM4_seasonal_variance.xlsx'
infile_TEM_year = pd.read_excel(infile,"Figure1e")


###=========================================== read data ===================###
### read SOS and get trend ###############
#GIMMS version1
SOS_avg_v1 = np.asarray(infile_SOS_v1['SOS_GIMMS3g'])
SOS_Years_v1 = np.asarray(infile_SOS_v1['Year'])
### read EOS and get trend ###############

## GIMMS version 1
EOS_avg_v1 = np.asarray(infile_EOS_v1['EOS_GIMMS3g'])
EOS_Years_v1 = np.asarray(infile_EOS_v1['Year'])

##### read temperature and get trend ##########


CRUTEM4_spr = np.asarray(infile_TEM_spr['CRUTEM4_spr'])
CRUTEM4_aut = np.asarray(infile_TEM_aut['CRUTEM4_aut'])
CRUTEM4_avg = np.asarray(infile_TEM_year['CRUTEM4_year'])

CRUTEM4_year = infile_TEM_spr['Year']
#==============================================================================

SOS_trend_slp = []
SOS_trend_p = []

EOS_trend_slp = []
EOS_trend_p = []

CRUTEM4_spr_trend_slp = []
CRUTEM4_spr_trend_p = []

CRUTEM4_aut_trend_slp = []
CRUTEM4_aut_trend_p = []

CRUTEM4_yr_trend_slp = []
CRUTEM4_yr_trend_p = []

###           1997   1998  1999
start_indx = [  15,    16,   17 ]

###           2012   2013  2014
end_indx   = [  31,    32,   33]

out_indx = []
period1 = []
period2 = []
for i in range(3):
    for j in range(3):
        wh_start = start_indx[i]
        wh_end = end_indx[j]
        print(wh_start,wh_end)
        
        out_indx.append("%d_%d" %(wh_start+1982, wh_end+1981))
        period1.append("%d ~ %d" %(1982, wh_start+1982))
        period2.append("%d ~ %d" %(wh_start+1982, wh_end+1981))

        #warming hiatus start 1998 end 2014
        SOS_bf98_v1 = SOS_avg_v1[0:wh_start+1]
        years_bf98_SOS_v1 = SOS_Years_v1[0:wh_start+1]
        SOS_af98_v1 = SOS_avg_v1[wh_start:wh_end]
        years_af98_SOS_v1 = SOS_Years_v1[wh_start:wh_end]
        
        h_bf98_SOS_v1, trend_bf98_SOS_v1, intp_bf98_SOS_v1, p_value_bf98_SOS_v1, z_bf98_SOS_v1 = MK.mk_trend(SOS_bf98_v1,years_bf98_SOS_v1,0.05)
        h_af98_SOS_v1, trend_af98_SOS_v1, intp_af98_SOS_v1, p_value_af98_SOS_v1, z_af98_SOS_v1 = MK.mk_trend(SOS_af98_v1,years_af98_SOS_v1,0.05)
        
        SOS_trend_slp.append(trend_bf98_SOS_v1)
        SOS_trend_slp.append(trend_af98_SOS_v1)
        SOS_trend_p.append(p_value_bf98_SOS_v1)
        SOS_trend_p.append(p_value_af98_SOS_v1)
        
        
        EOS_bf98_v1 = EOS_avg_v1[0:wh_start+1]
        years_bf98_EOS_v1 = EOS_Years_v1[0:wh_start+1]
        EOS_af98_v1 = EOS_avg_v1[wh_start:wh_end]
        years_af98_EOS_v1 = EOS_Years_v1[wh_start:wh_end]
        
        h_bf98_EOS_v1, trend_bf98_EOS_v1, intp_bf98_EOS_v1, p_value_bf98_EOS_v1, z_bf98_EOS_v1 = MK.mk_trend(EOS_bf98_v1,years_bf98_EOS_v1,0.05)
        h_af98_EOS_v1, trend_af98_EOS_v1, intp_af98_EOS_v1, p_value_af98_EOS_v1, z_af98_EOS_v1 = MK.mk_trend(EOS_af98_v1,years_af98_EOS_v1,0.05)
        
        EOS_trend_slp.append(trend_bf98_EOS_v1)
        EOS_trend_slp.append(trend_af98_EOS_v1)
        EOS_trend_p.append(p_value_bf98_EOS_v1)
        EOS_trend_p.append(p_value_af98_EOS_v1)
        
        ### MK trend spring average temperature #####
        CRUTEM4_spr_bf98 = CRUTEM4_spr[0:wh_start+1]
        years_bf98_CRUTEM4_spr = CRUTEM4_year[0:wh_start+1]
        CRUTEM4_spr_af98 = CRUTEM4_spr[wh_start:wh_end]
        years_af98_CRUTEM4_spr = CRUTEM4_year[wh_start:wh_end]
        
        h_bf98_CRUTEM4_spr, trend_bf98_CRUTEM4_spr, intp_bf98_CRUTEM4_spr, p_value_bf98_CRUTEM4_spr, z_bf98_CRUTEM4_spr = MK.mk_trend(CRUTEM4_spr_bf98,years_bf98_CRUTEM4_spr,0.05)
        h_af98_CRUTEM4_spr, trend_af98_CRUTEM4_spr, intp_af98_CRUTEM4_spr, p_value_af98_CRUTEM4_spr, z_af98_CRUTEM4_spr = MK.mk_trend(CRUTEM4_spr_af98,years_af98_CRUTEM4_spr,0.05)
        
        CRUTEM4_spr_trend_slp.append(trend_bf98_CRUTEM4_spr)
        CRUTEM4_spr_trend_slp.append(trend_af98_CRUTEM4_spr)
        CRUTEM4_spr_trend_p.append(p_value_bf98_CRUTEM4_spr)
        CRUTEM4_spr_trend_p.append(p_value_af98_CRUTEM4_spr)
        
        ### MK trend autumn average temperature #####
        CRUTEM4_aut_bf98 = CRUTEM4_aut[0:wh_start+1]
        years_bf98_CRUTEM4_aut = CRUTEM4_year[0:wh_start+1]
        CRUTEM4_aut_af98 = CRUTEM4_aut[wh_start:wh_end]
        years_af98_CRUTEM4_aut = CRUTEM4_year[wh_start:wh_end]
        
        h_bf98_CRUTEM4_aut, trend_bf98_CRUTEM4_aut, intp_bf98_CRUTEM4_aut, p_value_bf98_CRUTEM4_aut, z_bf98_CRUTEM4_aut = MK.mk_trend(CRUTEM4_aut_bf98,years_bf98_CRUTEM4_aut,0.05)
        h_af98_CRUTEM4_aut, trend_af98_CRUTEM4_aut, intp_af98_CRUTEM4_aut, p_value_af98_CRUTEM4_aut, z_af98_CRUTEM4_aut = MK.mk_trend(CRUTEM4_aut_af98,years_af98_CRUTEM4_aut,0.05)
        
        CRUTEM4_aut_trend_slp.append(trend_bf98_CRUTEM4_aut)
        CRUTEM4_aut_trend_slp.append(trend_af98_CRUTEM4_aut)
        CRUTEM4_aut_trend_p.append(p_value_bf98_CRUTEM4_aut)
        CRUTEM4_aut_trend_p.append(p_value_af98_CRUTEM4_aut)
        
        ### MK trend year average temperature #####
        CRUTEM4_avg_bf98 = CRUTEM4_avg[0:wh_start+1]
        years_bf98_CRUTEM4_avg = CRUTEM4_year[0:wh_start+1]
        CRUTEM4_avg_af98 = CRUTEM4_avg[wh_start:wh_end]
        years_af98_CRUTEM4_avg = CRUTEM4_year[wh_start:wh_end]
        
        h_bf98_CRUTEM4_avg, trend_bf98_CRUTEM4_avg, intp_bf98_CRUTEM4_avg, p_value_bf98_CRUTEM4_avg, z_bf98_CRUTEM4_avg = MK.mk_trend(CRUTEM4_avg_bf98,years_bf98_CRUTEM4_avg,0.05)
        h_af98_CRUTEM4_avg, trend_af98_CRUTEM4_avg, intp_af98_CRUTEM4_avg, p_value_af98_CRUTEM4_avg, z_af98_CRUTEM4_avg = MK.mk_trend(CRUTEM4_avg_af98,years_af98_CRUTEM4_avg,0.05)
        
        CRUTEM4_yr_trend_slp.append(trend_bf98_CRUTEM4_avg)
        CRUTEM4_yr_trend_slp.append(trend_af98_CRUTEM4_avg)
        CRUTEM4_yr_trend_p.append(p_value_bf98_CRUTEM4_avg)
        CRUTEM4_yr_trend_p.append(p_value_af98_CRUTEM4_avg)




SOS_trend_slp = np.reshape(SOS_trend_slp,[len(SOS_trend_slp)/2,2])
SOS_trend_p = np.reshape(SOS_trend_p,[len(SOS_trend_p)/2,2])

EOS_trend_slp = np.reshape(EOS_trend_slp,[len(EOS_trend_slp)/2,2])
EOS_trend_p = np.reshape(EOS_trend_p,[len(EOS_trend_p)/2,2])

CRUTEM4_spr_trend_slp = np.reshape(CRUTEM4_spr_trend_slp,[len(CRUTEM4_spr_trend_slp)/2,2])
CRUTEM4_spr_trend_p = np.reshape(CRUTEM4_spr_trend_p,[len(CRUTEM4_spr_trend_p)/2,2])

CRUTEM4_aut_trend_slp = np.reshape(CRUTEM4_aut_trend_slp,[len(CRUTEM4_aut_trend_slp)/2,2])
CRUTEM4_aut_trend_p = np.reshape(CRUTEM4_aut_trend_p,[len(CRUTEM4_aut_trend_p)/2,2])

CRUTEM4_yr_trend_slp = np.reshape(CRUTEM4_yr_trend_slp,[len(CRUTEM4_yr_trend_slp)/2,2])
CRUTEM4_yr_trend_p = np.reshape(CRUTEM4_yr_trend_p,[len(CRUTEM4_yr_trend_p)/2,2])
period1 = np.reshape(period1,[len(period1)/1,1]) 
period2 = np.reshape(period2,[len(period2)/1,1]) 

flds = ["Period1","Period2","SOS_slp_bf_wh","SOS_slp_af_wh","EOS_slp_bf_wh","EOS_slp_af_wh","temp_spr_slp_bf_wh","temp_spr_slp_af_wh","temp_aut_slp_bf_wh","temp_aut_slp_af_wh","temp_yr_slp_bf_wh","temp_yr_slp_af_wh",\
        "SOS_P_bf_wh","SOS_P_af_wh","EOS_P_bf_wh","EOS_P_af_wh","temp_spr_P_bf_wh","temp_spr_P_af_wh","temp_aut_P_bf_wh","temp_aut_P_af_wh","temp_yr_P_bf_wh","temp_yr_P_af_wh"]

out_data = np.hstack((period1,period2,SOS_trend_slp,EOS_trend_slp,CRUTEM4_spr_trend_slp,CRUTEM4_aut_trend_slp,CRUTEM4_yr_trend_slp,\
                  SOS_trend_p,EOS_trend_p,CRUTEM4_spr_trend_p,CRUTEM4_aut_trend_p,CRUTEM4_yr_trend_p))



out_df = pd.DataFrame(data = out_data, columns = flds, index = out_indx)
out_file = 'warming_hiatus_sensitivity.csv'
out_df.to_csv(out_file)

