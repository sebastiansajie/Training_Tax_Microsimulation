"""
pitaxcalc-demo functions that calculate personal income tax liability.
"""
# CODING-STYLE CHECKS:
# pycodestyle functions.py
# pylint --disable=locally-disabled functions.py

import math
import copy
import numpy as np
from taxcalc.decorators import iterate_jit

"Calculation for Assesible Income"

@iterate_jit(nopython=True)
def cal_Assessible_Income(EmpIncCages10,BussIncCages20,InvestIncomeCages30,
                          OtherIncomeCages40, Calculated_Assessible_Income):
    Calculated_Assessible_Income = EmpIncCages10+BussIncCages20+InvestIncomeCages30+OtherIncomeCages40    
    return Calculated_Assessible_Income

"Calculation for Total Deductions"

@iterate_jit(nopython=True)
def cal_total_deductions(Calculated_Total_Deductions):
    Calculated_Total_Deductions = 0   
    return Calculated_Total_Deductions

"Calculation for Taxable Income"

@iterate_jit(nopython=True)
def cal_taxable_income(Calculated_Assessible_Income, Calculated_Total_Deductions, Calculated_Taxable_Income):
    Calculated_Taxable_Income = Calculated_Assessible_Income - Calculated_Total_Deductions
    return Calculated_Taxable_Income

"Calculation for PIT"
@iterate_jit(nopython=True)
def cal_pit(rate1, rate2, rate3, rate4, tbrk1, tbrk2, tbrk3, Calculated_Taxable_Income, pitax):
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
    inc = Calculated_Taxable_Income
    if (inc <= tbrk1):
        pitax = rate1 * (inc - 0)
    elif inc <= tbrk2:
         pitax = (rate1 * (tbrk1 - 0)) + (rate2 * (inc - tbrk1))
    elif inc <= tbrk3:
        pitax = (rate1 * (tbrk1 - 0)) + (rate2 * (tbrk2 - tbrk1)) + (rate3 * (inc - tbrk2))
    else:
        pitax = (rate1 * (tbrk1 - 0)) + (rate2 * (tbrk2 - tbrk1)) + (rate3 * (tbrk3 - tbrk2)) + (rate4 * (inc - tbrk3))
    return (pitax)
    
    
    
    
    
    
    
    
    
    