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

sensitivity_file = '../NCOMMS-19-00016-T-SourceDataFile/Supplementary_Figure_13_end_date_sensitivity.xlsx'

sensitivity_data_SOS = pd.read_excel(sensitivity_file,"FigureS13a")
sensitivity_data_EOS = pd.read_excel(sensitivity_file,"FigureS13b")
sensitivity_data_spr = pd.read_excel(sensitivity_file,"FigureS13c")
sensitivity_data_aut = pd.read_excel(sensitivity_file,"FigureS13d")
sensitivity_data_yr = pd.read_excel(sensitivity_file,"FigureS13e")


fld1 = sensitivity_data_SOS["Period1"]
fld2 = sensitivity_data_SOS["Period2"]
### slope #########
SOS_slp_bf_wh = sensitivity_data_SOS["SOS_slp_bf_wh"]
SOS_slp_af_wh = sensitivity_data_SOS["SOS_slp_af_wh"]

EOS_slp_bf_wh = sensitivity_data_EOS["EOS_slp_bf_wh"]
EOS_slp_af_wh = sensitivity_data_EOS["EOS_slp_af_wh"]


temp_spr_slp_bf_wh = sensitivity_data_spr["temp_spr_slp_bf_wh"]
temp_spr_slp_af_wh = sensitivity_data_spr["temp_spr_slp_af_wh"]

temp_aut_slp_bf_wh = sensitivity_data_aut["temp_aut_slp_bf_wh"]
temp_aut_slp_af_wh = sensitivity_data_aut["temp_aut_slp_af_wh"]

temp_yr_slp_bf_wh = sensitivity_data_yr["temp_yr_slp_bf_wh"]
temp_yr_slp_af_wh = sensitivity_data_yr["temp_yr_slp_af_wh"]

### P value #######
SOS_P_bf_wh = sensitivity_data_SOS["SOS_P_bf_wh"]
SOS_P_af_wh = sensitivity_data_SOS["SOS_P_af_wh"]
EOS_P_bf_wh = sensitivity_data_EOS["EOS_P_bf_wh"]
EOS_P_af_wh = sensitivity_data_EOS["EOS_P_af_wh"]
temp_spr_P_bf_wh = sensitivity_data_spr["temp_spr_P_bf_wh"]
temp_spr_P_af_wh = sensitivity_data_spr["temp_spr_P_af_wh"]
temp_aut_P_bf_wh = sensitivity_data_aut["temp_aut_P_bf_wh"]
temp_aut_P_af_wh = sensitivity_data_aut["temp_aut_P_af_wh"]
temp_yr_P_bf_wh = sensitivity_data_yr["temp_yr_P_bf_wh"]
temp_yr_P_af_wh = sensitivity_data_yr["temp_yr_P_af_wh"]


x_axis = np.arange(len(fld1))

flds  = []
for i in range(len(x_axis)):
    flds.append("%s\n%s" %(fld1[i],fld2[i]))
    
    
width = 0.4
fig=plt.figure(figsize=cm2inch(20, 20))
############### plot SOS ###############
ax1 = plt.subplot(3,2,1)
ax1.plot([-1,12],[0,0],color='k')
rects1 = ax1.bar(x_axis-0.2, SOS_slp_bf_wh, width, color='g', label="before warming hiatus") #, yerr=envir_SOS_data_std
rects2 = ax1.bar(x_axis+0.2, SOS_slp_af_wh, width, color='r', label="during warming hiatus") #, yerr=envir_SOS_data_std
ax1.set_ylim([-0.6,0.6])
ax1.set_xlim([-0.5,8.5])
ax1.set_xticks(range(9))
ax1.set_yticks([-0.4,-0.2,0,0.2,0.4])
ax1.set_yticklabels([-0.4,-0.2,0,0.2,0.4],fontproperties = font_tick)
ax1.set_ylabel('days/year',fontproperties = font_label)
#ax1.set_xticklabels(flds,rotation=90)
ax1.grid(color = 'lightgrey',linestyle='--')
ax1.set_axisbelow(True)
ax1.text(0,0.5,'a: GIMMS3g SOS',fontproperties = font_sub_title)
plt.legend(frameon=False,prop=font_tick)
# Add counts above the two bar graphs
for i in range(len(rects1)):
    rect = rects1[i]
    if(SOS_P_bf_wh[i]<=0.05):
        height = rect.get_height()
        plt.text(rect.get_x() + rect.get_width()/2.0, height+height*0.3, "**", ha='center', va='bottom',fontproperties = font_tick)
    elif(SOS_P_bf_wh[i]<=0.1):
        height = rect.get_height()
        plt.text(rect.get_x() + rect.get_width()/2.0, height + height*0.3, "*", ha='center', va='bottom',fontproperties = font_tick)
