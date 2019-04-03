# -*- coding: utf-8 -*-
"""
Created on Mon Jul 09 14:59:30 2018

@author: wxf
"""

from netCDF4 import Dataset
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

inpath = 'D:/3.UNH_visiting/Phenology_from_fluxnet/Paper Writing/NC_submission/revise_round1/TEMP_data/NOAA'
outpath = 'D:/3.UNH_visiting/Phenology_from_fluxnet/Paper Writing/NC_submission/revise_round1/TEMP_data/NOAA'

NOAA_file = 'D:/3.UNH_visiting/Phenology_from_fluxnet/Paper Writing/NC_submission/revise_round1/TEMP_data/NOAA/grid-mntp-1880-current-v3.3.0.dat'


GL_all = []
NH_all = []
NH30_90_all = []
NH30_75_all = []
SH_all = []

#temperature_anomaly_all = np.genfromtxt(NOAA_file,skip_header=1,skip_footer=(62160-37))

years = range(1880,2018)
for i in years:
    print i
    for m in range(12):
        t = (i-1880)*12+m
        s_header = t*37 +1
        s_footer = 62160 - s_header- 36
        
        temp_anomaly = np.asarray(np.genfromtxt(NOAA_file, skip_header=s_header, skip_footer=s_footer))
        temp_anomaly[temp_anomaly == -9999] = np.nan
        
        plt.imshow(temp_anomaly)
        plt.show()
        '''
        '''
        plt.imshow(temp_anomaly[0:18,:])
        plt.show()
        
        plt.imshow(temp_anomaly[0:12,:])
        plt.show()
        
        
        GL_all.append(np.nanmean(temp_anomaly))
        NH_all.append(np.nanmean(temp_anomaly[0:18,:]))
        NH30_90_all.append(np.nanmean(temp_anomaly[0:12,:]))
        NH30_75_all.append(np.nanmean(temp_anomaly[4:12,:]))
        SH_all.append(np.nanmean(temp_anomaly[18:36,:]))
        
        print np.nanmean(temp_anomaly[0:12,:]),np.nanmean(temp_anomaly[4:12,:])
        
out_monthly_data = np.transpose(np.vstack((GL_all,NH_all,NH30_90_all,NH30_75_all,SH_all)))
flds = ['GL_all','NH_all','NH30_90_all','NH30_75_all','SH_all']
out_df = pd.DataFrame(data = out_monthly_data,columns = flds)
outfile = '%s/NOAA_new_1750-2017.xlsx' %(outpath)
out_df.to_excel(outfile)


GL_avg = []
GL_spr = []
GL_smr = []
GL_aut = []
GL_wit = []

NH_avg = []
NH_spr = []
NH_smr = []
NH_aut = []
NH_wit = []

NH30_90_avg = []
NH30_90_spr = []
NH30_90_smr = []
NH30_90_aut = []
NH30_90_wit = []

NH30_75_avg = []
NH30_75_spr = []
NH30_75_smr = []
NH30_75_aut = []
NH30_75_wit = []


for yr in years:
    start = (yr-1880)*12
    GL_avg.append(np.nanmean(GL_all[0+start:12+start]))
    GL_spr.append(np.nanmean(GL_all[2+start:5+start]))
    GL_smr.append(np.nanmean(GL_all[5+start:8+start]))
    GL_aut.append(np.nanmean(GL_all[8+start:11+start]))
    
    NH_avg.append(np.nanmean(NH_all[0+start:12+start]))
    NH_spr.append(np.nanmean(NH_all[2+start:5+start]))
    NH_smr.append(np.nanmean(NH_all[5+start:8+start]))
    NH_aut.append(np.nanmean(NH_all[8+start:11+start]))
    
    NH30_90_avg.append(np.nanmean(NH30_90_all[0+start:12+start]))
    NH30_90_spr.append(np.nanmean(NH30_90_all[2+start:5+start]))
    NH30_90_smr.append(np.nanmean(NH30_90_all[5+start:8+start]))
    NH30_90_aut.append(np.nanmean(NH30_90_all[8+start:11+start]))
    
    NH30_75_avg.append(np.nanmean(NH30_75_all[0+start:12+start]))
    NH30_75_spr.append(np.nanmean(NH30_75_all[2+start:5+start]))
    NH30_75_smr.append(np.nanmean(NH30_75_all[5+start:8+start]))
    NH30_75_aut.append(np.nanmean(NH30_75_all[8+start:11+start]))
    
    if(yr == 1750):
        GL_wit.append(np.nan)
        NH_wit.append(np.nan)
        NH30_90_wit.append(np.nan)
        NH30_75_wit.append(np.nan)
    else:
        GL_wit.append(np.nanmean(GL_all[-1+start:2+start]))
        NH_wit.append(np.nanmean(NH_all[-1+start:2+start]))
        NH30_90_wit.append(np.nanmean(NH30_90_all[-1+start:2+start]))
        NH30_75_wit.append(np.nanmean(NH30_75_all[-1+start:2+start]))

            
out_season_data = np.vstack((GL_avg,GL_spr,NH_smr,GL_aut,GL_wit,\
                             NH_avg,NH_spr,NH_smr,NH_aut,NH_wit,\
                             NH30_90_avg,NH30_90_spr,NH30_90_smr,NH30_90_aut,NH30_90_wit,\
                             NH30_75_avg,NH30_75_spr,NH30_75_smr,NH30_75_aut,NH30_75_wit))        

out_season_data = np.transpose(out_season_data)            
flds = ['GL_avg','GL_spr','NH_smr','GL_aut','GL_wit',\
        'NH_avg','NH_spr','NH_smr','NH_aut','GL_wit',\
        'NH30_90_avg','NH30_90_spr','NH30_90_smr','NH30_90_aut','NH30_90_wit',\
        'NH30_75_avg','NH30_75_spr','NH30_75_smr','NH30_75_aut','NH30_75_wit']

out_df = pd.DataFrame(data = out_season_data,columns = flds,index = years)
outfile = '%s/NOAA_new_seasonal_1750_2018.xlsx' %(outpath)
out_df.to_excel(outfile)


        