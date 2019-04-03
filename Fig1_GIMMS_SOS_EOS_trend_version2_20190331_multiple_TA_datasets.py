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

def cm2inch(*tupl):
    inch = 2.54
    if isinstance(tupl[0], tuple):
        return tuple(i/inch for i in tupl[0])
    else:
        return tuple(i/inch for i in tupl) 


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

infile = "../NCOMMS-19-00016-T-SourceDataFile/Figure1.data.xlsx"        


data_SOS_v1 = pd.read_excel(infile,"Figure1a")


### read SOS and get trend ###############
#GIMMS version1
SOS_avg_v1 = np.asarray(data_SOS_v1['SOS_GIMMS3g'])
SOS_Years_v1 = np.asarray(data_SOS_v1['Year'])

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
data_EOS_v1 = pd.read_excel(infile,"Figure1b")
EOS_avg_v1 = np.asarray(data_EOS_v1['EOS_GIMMS3g'])
EOS_Years_v1 = np.asarray(data_EOS_v1['Year'])

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


##### read temperature and get trend ##########
Tair_spr_data = pd.read_excel(infile,"Figure1c")
CRUTEM4_spr = np.asarray(Tair_spr_data['CRUTEM4_spr'])
CRUTEM3_spr = np.asarray(Tair_spr_data['CRUTEM3_spr'])
ind = ~np.isnan(CRUTEM3_spr)
CRUTEM3_spr = CRUTEM3_spr[ind]
NOAA_spr = np.asarray(Tair_spr_data['NOAA_spr'])
Berkely_Earth_spr = np.asarray(Tair_spr_data['Berkely_Earth_spr'])
NASA_GISTEMP_spr = np.asarray(Tair_spr_data['NASA_spr'])


Tair_aut_data = pd.read_excel(infile,"Figure1d")
CRUTEM4_aut = np.asarray(Tair_aut_data['CRUTEM4_aut'])
CRUTEM3_aut = np.asarray(Tair_aut_data['CRUTEM3_aut'])
ind = ~np.isnan(CRUTEM3_aut)
CRUTEM3_aut = CRUTEM3_aut[ind]
NOAA_aut = np.asarray(Tair_aut_data['NOAA_aut'])
Berkely_Earth_aut = np.asarray(Tair_aut_data['Berkely_Earth_aut'])
NASA_GISTEMP_aut = np.asarray(Tair_aut_data['NASA_aut'])

Tair_year_data = pd.read_excel(infile,"Figure1e")
CRUTEM4_avg = np.asarray(Tair_year_data['CRUTEM4_year'])
CRUTEM3_avg = np.asarray(Tair_year_data['CRUTEM3_year'])
ind = ~np.isnan(CRUTEM3_avg)
CRUTEM3_avg = CRUTEM3_avg[ind]
NOAA_avg = np.asarray(Tair_year_data['NOAA_year'])
Berkely_Earth_avg = np.asarray(Tair_year_data['Berkely_Earth_year'])
NASA_GISTEMP_avg = np.asarray(Tair_year_data['NASA_year'])


CRUTEM4_year = Tair_year_data['Year']
CRUTEM3_year = CRUTEM4_year[ind]
NOAA_year = CRUTEM4_year
Berkely_Earth_year = CRUTEM4_year
NASA_GISTEMP_year = CRUTEM4_year

### linear trend spring average temperature #####
CRUTEM4_spr_bf98 = CRUTEM4_spr[0:17]
years_bf98_CRUTEM4_spr = CRUTEM4_year[0:17]
CRUTEM4_spr_af98 = CRUTEM4_spr[16:33]
years_af98_CRUTEM4_spr = CRUTEM4_year[16:33]

h_bf98_CRUTEM4_spr, trend_bf98_CRUTEM4_spr, intp_bf98_CRUTEM4_spr, p_value_bf98_CRUTEM4_spr, z_bf98_CRUTEM4_spr = MK.mk_trend(CRUTEM4_spr_bf98,years_bf98_CRUTEM4_spr,0.05)
h_af98_CRUTEM4_spr, trend_af98_CRUTEM4_spr, intp_af98_CRUTEM4_spr, p_value_af98_CRUTEM4_spr, z_af98_CRUTEM4_spr = MK.mk_trend(CRUTEM4_spr_af98,years_af98_CRUTEM4_spr,0.05)

x_bf98_CRUTEM4_spr = np.asarray([1982,1998])
x_af98_CRUTEM4_spr = np.asarray([1998,2014])
y_bf98_CRUTEM4_spr = trend_bf98_CRUTEM4_spr*x_bf98_CRUTEM4_spr+intp_bf98_CRUTEM4_spr
y_af98_CRUTEM4_spr = trend_af98_CRUTEM4_spr*x_af98_CRUTEM4_spr+intp_af98_CRUTEM4_spr


CRUTEM3_spr_bf98 = CRUTEM3_spr[0:17]
years_bf98_CRUTEM3_spr = CRUTEM3_year[0:17]
CRUTEM3_spr_af98 = CRUTEM3_spr[16:32]
years_af98_CRUTEM3_spr = CRUTEM3_year[16:32]

h_bf98_CRUTEM3_spr, trend_bf98_CRUTEM3_spr, intp_bf98_CRUTEM3_spr, p_value_bf98_CRUTEM3_spr, z_bf98_CRUTEM3_spr = MK.mk_trend(CRUTEM3_spr_bf98,years_bf98_CRUTEM3_spr,0.05)
h_af98_CRUTEM3_spr, trend_af98_CRUTEM3_spr, intp_af98_CRUTEM3_spr, p_value_af98_CRUTEM3_spr, z_af98_CRUTEM3_spr = MK.mk_trend(CRUTEM3_spr_af98,years_af98_CRUTEM3_spr,0.05)

x_bf98_CRUTEM3_spr = np.asarray([1982,1998])
x_af98_CRUTEM3_spr = np.asarray([1998,2013])
y_bf98_CRUTEM3_spr = trend_bf98_CRUTEM3_spr*x_bf98_CRUTEM3_spr+intp_bf98_CRUTEM3_spr
y_af98_CRUTEM3_spr = trend_af98_CRUTEM3_spr*x_af98_CRUTEM3_spr+intp_af98_CRUTEM3_spr

NOAA_spr_bf98 = NOAA_spr[0:17]
years_bf98_NOAA_spr = NOAA_year[0:17]
NOAA_spr_af98 = NOAA_spr[16:33]
years_af98_NOAA_spr = NOAA_year[16:33]

h_bf98_NOAA_spr, trend_bf98_NOAA_spr, intp_bf98_NOAA_spr, p_value_bf98_NOAA_spr, z_bf98_NOAA_spr = MK.mk_trend(NOAA_spr_bf98,years_bf98_NOAA_spr,0.05)
h_af98_NOAA_spr, trend_af98_NOAA_spr, intp_af98_NOAA_spr, p_value_af98_NOAA_spr, z_af98_NOAA_spr = MK.mk_trend(NOAA_spr_af98,years_af98_NOAA_spr,0.05)

x_bf98_NOAA_spr = np.asarray([1982,1998])
x_af98_NOAA_spr = np.asarray([1998,2014])
y_bf98_NOAA_spr = trend_bf98_NOAA_spr*x_bf98_NOAA_spr+intp_bf98_NOAA_spr
y_af98_NOAA_spr = trend_af98_NOAA_spr*x_af98_NOAA_spr+intp_af98_NOAA_spr