for i in range(len(rects2)):
    rect = rects2[i]
    if(SOS_P_af_wh[i]<=0.05):
        height = rect.get_height()
        plt.text(rect.get_x() + rect.get_width()/2.0, height+height*0.3, "**", ha='center', va='bottom',fontproperties = font_tick)
    elif(SOS_P_af_wh[i]<=0.1):
        height = rect.get_height()
        plt.text(rect.get_x() + rect.get_width()/2.0, height + height*0.3, "*", ha='center', va='bottom',fontproperties = font_tick)
            

ax2 = plt.subplot(3,2,2)
ax2.plot([-1,12],[0,0],color='k')
rects3 = ax2.bar(x_axis-0.2, EOS_slp_bf_wh, width, color='g') #, yerr=envir_EOS_data_std
rects4 = ax2.bar(x_axis+0.2, EOS_slp_af_wh, width, color='r') #, yerr=envir_EOS_data_std
ax2.set_ylim([-0.6,0.6])
ax2.set_xlim([-0.5,8.5])
ax2.set_xticks(range(9))
ax2.set_yticks([-0.4,-0.2,0,0.2,0.4])
#ax2.set_xticklabels(flds,rotation=90)
ax2.set_yticklabels([])
ax2.grid(color = 'lightgrey',linestyle='--')
ax2.set_axisbelow(True)
ax2.text(0,0.5,'b: GIMMS3g EOS',fontproperties = font_sub_title)
# Add counts above the two bar graphs
for i in range(len(rects3)):
    rect = rects3[i]
    if(EOS_P_bf_wh[i]<=0.05):
        height = rect.get_height()
        plt.text(rect.get_x() + rect.get_width()/2.0, height+height*0.01, "**", ha='center', va='bottom',fontproperties = font_tick)
    elif(EOS_P_bf_wh[i]<=0.1):
        height = rect.get_height()
        plt.text(rect.get_x() + rect.get_width()/2.0, height + height*0.01, "*", ha='center', va='bottom',fontproperties = font_tick)
for i in range(len(rects4)):
    rect = rects4[i]
    if(EOS_P_af_wh[i]<=0.05):
        height = rect.get_height()
        plt.text(rect.get_x() + rect.get_width()/2.0, height+height*0.01, "**", ha='center', va='bottom',fontproperties = font_tick)
    elif(EOS_P_af_wh[i]<=0.1):
        height = rect.get_height()
        plt.text(rect.get_x() + rect.get_width()/2.0, height + height*0.01, "*", ha='center', va='bottom',fontproperties = font_tick)




ax3 = plt.subplot(3,2,3)
ax3.plot([-1,12],[0,0],color='k')
rects5 = ax3.bar(x_axis-0.2, temp_spr_slp_bf_wh, width, color='g') #, yerr=envir_EOS_data_std
rects6 = ax3.bar(x_axis+0.2, temp_spr_slp_af_wh, width, color='r') #, yerr=envir_EOS_data_std
ax3.set_ylim([0,0.09])
ax3.set_yticks([0.00,0.02,0.04,0.06,0.08])
ax3.set_yticklabels([0.00,0.02,0.04,0.06,0.08],fontproperties = font_sub_title)
ax3.set_xlim([-0.5,8.5])
ax3.set_xticks(range(9))
ax3.set_ylabel('Mann-Kendall Trend\n $^\circ$C/year',fontproperties = font_label)
#ax3.set_xticklabels(flds,rotation=90)
#ax3.set_yticklabels([])
ax3.grid(color = 'lightgrey',linestyle='--')
ax3.set_axisbelow(True)
ax3.text(0,0.08,'c: Spring CRUTEM4',fontproperties = font_sub_title)
# Add counts above the two bar graphs
for i in range(len(rects5)):
    rect = rects5[i]
    if(temp_spr_P_bf_wh[i]<=0.05):
        height = rect.get_height()
        plt.text(rect.get_x() + rect.get_width()/2.0, height+height*0.01, "**", ha='center', va='bottom',fontproperties = font_tick)
    elif(temp_spr_P_bf_wh[i]<=0.1):
        height = rect.get_height()
        plt.text(rect.get_x() + rect.get_width()/2.0, height + height*0.01, "*", ha='center', va='bottom',fontproperties = font_tick)
for i in range(len(rects6)):
    rect = rects6[i]
    if(temp_spr_P_af_wh[i]<=0.05):
        height = rect.get_height()
        plt.text(rect.get_x() + rect.get_width()/2.0, height+height*0.01, "**", ha='center', va='bottom',fontproperties = font_tick)
    elif(temp_spr_P_af_wh[i]<=0.1):
        height = rect.get_height()
        plt.text(rect.get_x() + rect.get_width()/2.0, height + height*0.01, "*", ha='center', va='bottom',fontproperties = font_tick)



