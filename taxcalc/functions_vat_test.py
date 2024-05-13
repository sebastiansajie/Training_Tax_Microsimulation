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

"Calculation for Other Consumption"

@iterate_jit(nopython=True)
def cal_other_consumption(TOT_EXP,M_EXP_FOOD,M_EXP_INTOXICANTS,
                          M_EXP_POWER_N_FUEL, OTHER_CONSUMPTION):
    OTHER_CONSUMPTION = TOT_EXP - M_EXP_FOOD - M_EXP_INTOXICANTS - M_EXP_POWER_N_FUEL
    return OTHER_CONSUMPTION


"Calculation for VAT"
@iterate_jit(nopython=True)
def cal_vat(rate_FOOD, rate_INTOXICANTS, rate_ENERGY, rate_OTHER_CONS, M_EXP_FOOD, M_EXP_INTOXICANTS, M_EXP_POWER_N_FUEL, OTHER_CONSUMPTION, vatax):
    """
    Compute tax liability given the progressive tax rate schedule specified
    by the (marginal tax) rate* and (upper tax bracket) brk* parameters and
    given taxable income (taxinc)
    """
    vatax = (rate_FOOD * M_EXP_FOOD + rate_INTOXICANTS * M_EXP_INTOXICANTS + rate_ENERGY * M_EXP_POWER_N_FUEL + rate_OTHER_CONS * OTHER_CONSUMPTION)
    return (vatax)
    
    
    
    
    
    
    
    
    
    