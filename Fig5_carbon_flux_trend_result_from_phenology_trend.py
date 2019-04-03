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


infile = "../NCOMMS-19-00016-T-SourceDataFile/Figure5.data.xlsx"
frac_SOS_data = np.asarray(pd.read_excel(infile,"Figure5a"))

frac_SOS_sig = frac_SOS_data[0,:] # [0.6,	0.4, 0.4]
frac_SOS_nosig = frac_SOS_data[1,:] #[0.058823529, 0.156862745, 0.098039216]

SOS_x_labels = ['Spring GPP','Spring ER','Spring NEE']

frac_EOS_data = np.asarray(pd.read_excel(infile,"Figure5b"))
frac_EOS_sig = frac_EOS_data[0,:]  #[0.833333333, 0.833333333, 0.166666667]
frac_EOS_nosig = frac_EOS_data[0,:]  #[0.136363636, 0.113636364, 0.136363636]

EOS_x_labels = ['Autumn GPP','Autumn ER','Autumn NEE']



width = 0.3
x_axis = np.arange(len(frac_SOS_sig))

fig=plt.figure(figsize=cm2inch(18, 6))
############### plot SOS ###############
ax1 = plt.subplot(1,2,1)
#ax1.plot([-1,12],[0,0],color='k')
rects1 = ax1.bar(x_axis-width/2, frac_SOS_sig, width, color='r',label='SOS with trend') #, yerr=envir_SOS_data_sem
rects2 = ax1.bar(x_axis+width/2, frac_SOS_nosig, width, color='b',label='SOS without trend') #, yerr=envir_SOS_data_sem
ax1.set_ylim([0.0,1])
ax1.set_xlim([-0.5,2.5])
ax1.set_xticks(range(3))
ax1.set_xticklabels(SOS_x_labels,rotation=0, fontproperties = font_tick)
ax1.grid(color = 'lightgrey',linestyle='--')
ax1.set_axisbelow(True)
ax1.set_ylabel('Ratio of site numbers with trend', fontproperties = font_label)
ax1.text(-0.4,0.9,'a: SOS', fontproperties = font_sub_title)
plt.legend([rects1,rects2], ['SOS trend','SOS no trend'],frameon=False, prop = font_tick)

ax2 = plt.subplot(1,2,2)
#ax2.plot([-1,12],[0,0],color='k')
rects3 = ax2.bar(x_axis-width/2, frac_EOS_sig, width, color='r',label='EOS_with_trend') #, yerr=envir_SOS_data_std
rects4 = ax2.bar(x_axis+width/2, frac_SOS_nosig, width, color='b',label='EOS_without_trend') #, yerr=envir_SOS_data_std
ax2.set_ylim([0.0,1])
ax2.set_xlim([-0.5,2.5])
ax2.set_xticks(range(3))
ax2.set_xticklabels(EOS_x_labels,rotation=0, fontproperties = font_tick)
ax2.set_yticklabels([])
ax2.grid(color = 'lightgrey',linestyle='--')
ax2.set_axisbelow(True)
ax2.text(-0.4,0.9,'b: EOS', fontproperties = font_sub_title)
plt.legend([rects3,rects4], ['EOS trend','EOS no trend'],frameon=False, prop = font_tick)

fig.tight_layout()
plt.subplots_adjust(left=0.05, bottom=0.05, top=0.95, right=0.95, wspace=0, hspace=0) 
plt.savefig('output_figures/Fig5_FLX_trend_phen_trend.png',format='png',dpi=300,bbox_inches='tight')
plt.show()

