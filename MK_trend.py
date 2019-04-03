# -*- coding: utf-8 -*-
"""
Created on Thu May 11 16:21:46 2017

@author: wxf
"""

from __future__ import division
import numpy as np
from scipy import stats
from scipy.stats import norm

def mmk_trend(y,x, alpha = 0.05):
    """
    Performs the Modified Mann-Kendall test to check if there is any trend present.
    Based on Mann-Kendall test code by Sat Kumar Tomer. Modified to account for autocorrelation (Hamed and Rao 1998)
    
    Input:
        v: a vector
        alpha: significance level
        (example: if alpha is 0.05, 95% confidence)
    
    Output:
        h: True (if trend is present) or False (if trend is absent)
        trend: the slope as the median of all slopes between paired values (Sen, 1968)
        p: p value of the significance test
        z: normalised test statistic
    """
    
    n = y.shape[0]
    
    # calculate s
    s = 0
    for i in xrange(n-1):
        for j in xrange(i+1,n):
            s += np.sign(y[j] - y[i])
            
    # calculate variance of s
    v_uniq = np.unique(y)
    g = v_uniq.shape[0]
    if n==g: # no tie
        var_s = n*(n-1)*(2*n+5)/18
    else: # tied groups
        tp = np.zeros(g)
        for i in xrange(g):
            tp[i] = sum(v_uniq[i] == y)
        var_s = (n*(n-1)*(2*n+5) + np.sum(tp*(tp-1)*(2*tp+5)))/18
        
    # detrend
    t = stats.theilslopes(y,x,1-alpha)
    xx = range(1,n+1)
    v_detrend = y - np.multiply(xx,t[0])
    
    # account for autocorrelation
    I = np.argsort(v_detrend)
    d = n * np.ones(2 * n - 1)
    acf = (np.correlate(I, I, 'full') / d)[n - 1:]
    acf = acf / acf[0]
    interval = stats.norm.ppf(1 - alpha / 2) / np.sqrt(n)
    u_bound = 0 + interval;
    l_bound = 0 - interval;
    
    sni = 0
    for i in xrange(1,n-1):
        if (acf[i] > u_bound or acf[i] < l_bound):
            sni += (n-i) * (n-i-1) * (n-i-2) * acf[i]
    n_ns = 1 + (2 / (n * (n-1) * (n-2))) * sni
    v_s = var_s * n_ns
    
    # calculate z (normalised test statistic)    
    if s > 0:
        z = (s - 1)/np.sqrt(v_s)
    elif s == 0:
            z = 0
    elif s < 0:
        z = (s + 1)/np.sqrt(v_s)
        
    # significance
    p = 2*(1-stats.norm.cdf(abs(z))) # two tail test
    h = abs(z) > stats.norm.ppf(1-alpha/2)
    
    # trend
    if h:
        trend = t[0]
        intp = t[1]
    else:
        trend = 0
        intp = 0
    
    return h, trend, intp, p, z


def mk_trend(y,x, alpha=0.05):
    """
    This function is derived from code originally posted by Sat Kumar Tomer
    (satkumartomer@gmail.com)
    See also: http://vsp.pnnl.gov/help/Vsample/Design_Trend_Mann_Kendall.htm
    The purpose of the Mann-Kendall (MK) test (Mann 1945, Kendall 1975, Gilbert
    1987) is to statistically assess if there is a monotonic upward or downward
    trend of the variable of interest over time. A monotonic upward (downward)
    trend means that the variable consistently increases (decreases) through
    time, but the trend may or may not be linear. The MK test can be used in
    place of a parametric linear regression analysis, which can be used to test
    if the slope of the estimated linear regression line is different from
    zero. The regression analysis requires that the residuals from the fitted
    regression line be normally distributed; an assumption not required by the
    MK test, that is, the MK test is a non-parametric (distribution-free) test.
    Hirsch, Slack and Smith (1982, page 107) indicate that the MK test is best
    viewed as an exploratory analysis and is most appropriately used to
    identify stations where changes are significant or of large magnitude and
    to quantify these findings.
    Input:
        x:   a vector of data
        alpha: significance level (0.05 default)
    Output:
        trend: tells the trend (increasing, decreasing or no trend)
        h: True (if trend is present) or False (if trend is absence)
        p: p value of the significance test
        z: normalized test statistics
    Examples
    --------
      >>> x = np.random.rand(100)
      >>> trend,h,p,z = mk_test(x,0.05)
    """
    n = len(y)

    # calculate S
    s = 0
    for k in range(n-1):
        for j in range(k+1, n):
            s += np.sign(y[j] - y[k])

    # calculate the unique data
    unique_y = np.unique(y)
    g = len(unique_y)

    # calculate the var(s)
    if n == g:  # there is no tie
        var_s = (n*(n-1)*(2*n+5))/18
    else:  # there are some ties in data
        tp = np.zeros(unique_y.shape)
        for i in range(len(unique_y)):
            tp[i] = sum(y == unique_y[i])
        var_s = (n*(n-1)*(2*n+5) - np.sum(tp*(tp-1)*(2*tp+5)))/18

    if s > 0:
        z = (s - 1)/np.sqrt(var_s)
    elif s == 0:
            z = 0
    elif s < 0:
        z = (s + 1)/np.sqrt(var_s)

    # calculate the p_value
    p = 2*(1-norm.cdf(abs(z)))  # two tail test
    h = abs(z) > norm.ppf(1-alpha/2)
    
    t = stats.theilslopes(y,x,1-alpha)

    
    trend = t[0]
    intp = t[1]
    

    return h, trend, intp, p, z