ax4 = plt.subplot(3,2,4)
ax4.plot([-1,12],[0,0],color='k')
rects7 = ax4.bar(x_axis-0.2, temp_aut_slp_bf_wh, width, color='g') #, yerr=envir_EOS_data_std
rects8 = ax4.bar(x_axis+0.2, temp_aut_slp_af_wh, width, color='r') #, yerr=envir_EOS_data_std
ax4.set_ylim([0,0.09])
ax4.set_yticks([0.00,0.02,0.04,0.06,0.08])
ax4.set_xlim([-0.5,8.5])
ax4.set_xticks(range(9))
ax4.set_xticklabels(flds,rotation=90,fontproperties=font_tick)
ax4.set_yticklabels([])
ax4.grid(color = 'lightgrey',linestyle='--')
ax4.set_axisbelow(True)
ax4.text(0,0.08,'d: Autumn CRUTEM4',fontproperties = font_sub_title)

# Add counts above the two bar graphs
for i in range(len(rects7)):
    rect = rects7[i]
    if(temp_aut_P_bf_wh[i]<=0.05):
        height = rect.get_height()
        plt.text(rect.get_x() + rect.get_width()/2.0, height+height*0.01, "**", ha='center', va='bottom',fontproperties = font_tick)
    elif(temp_aut_P_bf_wh[i]<=0.1):
        height = rect.get_height()
        plt.text(rect.get_x() + rect.get_width()/2.0, height + height*0.01, "*", ha='center', va='bottom',fontproperties = font_tick)
for i in range(len(rects8)):
    rect = rects8[i]
    if(temp_aut_P_af_wh[i]<=0.05):
        height = rect.get_height()
        plt.text(rect.get_x() + rect.get_width()/2.0, height+height*0.01, "**", ha='center', va='bottom',fontproperties = font_tick)
    elif(temp_aut_P_af_wh[i]<=0.1):
        height = rect.get_height()
        plt.text(rect.get_x() + rect.get_width()/2.0, height + height*0.01, "*", ha='center', va='bottom',fontproperties = font_tick)
        

ax5 = plt.subplot(3,2,5)
ax5.plot([-1,12],[0,0],color='k')
rects9 = ax5.bar(x_axis-0.2, temp_yr_slp_bf_wh, width, color='g') #, yerr=envir_EOS_data_std
rects10 = ax5.bar(x_axis+0.2, temp_yr_slp_af_wh, width, color='r') #, yerr=envir_EOS_data_std
ax5.set_ylim([0,0.09])
ax5.set_yticks([0.00,0.02,0.04,0.06,0.08])
ax5.set_xlim([-0.5,8.5])
ax5.set_xticks(range(9))
ax5.set_xticklabels(flds,rotation=90,fontproperties=font_tick)
#ax5.set_yticklabels([])
ax5.grid(color = 'lightgrey',linestyle='--')
ax5.set_axisbelow(True)
ax5.text(0,0.08,'e: Annual CRUTEM4',fontproperties = font_sub_title)
ax5.set_ylabel('$^\circ$C/year',fontproperties = font_label)


# Add counts above the two bar graphs
for i in range(len(rects9)):
    rect = rects9[i]
    if(temp_yr_P_bf_wh[i]<=0.05):
        height = rect.get_height()
        plt.text(rect.get_x() + rect.get_width()/2.0, height+height*0.01, "**", ha='center', va='bottom',fontproperties = font_tick)
    elif(temp_yr_P_bf_wh[i]<=0.1):
        height = rect.get_height()
        plt.text(rect.get_x() + rect.get_width()/2.0, height + height*0.01, "*", ha='center', va='bottom',fontproperties = font_tick)
for i in range(len(rects10)):
    rect = rects10[i]
    if(temp_yr_P_af_wh[i]<=0.05):
        height = rect.get_height()
        plt.text(rect.get_x() + rect.get_width()/2.0, height+height*0.01, "**", ha='center', va='bottom',fontproperties = font_tick)
    elif(temp_yr_P_af_wh[i]<=0.1):
        height = rect.get_height()
        plt.text(rect.get_x() + rect.get_width()/2.0, height + height*0.01, "*", ha='center', va='bottom',fontproperties = font_tick)

fig.tight_layout()
plt.subplots_adjust(left=0.05, bottom=0.05, top=0.95, right=0.95, wspace=0, hspace=0) 
plt.savefig('output_figures/FigS13_wh_sensitivity_ok.png',format='png',dpi=300,bbox_inches='tight')
plt.show()