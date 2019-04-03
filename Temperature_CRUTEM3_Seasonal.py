# -*- coding: utf-8 -*-
"""
Created on Mon Jul 09 14:59:30 2018

@author: wxf
"""

from netCDF4 import Dataset
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

#### set the input/output path ################################################
inpath = 'D:/3.UNH_visiting/Phenology_from_fluxnet/Paper Writing/global_warming_hiatus/CRUTEM.4'
outpath = 'D:/3.UNH_visiting/Phenology_from_fluxnet/Paper Writing/global_warming_hiatus/CRUTEM.4'

##### specify the CRUTEM3.nc file #############################################
CRUTEM3_file = '%s/CRUTEM3.nc' %(inpath)

NC_data = Dataset(CRUTEM3_file)
print NC_data



GL_all = []
NH30_90_all = []


unspecified = NC_data['unspecified']
temperature_anomaly_all = NC_data['temp'] #temperature_anomaly

years = range(1850,2014)
for i in years:
    print i
    for m in range(12):
        t = (i-1850)*12+m
        temp_anomaly = temperature_anomaly_all[t,0,:,:]
        
        
        plt.imshow(temp_anomaly[18:36,:])
        plt.show()
        plt.imshow(temp_anomaly[24:36,:])
        plt.show()
        
        
        GL_all.append(np.mean(temp_anomaly))
        NH30_90_all.append(np.mean(temp_anomaly[24:36,:]))
        

out_monthly_data = np.transpose(np.vstack((GL_all,NH_all,NH30_90_all,SH_all)))
flds = ['GL_all','NH30_90_all']
out_df = pd.DataFrame(data = out_monthly_data,columns = flds)
outfile = '%s/CRU_TEM3.xlsx' %(outpath)
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
outfile = '%s/CRU_TEM3_seasonal.xlsx' %(outpath)
out_df.to_excel(outfile)


        