Berkely_Earth_spr_bf98 = Berkely_Earth_spr[0:17]
years_bf98_Berkely_Earth_spr = Berkely_Earth_year[0:17]
Berkely_Earth_spr_af98 = Berkely_Earth_spr[16:33]
years_af98_Berkely_Earth_spr = Berkely_Earth_year[16:33]

h_bf98_Berkely_Earth_spr, trend_bf98_Berkely_Earth_spr, intp_bf98_Berkely_Earth_spr, p_value_bf98_Berkely_Earth_spr, z_bf98_Berkely_Earth_spr = MK.mk_trend(Berkely_Earth_spr_bf98,years_bf98_Berkely_Earth_spr,0.05)
h_af98_Berkely_Earth_spr, trend_af98_Berkely_Earth_spr, intp_af98_Berkely_Earth_spr, p_value_af98_Berkely_Earth_spr, z_af98_Berkely_Earth_spr = MK.mk_trend(Berkely_Earth_spr_af98,years_af98_Berkely_Earth_spr,0.05)

x_bf98_Berkely_Earth_spr = np.asarray([1982,1998])
x_af98_Berkely_Earth_spr = np.asarray([1998,2014])
y_bf98_Berkely_Earth_spr = trend_bf98_Berkely_Earth_spr*x_bf98_Berkely_Earth_spr+intp_bf98_Berkely_Earth_spr
y_af98_Berkely_Earth_spr = trend_af98_Berkely_Earth_spr*x_af98_Berkely_Earth_spr+intp_af98_Berkely_Earth_spr

NASA_GISTEMP_spr_bf98 = NASA_GISTEMP_spr[0:17]
years_bf98_NASA_GISTEMP_spr = NASA_GISTEMP_year[0:17]
NASA_GISTEMP_spr_af98 = NASA_GISTEMP_spr[16:33]
years_af98_NASA_GISTEMP_spr = NASA_GISTEMP_year[16:33]

h_bf98_NASA_GISTEMP_spr, trend_bf98_NASA_GISTEMP_spr, intp_bf98_NASA_GISTEMP_spr, p_value_bf98_NASA_GISTEMP_spr, z_bf98_NASA_GISTEMP_spr = MK.mk_trend(NASA_GISTEMP_spr_bf98,years_bf98_NASA_GISTEMP_spr,0.05)
h_af98_NASA_GISTEMP_spr, trend_af98_NASA_GISTEMP_spr, intp_af98_NASA_GISTEMP_spr, p_value_af98_NASA_GISTEMP_spr, z_af98_NASA_GISTEMP_spr = MK.mk_trend(NASA_GISTEMP_spr_af98,years_af98_NASA_GISTEMP_spr,0.05)

x_bf98_NASA_GISTEMP_spr = np.asarray([1982,1998])
x_af98_NASA_GISTEMP_spr = np.asarray([1998,2014])
y_bf98_NASA_GISTEMP_spr = trend_bf98_NASA_GISTEMP_spr*x_bf98_NASA_GISTEMP_spr + intp_bf98_NASA_GISTEMP_spr
y_af98_NASA_GISTEMP_spr = trend_af98_NASA_GISTEMP_spr*x_af98_NASA_GISTEMP_spr + intp_af98_NASA_GISTEMP_spr

### linear trend autumn average temperature #####
CRUTEM4_aut_bf98 = CRUTEM4_aut[0:17]
years_bf98_CRUTEM4_aut = CRUTEM4_year[0:17]
CRUTEM4_aut_af98 = CRUTEM4_aut[16:33]
years_af98_CRUTEM4_aut = CRUTEM4_year[16:33]

h_bf98_CRUTEM4_aut, trend_bf98_CRUTEM4_aut, intp_bf98_CRUTEM4_aut, p_value_bf98_CRUTEM4_aut, z_bf98_CRUTEM4_aut = MK.mk_trend(CRUTEM4_aut_bf98,years_bf98_CRUTEM4_aut,0.05)
h_af98_CRUTEM4_aut, trend_af98_CRUTEM4_aut, intp_af98_CRUTEM4_aut, p_value_af98_CRUTEM4_aut, z_af98_CRUTEM4_aut = MK.mk_trend(CRUTEM4_aut_af98,years_af98_CRUTEM4_aut,0.05)

x_bf98_CRUTEM4_aut = np.asarray([1982,1998])
x_af98_CRUTEM4_aut = np.asarray([1998,2014])
y_bf98_CRUTEM4_aut = trend_bf98_CRUTEM4_aut*x_bf98_CRUTEM4_aut+intp_bf98_CRUTEM4_aut
y_af98_CRUTEM4_aut = trend_af98_CRUTEM4_aut*x_af98_CRUTEM4_aut+intp_af98_CRUTEM4_aut


CRUTEM3_aut_bf98 = CRUTEM3_aut[0:17]
years_bf98_CRUTEM3_aut = CRUTEM3_year[0:17]
CRUTEM3_aut_af98 = CRUTEM3_aut[16:32]
years_af98_CRUTEM3_aut = CRUTEM3_year[16:32]

h_bf98_CRUTEM3_aut, trend_bf98_CRUTEM3_aut, intp_bf98_CRUTEM3_aut, p_value_bf98_CRUTEM3_aut, z_bf98_CRUTEM3_aut = MK.mk_trend(CRUTEM3_aut_bf98,years_bf98_CRUTEM3_aut,0.05)
h_af98_CRUTEM3_aut, trend_af98_CRUTEM3_aut, intp_af98_CRUTEM3_aut, p_value_af98_CRUTEM3_aut, z_af98_CRUTEM3_aut = MK.mk_trend(CRUTEM3_aut_af98,years_af98_CRUTEM3_aut,0.05)

x_bf98_CRUTEM3_aut = np.asarray([1982,1998])
x_af98_CRUTEM3_aut = np.asarray([1998,2013])
y_bf98_CRUTEM3_aut = trend_bf98_CRUTEM3_aut*x_bf98_CRUTEM3_aut+intp_bf98_CRUTEM3_aut
y_af98_CRUTEM3_aut = trend_af98_CRUTEM3_aut*x_af98_CRUTEM3_aut+intp_af98_CRUTEM3_aut

NOAA_aut_bf98 = NOAA_aut[0:17]
years_bf98_NOAA_aut = NOAA_year[0:17]
NOAA_aut_af98 = NOAA_aut[16:33]
years_af98_NOAA_aut = NOAA_year[16:33]

h_bf98_NOAA_aut, trend_bf98_NOAA_aut, intp_bf98_NOAA_aut, p_value_bf98_NOAA_aut, z_bf98_NOAA_aut = MK.mk_trend(NOAA_aut_bf98,years_bf98_NOAA_aut,0.05)
h_af98_NOAA_aut, trend_af98_NOAA_aut, intp_af98_NOAA_aut, p_value_af98_NOAA_aut, z_af98_NOAA_aut = MK.mk_trend(NOAA_aut_af98,years_af98_NOAA_aut,0.05)

x_bf98_NOAA_aut = np.asarray([1982,1998])
x_af98_NOAA_aut = np.asarray([1998,2014])
y_bf98_NOAA_aut = trend_bf98_NOAA_aut*x_bf98_NOAA_aut+intp_bf98_NOAA_aut
y_af98_NOAA_aut = trend_af98_NOAA_aut*x_af98_NOAA_aut+intp_af98_NOAA_aut



Berkely_Earth_aut_bf98 = Berkely_Earth_aut[0:17]
years_bf98_Berkely_Earth_aut = Berkely_Earth_year[0:17]
Berkely_Earth_aut_af98 = Berkely_Earth_aut[16:33]
years_af98_Berkely_Earth_aut = Berkely_Earth_year[16:33]

