
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

inpath = 'input'
outpath = 'output'
outpath_fig = 'output/figures'
sitename = "US-UMB"

in_file = '%s/FLX_US-UMB_FLUXNET2015_SUBSET_DD_2000-2014_1-3.csv' %(inpath)
in_data = pd.read_csv(in_file)    
multi_year_GPP_NT = in_data['GPP_NT_VUT_REF']    
multi_year_data_QC = in_data['NEE_VUT_REF_QC'] 
Time_stamp = in_data['TIMESTAMP']


start_year = 2000
end_year = 2014
end_year_name = end_year

start_row = 0 # 

i = 0
years = []
thred_p15 = get_thredhold_p15(multi_year_GPP_NT,multi_year_data_QC)

print thred_p15
            
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
    
    one_year_data_QC = multi_year_data_QC[start_row:end_row]
    
    QC_flag = Cflux_Qualit_assess(one_year_data_QC)
    
    # GPP night time ###############################
    func = Gauss_func
    ind = one_year_GPP_NT != -9999
    one_year_GPP_NT_ok = one_year_GPP_NT[ind]
    doy_ok = doy[ind]
    
    if(len(one_year_GPP_NT_ok)>330):  #### when missed value greater than 330 days, do not estimate SOS and EOS
        SOS_p15_GA_GP_NT, EOS_p15_GA_GP_NT, sm_flux_data_GA_GP_NT = get_phen_date_fixed_per15(doy_ok,one_year_GPP_NT_ok,func,thred_p15)
        
        f, (ax1, ax2) = plt.subplots(2, sharex=True)
        # plot GPP_NT, GPP_NT and NEP and soothed curve #####################
        lged1 = ax1.plot(doy,one_year_GPP_NT,color = 'grey',label='GPP_NT')
        lged3 = ax1.plot(doy_ok,sm_flux_data_GA_GP_NT, 'g--',label='GA_GPP_NT')                    
        
        #plt.plot(doy,sm_flux_data_SP, 'b:',label='Sp800')
        mval = np.nanmax(sm_flux_data_GA_GP_NT)
        lged8 = ax1.plot([SOS_p15_GA_GP_NT,SOS_p15_GA_GP_NT],[0,mval],'g--',linewidth =  2, label='GA15%_NT')
        ax1.plot([EOS_p15_GA_GP_NT,EOS_p15_GA_GP_NT],[0,mval],'g--',linewidth =  2)
        ax1.set_xlim([0,366])
        
        
        ax1.legend(bbox_to_anchor=(0.3, 0.9),framealpha=0.9,ncol = 1,fontsize = 8)
        ax1.plot([0,366],[1,1],'--',color='grey',linewidth =  1)  
        ax1.plot([0,366],[thred_p15,thred_p15],'b--',linewidth =  1)   
        print thred_p15
        
    # plot data quality date in axes2
    
        
        lged10 = ax2.plot(doy,one_year_data_QC,color = 'grey', label='QC')
        lged11 = ax2.plot([0,366],[0.75,0.75], color = 'r', label='0.75')
        
        ax2.set_xlim([0,366]) 
        ax2.set_ylim([-0.1,1.1]) 
        ax2.set_yticks([0, 0.2, 0.4, 0.6, 0.8]) 
        lns = lged10 + lged11
        labs = [l.get_label() for l in lns]
        
        ax2.legend(bbox_to_anchor=(0.5, 0.3),framealpha=0.2, ncol = 2)
        
        # Fine-tune figure; make subplots close to each other and hide x ticks for
        # all but bottom plot.
        f.subplots_adjust(hspace=0)
        plt.setp([a.get_xticklabels() for a in f.axes[:-1]], visible=False)      
        
        flux = 'GPP'        
        out_fig = '%s/GPP_phenology_%s_%d_QC%d.png' %(outpath_fig,sitename,year,QC_flag)
        plt.savefig(out_fig,fmt = 'png',dpi = 150, bbox_inches='tight')
        plt.show()
        plt.close()
        
        phen_temp = np.asarray([SOS_p15_GA_GP_NT, EOS_p15_GA_GP_NT, QC_flag])
        
    if(yr == start_year):
        out_phen = phen_temp
    else:
        out_phen =np.vstack((out_phen, phen_temp))
            
    # get start for next loop
    start_row = start_row + days
    
    if(len(years) > 0):
        flds = ['SOS_15%_GA_GP_NT','EOS_15%_GA_GP_NT', 'QC_flag']
        
    if(len(years)==1):
        out_phen=np.reshape(out_phen,[1,3])
    
out_df = pd.DataFrame(data = out_phen, index = years, columns = flds)
outfile = '%s/GPP_phenology_%s_%d_%d.csv' %(outpath,sitename,start_year,end_year_name)
out_df.to_csv(outfile)

