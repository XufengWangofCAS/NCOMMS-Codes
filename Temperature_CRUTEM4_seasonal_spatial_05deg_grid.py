# -*- coding: utf-8 -*-
"""
Created on Mon Feb 25 23:39:07 2019

@author: wxf
"""

# -*- coding: utf-8 -*-
"""
Created on Mon Jul 09 14:59:30 2018

@author: wxf
"""

from netCDF4 import Dataset
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import Geotiff_read_write as Geotiff_RW
import MK_trend as MK

#######  set the input/output path ############################################
inpath = 'D:/3.UNH_visiting/Phenology_from_fluxnet/Paper Writing/global_warming_hiatus/CRUTEM.4/CRUTEM4.02_grid0.5deg'
outpath = 'D:/3.UNH_visiting/Phenology_from_fluxnet/Paper Writing/global_warming_hiatus/CRUTEM.4/CRUTEM4.02_grid0.5deg/seasonal_average_tifs'


#print NC_data
refer_tif_file_CRUTEM4 = "tmp_geo_reference.tif"
[GeoT, Proj] = Geotiff_RW.GetGeoInfo(refer_tif_file_CRUTEM4)

  #temperature_anomaly
  
GL_all = []
NH_all = []
NH30_90_all = []
NH30_75_all = []
SH_all = []


start_year = [1981, 1991, 2001, 2011]
end_year = [1990, 2000, 2010, 2017]


for i in range(len(start_year)):
    print i
    CRUTEM4_file = '%s/cru_ts4.02.%d.%d.tmp.dat.nc' %(inpath,start_year[i],end_year[i])
    NC_data = Dataset(CRUTEM4_file)
    temperature_anomaly_all = NC_data['tmp'] 
    for yr in range(start_year[i],end_year[i]+1):
        for m in range(12):
            t = (yr-start_year[i])*12+m
            temp_anomaly = np.asarray(temperature_anomaly_all[t,:,:])
            fill_value = np.max(temp_anomaly)
            print(fill_value)
            temp_anomaly[temp_anomaly == fill_value] = np.nan
            '''
            plt.imshow(temp_anomaly[180:360,:])
            plt.show()
            plt.imshow(temp_anomaly[240:360,:])
            plt.show()
            plt.imshow(temp_anomaly[240:340,:])
            plt.show()
            '''
            
            GL_all.append(np.nanmean(temp_anomaly))
            NH_all.append(np.nanmean(temp_anomaly[180:360,:]))
            NH30_90_all.append(np.nanmean(temp_anomaly[240:360,:]))
            NH30_75_all.append(np.nanmean(temp_anomaly[240:340,:]))
            SH_all.append(np.nanmean(temp_anomaly[0:180,:]))
        
        
            temp_anomaly = np.reshape(temp_anomaly,[1,360*720]).squeeze()            
            if(m==0):
                temp_all = temp_anomaly
            else:
                temp_all = np.vstack((temp_all,temp_anomaly))
        
        
        
        
        temp_spring = np.mean(temp_all[2:5,:],axis=0)
        temp_autumn = np.mean(temp_all[8:11,:],axis=0)
        temp_yr = np.mean(temp_all,axis=0)
        Xsize = 720
        Ysize = 360
        
        temp_spring = np.reshape(temp_spring,[Ysize,Xsize])
        temp_autumn = np.reshape(temp_autumn,[Ysize,Xsize])
        temp_yr = np.reshape(temp_yr,[Ysize,Xsize])
        
        for r in range(Ysize/2):
            a = temp_spring[r,:].copy()
            temp_spring[r,:] = temp_spring[Ysize-1-r,:]
            temp_spring[Ysize-1-r,:] = a
            
       
            b = temp_autumn[r,:].copy()
            temp_autumn[r,:] = temp_autumn[Ysize-1-r,:]
            temp_autumn[Ysize-1-r,:] = b
            
            c = temp_yr[r,:].copy()
            temp_yr[r,:] = temp_yr[Ysize-1-r,:]
            temp_yr[Ysize-1-r,:] = c
        
        
    
        plt.imshow(temp_spring)
        plt.show()
        plt.imshow(temp_autumn)
        plt.show()
        plt.imshow(temp_yr)
        plt.show()
        
        temp_spring[np.isnan(temp_spring)]= -9999.0
        temp_autumn[np.isnan(temp_autumn)]= -9999.0
        temp_yr[np.isnan(temp_yr)]= -9999.0
        
        NoData_value = -9999.0
        outfile_TEMP_spr = '%s/CRUTEM4v_05deg_spr_%d' %(outpath,yr)
        Geotiff_RW.CreateGeoTiff(outfile_TEMP_spr, temp_spring, Xsize, Ysize, GeoT, Proj, NoData_value)
        
        outfile_TEMP_aut = '%s/CRUTEM4v_05deg_aut_%d' %(outpath,yr)
        Geotiff_RW.CreateGeoTiff(outfile_TEMP_aut, temp_autumn, Xsize, Ysize, GeoT, Proj, NoData_value)
        
        outfile_TEMP_yr = '%s/CRUTEM4v_05deg_year_%d' %(outpath,yr)
        Geotiff_RW.CreateGeoTiff(outfile_TEMP_yr, temp_yr, Xsize, Ysize, GeoT, Proj, NoData_value)
    


out_monthly_data = np.transpose(np.vstack((GL_all,NH_all,NH30_90_all,NH30_75_all,SH_all)))
flds = ['GL_all','NH_all','NH30_90_all','NH30_75_all','SH_all']
out_df = pd.DataFrame(data = out_monthly_data,columns = flds)
outfile = '%s/CRU_TEM4_05deg_1981-2017.xlsx' %(outpath)
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

years_out = range(1981,2018)
for yr in range(1981,2018):
    start = (yr-1981)*12
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
    
    if(yr == 1981):
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

out_df = pd.DataFrame(data = out_season_data,columns = flds,index = years_out)
outfile = '%s/CRU_TEM4_05deg_seasonal_1981_2017.xlsx' %(outpath)
out_df.to_excel(outfile)