h_bf98_Berkely_Earth_aut, trend_bf98_Berkely_Earth_aut, intp_bf98_Berkely_Earth_aut, p_value_bf98_Berkely_Earth_aut, z_bf98_Berkely_Earth_aut = MK.mk_trend(Berkely_Earth_aut_bf98,years_bf98_Berkely_Earth_aut,0.05)
h_af98_Berkely_Earth_aut, trend_af98_Berkely_Earth_aut, intp_af98_Berkely_Earth_aut, p_value_af98_Berkely_Earth_aut, z_af98_Berkely_Earth_aut = MK.mk_trend(Berkely_Earth_aut_af98,years_af98_Berkely_Earth_aut,0.05)

x_bf98_Berkely_Earth_aut = np.asarray([1982,1998])
x_af98_Berkely_Earth_aut = np.asarray([1998,2014])
y_bf98_Berkely_Earth_aut = trend_bf98_Berkely_Earth_aut*x_bf98_Berkely_Earth_aut+intp_bf98_Berkely_Earth_aut
y_af98_Berkely_Earth_aut = trend_af98_Berkely_Earth_aut*x_af98_Berkely_Earth_aut+intp_af98_Berkely_Earth_aut


NASA_GISTEMP_aut_bf98 = NASA_GISTEMP_aut[0:17]
years_bf98_NASA_GISTEMP_aut = NASA_GISTEMP_year[0:17]
NASA_GISTEMP_aut_af98 = NASA_GISTEMP_aut[16:33]
years_af98_NASA_GISTEMP_aut = NASA_GISTEMP_year[16:33]

h_bf98_NASA_GISTEMP_aut, trend_bf98_NASA_GISTEMP_aut, intp_bf98_NASA_GISTEMP_aut, p_value_bf98_NASA_GISTEMP_aut, z_bf98_NASA_GISTEMP_aut = MK.mk_trend(NASA_GISTEMP_aut_bf98,years_bf98_NASA_GISTEMP_aut,0.05)
h_af98_NASA_GISTEMP_aut, trend_af98_NASA_GISTEMP_aut, intp_af98_NASA_GISTEMP_aut, p_value_af98_NASA_GISTEMP_aut, z_af98_NASA_GISTEMP_aut = MK.mk_trend(NASA_GISTEMP_aut_af98,years_af98_NASA_GISTEMP_aut,0.05)

x_bf98_NASA_GISTEMP_aut = np.asarray([1982,1998])
x_af98_NASA_GISTEMP_aut = np.asarray([1998,2014])
y_bf98_NASA_GISTEMP_aut = trend_bf98_NASA_GISTEMP_aut*x_bf98_NASA_GISTEMP_aut+intp_bf98_NASA_GISTEMP_aut
y_af98_NASA_GISTEMP_aut = trend_af98_NASA_GISTEMP_aut*x_af98_NASA_GISTEMP_aut+intp_af98_NASA_GISTEMP_aut

### linear trend year average temperature #####
CRUTEM4_avg_bf98 = CRUTEM4_avg[0:17]
years_bf98_CRUTEM4_avg = CRUTEM4_year[0:17]
CRUTEM4_avg_af98 = CRUTEM4_avg[16:33]
years_af98_CRUTEM4_avg = CRUTEM4_year[16:33]

h_bf98_CRUTEM4_avg, trend_bf98_CRUTEM4_avg, intp_bf98_CRUTEM4_avg, p_value_bf98_CRUTEM4_avg, z_bf98_CRUTEM4_avg = MK.mk_trend(CRUTEM4_avg_bf98,years_bf98_CRUTEM4_avg,0.05)
h_af98_CRUTEM4_avg, trend_af98_CRUTEM4_avg, intp_af98_CRUTEM4_avg, p_value_af98_CRUTEM4_avg, z_af98_CRUTEM4_avg = MK.mk_trend(CRUTEM4_avg_af98,years_af98_CRUTEM4_avg,0.05)

x_bf98_CRUTEM4_avg = np.asarray([1982,1998])
x_af98_CRUTEM4_avg = np.asarray([1998,2014])
y_bf98_CRUTEM4_avg = trend_bf98_CRUTEM4_avg*x_bf98_CRUTEM4_avg+intp_bf98_CRUTEM4_avg
y_af98_CRUTEM4_avg = trend_af98_CRUTEM4_avg*x_af98_CRUTEM4_avg+intp_af98_CRUTEM4_avg


CRUTEM3_avg_bf98 = CRUTEM3_avg[0:17]
years_bf98_CRUTEM3_avg = CRUTEM3_year[0:17]
CRUTEM3_avg_af98 = CRUTEM3_avg[16:32]
years_af98_CRUTEM3_avg = CRUTEM3_year[16:32]

h_bf98_CRUTEM3_avg, trend_bf98_CRUTEM3_avg, intp_bf98_CRUTEM3_avg, p_value_bf98_CRUTEM3_avg, z_bf98_CRUTEM3_avg = MK.mk_trend(CRUTEM3_avg_bf98,years_bf98_CRUTEM3_avg,0.05)
h_af98_CRUTEM3_avg, trend_af98_CRUTEM3_avg, intp_af98_CRUTEM3_avg, p_value_af98_CRUTEM3_avg, z_af98_CRUTEM3_avg = MK.mk_trend(CRUTEM3_avg_af98,years_af98_CRUTEM3_avg,0.05)

x_bf98_CRUTEM3_avg = np.asarray([1982,1998])
x_af98_CRUTEM3_avg = np.asarray([1998,2013])
y_bf98_CRUTEM3_avg = trend_bf98_CRUTEM3_avg*x_bf98_CRUTEM3_avg+intp_bf98_CRUTEM3_avg
y_af98_CRUTEM3_avg = trend_af98_CRUTEM3_avg*x_af98_CRUTEM3_avg+intp_af98_CRUTEM3_avg

NOAA_avg_bf98 = NOAA_avg[0:17]
years_bf98_NOAA_avg = NOAA_year[0:17]
NOAA_avg_af98 = NOAA_avg[16:33]
years_af98_NOAA_avg = NOAA_year[16:33]

h_bf98_NOAA_avg, trend_bf98_NOAA_avg, intp_bf98_NOAA_avg, p_value_bf98_NOAA_avg, z_bf98_NOAA_avg = MK.mk_trend(NOAA_avg_bf98,years_bf98_NOAA_avg,0.05)
h_af98_NOAA_avg, trend_af98_NOAA_avg, intp_af98_NOAA_avg, p_value_af98_NOAA_avg, z_af98_NOAA_avg = MK.mk_trend(NOAA_avg_af98,years_af98_NOAA_avg,0.05)

x_bf98_NOAA_avg = np.asarray([1982,1998])
x_af98_NOAA_avg = np.asarray([1998,2014])
y_bf98_NOAA_avg = trend_bf98_NOAA_avg*x_bf98_NOAA_avg+intp_bf98_NOAA_avg
y_af98_NOAA_avg = trend_af98_NOAA_avg*x_af98_NOAA_avg+intp_af98_NOAA_avg



Berkely_Earth_avg_bf98 = Berkely_Earth_avg[0:17]
years_bf98_Berkely_Earth_avg = Berkely_Earth_year[0:17]
Berkely_Earth_avg_af98 = Berkely_Earth_avg[16:33]
years_af98_Berkely_Earth_avg = Berkely_Earth_year[16:33]

