# -*- coding: utf-8 -*-
"""
Created on Tue May 23 08:59:46 2017

@author: wxf
"""

import matplotlib.pyplot as plt
import os
import numpy as np
#import string
#import scipy.stats as stats
import pandas as pd
from MK_trend import *
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

def get_site_value(phen_sites,R2_sites,R2_all):
    R2_sites_list = []
    R2_out = []
    R2_sites = np.asarray(R2_sites)
    R2_all = np.asarray(R2_all)
    for st in R2_sites:
        if(st[0:2] == 'MF'):
            R2_sites_list.append(st[7:13])
        else:
            R2_sites_list.append(st[8:14])
    for st in phen_sites:
        ind = R2_sites_list.index(st)
        R2_out.append(R2_all[ind]) 
        
    R2_out = np.asarray(R2_out)
    return R2_out
    
    
############# start main program here #################################
SOS_R2_infile = '../NCOMMS-19-00016-T-SourceDataFile/Supplementary_Figure_5_SOS_vs_env_R2_P_latitude_sorted.xlsx'
EOS_R2_infile = '../NCOMMS-19-00016-T-SourceDataFile/Supplementary_Figure_6_EOS_vs_env_R2_P_latitude_sorted.xlsx'

SOS_R2 = pd.read_excel(SOS_R2_infile,'FigureS5')
EOS_R2 = pd.read_excel(EOS_R2_infile,'FigureS6')

site_names = SOS_R2['sitename']


xENF=16
xDBF=29
xMF = 34
xOSH = 36
xWSA = 37
xGRA = 46
xWET = 48
xCRO = 56


xgrid_value = [xENF,xDBF,xMF,xOSH,xWSA, xGRA, xWET]
xgrid_value2 = [1,xENF,xDBF,xMF,xOSH,xWSA, xGRA, xWET]
types = ['ENF','DBF','MF','OSH','WSA','GRA','WET','CRO']


#################### plot SOS R2 ###########################
flds = ['SOS_Ta_spr','SOS_Ta_wit', \
        'SOS_SW_IN_spr', 'SOS_SW_IN_wit', \
       'SOS_P_spr', 'SOS_P_wit',\
       'SOS_VPD_spr', 'SOS_VPD_wit',\
       'SOS_TS_MDS_1_spr', 'SOS_TS_MDS_1_wit',\
       'SOS_SWC_MDS_1_spr', 'SOS_SWC_MDS_1_wit']

xlabels = ['Spring Tair','Winter Tair', 'Spring SR', 'Winter SR',\
           'Spring Prec','Winter Prec', 'Spring VPD','Winter VPD', 'Spring TS','Winter TS',\
           'Spring SWC','Winter SWC']

R2_sites = SOS_R2['site']
SOS_MK_slp = SOS_R2['SOS_NT_MK_slp']
SOS_MK_P = SOS_R2['SOS_NT_MK_P']

EOS_MK_slp = EOS_R2['EOS_NT_MK_slp']
EOS_MK_P = EOS_R2['EOS_NT_MK_P']


fig=plt.figure(figsize=cm2inch(21, 26))

count = 1
x=np.arange(1,57)
p05 = np.zeros(56)
p10 = np.zeros(56)

