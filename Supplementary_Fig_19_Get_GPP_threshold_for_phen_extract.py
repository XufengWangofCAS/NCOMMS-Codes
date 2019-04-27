
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 06 20:50:59 2016

@author: wxf
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os
import glob
import calendar
from GPP_smooth_func import *
from matplotlib.font_manager import FontProperties

plt.rcParams["font.family"] = "Arial"
font0 = FontProperties()

font0 = FontProperties()
font_sub_title = font0.copy()
font_sub_title.set_size('12')
font_sub_title.set_weight('bold')

font_label = font0.copy()
font_label.set_size('11')
font_label.set_weight('bold')

font_tick = font0.copy()
font_tick.set_size('10')

def cm2inch(*tupl):
    inch = 2.54
    if isinstance(tupl[0], tuple):
        return tuple(i/inch for i in tupl[0])
    else:
        return tuple(i/inch for i in tupl) 

fontP = FontProperties()
fontP.set_name('Arial')
fontP.set_size(10)


# fluxnet daily data path
in_dir = 'D:/10.data/fluxnet2015_tier2_updated_Nov_3_2016/unzip_data/FLX_US-UMB_FLUXNET2015_SUBSET_2000-2014_1-3'
# fluxnet daily data file (choose site have high quality data for all the year)
fl = 'FLX_US-UMB_FLUXNET2015_SUBSET_DD_2000-2014_1-3.csv'

in_file = "%s/%s" %(in_dir,fl)
in_data = pd.read_csv(in_file)    
multi_year_GPP_NT = in_data['GPP_NT_VUT_REF']     #GPP_NT_VUT_REF
multi_year_GPP_DT = in_data['GPP_DT_VUT_REF']
        
multi_year_NEE = in_data['NEE_VUT_REF']
        
multi_year_data_QC = in_data['NEE_VUT_REF_QC'] 
Time_stamp = in_data['TIMESTAMP']
        

#### exclude according the lat
start_year = int(fl[33:37])
end_year = int(fl[38:42])
end_year_name = end_year



