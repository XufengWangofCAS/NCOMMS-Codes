# -*- coding: utf-8 -*-
"""
Created on Mon Jul 09 14:59:30 2018

@author: wxf
"""

from netCDF4 import Dataset
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

########  set the input/output path ###########################################
inpath = 'D:/3.UNH_visiting/Phenology_from_fluxnet/Paper Writing/global_warming_hiatus/CRUTEM.4'
outpath = 'D:/3.UNH_visiting/Phenology_from_fluxnet/Paper Writing/global_warming_hiatus/CRUTEM.4'

######### specify the CRUTEM4.nc file #########################################
CRUTEM4_file = '%s/CRUTEM.4.6.0.0.anomalies.nc' %(inpath)

NC_data = Dataset(CRUTEM4_file)
#print NC_data

GL_all = []
NH30_90_all = []

temperature_anomaly_all = NC_data['temperature_anomaly'] #temperature_anomaly

years = range(1850,2018)
for i in years:
    print i
    for m in range(12):
        t = (i-1850)*12+m
        temp_anomaly = temperature_anomaly_all[t,:,:]
        
        '''
        plt.imshow(temp_anomaly[18:36,:])
        plt.show()
        plt.imshow(temp_anomaly[24:36,:])
        plt.show()
        plt.imshow(temp_anomaly[24:34,:])
        plt.show()
        '''
        
        GL_all.append(np.mean(temp_anomaly))
        NH30_90_all.append(np.mean(temp_anomaly[24:36,:]))
        
        
        print np.mean(temp_anomaly[24:36,:]),np.mean(temp_anomaly[24:33,:])
        

out_monthly_data = np.transpose(np.vstack((GL_all,NH30_90_all)))
flds = ['GL_all','NH30_90_all']
out_df = pd.DataFrame(data = out_monthly_data,columns = flds)
outfile = '%s/CRU_TEM4_new_1850-2017.xlsx' %(outpath)
out_df.to_excel(outfile)


GL_avg = []
GL_spr = []
GL_smr = []
GL_aut = []
GL_wit = []

NH30_90_avg = []
NH30_90_spr = []
NH30_90_smr = []
NH30_90_aut = []
NH30_90_wit = []



for yr in years:
    start = (yr-1850)*12
    GL_avg.append(np.nanmean(GL_all[0+start:12+start]))
    GL_spr.append(np.nanmean(GL_all[2+start:5+start]))
    GL_smr.append(np.nanmean(GL_all[5+start:8+start]))
    GL_aut.append(np.nanmean(GL_all[8+start:11+start]))
    
    NH30_90_avg.append(np.nanmean(NH30_90_all[0+start:12+start]))
    NH30_90_spr.append(np.nanmean(NH30_90_all[2+start:5+start]))
    NH30_90_smr.append(np.nanmean(NH30_90_all[5+start:8+start]))
    NH30_90_aut.append(np.nanmean(NH30_90_all[8+start:11+start]))
    
    
    if(yr == 1850):
        GL_wit.append(np.nan)
        NH30_90_wit.append(np.nan)
    else:
        GL_wit.append(np.nanmean(GL_all[-1+start:2+start]))
        NH30_90_wit.append(np.nanmean(NH30_90_all[-1+start:2+start]))

            
out_season_data = np.vstack((GL_avg,GL_spr,GL_smr,GL_aut,GL_wit,\
                             NH30_90_avg,NH30_90_spr,NH30_90_smr,NH30_90_aut,NH30_90_wit))        

out_season_data = np.transpose(out_season_data)            
flds = ['GL_avg','GL_spr','GL_smr','GL_aut','GL_wit',\
        'NH30_90_avg','NH30_90_spr','NH30_90_smr','NH30_90_aut','NH30_90_wit']

out_df = pd.DataFrame(data = out_season_data,columns = flds,index = years)
outfile = '%s/CRU_TEM4_new_seasonal_1850_2018.xlsx' %(outpath)
out_df.to_excel(outfile)


        