wid = 0.4
clrs = []
for i in range(len(flds)):
    fld = flds[i]
    ax_SOS = plt.subplot(1, 12, count)  
    
    R2_all = SOS_R2["%s_R" %(fld)]
    P_all = SOS_R2["%s_P" %(fld)]
    cor_s = get_site_value(site_names,R2_sites,R2_all)
    P_vals = get_site_value(site_names,R2_sites,P_all)

    for j in range(len(cor_s)):
        if cor_s[j] <0:
            clrs.append('r')
        else:
            clrs.append('g')
            
        if( SOS_MK_P[j]< 0.1):
            if(SOS_MK_slp[j]<0):                
                ax_SOS.axhspan(j+0.5, j+1.5, alpha=0.5, color='lightgreen')
            else:
                ax_SOS.axhspan(j+0.5, j+1.5, alpha=0.5, color='lightsalmon')
                
                
    R2s = cor_s*cor_s
    ydata = R2s
    ind = ydata == 99980001
    ydata[ind]=np.nan
    
    ind = cor_s<0
    ydata_negetive = ydata.copy()
    ydata_negetive[~ind] = np.nan
    ydata_positive =  ydata.copy()
    ydata_positive[ind] = np.nan
    
    p05 = ydata + 0.1
    p10 = ydata + 0.07
    ind = (P_vals <=0.05) & (P_vals > 0)
    #p05[ind] = 0.5
    p05[~ind] = np.nan

    ind1 = (P_vals <=0.1) & (P_vals >0.05)
    #p10[ind1] = 0.5
    p10[~ind1] = np.nan
    
    ind = P_vals > 0.1
    ydata_negetive[ind] = np.nan
    ydata_positive[ind] = np.nan
    
    ax_SOS.barh(x,ydata_negetive,height=wid,edgecolor='k',fill=False, hatch='////',label = 'Negative correlation')
    ax_SOS.barh(x,ydata_positive,height=wid,color='k',label = 'Positive correlation')
    
    ax_SOS.plot(p05,x,'k',marker=r'$* *$',linewidth = 0,MarkerSize=7,label = 'P < 0.05')
    ax_SOS.plot(p10,x,'k',marker=r'$*$',linewidth = 0, MarkerSize=4, label = 'P < 0.1')
    
    ax_SOS.set_xlim([0,1.15])
    ax_SOS.set_ylim([0,57])
    
    
    ax_SOS.set_yticks(x)
    ax_SOS.set_xticks([0.2,0.5,0.8])
    ax_SOS.set_xticklabels([0.2,0.5,0.8],rotation = 90,fontproperties = font_tick)
    ax_SOS.set_xlabel(xlabels[i],x=0.2,rotation = 30, fontproperties = font_label)
    if count ==1:
        ax_SOS.set_yticklabels(site_names,fontproperties = font_tick)
        ax_SOS.set_ylabel('Site ID',fontproperties = font_label)
    else:
        ax_SOS.set_yticklabels('')
        
    ax_SOS.grid(color='lightgray',linestyle='dashed')
    ax_SOS.set_axisbelow(True)
    
    for a in xgrid_value:
        ax_SOS.plot([0,1.2],[a+0.5,a+0.5],linestyle = '-',color = 'k',lw=1)

    
    count = count+1

i=0
for a in xgrid_value:
    ax_SOS.text(0.5,a-0.5,types[i],fontproperties = font_tick)
    i=i+1
ax_SOS.text(0.5,56,types[i],fontproperties = font_tick)

fig.tight_layout()
plt.subplots_adjust(left=0.05, bottom=0.05, top=0.95, right=0.95, wspace=0, hspace=0)  
plt.legend(bbox_to_anchor=(0.12, 1.04),frameon=False,prop = font_tick,handlelength=2,ncol=4)
 
out_fig_SOS='output_figures/FigS5_SOS_R2_season20190302_lat_sorted_disp_sig.png'  
plt.savefig(out_fig_SOS,format='png',dpi=300,bbox_inches='tight')
plt.show()

###############################################################################
#################### plot EOS R2 ##############################################
flds = ['EOS_Ta_smr','EOS_Ta_aut', \
        'EOS_SW_IN_smr', 'EOS_SW_IN_aut', \
       'EOS_P_smr', 'EOS_P_aut',\
       'EOS_VPD_smr', 'EOS_VPD_aut',\
       'EOS_TS_MDS_1_smr', 'EOS_TS_MDS_1_aut',\
       'EOS_SWC_MDS_1_smr', 'EOS_SWC_MDS_1_aut']

xlabels = ['Summer Tair','Autumn Tair', 'Summer SR', 'Autumn SR',\
           'Summer Prec','Autumn Prec', 'Summer VPD','Autumn VPD',\
           'Summer TS','Autumn TS','Summer SWC','Autumn SWC_smr']

R2_sites = EOS_R2['site']


fig=plt.figure(figsize=cm2inch(21, 26))

