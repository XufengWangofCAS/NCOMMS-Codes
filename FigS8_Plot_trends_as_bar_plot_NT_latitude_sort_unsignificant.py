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

method = 'NT' #'NT' for daytime  'DT' for nighttime    
infile = '../NCOMMS-19-00016-T-SourceDataFile/FigureS8.data.xlsx'

data = pd.read_excel(infile,'FigureS8')
sites = np.asarray(data['sitename'])
SOS_slp = np.asarray(data['SOS_%s_MK_slp' %(method)])
SOS_P = np.asarray(data['SOS_%s_MK_P' %(method)])
EOS_slp = np.asarray(data['EOS_%s_MK_slp' %(method)])
EOS_P = np.asarray(data['EOS_%s_MK_P' %(method)])
year_QC = np.asarray(data['Years_QC_control'])

SOS_slp[SOS_slp==-9999] = 0
SOS_P[SOS_P==-9999] = 1
EOS_slp[EOS_slp==-9999] = 0
EOS_P[EOS_P==-9999] = 1

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



x=np.arange(1,len(sites)+1)
wid = 0.5

fig=plt.figure(figsize=cm2inch(18, 28))
ax_SOS = plt.subplot(1, 2,1) 
############# plot SOS ########################################

 
ydata = np.asarray(SOS_slp.copy())
ind_y = SOS_P > 0.1
ydata[ind_y] = np.nan
ind_p = ydata < 0
ind_n = ydata > 0
ydata_posi = ydata.copy()
ydata_neg = ydata.copy()
ydata_posi[ind_p] = np.nan
ydata_neg[ind_n] = np.nan

ax_SOS.barh(x,ydata_posi,color = 'brown', height =wid)
ax_SOS.barh(x,np.abs(ydata_neg),color = 'g',height =wid)

ax_SOS.set_yticks(range(1,len(sites)+1))
ax_SOS.set_yticklabels(yticks,rotation=0,fontproperties = font_tick)
ax_SOS.set_xlabel("SOS" ,fontproperties = font_label)
ax_SOS.set_ylabel("Site ID",fontproperties = font_label)
ax_SOS.plot([0,0],[0,57],'k-')

for i in range(len(xgrid_value)):
    a = xgrid_value[i]+0.5
    ax_SOS.plot([0,8],[a,a],'k-',lw=1)

#    ax_SOS.text(4,a-1,types[i], fontsize = 10)
#ax_SOS.text(4,56,'CRO', fontsize = 10)        

y_p05 = np.abs(ydata.copy()) + 0.5
ind = SOS_P > 0.05
y_p05[ind] = np.nan

y_p1 = np.abs(ydata.copy()) + 0.5
ind = SOS_P > 0.1
y_p1[ind] = np.nan
ind = SOS_P <= 0.05
y_p1[ind] = np.nan

ax_SOS.plot(y_p05,x,'k',marker=u'$* *$',linewidth = 0,MarkerSize=10,label = 'P < 0.05')
ax_SOS.plot(y_p1,x,'k',marker=u'$*$',linewidth = 0, MarkerSize=7, label = 'P < 0.1')
ax_SOS.set_ylim([0,57])
ax_SOS.set_xlim([0,8])
ax_SOS.set_xticks([0,1,3,5,7])
ax_SOS.set_xticklabels([0,1,3,5,7],fontproperties = font_tick)
plt.grid(linestyle='dashed')
ax_SOS.set_axisbelow(True)


############# plot EOS ########################################
ax_EOS = plt.subplot(1, 2,2)  
ydata = np.asarray(EOS_slp.copy())
ind_y = EOS_P > 0.1
ydata[ind_y] = np.nan
ind_p = ydata < 0
ind_n = ydata > 0
ydata_posi = ydata.copy()
ydata_neg = ydata.copy()
ydata_posi[ind_p] = np.nan
ydata_neg[ind_n] = np.nan

ax_EOS.barh(x,ydata_posi,color = 'g', height =wid, label = 'SOS advance/EOS delay')
ax_EOS.barh(x,np.abs(ydata_neg),color = 'brown',height =wid, label = 'SOS delay/EOS advance/GSL shorten')