h_bf98_Berkely_Earth_avg, trend_bf98_Berkely_Earth_avg, intp_bf98_Berkely_Earth_avg, p_value_bf98_Berkely_Earth_avg, z_bf98_Berkely_Earth_avg = MK.mk_trend(Berkely_Earth_avg_bf98,years_bf98_Berkely_Earth_avg,0.05)
h_af98_Berkely_Earth_avg, trend_af98_Berkely_Earth_avg, intp_af98_Berkely_Earth_avg, p_value_af98_Berkely_Earth_avg, z_af98_Berkely_Earth_avg = MK.mk_trend(Berkely_Earth_avg_af98,years_af98_Berkely_Earth_avg,0.05)

x_bf98_Berkely_Earth_avg = np.asarray([1982,1998])
x_af98_Berkely_Earth_avg = np.asarray([1998,2014])
y_bf98_Berkely_Earth_avg = trend_bf98_Berkely_Earth_avg*x_bf98_Berkely_Earth_avg+intp_bf98_Berkely_Earth_avg
y_af98_Berkely_Earth_avg = trend_af98_Berkely_Earth_avg*x_af98_Berkely_Earth_avg+intp_af98_Berkely_Earth_avg


NASA_GISTEMP_avg_bf98 = NASA_GISTEMP_avg[0:17]
years_bf98_NASA_GISTEMP_avg = NASA_GISTEMP_year[0:17]
NASA_GISTEMP_avg_af98 = NASA_GISTEMP_avg[16:33]
years_af98_NASA_GISTEMP_avg = NASA_GISTEMP_year[16:33]

h_bf98_NASA_GISTEMP_avg, trend_bf98_NASA_GISTEMP_avg, intp_bf98_NASA_GISTEMP_avg, p_value_bf98_NASA_GISTEMP_avg, z_bf98_NASA_GISTEMP_avg = MK.mk_trend(NASA_GISTEMP_avg_bf98,years_bf98_NASA_GISTEMP_avg,0.05)
h_af98_NASA_GISTEMP_avg, trend_af98_NASA_GISTEMP_avg, intp_af98_NASA_GISTEMP_avg, p_value_af98_NASA_GISTEMP_avg, z_af98_NASA_GISTEMP_avg = MK.mk_trend(NASA_GISTEMP_avg_af98,years_af98_NASA_GISTEMP_avg,0.05)

x_bf98_NASA_GISTEMP_avg = np.asarray([1982,1998])
x_af98_NASA_GISTEMP_avg = np.asarray([1998,2014])
y_bf98_NASA_GISTEMP_avg = trend_bf98_NASA_GISTEMP_avg*x_bf98_NASA_GISTEMP_avg+intp_bf98_NASA_GISTEMP_avg
y_af98_NASA_GISTEMP_avg = trend_af98_NASA_GISTEMP_avg*x_af98_NASA_GISTEMP_avg+intp_af98_NASA_GISTEMP_avg

### plot figures ######
fig=plt.figure(figsize=cm2inch(21, 15))
############### plot SOS ###############
ax1 = plt.subplot(3,2,1)
ax1.plot(SOS_Years_v1,SOS_avg_v1,'b-o',Markersize=4,linewidth = 1,label='GIMMS3g')
ax1.plot(x_bf98_SOS_v1,y_bf98_SOS_v1,color='b',linestyle='--')
ax1.plot(x_af98_SOS_v1,y_af98_SOS_v1,color='b',linestyle='--')

ax1.set_xlim([1981,2015])
#ax1.set_ylim([109,119])
#ax1.set_yticks([110,112,114,116,118])
ax1.set_ylim([113,123])
ax1.set_yticks([114,116,118,120,122])
ax1.set_yticklabels([114,116,118,120,122],fontproperties = font_tick)
ax1.set_ylabel('SOS (DOY)',fontproperties = font_label)
ax1.fill_between([1998,2012],[130,130],[100,100],color = 'lightgrey',alpha = 0.5)
ax1.grid(color = 'lightgrey',linestyle = '--')
ax1.set_xticklabels([])
ax1.text(1982,114,'a: SOS',fontproperties = font_sub_title)
#plt.legend(frameon=False, prop=font_tick)

############### plot EOS ###############
ax2 = plt.subplot(3,2,2)
ax2.plot(EOS_Years_v1,EOS_avg_v1,'b-o',Markersize=4,linewidth = 1,label='GIMMS3g')
ax2.plot(x_bf98_EOS_v1,y_bf98_EOS_v1,color='b',linestyle='--')
ax2.plot(x_af98_EOS_v1,y_af98_EOS_v1,color='b',linestyle='--')

ax2.set_xlim([1981,2015])
ax2.set_ylim([285,305])
ax2.set_yticks([287,291,295,299,303])
ax2.set_yticklabels([287,291,295,299,303],fontproperties = font_tick)
ax2.set_ylabel('EOS (DOY)',fontproperties = font_label)
ax2.fill_between([1998,2012],[310,310],[280,280],color = 'lightgrey',alpha = 0.5)
ax2.grid(color = 'lightgrey',linestyle = '--')
ax2.yaxis.tick_right()
ax2.yaxis.set_label_position("right")
ax2.set_xticklabels([])
ax2.text(1982,301,'b: EOS',fontproperties = font_sub_title)
plt.legend(frameon=False, bbox_to_anchor=(0.8, -1.63), prop=font_tick)

############### plot spring temperature ###############
ax3 = plt.subplot(3,2,3)

ax3.plot(CRUTEM3_year,CRUTEM3_spr,'r-',Markersize=4,linewidth = 1,label='CRUTEM3')
ax3.plot(x_bf98_CRUTEM3_spr,y_bf98_CRUTEM3_spr,color='r',linestyle='--')
ax3.plot(x_af98_CRUTEM3_spr,y_af98_CRUTEM3_spr,color='r',linestyle='--')

ax3.plot(CRUTEM4_year,CRUTEM4_spr,'b-',Markersize=4,linewidth = 1,label='CRUTEM4')
ax3.plot(x_bf98_CRUTEM4_spr,y_bf98_CRUTEM4_spr,color='b',linestyle='--')
ax3.plot(x_af98_CRUTEM4_spr,y_af98_CRUTEM4_spr,color='b',linestyle='--')

ax3.plot(NOAA_year,NOAA_spr,'k-',Markersize=4,linewidth = 1,label='NOAA')
ax3.plot(x_bf98_NOAA_spr,y_bf98_NOAA_spr,color='k',linestyle='--')
ax3.plot(x_af98_NOAA_spr,y_af98_NOAA_spr,color='k',linestyle='--')

ax3.plot(Berkely_Earth_year,Berkely_Earth_spr,'m-',Markersize=4,linewidth = 1,label='Berkley Earth')
ax3.plot(x_bf98_Berkely_Earth_spr,y_bf98_Berkely_Earth_spr,color='m',linestyle='--')
ax3.plot(x_af98_Berkely_Earth_spr,y_af98_Berkely_Earth_spr,color='m',linestyle='--')

ax3.plot(NASA_GISTEMP_year,NASA_GISTEMP_spr,'y-',Markersize=4,linewidth = 1,label='NASA GISTEMP')
ax3.plot(x_bf98_NASA_GISTEMP_spr,y_bf98_NASA_GISTEMP_spr,color='y',linestyle='--')
ax3.plot(x_af98_NASA_GISTEMP_spr,y_af98_NASA_GISTEMP_spr,color='y',linestyle='--')