SOS_std = []
EOS_std = []
per = range(4,30,2)
for i in range(4,30,2):
    thred_NT = get_thredhold_flexible(multi_year_GPP_NT,multi_year_data_QC, i/100.0)
    thred_DT = get_thredhold_flexible(multi_year_GPP_DT,multi_year_data_QC, i/100.0)
    print thred_NT, thred_DT
    
    SOS_NT = []
    SOS_DT = []
    EOS_NT = []
    EOS_DT = []
    
    start_row = 0
    years = []
    for yr in range(start_year,end_year+1):
        year = np.floor(Time_stamp[start_row]/10000.0)
        
        years.append(year)
        if (calendar.isleap(year)):
            days = 366
        else:
            days = 365                 
        doy = np.arange(1,days+1)
        print year, days
        end_row =  start_row + days   
        one_year_GPP_NT = np.asarray(multi_year_GPP_NT[start_row:end_row])
        one_year_GPP_DT = np.asarray(multi_year_GPP_DT[start_row:end_row])
        one_year_NEE = np.asarray(multi_year_NEE[start_row:end_row])
        
        one_year_NEP = -one_year_NEE
        
        one_year_data_QC = multi_year_data_QC[start_row:end_row]
        
        
        QC_flag = Cflux_Qualit_assess(one_year_data_QC)
        
        # GPP night time ###############################
        func = Gauss_func
        ind = one_year_GPP_NT != -9999
        one_year_GPP_NT_ok = one_year_GPP_NT[ind]
        doy_ok = doy[ind]
        
        ind_DT = one_year_GPP_DT != -9999
        one_year_GPP_DT_ok = one_year_GPP_DT[ind_DT]
        doy_DT_ok = doy[ind]
        
        if(len(one_year_GPP_NT_ok)>300 and len(one_year_GPP_DT_ok)>300):
            SOS_p15_GA_GP_NT, EOS_p15_GA_GP_NT, sm_flux_data_GA_GP_NT = get_phen_date_fixed_per15(doy_ok,one_year_GPP_NT_ok,func,thred_NT)
            
            SOS_p15_GA_GP_DT, EOS_p15_GA_GP_DT, sm_flux_data_GA_GP_DT = get_phen_date_fixed_per15(doy_DT_ok,one_year_GPP_DT_ok,func,thred_NT)
            
            SOS_NT.append(SOS_p15_GA_GP_NT)
            EOS_NT.append(EOS_p15_GA_GP_NT)
            
            SOS_DT.append(SOS_p15_GA_GP_DT)
            EOS_DT.append(EOS_p15_GA_GP_DT)

            
            fig=plt.figure(figsize=cm2inch(14, 6))
            ax1 = plt.subplot(1,1,1)
            # plot GPP_NT, GPP_NT and NEP and soothed curve #####################
            lged1 = ax1.plot(doy,one_year_GPP_NT,color = 'lightgreen',label='GPP_NT',linewidth = 1)
            #lged11 = ax1.plot(doy,one_year_GPP_DT,color = 'lightblue',label='GPP_DT',linewidth = 1)                    
            lged3 = ax1.plot(doy_ok,sm_flux_data_GA_GP_NT, 'g--',label='GPP_NT_smooth',linewidth = 1)                    
            #lged31 = ax1.plot(doy,sm_flux_data_GA_GP_DT, 'b--',label='GPP_DT_smooth',linewidth = 1)
            
            
            #plt.plot(doy,sm_flux_data_SP, 'b:',label='Sp800')
            mval = np.nanmax(sm_flux_data_GA_GP_NT)
            
            lged8 = ax1.plot([SOS_p15_GA_GP_NT,SOS_p15_GA_GP_NT],[0,mval],'g--',linewidth =  2, label='Phen_GPP_NT')
            
            ax1.plot([EOS_p15_GA_GP_NT,EOS_p15_GA_GP_NT],[0,mval],'g--',linewidth =  2)
            
            #lged81 = ax1.plot([SOS_p15_GA_GP_DT,SOS_p15_GA_GP_DT],[mval/2,mval],'k--',linewidth =  2, label='Phen_GPP_DT')
            
            #ax1.plot([EOS_p15_GA_GP_DT,EOS_p15_GA_GP_DT],[mval/2,mval],'k--',linewidth =  2)        
            
            ax1.set_xlim([0,366])
            ax1.set_yticks([0,5,10,15])
            ax1.set_yticklabels([0,5,10,15],fontproperties = font_tick)
            ax1.set_xticks([0,50,100,150,200,250,300,350])
            ax1.set_xticklabels([0,50,100,150,200,250,300,350],fontproperties = font_tick)
            ax1.set_ylabel("GPP (gC/m$^2$/day)",fontproperties = font_label)
            ax1.set_xlabel("Doy", fontproperties = font_label)
            
            
            L = ax1.legend(bbox_to_anchor=(0.35, 0.8),framealpha=0.8,ncol = 1, frameon = False)
            plt.setp(L.texts, fontname='Arial',fontsize = 8)
            #ax1.plot([0,366],[1,1],'--',color='grey',linewidth =  1)  
            ax1.plot([0,366],[thred_NT,thred_NT],'b--',linewidth =  1)   
           
            flux = 'GPP'        

            plt.show()
            plt.close()
            
            # get start for next loop
            start_row = start_row + days
            
    SOS_NT = np.asarray(SOS_NT)
    SOS_DT = np.asarray(SOS_DT)
    EOS_NT = np.asarray(EOS_NT)
    EOS_DT = np.asarray(EOS_DT)    
    
    SOS_std.append(np.std(SOS_NT-SOS_DT))
    EOS_std.append(np.std(EOS_NT-EOS_DT))

plt.plot(per,SOS_std,label = 'SOS')
plt.plot(per,EOS_std,label = 'EOS')
plt.xlabel('Thredhold (%)', fontproperties = font_label)
plt.ylabel('Standard devation (Days)', fontproperties = font_label)
plt.grid(color='Gray',linestyle = '--')
plt.legend(prop = font_label, frameon = False)
out_fig = 'output_figures/FigS19_get_Threshold.png'
plt.savefig(out_fig,fmt = 'png',dpi = 300, bbox_inches='tight')
plt.show()
    
    
    
    
            