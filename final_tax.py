#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 28 12:47:07 2024

@author: windi
"""
import math
import copy
import pandas as pd
import numpy as np
from taxcalc.decorators import iterate_jit

"Calculation for Final Tax on INTEREST OF DEPOSIT, SAVINGS, DISCOUNT ON BANK INDONESIA CERTIFICATES, STATE SECURITIES"
@iterate_jit(nopython=True)
def cal_finaltax_InterestSaving(rate_InterestSaving, JNS_SPT_NUM, JML_PH_BRUTO_DISKONTO_SBI, 
            finaltax_InterestSaving_1770SS, finaltax_InterestSaving_1770S, finaltax_InterestSaving_1770, 
            finaltax_InterestSaving):

    finaltax_InterestSaving = rate_InterestSaving * max(0, JML_PH_BRUTO_DISKONTO_SBI) 
    
    if (JNS_SPT_NUM == 0):
      finaltax_InterestSaving_1770SS = finaltax_InterestSaving
      finaltax_InterestSaving_1770S = 0
      finaltax_InterestSaving_1770 = 0
    elif (JNS_SPT_NUM == 1):
      finaltax_InterestSaving_1770S = finaltax_InterestSaving
      finaltax_InterestSaving_1770 = 0
      finaltax_InterestSaving_1770SS = 0
    else:
      finaltax_InterestSaving_1770 = finaltax_InterestSaving
      finaltax_InterestSaving_1770S = 0
      finaltax_InterestSaving_1770SS = 0               
    return (finaltax_InterestSaving_1770SS, finaltax_InterestSaving_1770S, finaltax_InterestSaving_1770, 
            finaltax_InterestSaving)