count = 1
x=np.arange(1,57)
p05 = np.zeros(56)
p10 = np.zeros(56)

wid = 0.4
clrs = []
for i in range(len(flds)):
    fld = flds[i]
    ax_EOS = plt.subplot(1, 12, count)  
    
    R2_all = EOS_R2["%s_R" %(fld)]
    P_all = EOS_R2["%s_P" %(fld)]
    cor_s = get_site_value(site_names,R2_sites,R2_all)
    P_vals = get_site_value(site_names,R2_sites,P_all)
    
    for j in range(len(cor_s)):
        if cor_s[j] <0:
            clrs.append('r')
        else:
            clrs.append('g')
        if( EOS_MK_P[j]< 0.1):
            if(EOS_MK_slp[j]<0):                
                ax_EOS.axhspan(j+0.5, j+1.5, alpha=0.5, color='lightsalmon')
            else:
                ax_EOS.axhspan(j+0.5, j+1.5, alpha=0.5, color='lightgreen')
                
    R2s = cor_s*cor_s
    ydata = R2s
    ind = ydata == 99980001 #(-9999*-9999)
    ydata[ind]=np.nan
    
    ind = cor_s<0
    ydata_negetive = ydata.copy()
    ydata_negetive[~ind] = np.nan
    ydata_positive =  ydata.copy()
    ydata_positive[ind] = np.nan
    
    p05 = ydata + 0.1
    ind = (P_vals <=0.05) & (P_vals > 0)    
    p05[~ind] = np.nan
    
    p10 = ydata + 0.07
    ind1 = (P_vals <=0.1) & (P_vals >0.05)    
    p10[~ind1] = np.nan
    
    ind = P_vals > 0.1
    ydata_negetive[ind] = np.nan
    ydata_positive[ind] = np.nan
    
    ax_EOS.barh(x, ydata_negetive,height=wid,edgecolor='k',fill=False, hatch='////',label = 'Negative correlation')
    ax_EOS.barh(x, ydata_positive,height=wid,color='k',label = 'Positive correlation')
    
    ax_EOS.plot(p05,x,'k',marker=r'$* *$',linewidth = 0,MarkerSize=7,label = 'P < 0.05')
    ax_EOS.plot(p10,x,'k',marker=r'$*$',linewidth = 0,MarkerSize=4,label = 'P < 0.1')
    
    ax_EOS.set_xlim([0,1.15])
    ax_EOS.set_ylim([0,57])
    
    
    ax_EOS.set_yticks(x)
    ax_EOS.set_xticks([0.2,0.5,0.8])
    ax_EOS.set_xticklabels([0.2,0.5,0.8],rotation = 90,fontproperties = font_tick)
    ax_EOS.set_xlabel(xlabels[i],x=0.2, rotation = 30,fontproperties = font_label)
    if count ==1:
        ax_EOS.set_yticklabels(site_names,fontproperties = font_tick)
        ax_EOS.set_ylabel('Site ID',fontproperties = font_label)
    else:
        ax_EOS.set_yticklabels('')
        
    ax_EOS.grid(color='lightgray', linestyle='dashed')
    ax_EOS.set_axisbelow(True)
    
    for a in xgrid_value:
        ax_EOS.plot([0,1.2],[a+0.5,a+0.5], linestyle = '-',color = 'gray',lw=1)

    count = count+1


i=0
for a in xgrid_value:
    ax_EOS.text(0.5,a-0.5,types[i],fontproperties = font_tick)
    i=i+1
ax_EOS.text(0.5,56,types[i],fontproperties = font_tick)

fig.tight_layout()
plt.subplots_adjust(left=0.05, bottom=0.05, top=0.95, right=0.95, wspace=0, hspace=0)  
plt.legend(bbox_to_anchor=(0.12, 1.04),frameon=False,prop = font_tick,handlelength=2,ncol=4)
 
out_fig_EOS='output_figures/FigS6_EOS_R2_season20190302_lat_sorted_disp_sig.png'  
plt.savefig(out_fig_EOS,format='png',dpi=300,bbox_inches='tight')
plt.show()


