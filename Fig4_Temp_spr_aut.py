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


in_path = '../NCOMMS-19-00016-T-SourceDataFile/Figure4.data.xlsx'
data_spr = pd.read_excel(in_path,"Figure4a")
data_spr_MK_trend = pd.read_excel(in_path,"Figure4b")
data_aut = pd.read_excel(in_path,"Figure4c")
data_aut_MK_trend = pd.read_excel(in_path,"Figure4d")
    

################## plot SOS spaghetti ##################################################

fig=plt.figure(figsize=cm2inch(19, 15))
gs = gridspec.GridSpec(2, 2, width_ratios=[2, 1]) 
ax1 = plt.subplot(gs[0])

data_spr = np.asarray(data_spr)
for i in range(56):
    ### read data
    years = np.asarray(data_spr[:,0])
    TA_spr = np.asarray(data_spr[:,i+1])
    TA_spr_QC = np.asarray(data_spr[:,i+57])
    
    ### plot spring temperature ########
    TA_spr_QC = np.asarray(TA_spr_QC)
    TA_spr = np.asarray(TA_spr)
    years = np.asarray(years)
    ind = (TA_spr_QC  > 0.75) & (TA_spr > -9999)
    TA_spr_ok = TA_spr[ind]
    TA_spr_ok_anomalies = (TA_spr[ind]-np.mean(TA_spr[ind]))
    years_ok = years[ind]
    
    if(len(TA_spr_ok)>6):

        ax1.plot(years_ok,TA_spr_ok,'-')
    


x_ticks = range(1990,2015,4)
ax1.set_xlim([1990,2015])
ax1.set_ylim([-19,24])
ax1.set_yticks([-15,-10,-5,0,5,10,15,20])
ax1.set_yticklabels([-15,-10,-5,0,5,10,15,20],fontproperties = font_tick)
ax1.set_xticks(x_ticks)
ax1.set_xticklabels([])  
ax1.grid(color = 'lightgray',linestyle = '--')
ax1.set_ylabel('Spring Tair ($^\circ$C)',fontproperties = font_label)
ax1.fill_between([1998,2012],[-50,-50],[50,50],color = 'lightgrey',alpha = 0.5)
ax1.text(1992,22,'a',fontproperties = font_sub_title) #,fontweight='bold'
        
### plot statistic of SOS trend as bar ####        
ax2 = plt.subplot(gs[1])
width=0.4

x = np.asarray([1,2,3])

y_decr_TA_spr = np.asarray(data_spr_MK_trend["Decrease"])
y_incr_TA_spr = np.asarray(data_spr_MK_trend["Increase"])
rect1 = ax2.bar(x-width/2,y_decr_TA_spr,width,color='c',label='Decrease')
rect2 = ax2.bar(x+width/2,y_incr_TA_spr,width,color='red',label='Increase')
ax2.yaxis.tick_right()
ax2.yaxis.set_label_position("right")
#ax2.plot([0,4],[0,0],color='k')
ax2.set_xlim([0.5,3.5])
ax2.set_xticks([1,2,3])
ax2.set_ylim([0,39])
ax2.set_yticks(range(0,36,5))
ax2.set_yticklabels(range(0,36,5),fontproperties = font_tick)
ax2.set_ylabel('Spring Tair site number',fontproperties = font_label)
plt.legend(frameon=False,prop = font_tick)
ax2.text(0.7,36,'b',fontproperties = font_sub_title)

autolabel(ax2,rect1)
autolabel(ax2,rect2)

out_fld_TA_aut = []
out_fld_TA_aut_QC = []

################## plot EOS spaghetti ##################################################
data_aut = np.asarray(data_aut)
ax3 = plt.subplot(gs[2])
for i in range(56):
    ### read data
    years = np.asarray(data_aut[:,0])
    TA_aut = np.asarray(data_aut[:,i+1])
    TA_aut_QC = np.asarray(data_aut[:,i+57])
        
    
    TA_aut_QC = np.asarray(TA_aut_QC)
    TA_aut = np.asarray(TA_aut)
    years = np.asarray(years)
    ind = (TA_aut_QC  > 0.75) & (TA_aut > -9999)
    TA_aut_ok = TA_aut[ind]
    
    years_ok = years[ind]
    if(len(TA_aut_ok)>6):        
        ax3.plot(years_ok,TA_aut_ok,'-')        
    

x_ticks = range(1990,2015,4)
ax3.set_xlim([1990,2015])
ax3.set_ylim([-19,24])
ax3.set_yticks([-15,-10,-5,0,5,10,15,20])
ax3.set_yticklabels([-15,-10,-5,0,5,10,15,20],fontproperties = font_tick)
ax3.set_xticks(x_ticks)
ax3.set_xticklabels(x_ticks,fontproperties = font_tick)  
ax3.grid(color = 'lightgray',linestyle = '--')
ax3.set_ylabel('Autumn Tair ($^\circ$C)',fontproperties = font_label)
ax3.fill_between([1998,2012],[-50,-50],[50,50],color = 'lightgrey',alpha = 0.5)

ax3.set_xlabel('Year',fontproperties = font_label)
ax3.text(1992,22,'c',fontproperties = font_sub_title)

### plot statistic of EOS trend as bar ####        
ax4 = plt.subplot(gs[3])

width=0.4

x = np.asarray([1,2,3])

y_decr_TA_aut = np.asarray(data_aut_MK_trend["Decrease"])
y_incr_TA_aut = np.asarray(data_aut_MK_trend["Increase"])
rect3 = ax4.bar(x-width/2, y_decr_TA_aut, width,color='c', label='Decrease')
rect4 = ax4.bar(x+width/2, y_incr_TA_aut, width, color='red', label='Increase')   
ax4.yaxis.tick_right()
ax4.yaxis.set_label_position("right")
#ax4.plot([0,4],[0,0],color='k')  
ax4.set_xlim([0.5,3.5])
ax4.set_xticks([1,2,3])
ax4.set_xticklabels(['All','p<0.1','p<0.05'],fontproperties = font_tick)
ax4.set_ylim([0,39])
ax4.set_yticks(range(0,36,5))
ax4.set_ylabel('Autumn Tair site number',fontproperties = font_label)
ax4.set_xlabel('Different confidence',fontproperties = font_label)
ax4.text(0.7,36,'d',fontproperties = font_sub_title)

plt.legend(frameon=False,prop = font_tick)
autolabel(ax4,rect3)
autolabel(ax4,rect4)
        
fig.tight_layout()
plt.subplots_adjust(left=0.05, bottom=0.05, top=0.95, right=0.95, wspace=0, hspace=0) 
plt.savefig('output_figures/Fig4_TA_trend.png',format='png',dpi=300,bbox_inches='tight')
plt.show()