ax3.set_xlim([1981,2015])
ax3.set_ylim([-0.4,2.1])
ax3.set_yticks([0,0.4,0.8,1.2,1.6])
ax3.set_yticklabels([0,0.4,0.8,1.2,1.6],fontproperties = font_tick)
ax3.set_ylabel('Spring Tair ($^\circ$C)',fontproperties = font_label)
ax3.fill_between([1998,2012],[3,3],[-0.5,-0.5],color = 'lightgrey',alpha = 0.5)
ax3.grid(color = 'lightgrey',linestyle = '--')
ax3.set_xticklabels([])
ax3.text(1982,1.6,'c: Spring',fontproperties = font_sub_title)
#plt.legend(frameon=False,loc=4, prop=font_tick)

############### plot autumn temperature ###############
ax4 = plt.subplot(3,2,4)

ax4.plot(CRUTEM3_year,CRUTEM3_aut,'r-',Markersize=4,linewidth = 1,label='CRUTEM3')
ax4.plot(x_bf98_CRUTEM3_aut,y_bf98_CRUTEM3_aut,color='r',linestyle='--')
ax4.plot(x_af98_CRUTEM3_aut,y_af98_CRUTEM3_aut,color='r',linestyle='--')

ax4.plot(CRUTEM4_year,CRUTEM4_aut,'b-',Markersize=4,linewidth = 1,label='CRUTEM4')
ax4.plot(x_bf98_CRUTEM4_aut,y_bf98_CRUTEM4_aut,color='b',linestyle='--')
ax4.plot(x_af98_CRUTEM4_aut,y_af98_CRUTEM4_aut,color='b',linestyle='--')

ax4.plot(NOAA_year,NOAA_aut,'k-',Markersize=4,linewidth = 1,label='NOAA')
ax4.plot(x_bf98_NOAA_aut,y_bf98_NOAA_aut,color='k',linestyle='--')
ax4.plot(x_af98_NOAA_aut,y_af98_NOAA_aut,color='k',linestyle='--')

ax4.plot(Berkely_Earth_year,Berkely_Earth_aut,'m-',Markersize=4,linewidth = 1,label='Berkley Earth')
ax4.plot(x_bf98_Berkely_Earth_aut,y_bf98_Berkely_Earth_aut,color='m',linestyle='--')
ax4.plot(x_af98_Berkely_Earth_aut,y_af98_Berkely_Earth_aut,color='m',linestyle='--')

ax4.plot(NASA_GISTEMP_year,NASA_GISTEMP_aut,'y-',Markersize=4,linewidth = 1,label='NASA GISTEMP')
ax4.plot(x_bf98_NASA_GISTEMP_aut,y_bf98_NASA_GISTEMP_aut,color='y',linestyle='--')
ax4.plot(x_af98_NASA_GISTEMP_aut,y_af98_NASA_GISTEMP_aut,color='y',linestyle='--')


ax4.set_xlim([1981,2015])
ax4.set_ylim([-1,2.1])
ax4.set_yticks([-0.5,0,0.5,1.0,1.5])
ax4.set_yticklabels([-0.5,0,0.5,1.0,1.5],fontproperties = font_tick)
ax4.set_ylabel('Autumn Tair ($^\circ$C)',fontproperties = font_label)
ax4.set_xlabel('Year',fontproperties = font_label)
ax4.fill_between([1998,2012],[2.1,2.2],[-1.5,-1.5],color = 'lightgrey',alpha = 0.5)
ax4.grid(color = 'lightgrey',linestyle = '--')
ax4.yaxis.tick_right()
ax4.yaxis.set_label_position("right")
ax4.text(1982,1.5,'d: Autumn',fontproperties = font_sub_title)
#plt.legend(frameon=False,loc=4, prop=font_tick)

############### plot temperature ###############
ax5 = plt.subplot(3,2,5)

ax5.plot(CRUTEM3_year,CRUTEM3_avg,'r-',Markersize=4,linewidth = 1,label='CRUTEM3')
ax5.plot(x_bf98_CRUTEM3_avg,y_bf98_CRUTEM3_avg,color='r',linestyle='--')
ax5.plot(x_af98_CRUTEM3_avg,y_af98_CRUTEM3_avg,color='r',linestyle='--')

ax5.plot(CRUTEM4_year,CRUTEM4_avg,'b-',Markersize=4,linewidth = 1,label='CRUTEM4')
ax5.plot(x_bf98_CRUTEM4_avg,y_bf98_CRUTEM4_avg,color='b',linestyle='--')
ax5.plot(x_af98_CRUTEM4_avg,y_af98_CRUTEM4_avg,color='b',linestyle='--')

ax5.plot(NOAA_year,NOAA_avg,'k-',Markersize=4,linewidth = 1,label='NOAA')
ax5.plot(x_bf98_NOAA_avg,y_bf98_NOAA_avg,color='k',linestyle='--')
ax5.plot(x_af98_NOAA_avg,y_af98_NOAA_avg,color='k',linestyle='--')

ax5.plot(Berkely_Earth_year,Berkely_Earth_avg,'m-',Markersize=4,linewidth = 1,label='Berkley Earth')
ax5.plot(x_bf98_Berkely_Earth_avg,y_bf98_Berkely_Earth_avg,color='m',linestyle='--')
ax5.plot(x_af98_Berkely_Earth_avg,y_af98_Berkely_Earth_avg,color='m',linestyle='--')

ax5.plot(NASA_GISTEMP_year,NASA_GISTEMP_avg,'y-',Markersize=4,linewidth = 1,label='NASA GISTEMP')
ax5.plot(x_bf98_NASA_GISTEMP_avg,y_bf98_NASA_GISTEMP_avg,color='y',linestyle='--')
ax5.plot(x_af98_NASA_GISTEMP_avg,y_af98_NASA_GISTEMP_avg,color='y',linestyle='--')

ax5.set_xlim([1981,2015])
ax5.set_ylim([-0.3,1.4])
ax5.set_yticks([0,0.3,0.6,0.9,1.2])
ax5.set_yticklabels([0,0.3,0.6,0.9,1.2],fontproperties = font_tick)
ax5.set_ylabel('Annual Tair ($^\circ$C)',fontproperties = font_label)
ax5.set_xlabel('Year',fontproperties = font_label)
ax5.fill_between([1998,2012],[2,2],[-0.5,-0.5],color = 'lightgrey',alpha = 0.5)
ax5.grid(color = 'lightgrey',linestyle = '--')
ax5.text(1982,1.1,'e: Annual',fontproperties = font_sub_title)
plt.legend(frameon=False,bbox_to_anchor=(1.1, 0.6), prop=font_tick,ncol=2)

###### txt_SOS_v1 ### 
if (intp_bf98_SOS_v1 >= 0):
    txt_SOS_v1 = "SOS_GIMMS: y=%4.3f*x + %4.1f P=%4.3f;" %(trend_bf98_SOS_v1, intp_bf98_SOS_v1, p_value_bf98_SOS_v1)
else:
    txt_SOS_v1 = "SOS_GIMMS: y=%4.3f*x - %4.1f P=%4.3f;" %(trend_bf98_SOS_v1, np.abs(intp_bf98_SOS_v1), p_value_bf98_SOS_v1)
    
if (intp_af98_SOS_v1 >= 0):
    txt_SOS_v1 = "%s  y=%4.3f*x + %4.1f P=%4.3f" %(txt_SOS_v1, trend_af98_SOS_v1, intp_af98_SOS_v1, p_value_af98_SOS_v1)
else:
    txt_SOS_v1 = "%s  y=%4.3f*x - %4.1f P=%4.3f" %(txt_SOS_v1, trend_af98_SOS_v1, np.abs(intp_af98_SOS_v1), p_value_af98_SOS_v1)
    
    
###### txt_EOS_v1 ###
if(intp_bf98_EOS_v1 >= 0):
    txt_EOS_v1 = "EOS_GIMMS: y=%4.3f*x + %4.1f P=%4.3f;" %(trend_bf98_EOS_v1, intp_bf98_EOS_v1, p_value_bf98_EOS_v1)
