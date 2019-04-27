# -*- coding: utf-8 -*-
"""
Created on Mon May 29 19:58:31 2017

@author: wxf
"""
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
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
        
infile = '../NCOMMS-19-00016-T-SourceDataFile/Supplementary_Figure_2_flux_SOS_EOS_avg_std.data.xlsx'

data = pd.read_excel(infile,'FigureS2')
sites = np.asarray(data['sitename'])
SOS_avg = np.asarray(data['SOS_avg'])
SOS_std = np.asarray(data['SOS_std'])
EOS_avg = np.asarray(data['EOS_avg'])
EOS_std = np.asarray(data['EOS_std'])
year_QC = np.asarray(data['Years_QC_control'])

xENF=16
xDBF=29
xMF = 34
xOSH = 36
xWSA = 37
xGRA = 46
xWET = 48
xCRO = 56

yticks = []
for i in range(len(sites)):
    yticks.append("%s: %2d" %(sites[i],year_QC[i]))


xgrid_value = [xENF,xDBF,xMF,xOSH,xWSA, xGRA, xWET]
xgrid_value2 = [1,xENF,xDBF,xMF,xOSH,xWSA, xGRA, xWET]
types = ['ENF','DBF','MF','OSH','WSA','GRA','WET','CRO']

y = np.arange(1,len(sites)+1)
wid = 0.5

fig=plt.figure(figsize=cm2inch(17, 28))
ax_SOS = plt.subplot(1, 1,1) 
############# plot SOS ########################################

ax_SOS.errorbar(SOS_avg,y,xerr=SOS_std,fmt='o',markersize=4,color='g',ecolor='g',capsize=3,elinewidth=1,capthick=0.5,mfc='white',label='SOS')

ax_SOS.errorbar(EOS_avg,y,xerr=EOS_std,fmt='d',markersize=4,color='y',ecolor='y',capsize=3,elinewidth=1,capthick=0.5,mfc='white',label='EOS')

#ax_SOS.errorbar(GSL_avg,y, xerr=GSL_std, fmt='s',markersize=4,color='k',ecolor='k',capsize=3,elinewidth=1,capthick=0.5,mfc='white')

for i in range(len(xgrid_value)):
    a = xgrid_value[i]+0.25
    ax_SOS.plot([0,366],[a,a],'k-',lw=1)
    ax_SOS.text(345,a-1,types[i],fontproperties = font_tick)
ax_SOS.text(345,56,'CRO',fontproperties = font_tick) 

ax_SOS.set_yticks(range(1,len(sites)+1))
ax_SOS.set_yticklabels(yticks,rotation=0,fontproperties = font_tick)
ax_SOS.set_xlabel("Phenology date (Doy)",fontproperties = font_label)
ax_SOS.set_ylabel("Site name",fontproperties = font_label)
ax_SOS.plot([0,0],[0,57],'k-')


ax_SOS.set_ylim([0,57])
ax_SOS.set_xlim([0,366])
plt.grid(linestyle='dashed')
ax_SOS.set_axisbelow(True)
#outfig_file = 'D:/UNH_visiting/Phenology_from_fluxnet/Figures_in_Paper/Fig3_SOS_MKtrend.png'
#plt.savefig(outfig_file,format='png',dpi=300,bbox_inches='tight')
#plt.show()


fig.tight_layout()
plt.subplots_adjust(left=0.05, bottom=0.05, top=0.95, right=0.95, wspace=0, hspace=0) 
plt.legend(bbox_to_anchor=(0.05, 0.05),frameon=False,fontsize=9,handlelength=0.6,prop = font_tick)
outfig_file = 'output_figures/FigS2_SOS_EOS_result20171023_latitude_sort.png'
plt.savefig(outfig_file,format='png',dpi=300,bbox_inches='tight')
plt.show()



