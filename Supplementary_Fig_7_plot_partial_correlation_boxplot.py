# -*- coding: utf-8 -*-
"""
Created on Wed Aug 08 15:28:45 2018

@author: wxf
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stat
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

infile = "../NCOMMS-19-00016-T-SourceDataFile/Supplementary_Figure_7_Pcor_phenology_enviro_cor_season.xlsx"

envir_SOS_data = pd.read_excel(infile,'FigureS7a')
envir_EOS_data = pd.read_excel(infile,'FigureS7b')

flds_SOS = ['Spring Tair','Winter Tair', 'Spring VPD', 'Winter VPD', 'Spring Prec', 'Winter Prec', 'Spring SR', 'Winter SR']  
flds_EOS = ['Summer Tair','Autumn Tair', 'Summer VPD', 'Autumn VPD', 'Summer Prec', 'Autumn Prec', 'Summer SR', 'Autumn SR']
        

envir_SOS_data = np.asarray(envir_SOS_data)
envir_SOS_data = np.asarray(envir_SOS_data[:,1:9],dtype = float)
ind = envir_SOS_data == -9999
envir_SOS_data[ind] = np.nan

envir_SOS_data_R = np.nanmean(envir_SOS_data,axis=0)
envir_SOS_data_var = np.nanvar(envir_SOS_data,axis=0,ddof=0)
envir_SOS_data_std = np.nanstd(envir_SOS_data,axis=0,ddof=0)

#envir_SOS_data_sem = stat.sem(envir_SOS_data,axis=0, nan_policy = 'omit')

envir_EOS_data = np.asarray(envir_EOS_data)
envir_EOS_data = np.asarray(envir_EOS_data[:,1:9],dtype = float)
ind = envir_EOS_data == -9999
envir_EOS_data[ind] = np.nan

envir_EOS_data_R = np.nanmean(envir_EOS_data,axis=0)
envir_EOS_data_var = np.nanvar(envir_EOS_data,axis=0,ddof=0)
envir_EOS_data_std = np.nanstd(envir_EOS_data,axis=0,ddof=0)
#envir_EOS_data_sem = stat.sem(envir_EOS_data,axis=0, nan_policy = 'omit')

width = 0.7
x_axis = range(len(envir_SOS_data_R))

fig=plt.figure(figsize=cm2inch(18, 6))
############### plot SOS ###############
ax1 = plt.subplot(1,2,1)
ax1.plot([-1,9],[0,0],color='k')

SOS_box = ax1.boxplot(envir_SOS_data,showmeans=True)
ax1.set_xlim([0,9])
ax1.set_xticks(range(1,9))
ax1.set_ylim([-1.1,1.1])
ax1.set_xticklabels(flds_SOS,rotation=30, x=0.3,fontproperties = font_tick)
ax1.set_ylabel('Partial Correlation Coefficient',fontproperties = font_label)
ax1.set_xlabel('Variable name',x=1,fontproperties = font_label)
ax1.text(0.1,0.9,'a: SOS',fontproperties = font_sub_title)

ax1.grid(color='lightgray',linestyle = "--")
ax1.set_axisbelow(True)


for median in SOS_box['medians']:
    median.set(color='r', linewidth=1)
for whisker in SOS_box['whiskers']:
    whisker.set(color='gray', linewidth=1)
for cap in SOS_box['caps']:
    cap.set(color='gray', linewidth=1)

ax2 = plt.subplot(1,2,2)
ax2.plot([-1,9],[0,0],color='k')
EOS_box = ax2.boxplot(envir_EOS_data,showmeans=True)
#rects1 = ax2.bar(x_axis, envir_EOS_data_R, width, color='g',yerr=envir_EOS_data_std, linewidth=0.4,ecolor='k', capsize=5) #, yerr=envir_EOS_data_std

ax2.set_xlim([0,9])
ax2.set_xticks(range(1,9))
ax2.set_ylim([-1.1, 1.1])
ax2.set_yticklabels("")
ax2.set_xticklabels(flds_EOS,rotation=30, x=0.3, fontproperties = font_tick)

ax2.grid(color='lightgray',linestyle = "--")
ax2.set_axisbelow(True)


for median in EOS_box['medians']:
    median.set(color='r', linewidth=1)
for whisker in EOS_box['whiskers']:
    whisker.set(color='gray', linewidth=1)
for cap in EOS_box['caps']:
    cap.set(color='gray', linewidth=1)

ax2.text(7.1,0.9,'b: EOS',fontproperties = font_sub_title)

fig.tight_layout()
plt.subplots_adjust(left=0.05, bottom=0.05, top=0.95, right=0.95, wspace=0, hspace=0) 
plt.savefig('output_figures/FigS7_partial_cor_FLX_phen_envir_CC_with_yerr.png',format='png',dpi=300,bbox_inches='tight')
plt.show()