else:
    txt_EOS_v1 = "EOS_GIMMS: y=%4.3f*x - %4.1f P=%4.3f;" %(trend_bf98_EOS_v1, np.abs(intp_bf98_EOS_v1), p_value_bf98_EOS_v1)
    
if(intp_af98_EOS_v1 >= 0):    
    txt_EOS_v1 = "%s  y=%4.3f*x + %4.1f P=%4.3f" %(txt_EOS_v1,trend_af98_EOS_v1, intp_af98_EOS_v1, p_value_af98_EOS_v1)
else:
    txt_EOS_v1 = "%s  y=%4.3f*x - %4.1f P=%4.3f" %(txt_EOS_v1,trend_af98_EOS_v1, np.abs(intp_af98_EOS_v1), p_value_af98_EOS_v1)
    

###### txt_temp_spr_C4 ###
if(intp_bf98_CRUTEM4_spr >= 0): 
    txt_temp_spr_C4 = "CRUTEM4_spr: y=%4.3f*x + %4.1f P=%4.3f;" %(trend_bf98_CRUTEM4_spr, intp_bf98_CRUTEM4_spr, p_value_bf98_CRUTEM4_spr)
else:
    txt_temp_spr_C4 = "CRUTEM4_spr: y=%4.3f*x - %4.1f P=%4.3f;" %(trend_bf98_CRUTEM4_spr, np.abs(intp_bf98_CRUTEM4_spr), p_value_bf98_CRUTEM4_spr)
    
if(intp_af98_CRUTEM4_spr >= 0): 
    txt_temp_spr_C4 = "%s  y=%4.3f*x + %4.1f P=%4.3f" %(txt_temp_spr_C4, trend_af98_CRUTEM4_spr, intp_af98_CRUTEM4_spr, p_value_af98_CRUTEM4_spr)
else:
    txt_temp_spr_C4 = "%s  y=%4.3f*x - %4.1f P=%4.3f" %(txt_temp_spr_C4, trend_af98_CRUTEM4_spr, np.abs(intp_af98_CRUTEM4_spr), p_value_af98_CRUTEM4_spr)
    
###### txt_temp_spr_C3 ###
if(intp_bf98_CRUTEM3_spr >= 0):
    txt_temp_spr_C3 = "CRUTEM3_spr: y=%4.3f*x + %4.1f P=%4.3f;" %(trend_bf98_CRUTEM3_spr, intp_bf98_CRUTEM3_spr, p_value_bf98_CRUTEM3_spr)
else:
    txt_temp_spr_C3 = "CRUTEM3_spr: y=%4.3f*x - %4.1f P=%4.3f;" %(trend_bf98_CRUTEM3_spr, np.abs(intp_bf98_CRUTEM3_spr), p_value_bf98_CRUTEM3_spr)

if(intp_af98_CRUTEM3_spr >= 0):    
    txt_temp_spr_C3 = "%s  y=%4.3f*x + %4.1f P=%4.3f" %(txt_temp_spr_C3, trend_af98_CRUTEM3_spr, intp_af98_CRUTEM3_spr, p_value_af98_CRUTEM3_spr)
else:
    txt_temp_spr_C3 = "%s  y=%4.3f*x - %4.1f P=%4.3f" %(txt_temp_spr_C3, trend_af98_CRUTEM3_spr, np.abs(intp_af98_CRUTEM3_spr), p_value_af98_CRUTEM3_spr)

###### txt_temp_spr_NOAA ###
if(intp_bf98_NOAA_spr >= 0):
    txt_temp_spr_NOAA = "NOAA_spr: y=%4.3f*x + %4.1f P=%4.3f;" %(trend_bf98_NOAA_spr, intp_bf98_NOAA_spr, p_value_bf98_NOAA_spr)
else:
    txt_temp_spr_NOAA = "NOAA_spr: y=%4.3f*x - %4.1f P=%4.3f;" %(trend_bf98_NOAA_spr, np.abs(intp_bf98_NOAA_spr), p_value_bf98_NOAA_spr)

if(intp_af98_NOAA_spr >= 0):    
    txt_temp_spr_NOAA = "%s  y=%4.3f*x + %4.1f P=%4.3f" %(txt_temp_spr_NOAA, trend_af98_NOAA_spr, intp_af98_NOAA_spr, p_value_af98_NOAA_spr)
else:
    txt_temp_spr_NOAA = "%s  y=%4.3f*x - %4.1f P=%4.3f" %(txt_temp_spr_NOAA, trend_af98_NOAA_spr, np.abs(intp_af98_NOAA_spr), p_value_af98_NOAA_spr)

###### txt_temp_spr_Berkely_Earth ###
if(intp_bf98_Berkely_Earth_spr >= 0):
    txt_temp_spr_Berkely_Earth = "Berkley_Earth_spr: y=%4.3f*x + %4.1f P=%4.3f;" %(trend_bf98_Berkely_Earth_spr, intp_bf98_Berkely_Earth_spr, p_value_bf98_Berkely_Earth_spr)
else:
    txt_temp_spr_Berkely_Earth = "Berkley_Earth_spr: y=%4.3f*x - %4.1f P=%4.3f;" %(trend_bf98_Berkely_Earth_spr, np.abs(intp_bf98_Berkely_Earth_spr), p_value_bf98_Berkely_Earth_spr)

if(intp_af98_Berkely_Earth_spr >= 0):    
    txt_temp_spr_Berkely_Earth = "%s  y=%4.3f*x + %4.1f P=%4.3f" %(txt_temp_spr_Berkely_Earth, trend_af98_Berkely_Earth_spr, intp_af98_Berkely_Earth_spr, p_value_af98_Berkely_Earth_spr)
else:
    txt_temp_spr_Berkely_Earth = "%s  y=%4.3f*x - %4.1f P=%4.3f" %(txt_temp_spr_Berkely_Earth, trend_af98_Berkely_Earth_spr, np.abs(intp_af98_Berkely_Earth_spr), p_value_af98_Berkely_Earth_spr)
    
###### txt_temp_spr_NASA_GISTEMP ###
if(intp_bf98_Berkely_Earth_spr >= 0):
    txt_temp_spr_NASA_GISTEMP = "NASA_GISTEMP_spr: y=%4.3f*x + %4.1f P=%4.3f;" %(trend_bf98_NASA_GISTEMP_spr, intp_bf98_NASA_GISTEMP_spr, p_value_bf98_NASA_GISTEMP_spr)
else:
    txt_temp_spr_NASA_GISTEMP = "NASA_GISTEMP_spr: y=%4.3f*x - %4.1f P=%4.3f;" %(trend_bf98_NASA_GISTEMP_spr, np.abs(intp_bf98_NASA_GISTEMP_spr), p_value_bf98_NASA_GISTEMP_spr)

if(intp_af98_NASA_GISTEMP_spr >= 0):    
    txt_temp_spr_NASA_GISTEMP = "%s  y=%4.3f*x + %4.1f P=%4.3f" %(txt_temp_spr_NASA_GISTEMP, trend_af98_NASA_GISTEMP_spr, intp_af98_NASA_GISTEMP_spr, p_value_af98_NASA_GISTEMP_spr)
else:
    txt_temp_spr_NASA_GISTEMP = "%s  y=%4.3f*x - %4.1f P=%4.3f" %(txt_temp_spr_NASA_GISTEMP, trend_af98_NASA_GISTEMP_spr, np.abs(intp_af98_NASA_GISTEMP_spr), p_value_af98_NASA_GISTEMP_spr)
    
