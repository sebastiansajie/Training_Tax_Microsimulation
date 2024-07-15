# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import pandas as pd
import numpy as np
import sys
#sys.path.insert(0, 'C:/Users/wb305167/OneDrive - WBG/python_latest/Tax-Revenue-Analysis')
from stata_python import *

df = pd.read_excel ("/Users/windi/Documents/SPRING 2024/Applied Tax Policy/Inequality/Lorenz_Curve_Worksheet_test.xlsx", sheet_name = "Original", index_col = None, header=0)



df ["cum_weight"] = np.cumsum(df["Weight"])
df ["cum_income"] = np.cumsum(df["Income"])
sum_weight = df["Weight"].sum()
df["cum_wt_percent"] = df["cum_weight"]/sum_weight
df ["cum_weight_shift"] = df["cum_weight"].shift(1)
sum_inc = df["Income"].sum()
df["cum_inc_percent"] = df ["cum_income"]/sum_inc
df ["cum_inc_shift"] = df["cum_income"].shift(1)