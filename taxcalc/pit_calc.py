#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 19 15:23:44 2024

@author: windi
"""
import pandas as pd
import numpy as np

def cal_pit(row):
    """
    Compute tax liability given the progressive tax rate schedule specified
    by the (marginal tax) rate* and (upper tax bracket) brk* parameters and
    given taxable income (taxinc)
    """
    # subtract TI_special_rates from TTI to get Aggregate_Income, which is
    # the portion of TTI that is taxed at normal rates
    """
    taxinc = tax_base_w  
    
    pit_w = (rate1 * min(taxinc, tbrk1) +
                    rate2 * min(tbrk2 - tbrk1, max(0., taxinc - tbrk1)) +
                    rate3 * min(tbrk3 - tbrk2, max(0., taxinc - tbrk2)) +
                    rate4 * max(0., taxinc - tbrk3))
        
    return (pit_w)
    """
    rate=[0.05, 0.15, 0.25, 0.30, 0.30, 0.30]
    tbrk=[50000000, 250000000, 500000000, 1e99, 2e99, 3e99]
    
    inc = row["JML_PH_NETO"]
    
    if (inc <= tbrk[0]):
        pitax = rate[0] * (inc - 0)
    elif inc <= tbrk[1]:
         pitax = (rate[0] * (tbrk[0] - 0)) + (rate[1] * (inc - tbrk[0]))
    elif inc <= tbrk[2]:
        pitax = (rate[0] * (tbrk[0] - 0)) + (rate[1] * (tbrk[1] - tbrk[0])) + (rate[2] * (inc - tbrk[1]))
    elif inc <= tbrk[3]:
        pitax = (rate[0] * (tbrk[0] - 0)) + (rate[1] * (tbrk[1] - tbrk[0])) + (rate[2] * (tbrk[2] - tbrk[1])) + (rate[3] * (inc - tbrk[2]))
    else:
        pitax = (rate[0] * (tbrk[0] - 0)) + (rate[1] * (tbrk[1] - tbrk[0])) + (rate[2] * (tbrk[2] - tbrk[1])) + (rate[3] * (tbrk[3] - tbrk[2])) + (rate[4] * (inc - tbrk[3]))
    return (pitax)


df = pd.read_csv("taxcalc/pit21.csv")

df['pitax'] = df.apply(cal_pit, axis=1)