###### txt_temp_aut_C4 ###    
if(intp_bf98_CRUTEM4_aut >= 0):
    txt_temp_aut_C4 = "CRUTEM4_aut: y=%4.3f*x + %4.1f P=%4.3f;" %(trend_bf98_CRUTEM4_aut, intp_bf98_CRUTEM4_aut, p_value_bf98_CRUTEM4_aut)
else:
    txt_temp_aut_C4 = "CRUTEM4_aut: y=%4.3f*x - %4.1f P=%4.3f;" %(trend_bf98_CRUTEM4_aut, np.abs(intp_bf98_CRUTEM4_aut), p_value_bf98_CRUTEM4_aut)

if(intp_af98_CRUTEM4_aut >= 0):
    txt_temp_aut_C4 = "%s  y=%4.3f*x + %4.1f P=%4.3f" %(txt_temp_aut_C4, trend_af98_CRUTEM4_aut, intp_af98_CRUTEM4_aut, p_value_af98_CRUTEM4_aut)
else:
    txt_temp_aut_C4 = "%s  y=%4.3f*x - %4.1f P=%4.3f" %(txt_temp_aut_C4, trend_af98_CRUTEM4_aut, np.abs(intp_af98_CRUTEM4_aut), p_value_af98_CRUTEM4_aut)
    
###### txt_temp_aut_C3 ###
if(intp_bf98_CRUTEM3_aut >= 0):
    txt_temp_aut_C3 = "CRUTEM3_aut: y=%4.3f*x + %4.1f P=%4.3f;" %(trend_bf98_CRUTEM3_aut, intp_bf98_CRUTEM3_aut, p_value_bf98_CRUTEM3_aut)
else:
    txt_temp_aut_C3 = "CRUTEM3_aut: y=%4.3f*x - %4.1f P=%4.3f;" %(trend_bf98_CRUTEM3_aut, np.abs(intp_bf98_CRUTEM3_aut), p_value_bf98_CRUTEM3_aut)

if(intp_af98_CRUTEM3_aut >= 0):    
    txt_temp_aut_C3 = "%s  y=%4.3f*x + %4.1f P=%4.3f" %(txt_temp_aut_C3, trend_af98_CRUTEM3_aut, intp_af98_CRUTEM3_aut, p_value_af98_CRUTEM3_aut)
else:
    txt_temp_aut_C3 = "%s  y=%4.3f*x - %4.1f P=%4.3f" %(txt_temp_aut_C3, trend_af98_CRUTEM3_aut, np.abs(intp_af98_CRUTEM3_aut), p_value_af98_CRUTEM3_aut)
    

###### txt_temp_aut_NOAA ###
if(intp_bf98_NOAA_aut >= 0):
    txt_temp_aut_NOAA = "NOAA_aut: y=%4.3f*x + %4.1f P=%4.3f;" %(trend_bf98_NOAA_aut, intp_bf98_NOAA_aut, p_value_bf98_NOAA_aut)
else:
    txt_temp_aut_NOAA = "NOAA_aut: y=%4.3f*x - %4.1f P=%4.3f;" %(trend_bf98_NOAA_aut, np.abs(intp_bf98_NOAA_aut), p_value_bf98_NOAA_aut)

if(intp_af98_NOAA_aut >= 0):    
    txt_temp_aut_NOAA = "%s  y=%4.3f*x + %4.1f P=%4.3f" %(txt_temp_aut_NOAA, trend_af98_NOAA_aut, intp_af98_NOAA_aut, p_value_af98_NOAA_aut)
else:
    txt_temp_aut_NOAA = "%s  y=%4.3f*x - %4.1f P=%4.3f" %(txt_temp_aut_NOAA, trend_af98_NOAA_aut, np.abs(intp_af98_NOAA_aut), p_value_af98_NOAA_aut)

###### txt_temp_aut_Berkely_Earth ###
if(intp_bf98_Berkely_Earth_aut >= 0):
    txt_temp_aut_Berkely_Earth = "Berkley_Earth_aut: y=%4.3f*x + %4.1f P=%4.3f;" %(trend_bf98_Berkely_Earth_aut, intp_bf98_Berkely_Earth_aut, p_value_bf98_Berkely_Earth_aut)
else:
    txt_temp_aut_Berkely_Earth = "Berkley_Earth_aut: y=%4.3f*x - %4.1f P=%4.3f;" %(trend_bf98_Berkely_Earth_aut, np.abs(intp_bf98_Berkely_Earth_aut), p_value_bf98_Berkely_Earth_aut)

if(intp_af98_Berkely_Earth_aut >= 0):    
    txt_temp_aut_Berkely_Earth = "%s  y=%4.3f*x + %4.1f P=%4.3f" %(txt_temp_aut_Berkely_Earth, trend_af98_Berkely_Earth_aut, intp_af98_Berkely_Earth_aut, p_value_af98_Berkely_Earth_aut)
else:
    txt_temp_aut_Berkely_Earth = "%s  y=%4.3f*x - %4.1f P=%4.3f" %(txt_temp_aut_Berkely_Earth, trend_af98_Berkely_Earth_aut, np.abs(intp_af98_Berkely_Earth_aut), p_value_af98_Berkely_Earth_aut)
    
###### txt_temp_aut_NASA_GISTEMP ###
if(intp_bf98_Berkely_Earth_aut >= 0):
    txt_temp_aut_NASA_GISTEMP = "NASA_GISTEMP_aut: y=%4.3f*x + %4.1f P=%4.3f;" %(trend_bf98_NASA_GISTEMP_aut, intp_bf98_NASA_GISTEMP_aut, p_value_bf98_NASA_GISTEMP_aut)
else:
    txt_temp_aut_NASA_GISTEMP = "NASA_GISTEMP_aut: y=%4.3f*x - %4.1f P=%4.3f;" %(trend_bf98_NASA_GISTEMP_aut, np.abs(intp_bf98_NASA_GISTEMP_aut), p_value_bf98_NASA_GISTEMP_aut)

if(intp_af98_NASA_GISTEMP_aut >= 0):    
    txt_temp_aut_NASA_GISTEMP_Earth = "%s  y=%4.3f*x + %4.1f P=%4.3f" %(txt_temp_aut_NASA_GISTEMP, trend_af98_NASA_GISTEMP_aut, intp_af98_NASA_GISTEMP_aut, p_value_af98_NASA_GISTEMP_aut)
else:
    txt_temp_aut_NASA_GISTEMP = "%s  y=%4.3f*x - %4.1f P=%4.3f" %(txt_temp_aut_NASA_GISTEMP, trend_af98_NASA_GISTEMP_aut, np.abs(intp_af98_NASA_GISTEMP_aut), p_value_af98_NASA_GISTEMP_aut)

    
###### txt_temp_year_C4 ###
if(intp_bf98_CRUTEM4_avg >= 0):   
    txt_temp_year_C4 = "CRUTEM4_year: y=%4.3f*x + %4.1f P=%4.3f;" %(trend_bf98_CRUTEM4_avg, intp_bf98_CRUTEM4_avg, p_value_bf98_CRUTEM4_avg)
else:
    txt_temp_year_C4 = "CRUTEM4_year: y=%4.3f*x - %4.1f P=%4.3f;" %(trend_bf98_CRUTEM4_avg, np.abs(intp_bf98_CRUTEM4_avg), p_value_bf98_CRUTEM4_avg)
