# -*- coding: utf-8 -*-
"""
Created on Mon Aug 06 15:29:15 2018

@author: wxf
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import MK_trend as MK
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

infile = '../NCOMMS-19-00016-T-SourceDataFile/FigureS10.data.xlsx'        

data_SOS = pd.read_excel(infile,'FigureS10a')
data_EOS = pd.read_excel(infile,'FigureS10b')

### read SOS and get trend ###############
#GIMMS version1
SOS_avg_v1 = np.asarray(data_SOS['SOS_avg'])
SOS_Years_v1 = np.asarray(data_SOS['Year'])

SOS_bf98_v1 = SOS_avg_v1[0:17]
years_bf98_SOS_v1 = SOS_Years_v1[0:17]
SOS_af98_v1 = SOS_avg_v1[16:33]
years_af98_SOS_v1 = SOS_Years_v1[16:33]

h_bf98_SOS_v1, trend_bf98_SOS_v1, intp_bf98_SOS_v1, p_value_bf98_SOS_v1, z_bf98_SOS_v1 = MK.mk_trend(SOS_bf98_v1,years_bf98_SOS_v1,0.05)
h_af98_SOS_v1, trend_af98_SOS_v1, intp_af98_SOS_v1, p_value_af98_SOS_v1, z_af98_SOS_v1 = MK.mk_trend(SOS_af98_v1,years_af98_SOS_v1,0.05)

x_bf98_SOS_v1 = np.asarray([1982,1998])
x_af98_SOS_v1 = np.asarray([1998,2014])
y_bf98_SOS_v1 = trend_bf98_SOS_v1*x_bf98_SOS_v1 + intp_bf98_SOS_v1
y_af98_SOS_v1 = trend_af98_SOS_v1*x_af98_SOS_v1 + intp_af98_SOS_v1


### read EOS and get trend ###############
## GIMMS version 1

EOS_avg_v1 = np.asarray(data_EOS['EOS_avg'])
EOS_Years_v1 = np.asarray(data_EOS['Year'])

EOS_bf98_v1 = EOS_avg_v1[0:17]
years_bf98_EOS_v1 = EOS_Years_v1[0:17]
EOS_af98_v1 = EOS_avg_v1[16:33]
years_af98_EOS_v1 = EOS_Years_v1[16:33]

h_bf98_EOS_v1, trend_bf98_EOS_v1, intp_bf98_EOS_v1, p_value_bf98_EOS_v1, z_bf98_EOS_v1 = MK.mk_trend(EOS_bf98_v1,years_bf98_EOS_v1,0.05)
h_af98_EOS_v1, trend_af98_EOS_v1, intp_af98_EOS_v1, p_value_af98_EOS_v1, z_af98_EOS_v1 = MK.mk_trend(EOS_af98_v1,years_af98_EOS_v1,0.05)

x_bf98_EOS_v1 = np.asarray([1982,1998])
x_af98_EOS_v1 = np.asarray([1998,2014])
y_bf98_EOS_v1 = trend_bf98_EOS_v1*x_bf98_EOS_v1+intp_bf98_EOS_v1
y_af98_EOS_v1 = trend_af98_EOS_v1*x_af98_EOS_v1+intp_af98_EOS_v1


### plot figures ######
fig=plt.figure(figsize=cm2inch(21, 6))
############### plot SOS ###############
ax1 = plt.subplot(1,2,1)
ax1.plot(SOS_Years_v1,SOS_avg_v1,'b-o',Markersize=4,linewidth = 1,label='GIMMS3g')
ax1.plot(x_bf98_SOS_v1,y_bf98_SOS_v1,color='b',linestyle='--')
ax1.plot(x_af98_SOS_v1,y_af98_SOS_v1,color='b',linestyle='--')

ax1.set_xlim([1981,2015])
ax1.set_ylim([80,120])
ax1.set_yticks([80,90,100,110])
ax1.set_yticklabels([80,90,100,110],fontproperties = font_tick)
ax1.set_ylabel('SOS (DOY)',fontproperties = font_label)
ax1.set_xlabel('Year',fontproperties = font_label)
ax1.fill_between([1998,2012],[130,130],[80,80],color = 'lightgrey',alpha = 0.5)
ax1.grid(color = 'lightgrey',linestyle = '--')
#ax1.set_xticklabels([])
ax1.text(1982,116,'a: SOS',fontproperties = font_sub_title)
plt.legend(frameon=False)

############### plot EOS ###############
ax2 = plt.subplot(1,2,2)
ax2.plot(EOS_Years_v1,EOS_avg_v1,'b-o',Markersize=4,linewidth = 1,label='GIMMS3g')
ax2.plot(x_bf98_EOS_v1,y_bf98_EOS_v1,color='b',linestyle='--')
ax2.plot(x_af98_EOS_v1,y_af98_EOS_v1,color='b',linestyle='--')


ax2.set_xlim([1981,2015])
ax2.set_ylim([285,325])
ax2.set_yticks([285,295,305,315])
ax2.set_yticklabels([285,295,305,315],fontproperties = font_tick)
ax2.set_ylabel('EOS (DOY)',fontproperties = font_label)
ax2.fill_between([1998,2012],[325,325],[280,280],color = 'lightgrey',alpha = 0.5)
ax2.grid(color = 'lightgrey',linestyle = '--')
ax2.yaxis.tick_right()
ax2.yaxis.set_label_position("right")
#ax2.set_xticklabels([])
ax2.text(1982,321,'b: EOS',fontproperties = font_sub_title)
ax2.set_xlabel('Year',fontproperties = font_label)
plt.legend(frameon=False,prop=font_tick)

if(intp_bf98_SOS_v1>0):
    txt_SOS_v1_bf98 = "bf98: y=%3.2f*x + %4.1f P=%4.3f" %(trend_bf98_SOS_v1, intp_bf98_SOS_v1, p_value_bf98_SOS_v1)
else:
    txt_SOS_v1_bf98 = "bf98: y=%3.2f*x - %4.1f P=%4.3f" %(trend_bf98_SOS_v1, np.abs(intp_bf98_SOS_v1), p_value_bf98_SOS_v1)

if(intp_af98_SOS_v1>0):
    txt_SOS_v1_af98 = "af98: y=%3.2f*x + %4.1f P=%4.3f" %(trend_af98_SOS_v1, intp_af98_SOS_v1, p_value_af98_SOS_v1)
else:
    txt_SOS_v1_af98 = "af98: y=%3.2f*x - %4.1f P=%4.3f" %(trend_af98_SOS_v1, np.abs(intp_af98_SOS_v1), p_value_af98_SOS_v1)

if(intp_bf98_EOS_v1>0):
    txt_EOS_v1_bf98 = "bf98: y=%3.2f*x + %4.1f P=%4.3f" %(trend_bf98_EOS_v1, intp_bf98_EOS_v1, p_value_bf98_EOS_v1)
else:
    txt_EOS_v1_bf98 = "bf98: y=%3.2f*x - %4.1f P=%4.3f" %(trend_bf98_EOS_v1, np.abs(intp_bf98_EOS_v1), p_value_bf98_EOS_v1)
    
if(intp_af98_EOS_v1>0):
    txt_EOS_v1_af98 = "af98: y=%3.2f*x + %4.1f P=%4.3f" %(trend_af98_EOS_v1, intp_af98_EOS_v1, p_value_af98_EOS_v1)
else:
    txt_EOS_v1_af98 = "af98: y=%3.2f*x - %4.1f P=%4.3f" %(trend_af98_EOS_v1, np.abs(intp_af98_EOS_v1), p_value_af98_EOS_v1)

ax1.text(1982,83,txt_SOS_v1_bf98,fontproperties = font_tick,color='k')
ax1.text(1982,81,txt_SOS_v1_af98,fontproperties = font_tick,color='k')

ax2.text(1982,288,txt_EOS_v1_bf98,fontproperties = font_tick,color='k')
ax2.text(1982,286,txt_EOS_v1_af98,fontproperties = font_tick,color='k')
#y_loc= y_loc - 0.15
#ax5.text(2016,y_loc,txt_EOS_v0,fontsize = 9,color='r')


fig.tight_layout()
plt.subplots_adjust(left=0.05, bottom=0.05, top=0.95, right=0.95, wspace=0, hspace=0)  
plt.savefig('output_figures/FigS10_flxsites_gimms_phen_trend.png',format='png',dpi=300,bbox_inches='tight')
plt.show()


