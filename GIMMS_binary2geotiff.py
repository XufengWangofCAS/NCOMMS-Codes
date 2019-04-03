
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 21 10:19:47 2016

@author: wxf
"""

import numpy as np
import matplotlib.pyplot as plt
import Geotiff_read_write as Geotiff_RW

inpath = 'E:/Data/NDVI_GIMMS_3g_1982_2013/AVHRR_3g'
outpath = 'E:/Data/NDVI_GIMMS_3g_1982_2013/AVHRR_3g_tiff'

import Geotiff_read_write as Geotiff_RW

refer_tif_file_gimms3g= 'GIMMS_1982_01_a.tif'

[GeoT, Proj] = Geotiff_RW.GetGeoInfo(refer_tif_file_gimms3g)


yearly_GSNDVI_avg=np.full((2160,4320), 0.0, dtype=float)
imgs=0.0

years=range(1982,2014)
months=['jan','feb','mar','apr','may','jun','jul','aug','sep','oct','nov','dec']
bimonthly=['a','b']

for year in years:   
    for m in months:
        for b in bimonthly:
            if(year<=1985):
                sat='n07'
                if((year==1985) and (months.index(m)>1)):
                    sat='n09'
            elif(year<=1988):
                sat='n09'
                if((year==1988) and (months.index(m)>9)):
                    sat='n11'
            elif((year<=1994) ):
                sat='n11'
                if((year==1994) and (months.index(m)>7)):
                    sat='n09'
            elif(year<=2000):
                sat='n14'
                if((year==2000) and (months.index(m)>9)):
                    sat='n16'
                if((year==1995) and (months.index(m)==0) and (b=='a')):
                    sat='n09'
            elif(year<=2003):
                sat='n16'
            elif(year<=2008):
                sat='n17'
            elif(year<=2011):
                sat='n18'
            elif(year<=2013):
                sat='n19'
            
            print year
            
            st=str(year)[2:4]
            fname = "%s/gimms%d/geo%s%s15%s.%s-VI3g"  %(inpath,year,st,m,b,sat)
            f=open(fname,"r")            
            print fname
            
            ndvi3g = np.fromfile(f,dtype='>i2' ) #dtype='>i2'
            ndvi3g = np.reshape(ndvi3g,(4320,2160))
            ndvi3g = np.transpose(ndvi3g)     
            
            data = ndvi3g.copy()
            data = np.asarray(data)*1.0    
            
            
            outfile_tif = '%s/GIMMS3g_NDVI_%d_%02d_%d' %(outpath,year,months.index(m)+1,bimonthly.index(b)+1)
            
            [Ysize, Xsize] = ndvi3g.shape
            
            NoData_value = -10000.0
            
            
            Geotiff_RW.CreateGeoTiff(outfile_tif, data, Xsize, Ysize, GeoT, Proj, NoData_value)
            
            del data
            del ndvi3g
            