ax_EOS.set_yticks(range(1,len(sites)+1))
ax_EOS.set_yticklabels(sites,rotation=0,fontproperties = font_tick)
ax_EOS.set_xlabel("EOS", fontproperties = font_label)
ax_EOS.text(-2,-4,"MK trend (Days/Year)", fontproperties = font_label)
#ax_EOS.set_ylabel("Site ID", fontsize = 12)
ax_EOS.plot([0,0],[0,57],'k-')

ax_EOS.plot([0,0],[0,57],'k-')
for i in range(len(xgrid_value)):
    a = xgrid_value[i]+0.5
    ax_EOS.plot([0,8],[a,a],'k-',lw=1)
    ax_EOS.text(7,a-1,types[i],fontproperties = font_tick)
ax_EOS.text(7,56,'CRO',fontproperties = font_tick)        

y_p05 = np.abs(ydata.copy()) + 0.5
ind = EOS_P > 0.05
y_p05[ind] = np.nan

y_p1 = np.abs(ydata.copy()) + 0.5
ind = EOS_P > 0.1
y_p1[ind] = np.nan
ind = EOS_P <= 0.05
y_p1[ind] = np.nan

ax_EOS.plot(y_p05,x,'k',marker=u'$* *$',linewidth = 0,MarkerSize=10,label = 'P < 0.05')
ax_EOS.plot(y_p1,x,'k',marker=u'$*$',linewidth = 0, MarkerSize=7, label = 'P < 0.1')
ax_EOS.set_ylim([0,57])
ax_EOS.set_xlim([0,8])
ax_EOS.set_xticks([0,1,3,5,7])
ax_EOS.set_xticklabels([0,1,3,5,7],fontproperties = font_tick)
ax_EOS.set_yticklabels([])


plt.grid(linestyle='dashed')
ax_EOS.set_axisbelow(True)


plt.legend(bbox_to_anchor=(0.02, 1),frameon=True,prop = font_tick,handlelength=2)
fig.tight_layout()
plt.subplots_adjust(left=0.05, bottom=0.05, top=0.95, right=0.95, wspace=0, hspace=0) 

outfig_file = 'output_figures/FigS8_SOS_EOS_MK_%s_trend20181009_latitude_sort.png' %(method)
plt.savefig(outfig_file,format='png',dpi=300,bbox_inches='tight')
plt.show()


'''
fig=plt.figure(figsize=cm2inch(14, 6))
hist_SOS = plt.subplot(1, 2,1) 
hist_SOS.hist(SOS_slp, 25, normed=True)
hist_SOS.plot([0,0],[0,1],color ='Gray' ,linestyle = '--')
hist_SOS.set_xlim([-8,8])
hist_SOS.set_ylim([0,0.9])
hist_SOS.plot([np.nanmean(SOS_slp),np.nanmean(SOS_slp)],[1,np.nanmean(SOS_slp)],'r')
plt.grid(linestyle='dashed')
hist_SOS.set_ylabel('Frequency',fontproperties = font_label)
hist_SOS.text(-7,0.7,'a: SOS',fontproperties = font_label)

hist_EOS = plt.subplot(1, 2,2) 
hist_EOS.hist(EOS_slp, 25, normed=True,label='Frequency')
hist_EOS.plot([0,0],[0,1],color ='Gray' ,linestyle = '--',label = 'Line: X=0')
hist_EOS.plot([np.nanmean(EOS_slp),np.nanmean(EOS_slp)],[1,np.nanmean(SOS_slp)],'r', label = 'Average')
hist_EOS.set_xlim([-8,8])
hist_EOS.set_ylim([0,0.9])
hist_EOS.set_yticklabels([])
hist_EOS.set_xlabel("MK trend (days/year)",fontproperties = font_label,x=0)
plt.grid(linestyle='dashed')
hist_EOS.text(-7,0.7,'b: EOS',fontproperties = font_label)


plt.grid(linestyle='dashed')

fig.tight_layout()
plt.subplots_adjust(left=0.05, bottom=0.05, top=0.95, right=0.95, wspace=0, hspace=0) 
leg = plt.legend(bbox_to_anchor=(0.4, 0.7),fontsize=10)
leg.get_frame().set_linewidth(0.0)
outfig_file = 'output_figures/Fig_S8_hist_SOS_EOS_MK_hist_%s_20181009.png' %(method)
plt.savefig(outfig_file,format='png',dpi=300,bbox_inches='tight')
plt.show()

'''


