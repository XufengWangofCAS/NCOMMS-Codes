# -*- coding: utf-8 -*-
"""
Created on Mon Nov 28 09:49:43 2016

@author: wxf
"""

import matplotlib.pyplot as plt

import os
import csv
import numpy as np
import string
import scipy.stats as stats
import pandas as pd


# set the input and output directory here #####################################
Out_path = 'D:/UNH_visiting/fluxnet_analyze_v2/FluxnetData_season_ver3'

### original unziped fluxnet2015_tier2 data folder  ###########################
Cur_path='D:/data/fluxnet2015_tier2_updated_Nov_3_2016/unzip_data'


#### choosed site list file ###################################################
infile='D:/UNH_visiting/fluxnet_analyze_v2/flux_site_new.csv'
outtxt=''
sitename=[]
site_IGBP=[]
with open(infile) as f:
    f_csv = csv.DictReader(f)
    for row in f_csv:
        sitename.append(row['SITE_ID'])
        site_IGBP.append(row['IGBP'])

outdata = []  
out_sitesname = []
out_siteIGBP = []
first=0      

for dirname in os.listdir(Cur_path):
    startyear=string.atoi(dirname[30:34])
    endyear=string.atoi(dirname[35:39])
    nyears=endyear-startyear+1
    N_records = 12*nyears
    Time_stamp = np.zeros(N_records)
    NEE=np.zeros(N_records)
    NEE_QC=np.zeros(N_records)
    TA=np.zeros(N_records)
    TA_QC=np.zeros(N_records)
    SW_IN_F=np.zeros(N_records)
    SW_IN_F_QC=np.zeros(N_records)    
    VPD_F=np.zeros(N_records)
    VPD_F_QC=np.zeros(N_records)
    P_F=np.zeros(N_records)
    P_F_QC=np.zeros(N_records)
    RECO_NT_VUT_MEAN=np.zeros(N_records)
    RECO_DT_VUT_MEAN=np.zeros(N_records)
    GPP_NT_VUT_MEAN=np.zeros(N_records)
    GPP_DT_VUT_MEAN=np.zeros(N_records)
    LE_F_MDS=np.zeros(N_records)
    LE_F_MDS_QC=np.zeros(N_records)
    LE_CORR=np.zeros(N_records)
    H_F_MDS=np.zeros(N_records)
    H_F_MDS_QC=np.zeros(N_records)
    H_CORR=np.zeros(N_records)
    WUE=np.zeros(N_records)
    
    CO2=np.zeros(N_records)
    CO2_QC=np.zeros(N_records)
    
    TS_F_MDS_1 = np.zeros(N_records)
    TS_F_MDS_1_QC = np.zeros(N_records)
    TS_F_MDS_2 = np.zeros(N_records)
    TS_F_MDS_2_QC = np.zeros(N_records)
    
    SWC_F_MDS_1 = np.zeros(N_records)
    SWC_F_MDS_1_QC = np.zeros(N_records)
    SWC_F_MDS_2 = np.zeros(N_records)
    SWC_F_MDS_2_QC = np.zeros(N_records)
    
    
    st=dirname[4:10]
    indx=sitename.index(st)
    st_IGBP=site_IGBP[indx]
    
    data_spr = []
    data_smr = []
    data_aut = []
    data_wit = []
    data_gs = []
    data_yr = []
    
    filename="%s/%s/%s_MM_%s.csv" %(Cur_path,dirname,dirname[0:29],dirname[30:44])
    print startyear,endyear,filename
    with open(filename) as f:
        f_csv = csv.DictReader(f)
        ind=0
        for row in f_csv:
            Time_stamp = row['TIMESTAMP']
            NEE[ind] = row['NEE_VUT_REF']
            NEE_QC[ind] = row['NEE_VUT_REF_QC']
            TA[ind] = row['TA_F']
            TA_QC[ind] = row['TA_F_QC']
            SW_IN_F[ind] = row['SW_IN_F']
            SW_IN_F_QC[ind] = row['SW_IN_F_QC']
            P_F[ind] = row['P_F']
            P_F_QC[ind] = row['P_F_QC']
            RECO_NT_VUT_MEAN[ind] = row['RECO_NT_VUT_REF']
            RECO_DT_VUT_MEAN[ind] = row['RECO_DT_VUT_REF']
            GPP_NT_VUT_MEAN[ind] = row['GPP_NT_VUT_REF']
            GPP_DT_VUT_MEAN[ind] = row['GPP_DT_VUT_REF']
            LE_F_MDS[ind] = row['LE_F_MDS']
            LE_F_MDS_QC[ind] = row['LE_F_MDS_QC']
            LE_CORR[ind] = row['LE_CORR']
            H_F_MDS[ind] = row['H_F_MDS']
            H_F_MDS_QC[ind] = row['H_F_MDS_QC']
            H_CORR[ind] = row['H_CORR']
            VPD_F[ind] = row['VPD_F']
            VPD_F_QC[ind] = row['VPD_F_QC']
            CO2[ind] = row['CO2_F_MDS']
            CO2_QC[ind] = row['CO2_F_MDS_QC']
            
            if(row.has_key("TS_F_MDS_1")):
                TS_F_MDS_1[ind] = row['TS_F_MDS_1']
                TS_F_MDS_1_QC[ind] = row['TS_F_MDS_1_QC']
            else:
                TS_F_MDS_1[ind] = -9999
                TS_F_MDS_1_QC[ind] = -9999
                
            if(row.has_key("TS_F_MDS_2")):
                TS_F_MDS_2[ind] = row['TS_F_MDS_2']
                TS_F_MDS_2_QC[ind] = row['TS_F_MDS_2_QC']
            else:
                TS_F_MDS_2[ind] = -9999
                TS_F_MDS_2_QC[ind] = -9999
                
                
            if(row.has_key("SWC_F_MDS_1")):
                SWC_F_MDS_1[ind] = row['SWC_F_MDS_1']
                SWC_F_MDS_1_QC[ind] = row['SWC_F_MDS_1_QC']
            else:
                SWC_F_MDS_1[ind] = -9999
                SWC_F_MDS_1_QC[ind] = -9999
                
            if(row.has_key("SWC_F_MDS_2")):
                SWC_F_MDS_2[ind] = row['SWC_F_MDS_2']
                SWC_F_MDS_2_QC[ind] = row['SWC_F_MDS_2_QC']
            else:
                SWC_F_MDS_2[ind] = -9999
                SWC_F_MDS_2_QC[ind] = -9999
            


            if (NEE[ind]==-9999):
                NEE[ind]=np.nan
            if (NEE_QC[ind]==-9999):
                NEE_QC[ind]=np.nan
                
            if (TA[ind]==-9999):
                TA[ind]=np.nan
            if (TA_QC[ind]==-9999):
                TA_QC[ind]=np.nan
            if (SW_IN_F[ind]==-9999):
                SW_IN_F[ind]=np.nan
            if (SW_IN_F_QC[ind]==-9999):
                SW_IN_F_QC[ind]=np.nan
            if(VPD_F[ind]==-9999):
                VPD_F[ind]=np.nan
            if(VPD_F_QC[ind]==-9999):
                VPD_F_QC[ind]=np.nan
            if(P_F[ind]==-9999):
                P_F[ind]=np.nan
            if(P_F_QC[ind]==-9999):
                P_F_QC[ind]=np.nan
            if(RECO_NT_VUT_MEAN[ind]<=-9999):
                RECO_NT_VUT_MEAN[ind]=np.nan
            if(RECO_DT_VUT_MEAN[ind]<=-9999):
                RECO_DT_VUT_MEAN[ind]=np.nan
            if(GPP_NT_VUT_MEAN[ind]<=-9999):
                GPP_NT_VUT_MEAN[ind]=np.nan
            if(GPP_DT_VUT_MEAN[ind]<=-9999):
                GPP_DT_VUT_MEAN[ind]=np.nan
            if(LE_F_MDS[ind]==-9999):
                LE_F_MDS[ind]=np.nan
            if(LE_F_MDS_QC[ind]==-9999):
                LE_F_MDS_QC[ind]=np.nan
            if(LE_CORR[ind]==-9999):
                LE_CORR[ind]=np.nan
            if(H_F_MDS[ind]==-9999):
                H_F_MDS[ind]=np.nan
            if(H_F_MDS_QC[ind]==-9999):
                H_F_MDS_QC[ind]=np.nan
            if(H_CORR[ind]==-9999):
                H_CORR[ind]=np.nan
                
            if(CO2[ind] == -9999):
                CO2[ind] = np.nan
            if(CO2_QC[ind] == -9999):
                CO2_QC[ind] = np.nan
            
            if(TS_F_MDS_1[ind] == -9999):
                TS_F_MDS_1[ind] = np.nan
            if(TS_F_MDS_1_QC[ind] == -9999):
                TS_F_MDS_1_QC[ind] = np.nan
            if(TS_F_MDS_2[ind] == -9999):
                TS_F_MDS_2[ind] = np.nan
            if(TS_F_MDS_2_QC[ind] == -9999):
                TS_F_MDS_2_QC[ind] = np.nan
                
            if(SWC_F_MDS_1[ind] == -9999):
                SWC_F_MDS_1[ind] = np.nan
            if(SWC_F_MDS_1_QC[ind] == -9999):
                SWC_F_MDS_1_QC[ind] = np.nan
            if(SWC_F_MDS_2[ind] == -9999):
                SWC_F_MDS_2[ind] = np.nan
            if(SWC_F_MDS_2_QC[ind] == -9999):
                SWC_F_MDS_2_QC[ind] = np.nan
            
            
            if((GPP_NT_VUT_MEAN[ind]!=-9999) and (LE_F_MDS[ind]!=-9999) and  (LE_F_MDS[ind]!=0)):
                WUE[ind]=(GPP_NT_VUT_MEAN[ind])/(LE_F_MDS[ind]*12.86667)
            else:
                WUE[ind]=np.nan
            
            ind = ind + 1

    for yr in range(startyear,endyear+1):
    ### get spring fluxes #########################
        spr_start = 3 + 12*(yr - startyear) - 1
        spr_end = 5 + 12*(yr - startyear)
        data_spr.append(np.mean(NEE[spr_start:spr_end]))
        data_spr.append(np.mean(NEE_QC[spr_start:spr_end]))
        data_spr.append(np.mean(GPP_NT_VUT_MEAN[spr_start:spr_end]))        
        data_spr.append(np.mean(RECO_NT_VUT_MEAN[spr_start:spr_end]))
        data_spr.append(np.mean(GPP_DT_VUT_MEAN[spr_start:spr_end]))        
        data_spr.append(np.mean(RECO_DT_VUT_MEAN[spr_start:spr_end]))
        
        data_spr.append(np.mean(LE_F_MDS[spr_start:spr_end]))
        data_spr.append(np.mean(LE_F_MDS_QC[spr_start:spr_end]))
        
        data_spr.append(np.mean(H_F_MDS[spr_start:spr_end]))
        data_spr.append(np.mean(H_F_MDS_QC[spr_start:spr_end]))
        
        data_spr.append(np.mean(WUE[spr_start:spr_end]))
        
        data_spr.append(np.mean(TA[spr_start:spr_end]))
        data_spr.append(np.mean(TA_QC[spr_start:spr_end]))
        
        data_spr.append(np.mean(SW_IN_F[spr_start:spr_end]))
        data_spr.append(np.mean(SW_IN_F_QC[spr_start:spr_end]))
        
        data_spr.append(np.mean(VPD_F[spr_start:spr_end]))
        data_spr.append(np.mean(VPD_F_QC[spr_start:spr_end]))
        
        data_spr.append(np.sum(P_F[spr_start:spr_end]))
        data_spr.append(np.mean(P_F_QC[spr_start:spr_end]))
        
        data_spr.append(np.mean(CO2[spr_start:spr_end]))
        data_spr.append(np.mean(CO2_QC[spr_start:spr_end]))
        
        data_spr.append(np.mean(TS_F_MDS_1[spr_start:spr_end]))
        data_spr.append(np.mean(TS_F_MDS_1_QC[spr_start:spr_end]))
        
        data_spr.append(np.mean(TS_F_MDS_2[spr_start:spr_end]))
        data_spr.append(np.mean(TS_F_MDS_2_QC[spr_start:spr_end]))
        
        data_spr.append(np.mean(SWC_F_MDS_1[spr_start:spr_end]))
        data_spr.append(np.mean(SWC_F_MDS_1_QC[spr_start:spr_end]))
        
        data_spr.append(np.mean(SWC_F_MDS_2[spr_start:spr_end]))
        data_spr.append(np.mean(SWC_F_MDS_2_QC[spr_start:spr_end]))


    ### get summer fluxes ##########################
        smr_start = 6 + 12*(yr - startyear) - 1
        smr_end = 8 + 12*(yr - startyear) 
        data_smr.append(np.mean(NEE[smr_start:smr_end]))
        data_smr.append(np.mean(NEE_QC[smr_start:smr_end]))
        data_smr.append(np.mean(GPP_NT_VUT_MEAN[smr_start:smr_end]))        
        data_smr.append(np.mean(RECO_NT_VUT_MEAN[smr_start:smr_end]))
        data_smr.append(np.mean(GPP_DT_VUT_MEAN[smr_start:smr_end]))        
        data_smr.append(np.mean(RECO_DT_VUT_MEAN[smr_start:smr_end]))
        
        data_smr.append(np.mean(LE_F_MDS[smr_start:smr_end]))
        data_smr.append(np.mean(LE_F_MDS_QC[smr_start:smr_end]))
        
        data_smr.append(np.mean(H_F_MDS[smr_start:smr_end]))
        data_smr.append(np.mean(H_F_MDS_QC[smr_start:smr_end]))
        
        data_smr.append(np.mean(WUE[smr_start:smr_end]))
        
        data_smr.append(np.mean(TA[smr_start:smr_end]))
        data_smr.append(np.mean(TA_QC[smr_start:smr_end]))
        
        data_smr.append(np.mean(SW_IN_F[smr_start:smr_end]))
        data_smr.append(np.mean(SW_IN_F_QC[smr_start:smr_end]))
        
        data_smr.append(np.mean(VPD_F[smr_start:smr_end]))
        data_smr.append(np.mean(VPD_F_QC[smr_start:smr_end]))
        
        data_smr.append(np.sum(P_F[smr_start:smr_end]))
        data_smr.append(np.mean(P_F_QC[smr_start:smr_end]))
        
        data_smr.append(np.mean(CO2[smr_start:smr_end]))
        data_smr.append(np.mean(CO2_QC[smr_start:smr_end]))
        
        data_smr.append(np.mean(TS_F_MDS_1[smr_start:smr_end]))
        data_smr.append(np.mean(TS_F_MDS_1_QC[smr_start:smr_end]))
        
        data_smr.append(np.mean(TS_F_MDS_2[smr_start:smr_end]))
        data_smr.append(np.mean(TS_F_MDS_2_QC[smr_start:smr_end]))
        
        data_smr.append(np.mean(SWC_F_MDS_1[smr_start:smr_end]))
        data_smr.append(np.mean(SWC_F_MDS_1_QC[smr_start:smr_end]))
        
        data_smr.append(np.mean(SWC_F_MDS_2[smr_start:smr_end]))
        data_smr.append(np.mean(SWC_F_MDS_2_QC[smr_start:smr_end]))


    ### get autumn fluxes ##########################
        aut_start = 9 + 12*(yr - startyear) - 1
        aut_end = 11 + 12*(yr - startyear) 
        data_aut.append(np.mean(NEE[aut_start:aut_end]))
        data_aut.append(np.mean(NEE_QC[aut_start:aut_end]))
        data_aut.append(np.mean(GPP_NT_VUT_MEAN[aut_start:aut_end]))        
        data_aut.append(np.mean(RECO_NT_VUT_MEAN[aut_start:aut_end]))
        data_aut.append(np.mean(GPP_DT_VUT_MEAN[aut_start:aut_end]))        
        data_aut.append(np.mean(RECO_DT_VUT_MEAN[aut_start:aut_end]))
        
        data_aut.append(np.mean(LE_F_MDS[aut_start:aut_end]))
        data_aut.append(np.mean(LE_F_MDS_QC[aut_start:aut_end]))
        
        data_aut.append(np.mean(H_F_MDS[aut_start:aut_end]))
        data_aut.append(np.mean(H_F_MDS_QC[aut_start:aut_end]))
        
        data_aut.append(np.mean(WUE[aut_start:aut_end]))
        
        data_aut.append(np.mean(TA[aut_start:aut_end]))
        data_aut.append(np.mean(TA_QC[aut_start:aut_end]))
        
        data_aut.append(np.mean(SW_IN_F[aut_start:aut_end]))
        data_aut.append(np.mean(SW_IN_F_QC[aut_start:aut_end]))
        
        data_aut.append(np.mean(VPD_F[aut_start:aut_end]))
        data_aut.append(np.mean(VPD_F_QC[aut_start:aut_end]))
        
        data_aut.append(np.sum(P_F[aut_start:aut_end]))
        data_aut.append(np.mean(P_F_QC[aut_start:aut_end]))
        
        data_aut.append(np.mean(CO2[aut_start:aut_end]))
        data_aut.append(np.mean(CO2_QC[aut_start:aut_end]))
        
        data_aut.append(np.mean(TS_F_MDS_1[aut_start:aut_end]))
        data_aut.append(np.mean(TS_F_MDS_1_QC[aut_start:aut_end]))
        
        data_aut.append(np.mean(TS_F_MDS_2[aut_start:aut_end]))
        data_aut.append(np.mean(TS_F_MDS_2_QC[aut_start:aut_end]))
        
        data_aut.append(np.mean(SWC_F_MDS_1[aut_start:aut_end]))
        data_aut.append(np.mean(SWC_F_MDS_1_QC[aut_start:aut_end]))
        
        data_aut.append(np.mean(SWC_F_MDS_2[aut_start:aut_end]))
        data_aut.append(np.mean(SWC_F_MDS_2_QC[aut_start:aut_end]))

    ### get winter fluxes ##########################
        wit_start = 12 + 12*(yr - startyear) - 1
        wit_end = 14 + 12*(yr - startyear) 
        if(yr != endyear):
            #wit_end = 12 + 12*(yr - startyear) - 1
            data_wit.append(np.mean(NEE[wit_start:wit_end]))
            data_wit.append(np.mean(NEE_QC[wit_start:wit_end]))
            data_wit.append(np.mean(GPP_NT_VUT_MEAN[wit_start:wit_end]))        
            data_wit.append(np.mean(RECO_NT_VUT_MEAN[wit_start:wit_end]))
            data_wit.append(np.mean(GPP_DT_VUT_MEAN[wit_start:wit_end]))        
            data_wit.append(np.mean(RECO_DT_VUT_MEAN[wit_start:wit_end]))
            
            data_wit.append(np.mean(LE_F_MDS[wit_start:wit_end]))
            data_wit.append(np.mean(LE_F_MDS_QC[wit_start:wit_end]))
            
            data_wit.append(np.mean(H_F_MDS[wit_start:wit_end]))
            data_wit.append(np.mean(H_F_MDS_QC[wit_start:wit_end]))
            
            data_wit.append(np.mean(WUE[wit_start:wit_end]))
            
            data_wit.append(np.mean(TA[wit_start:wit_end]))
            data_wit.append(np.mean(TA_QC[wit_start:wit_end]))
            
            data_wit.append(np.mean(SW_IN_F[wit_start:wit_end]))
            data_wit.append(np.mean(SW_IN_F_QC[wit_start:wit_end]))
            
            data_wit.append(np.mean(VPD_F[wit_start:wit_end]))
            data_wit.append(np.mean(VPD_F_QC[wit_start:wit_end]))
            
            data_wit.append(np.sum(P_F[wit_start:wit_end]))
            data_wit.append(np.mean(P_F_QC[wit_start:wit_end]))    
            
            data_wit.append(np.mean(CO2[wit_start:wit_end]))
            data_wit.append(np.mean(CO2_QC[wit_start:wit_end])) 
            
            data_wit.append(np.mean(TS_F_MDS_1[wit_start:wit_end]))
            data_wit.append(np.mean(TS_F_MDS_1_QC[wit_start:wit_end]))
            
            data_wit.append(np.mean(TS_F_MDS_2[wit_start:wit_end]))
            data_wit.append(np.mean(TS_F_MDS_2_QC[wit_start:wit_end]))
            
            data_wit.append(np.mean(SWC_F_MDS_1[wit_start:wit_end]))
            data_wit.append(np.mean(SWC_F_MDS_1_QC[wit_start:wit_end]))
            
            data_wit.append(np.mean(SWC_F_MDS_2[wit_start:wit_end]))
            data_wit.append(np.mean(SWC_F_MDS_2_QC[wit_start:wit_end]))
                
    
    ### get gs fluxes ##########################       
        
        data_gs.append(np.mean(NEE[spr_start:aut_end]))
        data_gs.append(np.mean(NEE_QC[spr_start:aut_end]))
        data_gs.append(np.mean(GPP_NT_VUT_MEAN[spr_start:aut_end]))        
        data_gs.append(np.mean(RECO_NT_VUT_MEAN[spr_start:aut_end]))
        data_gs.append(np.mean(GPP_DT_VUT_MEAN[spr_start:aut_end]))        
        data_gs.append(np.mean(RECO_DT_VUT_MEAN[spr_start:aut_end]))
        
        data_gs.append(np.mean(LE_F_MDS[spr_start:aut_end]))
        data_gs.append(np.mean(LE_F_MDS_QC[spr_start:aut_end]))
        
        data_gs.append(np.mean(H_F_MDS[spr_start:aut_end]))
        data_gs.append(np.mean(H_F_MDS_QC[spr_start:aut_end]))
        
        data_gs.append(np.mean(WUE[spr_start:aut_end]))
        
        data_gs.append(np.mean(TA[spr_start:aut_end]))
        data_gs.append(np.mean(TA_QC[spr_start:aut_end]))
        
        data_gs.append(np.mean(SW_IN_F[spr_start:aut_end]))
        data_gs.append(np.mean(SW_IN_F_QC[spr_start:aut_end]))
        
        data_gs.append(np.mean(VPD_F[spr_start:aut_end]))
        data_gs.append(np.mean(VPD_F_QC[spr_start:aut_end]))
        
        data_gs.append(np.sum(P_F[spr_start:aut_end]))
        data_gs.append(np.mean(P_F_QC[spr_start:aut_end]))
        
        data_gs.append(np.mean(CO2[spr_start:aut_end]))
        data_gs.append(np.mean(CO2_QC[spr_start:aut_end]))
        
        data_gs.append(np.mean(TS_F_MDS_1[spr_start:aut_end]))
        data_gs.append(np.mean(TS_F_MDS_1_QC[spr_start:aut_end]))
        
        data_gs.append(np.mean(TS_F_MDS_2[spr_start:aut_end]))
        data_gs.append(np.mean(TS_F_MDS_2_QC[spr_start:aut_end]))
        
        data_gs.append(np.mean(SWC_F_MDS_1[spr_start:aut_end]))
        data_gs.append(np.mean(SWC_F_MDS_1_QC[spr_start:aut_end]))
        
        data_gs.append(np.mean(SWC_F_MDS_2[spr_start:aut_end]))
        data_gs.append(np.mean(SWC_F_MDS_2_QC[spr_start:aut_end]))
    
    ### get year fluxes ##########################   
        yr_start = 0 + 12*(yr - startyear) 
        yr_end = 12 + 12*(yr - startyear) 
        data_yr.append(np.mean(NEE[yr_start:yr_end]))
        data_yr.append(np.mean(NEE_QC[yr_start:yr_end]))
        data_yr.append(np.mean(GPP_NT_VUT_MEAN[yr_start:yr_end]))        
        data_yr.append(np.mean(RECO_NT_VUT_MEAN[yr_start:yr_end]))
        data_yr.append(np.mean(GPP_DT_VUT_MEAN[yr_start:yr_end]))        
        data_yr.append(np.mean(RECO_DT_VUT_MEAN[yr_start:yr_end]))
        
        data_yr.append(np.mean(LE_F_MDS[yr_start:yr_end]))
        data_yr.append(np.mean(LE_F_MDS_QC[yr_start:yr_end]))
        
        data_yr.append(np.mean(H_F_MDS[yr_start:yr_end]))
        data_yr.append(np.mean(H_F_MDS_QC[yr_start:yr_end]))
        
        data_yr.append(np.mean(WUE[yr_start:yr_end]))
        
        data_yr.append(np.mean(TA[yr_start:yr_end]))
        data_yr.append(np.mean(TA_QC[yr_start:yr_end]))
        
        data_yr.append(np.mean(SW_IN_F[yr_start:yr_end]))
        data_yr.append(np.mean(SW_IN_F_QC[yr_start:yr_end]))
        
        data_yr.append(np.mean(VPD_F[yr_start:yr_end]))
        data_yr.append(np.mean(VPD_F_QC[yr_start:yr_end]))
        
        data_yr.append(np.sum(P_F[yr_start:yr_end]))
        data_yr.append(np.mean(P_F_QC[yr_start:yr_end]))
        
        data_yr.append(np.mean(CO2[yr_start:yr_end]))
        data_yr.append(np.mean(CO2_QC[yr_start:yr_end]))
        
        data_yr.append(np.mean(TS_F_MDS_1[yr_start:yr_end]))
        data_yr.append(np.mean(TS_F_MDS_1_QC[yr_start:yr_end]))
        
        data_yr.append(np.mean(TS_F_MDS_2[yr_start:yr_end]))
        data_yr.append(np.mean(TS_F_MDS_2_QC[yr_start:yr_end]))
        
        data_yr.append(np.mean(SWC_F_MDS_1[yr_start:yr_end]))
        data_yr.append(np.mean(SWC_F_MDS_1_QC[yr_start:yr_end]))
        
        data_yr.append(np.mean(SWC_F_MDS_2[yr_start:yr_end]))
        data_yr.append(np.mean(SWC_F_MDS_2_QC[yr_start:yr_end]))
    
    
    # output data ###############################    
    data_spr = np.reshape(data_spr,[nyears,len(data_spr)/nyears])
    data_smr = np.reshape(data_smr,[nyears,len(data_smr)/nyears])
    data_aut = np.reshape(data_aut,[nyears,len(data_aut)/nyears])
    data_wit = np.reshape(data_wit,[nyears-1,29])    
    row1_wit = np.ones(29)*-9999
    data_wit = np.vstack((row1_wit,data_wit))
    data_gs = np.reshape(data_gs,[nyears,len(data_gs)/nyears])
    data_yr = np.reshape(data_yr,[nyears,len(data_yr)/nyears])
    
    
    data_spr[np.isnan(data_spr)] = -9999
    data_smr[np.isnan(data_smr)] = -9999
    data_aut[np.isnan(data_aut)] = -9999
    data_wit[np.isnan(data_wit)] = -9999
    data_gs[np.isnan(data_gs)] = -9999
    data_yr[np.isnan(data_yr)] = -9999
    
    season_short = ['spr','sum','aut','wit','gs','yr']
    fld = ['NEE_VUT_REF','NEE_VUT_REF_QC','GPP_NT_VUT_REF','RECO_NT_VUT_REF','GPP_DT_VUT_REF','RECO_DT_VUT_REF','LE_F_MDS','LE_F_MDS_QC','H_F_MDS', \
           'H_F_MDS_QC', 'WUE', 'TA_F', 'TA_F_QC', 'SW_IN_F', 'SW_IN_F_QC', 'VPD_F', 'VPD_F_QC', 'P_F', 'P_F_QC', \
           'CO2_F_MDS', 'CO2_F_MDS_QC','TS_F_MDS_1', 'TS_F_MDS_1_QC','TS_F_MDS_2', 'TS_F_MDS_2_QC',\
           'SWC_F_MDS_1','SWC_F_MDS_1_QC','SWC_F_MDS_2','SWC_F_MDS_2_QC']
    fld_all = []
    for seas in season_short:
        for fd in fld:
            fld_all.append('%s_%s' %(fd, seas))
            
    indx = np.arange(startyear,endyear+1)
    
    df_spr = pd.DataFrame(data = data_spr, index = indx, columns = fld)
    outfile = '%s/spring/%s_spr.csv' %(Out_path,dirname[0:10])
    df_spr.to_csv(outfile, index_label = 'Year')
    
    
    df_smr = pd.DataFrame(data = data_smr, index = indx, columns = fld)
    outfile = '%s/summer/%s_sum.csv' %(Out_path,dirname[0:10])
    df_smr.to_csv(outfile, index_label = 'Year')
    
    
    df_aut = pd.DataFrame(data = data_aut, index = indx, columns = fld)
    outfile = '%s/autumn/%s_aut.csv' %(Out_path,dirname[0:10])
    df_aut.to_csv(outfile, index_label = 'Year')
    
    
    df_wit = pd.DataFrame(data = data_wit, index = indx, columns = fld)
    outfile = '%s/winter/%s_wit.csv' %(Out_path,dirname[0:10])
    df_wit.to_csv(outfile, index_label = 'Year')
    
    
    all_outdata = np.hstack((data_spr,data_smr,data_aut,data_wit,data_gs,data_yr))
    df_all = pd.DataFrame(data = all_outdata, index = indx, columns = fld_all)
    outfile = '%s/season_all/%s_season.csv' %(Out_path,dirname[0:10])
    df_all.to_csv(outfile, index_label = 'Year')
    
         