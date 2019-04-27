# -*- coding: utf-8 -*-
"""
Created on Sat Feb 23 21:41:47 2019

@author: wxf
"""

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

infile_envir = '../NCOMMS-19-00016-T-SourceDataFile/Supplementary_Figure_16_phen_enviro_two_group_forest.xlsx'

envir_SOS_data_group1 = pd.read_excel(infile_envir,'FigureS16a')
envir_SOS_data_group2 = pd.read_excel(infile_envir,'FigureS16b')
envir_EOS_data_group1 = pd.read_excel(infile_envir,'FigureS16c')
envir_EOS_data_group2 = pd.read_excel(infile_envir,'FigureS16d')

flds_SOS = ['Spring Tair','Winter Tair','Spring VPD','Winter VPD','Spring Prec','Winter Prec','Spring SR',\
        'Winter SR','Spring TS','Winter TS', 'Spring SWC','Winter SWC']
        
flds_EOS = ['Summer Tair','Autumn Tair','Summer VPD','Autumn VPD','Summer Prec','Autumn Prec','Summer SR',\
        'Autumn SR','Summer TS','Autumn TS', 'Summer SWC','Autumn SWC']
        


envir_SOS_data_group1_R = np.asarray(envir_SOS_data_group1).squeeze()
envir_SOS_data_group2_R = np.asarray(envir_SOS_data_group2).squeeze()

envir_EOS_data_group1_R = np.asarray(envir_EOS_data_group1).squeeze()
envir_EOS_data_group2_R = np.asarray(envir_EOS_data_group2).squeeze()


width = 0.7
x_axis = range(len(envir_SOS_data_group1_R))

fig=plt.figure(figsize=cm2inch(19, 12))
############### plot SOS ###############
ax_SOS_group1 = plt.subplot(2,2,1)
ax_SOS_group1.plot([-1,12],[0,0],color='k')
rects1 = ax_SOS_group1.bar(x_axis, envir_SOS_data_group1_R, width, color='g')   #
ax_SOS_group1.set_ylim([-1,1])
ax_SOS_group1.set_yticks([-0.8, -0.4, 0, 0.4, 0.8])
ax_SOS_group1.set_yticklabels([-0.8, -0.4, 0, 0.4, 0.8],fontproperties = font_tick)
ax_SOS_group1.set_xlim([-1,12])
ax_SOS_group1.set_xticks(range(12))
#ax_SOS_group1.set_xticklabels(flds_SOS,rotation=90)
ax_SOS_group1.grid(color = 'lightgrey',linestyle='--')
ax_SOS_group1.set_axisbelow(True)
ax_SOS_group1.set_ylabel('Average Correlation Coefficient',y=0,fontproperties = font_label)
ax_SOS_group1.text(0,0.8,'a: Group1 SOS',fontproperties = font_sub_title)

ax_SOS_group2 = plt.subplot(2,2,3)
ax_SOS_group2.plot([-1,12],[0,0],color='k')
rects3 = ax_SOS_group2.bar(x_axis, envir_SOS_data_group2_R, width, color='g')   #
ax_SOS_group2.set_ylim([-1,1])
ax_SOS_group2.set_yticks([-0.8, -0.4, 0, 0.4, 0.8])
ax_SOS_group2.set_yticklabels([-0.8, -0.4, 0, 0.4, 0.8],fontproperties = font_tick)
ax_SOS_group2.set_xlim([-1,12])
ax_SOS_group2.set_xticks(range(12))
ax_SOS_group2.set_xticklabels(flds_SOS,rotation=90,fontproperties = font_tick)
ax_SOS_group2.grid(color = 'lightgrey',linestyle='--')
ax_SOS_group2.set_axisbelow(True)
#ax_SOS_group2.set_ylabel('Correlation Coefficient')
ax_SOS_group2.text(0,0.8,'b: Group2 SOS',fontproperties = font_sub_title)


ax_EOS_group1 = plt.subplot(2,2,2)
ax_EOS_group1.plot([-1,12],[0,0],color='k')
rects2 = ax_EOS_group1.bar(x_axis, envir_EOS_data_group1_R, width, color='g') #, yerr=envir_EOS_data_std
ax_EOS_group1.set_ylim([-1,1])
ax_EOS_group1.set_yticks([-0.8, -0.4, 0, 0.4, 0.8])
ax_EOS_group1.set_yticklabels([-0.8, -0.4, 0, 0.4, 0.8],fontproperties = font_tick)
ax_EOS_group1.set_xlim([-1,12])
ax_EOS_group1.set_xticks(range(12))
#ax_EOS_group1.set_xticklabels(flds_EOS,rotation=90)
ax_EOS_group1.set_yticklabels([])
ax_EOS_group1.grid(color = 'lightgrey',linestyle='--')
ax_EOS_group1.set_axisbelow(True)
ax_EOS_group1.text(0,0.8,'c: Group1 EOS',fontproperties = font_sub_title)

ax_EOS_group2 = plt.subplot(2,2,4)
ax_EOS_group2.plot([-1,12],[0,0],color='k')
rects4 = ax_EOS_group2.bar(x_axis, envir_EOS_data_group2_R, width, color='g') #, yerr=envir_EOS_data_std
ax_EOS_group2.set_ylim([-1,1])
ax_EOS_group2.set_yticks([-0.8, -0.4, 0, 0.4, 0.8])
ax_EOS_group2.set_yticklabels([-0.8, -0.4, 0, 0.4, 0.8],fontproperties = font_tick)
ax_EOS_group2.set_xlim([-1,12])
ax_EOS_group2.set_xticks(range(12))
ax_EOS_group2.set_xticklabels(flds_EOS,rotation=90,fontproperties = font_tick)
ax_EOS_group2.set_yticklabels([])
ax_EOS_group2.grid(color = 'lightgrey',linestyle='--')
ax_EOS_group2.set_axisbelow(True)
ax_EOS_group2.text(0,0.8,'d: Group2 EOS',fontproperties = font_sub_title)


fig.tight_layout()
plt.subplots_adjust(left=0.05, bottom=0.05, top=0.95, right=0.95, wspace=0, hspace=0) 
plt.savefig('output_figures/FigS16_species_FLX_phen_envir_CC_with_yerr.png',format='png',dpi=300,bbox_inches='tight')
plt.show()