if(intp_af98_CRUTEM4_avg >= 0):
    txt_temp_year_C4 = "%s  y=%4.3f*x + %4.1f P=%4.3f" %(txt_temp_year_C4, trend_af98_CRUTEM4_avg, intp_af98_CRUTEM4_avg, p_value_af98_CRUTEM4_avg)
else:
    txt_temp_year_C4 = "%s  y=%4.3f*x - %4.1f P=%4.3f" %(txt_temp_year_C4, trend_af98_CRUTEM4_avg, np.abs(intp_af98_CRUTEM4_avg), p_value_af98_CRUTEM4_avg)
    

###### txt_temp_year_C3 ###
if(intp_bf98_CRUTEM3_avg >= 0):  
    txt_temp_year_C3 = "CRUTEM3_year: y=%4.3f*x + %4.1f P=%4.3f;" %(trend_bf98_CRUTEM3_avg, intp_bf98_CRUTEM3_avg, p_value_bf98_CRUTEM3_avg)
else:
    txt_temp_year_C3 = "CRUTEM3_year: y=%4.3f*x - %4.1f P=%4.3f;" %(trend_bf98_CRUTEM3_avg, np.abs(intp_bf98_CRUTEM3_avg), p_value_bf98_CRUTEM3_avg)
    
if(intp_af98_CRUTEM3_avg >= 0):  
    txt_temp_year_C3 = "%s  y=%4.3f*x + %4.1f P=%4.3f" %(txt_temp_year_C3,trend_af98_CRUTEM3_avg, intp_af98_CRUTEM3_avg, p_value_af98_CRUTEM3_avg)
else:
    txt_temp_year_C3 = "%s  y=%4.3f*x - %4.1f P=%4.3f" %(txt_temp_year_C3,trend_af98_CRUTEM3_avg, np.abs(intp_af98_CRUTEM3_avg), p_value_af98_CRUTEM3_avg)


###### txt_temp_year_NOAA ###
if(intp_bf98_NOAA_avg >= 0):
    txt_temp_year_NOAA = "NOAA_year: y=%4.3f*x + %4.1f P=%4.3f;" %(trend_bf98_NOAA_avg, intp_bf98_NOAA_avg, p_value_bf98_NOAA_avg)
else:
    txt_temp_year_NOAA = "NOAA_year: y=%4.3f*x - %4.1f P=%4.3f;" %(trend_bf98_NOAA_avg, np.abs(intp_bf98_NOAA_avg), p_value_bf98_NOAA_avg)

if(intp_af98_NOAA_avg >= 0):    
    txt_temp_year_NOAA = "%s  y=%4.3f*x + %4.1f P=%4.3f" %(txt_temp_year_NOAA, trend_af98_NOAA_avg, intp_af98_NOAA_avg, p_value_af98_NOAA_avg)
else:
    txt_temp_year_NOAA = "%s  y=%4.3f*x - %4.1f P=%4.3f" %(txt_temp_year_NOAA, trend_af98_NOAA_avg, np.abs(intp_af98_NOAA_avg), p_value_af98_NOAA_avg)

###### txt_temp_year_Berkely_Earth ###
if(intp_bf98_Berkely_Earth_avg >= 0):
    txt_temp_year_Berkely_Earth = "Berkley_Earth_year: y=%4.3f*x + %4.1f P=%4.3f;" %(trend_bf98_Berkely_Earth_avg, intp_bf98_Berkely_Earth_avg, p_value_bf98_Berkely_Earth_avg)
else:
    txt_temp_year_Berkely_Earth = "Berkley_Earth_year: y=%4.3f*x - %4.1f P=%4.3f;" %(trend_bf98_Berkely_Earth_avg, np.abs(intp_bf98_Berkely_Earth_avg), p_value_bf98_Berkely_Earth_avg)

if(intp_af98_Berkely_Earth_avg >= 0):    
    txt_temp_year_Berkely_Earth = "%s  y=%4.3f*x + %4.1f P=%4.3f" %(txt_temp_year_Berkely_Earth, trend_af98_Berkely_Earth_avg, intp_af98_Berkely_Earth_avg, p_value_af98_Berkely_Earth_avg)
else:
    txt_temp_year_Berkely_Earth = "%s  y=%4.3f*x - %4.1f P=%4.3f" %(txt_temp_year_Berkely_Earth, trend_af98_Berkely_Earth_avg, np.abs(intp_af98_Berkely_Earth_avg), p_value_af98_Berkely_Earth_avg)
    
###### txt_temp_year_NASA_GISTEMP ###
if(intp_bf98_NASA_GISTEMP_avg >= 0):
    txt_temp_year_NASA_GISTEMP = "NASA_GISTEMP_year: y=%4.3f*x + %4.1f P=%4.3f;" %(trend_bf98_NASA_GISTEMP_avg, intp_bf98_NASA_GISTEMP_avg, p_value_bf98_NASA_GISTEMP_avg)
else:
    txt_temp_year_NASA_GISTEMP = "NASA_GISTEMP_year: y=%4.3f*x - %4.1f P=%4.3f;" %(trend_bf98_NASA_GISTEMP_avg, np.abs(intp_bf98_NASA_GISTEMP_avg), p_value_bf98_NASA_GISTEMP_avg)

if(intp_af98_NASA_GISTEMP_avg >= 0):    
    txt_temp_year_NASA_GISTEMP = "%s  y=%4.3f*x + %4.1f P=%4.3f" %(txt_temp_year_NASA_GISTEMP, trend_af98_NASA_GISTEMP_avg, intp_af98_NASA_GISTEMP_avg, p_value_af98_NASA_GISTEMP_avg)
else:
    txt_temp_year_NASA_GISTEMP = "%s  y=%4.3f*x - %4.1f P=%4.3f" %(txt_temp_year_NASA_GISTEMP, trend_af98_NASA_GISTEMP_avg, np.abs(intp_af98_NASA_GISTEMP_avg), p_value_af98_NASA_GISTEMP_avg)

    
'''
txt_headline = "                         Before 1998             ;             After 1998"
ax5.text(2016,0.85,txt_headline,fontsize = 9,color='k')
y_loc= 0.7
ax5.text(2016,y_loc,txt_SOS_v1,fontsize = 9,color='b')
#y_loc= y_loc - 0.15
#ax5.text(2016,y_loc,txt_SOS_v0,fontsize = 9,color='r')
y_loc= y_loc - 0.15
ax5.text(2016,y_loc,txt_EOS_v1,fontsize = 9,color='b')
#y_loc= y_loc - 0.15
#ax5.text(2016,y_loc,txt_EOS_v0,fontsize = 9,color='r')
y_loc= y_loc - 0.15
ax5.text(2016,y_loc,txt_temp_spr_C4,fontsize = 9,color='b')
y_loc= y_loc - 0.15
ax5.text(2016,y_loc,txt_temp_spr_C3,fontsize = 9,color='r')
y_loc= y_loc - 0.15
ax5.text(2016,y_loc,txt_temp_aut_C4,fontsize = 9,color='b')
y_loc= y_loc - 0.15
ax5.text(2016,y_loc,txt_temp_aut_C3,fontsize = 9,color='r')
y_loc= y_loc - 0.15
ax5.text(2016,y_loc,txt_temp_year_C4,fontsize = 9,color='b')
y_loc= y_loc - 0.15
ax5.text(2016,y_loc,txt_temp_year_C3,fontsize = 9,color='r')
'''

fig.tight_layout()
plt.subplots_adjust(left=0.05, bottom=0.05, top=0.95, right=0.95, wspace=0, hspace=0)  
plt.savefig('output_figures/Fig1_gimms_phen_trend_20190331_multiple_TA_datasets.png',format='png',dpi=300,bbox_inches='tight')
plt.show()


