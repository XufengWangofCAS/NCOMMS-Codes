# -*- coding: utf-8 -*-
"""
Created on Tue May 30 15:52:21 2017

@author: wxf
"""
import os
import glob
import pandas as pd
import numpy as np
import calendar
import matplotlib.pyplot as plt
import scipy.stats as stat
import MK_trend as MK
from matplotlib import gridspec
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

def autolabel(ax,rects):
    """
    Attach a text label above each bar displaying its height
    """
    for rect in rects:
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width()/2., 0.5+height,
                '%d' % int(height),
                ha='center', va='bottom')    

############################################################################
############## main program start here #####################################
############################################################################


infile = "../NCOMMS-19-00016-T-SourceDataFile/Figure2.data.xlsx"
SOS_data = pd.read_excel(infile,"Figure2a")
EOS_data = pd.read_excel(infile,"Figure2c")
SOS_data_MK_trend = pd.read_excel(infile,"Figure2b")
EOS_data_MK_trend = pd.read_excel(infile,"Figure2d")

phen_sites = []
start_year = []
end_year = []

    

################## plot SOS spaghetti ##################################################

fig=plt.figure(figsize=cm2inch(19, 15))
gs = gridspec.GridSpec(2, 2, width_ratios=[2, 1]) 
ax1 = plt.subplot(gs[0])
SOS_data = np.asarray(SOS_data)
for i in range(56):
    ### read data
    SOS_ind = i*2+1
    SOS_flag_ind = i*2+2
    
    
    SOS = np.asarray(SOS_data[:,SOS_ind])
    phen_QC = np.asarray(SOS_data[:,SOS_flag_ind])
    years_phen = np.asarray(SOS_data[:,0])
    
    
    ### plot SOS ########
    ind = (phen_QC  > 0 ) & (SOS > 0)
    SOS_ok = SOS[ind]
    SOS_ok_anomalies = (SOS[ind]-np.mean(SOS[ind]))
    years_phen_ok = years_phen[ind]
    
    if(len(phen_QC)>6):

        ax1.plot(years_phen_ok,SOS_ok,'-',linewidth=1)

x_ticks = range(1990,2015,4)
ax1.set_xlim([1990,2015])
ax1.set_ylim([0,250])
ax1.set_yticks([0,50,100,150,200,250])
ax1.set_yticklabels([0,50,100,150,200,250],fontproperties = font_tick)
ax1.set_xticks(x_ticks)
ax1.set_xticklabels([])  
ax1.grid(color = 'lightgray',linestyle = '--')
ax1.set_ylabel('SOS (DOY)',fontproperties = font_label)
ax1.fill_between([1998,2012],[0,0],[365,365],color = 'lightgrey',alpha = 0.5)
ax1.text(1992,230,"a",fontproperties = font_sub_title)

        
### plot statistic of SOS trend as bar ####        
ax2 = plt.subplot(gs[1])
width=0.4
x = np.asarray([1,2,3])

y_advance_SOS = np.asarray(SOS_data_MK_trend["SOS advance"])
y_delay_SOS = np.asarray(SOS_data_MK_trend["SOS delay"])
rect1 = ax2.bar(x-width/2,y_advance_SOS,width,color='green',label='SOS advance')
rect2 = ax2.bar(x+width/2,y_delay_SOS,width,color='brown',label='SOS delay')
ax2.yaxis.tick_right()
ax2.yaxis.set_label_position("right")
#ax2.plot([0,4],[0,0],color='k')
ax2.set_xlim([0.5,3.5])
ax2.set_xticks([1,2,3])
ax2.set_ylim([0,39])
ax2.set_yticks(range(0,36,5))
ax2.set_yticklabels(range(0,36,5),fontproperties = font_tick)
ax2.set_ylabel('SOS Site number',fontproperties = font_label)
ax2.text(0.7,35,"b",fontproperties = font_sub_title)
plt.legend(frameon=False,prop = font_tick)

autolabel(ax2,rect1)
autolabel(ax2,rect2)

################## plot EOS spaghetti ##################################################
EOS_data = np.asarray(EOS_data)
ax3 = plt.subplot(gs[2])
for i in range(56):
    ### read data
    EOS_ind = i*2+1
    EOS_flag_ind = i*2+2
    
    EOS = np.asarray(EOS_data[:,EOS_ind])
    phen_QC = np.asarray(EOS_data[:,EOS_flag_ind])
    years_phen = np.asarray(EOS_data[:,0])
    
    ### plot EOS ########

    ind = (phen_QC  > 0 ) & (EOS > 0)
    EOS_ok = EOS[ind]
    EOS_ok_anomalies = (EOS[ind]-np.mean(EOS[ind]))
    years_phen_ok = years_phen[ind]
    
    if(len(phen_QC)>6):

        ax3.plot(years_phen_ok,EOS_ok,'-',linewidth=1)
        

#plt.plot(range(1990,2016),out_temp,'g-',lw=3) 
#plt.xticks(range(1990,2015),rotation=45)    
#plt.grid()
#plt.show()

x_ticks = range(1990,2015,4)
ax3.set_xlim([1990,2015])
ax3.set_ylim([100,360])
ax3.set_yticks([100,150,200,250,300,340])
ax3.set_yticklabels([100,150,200,250,300,340],fontproperties = font_tick)
ax3.set_xticks(x_ticks)
ax3.set_xticklabels(x_ticks,fontproperties = font_tick)  
ax3.grid(color = 'lightgray',linestyle = '--')
ax3.set_ylabel('EOS (DOY)',fontproperties = font_label)
ax3.fill_between([1998,2012],[0,0],[365,365],color = 'lightgrey',alpha = 0.5)
ax3.text(1992,340,"c",fontproperties = font_sub_title)
ax3.set_xlabel('Year',fontproperties = font_label)
        
        
### plot statistic of EOS trend as bar ####        
ax4 = plt.subplot(gs[3])

width=0.4

x = np.asarray([1,2,3])

y_advance_EOS = np.asarray(EOS_data_MK_trend["EOS advance"])
y_delay_EOS = np.asarray(EOS_data_MK_trend["EOS delay"])
rect3 = ax4.bar(x-width/2,y_advance_EOS,width,color='brown',label='EOS advance')
rect4 = ax4.bar(x+width/2,y_delay_EOS,width,color='green',label='EOS delay')   
ax4.yaxis.tick_right()
ax4.yaxis.set_label_position("right")
#ax4.plot([0,4],[0,0],color='k')  
ax4.set_xlim([0.5,3.5])
ax4.set_xticks([1,2,3])
ax4.set_xticklabels(['All','p<0.1','p<0.05'],fontproperties = font_tick)
ax4.set_ylim([0,39])
ax4.set_yticks(range(0,36,5))
ax4.set_yticklabels(range(0,36,5),fontproperties = font_tick)
ax4.set_ylabel('EOS Site number',fontproperties = font_label)
ax4.set_xlabel('Different confidence',fontproperties = font_label)
ax4.text(0.7,35,"d",fontproperties = font_sub_title)

plt.legend(frameon=False,prop = font_tick)
autolabel(ax4,rect3)
autolabel(ax4,rect4)
        
fig.tight_layout()
plt.subplots_adjust(left=0.05, bottom=0.05, top=0.95, right=0.95, wspace=0, hspace=0) 
plt.savefig('output_figures/Fig2_FLX_phen_trend.png',format='png',dpi=300,bbox_inches='tight')
plt.show()
