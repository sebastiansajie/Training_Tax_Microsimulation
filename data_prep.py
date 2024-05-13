#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 15 15:11:31 2024

@author: windi
"""

# insert into the file
#import sys
#sys.path.insert(0, 'C:/Users/wb305167/OneDrive - WBG/python_latest/Tax-Revenue-Analysis')
#from stata_python import *

import pandas as pd
import numpy as np
from stata_python import *

#'/Users/windi/Documents/SPRING 2024/Applied Tax Policy/Data/in_class_data/stata_python.py'

"""
#reading csv datasets with pipe ("|") delimited
df1 = pd.read_csv("o2122p/_op21_01.csv", sep= "|", on_bad_lines="warn")
df2 = pd.read_csv("o2122p/_op21_23.csv", sep= "|", on_bad_lines="warn")
df3 = pd.read_csv("o2122p/_op21_45.csv", sep= "|", on_bad_lines="warn")
df4 = pd.read_csv("o2122p/_op21_67.csv", sep= "|", on_bad_lines="warn")
df5 = pd.read_csv("o2122p/_op21_89.csv", sep= "|", on_bad_lines="warn")

#concatinating cvs datasets
df_all = pd.concat([df1, df2, df3, df4, df5], axis = 0)

#sorting total income
df_all = df_all.sort_values(by=['JML_PH_NETO'])

#separate JML_PH_NETO = 0 
df_0 = df_all[df_all['JML_PH_NETO'] <= 0]

#separate JML_PH_NETO not 0
df = df_all[df_all['JML_PH_NETO'] > 0] 

#writing the concatinated and sorted file
#df.to_csv("o2122p/pit21.csv", index = False)

#creating income orders
#df = df.reset_index()

# allocate the income into 10 bins
df['bin'] = pd.qcut(df['JML_PH_NETO'], 10, labels=False)
df['weight']=1

# bin_ratio is the fraction of the number of records selected in each bin
# 1/20,..., 1/10, 1/5, 1/1
bin_ratio=[20,20,20,20,20,20,20,10,5,1]
frames=[]
df_f={}
for i in range(len(bin_ratio)):
    # find out the size of each bin
    bin_size=len(df[df['bin']==i])//bin_ratio[i]
    # draw a random sample from each bin
    df_f[i]=df[df['bin']==i].sample(n=bin_size)
    df_f[i]['weight'] = bin_ratio[i]
    frames=frames+[df_f[i]]

df_sample = pd.concat(frames)
df_sample.to_csv('pit_sample_2021.csv')


#verify and comparing sample with the population
varlist = ['JML_PH_NETO', 'JML_PPH_TERUTANG']

total_weight_sample = df_sample['weight'].sum()
total_weight_population = df_sample['weight'].sum()

#comparing the statistic of the population and sample
for var in varlist:
    df_sample['weighted_'+var] = df_sample[var]*df_sample['weight']
    sample_sum = df_sample['weighted_'+var].sum()
    population_sum = df[var].sum()
    print("            Sample Sum for ", var, " = ", sample_sum)
    print("        Population Sum for ", var, " = ", population_sum)
    print(" Sampling Error for Sum(%) ", var, " = ", "{:.2%}".format((population_sum-sample_sum)/population_sum))
    sample_mean = sample_sum/total_weight_sample
    population_mean = population_sum/total_weight_population
    print("           Sample Mean for ", var, " = ", sample_mean)
    print("       Population Mean for ", var, " = ", population_mean)
    print("Sampling Error for Mean(%) ", var, " = ", "{:.2%}".format((population_mean-sample_mean)/population_mean))    


#merging sample files and repeat for all appendixes files

df_sample_big = pd.read_csv("pit_sample_2021.csv")
df_sample_big = df_sample_big.drop('Unnamed: 0', axis=1)

# Make small sample for verification
df_sample = df_sample_big.sample(n=100000)
df_sample.to_csv('pit_sample_2021_small.csv', index=False)
"""

#df_sample = pd.read_csv("pit_sample_2021_small.csv")

df_sample = pd.read_csv("pit_sample_2021.csv")
df_sample = df_sample.drop('Unnamed: 0', axis=1)
df_sample = df_sample.set_index('NPWP')

#FINAL INCOME
df_final1 = pd.read_csv("s2122p/SPT_OP_FINAL21_01.csv", sep= "|", on_bad_lines="warn")
df_final1 = df_final1.drop(['DW_PROCESS_DATE', 'ID_MS_TH_PJK',
                                'ID_SPT', 'ID_SPT_FIELD', 'ID_TEMPLATE',
                                'ISVALID', 'JNS_SPT', 'KPPADM', 'REV_NO',
                                'TGL_SPT_TT'], axis=1)
df_final1['JML_PPH_TERUTANG_FINAL']  = (df_final1['JML_PPH_TERUTANG_DISKONTO_SBI']
                                        +df_final1['JML_PPH_TERUTANG_OBLIGASI']
                                        +df_final1['JML_PPH_TERUTANG_PENJUALAN_SAHAM']
                                        +df_final1['JML_PPH_TERUTANG_HADIAN_UNDIAN']
                                        +df_final1['JML_PPH_TERUTANG_PESANGON']
                                        +df_final1['JML_PPH_TERUTANG_HONORARIUM_APBN']
                                        +df_final1['JML_PPH_TERUTANG_PHBTB']
                                        +df_final1['JML_PPH_TERUTANG_BANGUN_GUNA_SERAH']
                                        +df_final1['JML_PPH_TERUTANG_SEWA_TANAH_BANGUNAN']
                                        +df_final1['JML_PPH_TERUTANG_USAHA_JASKON']
                                        +df_final1['JML_PPH_TERUTANG_DEALER_BBM']
                                        +df_final1['JML_PPH_TERUTANG_BUNGA_SIMPANAN_KOPERASI']
                                        +df_final1['JML_PPH_TERUTANG_TRANSAKSI_DERIVATIF']
                                        +df_final1['JML_PPH_TERUTANG_DIVIDEN']
                                        +df_final1['JML_PPH_TERUTANG_PH_ISTRI']
                                        +df_final1['JML_PPH_TERUTANG_LAINNYA'])

df_final1 = df_final1.drop_duplicates(subset=['NPWP'], keep='last')
df_final1 = df_final1.set_index('NPWP')
df_sample = df_sample.join(df_final1,how='left')
sum_terutang = df_sample['JML_PPH_TERUTANG_FINAL'].sum()
print('sum terutang: ', sum_terutang/1e9)

#df_sample = df_sample.drop('_merge', axis=1)
df_final2 = pd.read_csv("s2122p/SPT_OP_FINAL21_23.csv", sep= "|", on_bad_lines="warn")
df_final2 = df_final2.drop(['DW_PROCESS_DATE', 'ID_MS_TH_PJK',
                                'ID_SPT', 'ID_SPT_FIELD', 'ID_TEMPLATE',
                                'ISVALID', 'JNS_SPT', 'KPPADM', 'REV_NO',
                                'TGL_SPT_TT'], axis=1)
df_final2['JML_PPH_TERUTANG_FINAL']  = (df_final2['JML_PPH_TERUTANG_DISKONTO_SBI']
                                        +df_final2['JML_PPH_TERUTANG_OBLIGASI']
                                        +df_final2['JML_PPH_TERUTANG_PENJUALAN_SAHAM']
                                        +df_final2['JML_PPH_TERUTANG_HADIAN_UNDIAN']
                                        +df_final2['JML_PPH_TERUTANG_PESANGON']
                                        +df_final2['JML_PPH_TERUTANG_HONORARIUM_APBN']
                                        +df_final2['JML_PPH_TERUTANG_PHBTB']
                                        +df_final2['JML_PPH_TERUTANG_BANGUN_GUNA_SERAH']
                                        +df_final2['JML_PPH_TERUTANG_SEWA_TANAH_BANGUNAN']
                                        +df_final2['JML_PPH_TERUTANG_USAHA_JASKON']
                                        +df_final2['JML_PPH_TERUTANG_DEALER_BBM']
                                        +df_final2['JML_PPH_TERUTANG_BUNGA_SIMPANAN_KOPERASI']
                                        +df_final2['JML_PPH_TERUTANG_TRANSAKSI_DERIVATIF']
                                        +df_final2['JML_PPH_TERUTANG_DIVIDEN']
                                        +df_final2['JML_PPH_TERUTANG_PH_ISTRI']
                                        +df_final2['JML_PPH_TERUTANG_LAINNYA'])
df_final2 = df_final2.drop_duplicates(subset=['NPWP'], keep='last')
df_final2 = df_final2.set_index('NPWP')
df_sample.update(df_final2)
sum_terutang = df_sample['JML_PPH_TERUTANG_FINAL'].sum()
print('sum terutang: ', sum_terutang/1e9)

df_final3 = pd.read_csv("s2122p/SPT_OP_FINAL21_45.csv", sep= "|", on_bad_lines="warn")
df_final3 = df_final3.drop(['DW_PROCESS_DATE', 'ID_MS_TH_PJK',
                                'ID_SPT', 'ID_SPT_FIELD', 'ID_TEMPLATE',
                                'ISVALID', 'JNS_SPT', 'KPPADM', 'REV_NO',
                                'TGL_SPT_TT'], axis=1)
df_final3['JML_PPH_TERUTANG_FINAL']  = (df_final3['JML_PPH_TERUTANG_DISKONTO_SBI']
                                        +df_final3['JML_PPH_TERUTANG_OBLIGASI']
                                        +df_final3['JML_PPH_TERUTANG_PENJUALAN_SAHAM']
                                        +df_final3['JML_PPH_TERUTANG_HADIAN_UNDIAN']
                                        +df_final3['JML_PPH_TERUTANG_PESANGON']
                                        +df_final3['JML_PPH_TERUTANG_HONORARIUM_APBN']
                                        +df_final3['JML_PPH_TERUTANG_PHBTB']
                                        +df_final3['JML_PPH_TERUTANG_BANGUN_GUNA_SERAH']
                                        +df_final3['JML_PPH_TERUTANG_SEWA_TANAH_BANGUNAN']
                                        +df_final3['JML_PPH_TERUTANG_USAHA_JASKON']
                                        +df_final3['JML_PPH_TERUTANG_DEALER_BBM']
                                        +df_final3['JML_PPH_TERUTANG_BUNGA_SIMPANAN_KOPERASI']
                                        +df_final3['JML_PPH_TERUTANG_TRANSAKSI_DERIVATIF']
                                        +df_final3['JML_PPH_TERUTANG_DIVIDEN']
                                        +df_final3['JML_PPH_TERUTANG_PH_ISTRI']
                                        +df_final3['JML_PPH_TERUTANG_LAINNYA'])
df_final3 = df_final3.drop_duplicates(subset=['NPWP'], keep='last')
df_final3 = df_final3.set_index('NPWP')
df_sample.update(df_final3)
sum_terutang = df_sample['JML_PPH_TERUTANG_FINAL'].sum()
print('sum terutang: ', sum_terutang/1e9)

df_final4 = pd.read_csv("s2122p/SPT_OP_FINAL21_67.csv", sep= "|", on_bad_lines="warn")
df_final4 = df_final4.drop(['DW_PROCESS_DATE', 'ID_MS_TH_PJK',
                                'ID_SPT', 'ID_SPT_FIELD', 'ID_TEMPLATE',
                                'ISVALID', 'JNS_SPT', 'KPPADM', 'REV_NO',
                                'TGL_SPT_TT'], axis=1)
df_final4['JML_PPH_TERUTANG_FINAL']  = (df_final4['JML_PPH_TERUTANG_DISKONTO_SBI']
                                        +df_final4['JML_PPH_TERUTANG_OBLIGASI']
                                        +df_final4['JML_PPH_TERUTANG_PENJUALAN_SAHAM']
                                        +df_final4['JML_PPH_TERUTANG_HADIAN_UNDIAN']
                                        +df_final4['JML_PPH_TERUTANG_PESANGON']
                                        +df_final4['JML_PPH_TERUTANG_HONORARIUM_APBN']
                                        +df_final4['JML_PPH_TERUTANG_PHBTB']
                                        +df_final4['JML_PPH_TERUTANG_BANGUN_GUNA_SERAH']
                                        +df_final4['JML_PPH_TERUTANG_SEWA_TANAH_BANGUNAN']
                                        +df_final4['JML_PPH_TERUTANG_USAHA_JASKON']
                                        +df_final4['JML_PPH_TERUTANG_DEALER_BBM']
                                        +df_final4['JML_PPH_TERUTANG_BUNGA_SIMPANAN_KOPERASI']
                                        +df_final4['JML_PPH_TERUTANG_TRANSAKSI_DERIVATIF']
                                        +df_final4['JML_PPH_TERUTANG_DIVIDEN']
                                        +df_final4['JML_PPH_TERUTANG_PH_ISTRI']
                                        +df_final4['JML_PPH_TERUTANG_LAINNYA'])
df_final4 = df_final4.drop_duplicates(subset=['NPWP'], keep='last')
df_final4 = df_final4.set_index('NPWP')
df_sample.update(df_final4)
sum_terutang = df_sample['JML_PPH_TERUTANG_FINAL'].sum()
print('sum terutang: ', sum_terutang/1e9)

df_final5 = pd.read_csv("s2122p/SPT_OP_FINAL21_89.csv", sep= "|", on_bad_lines="warn")
df_final5 = df_final5.drop(['DW_PROCESS_DATE', 'ID_MS_TH_PJK',
                                'ID_SPT', 'ID_SPT_FIELD', 'ID_TEMPLATE',
                                'ISVALID', 'JNS_SPT', 'KPPADM', 'REV_NO',
                                'TGL_SPT_TT'], axis=1)
df_final5['JML_PPH_TERUTANG_FINAL']  = (df_final5['JML_PPH_TERUTANG_DISKONTO_SBI']
                                        +df_final5['JML_PPH_TERUTANG_OBLIGASI']
                                        +df_final5['JML_PPH_TERUTANG_PENJUALAN_SAHAM']
                                        +df_final5['JML_PPH_TERUTANG_HADIAN_UNDIAN']
                                        +df_final5['JML_PPH_TERUTANG_PESANGON']
                                        +df_final5['JML_PPH_TERUTANG_HONORARIUM_APBN']
                                        +df_final5['JML_PPH_TERUTANG_PHBTB']
                                        +df_final5['JML_PPH_TERUTANG_BANGUN_GUNA_SERAH']
                                        +df_final5['JML_PPH_TERUTANG_SEWA_TANAH_BANGUNAN']
                                        +df_final5['JML_PPH_TERUTANG_USAHA_JASKON']
                                        +df_final5['JML_PPH_TERUTANG_DEALER_BBM']
                                        +df_final5['JML_PPH_TERUTANG_BUNGA_SIMPANAN_KOPERASI']
                                        +df_final5['JML_PPH_TERUTANG_TRANSAKSI_DERIVATIF']
                                        +df_final5['JML_PPH_TERUTANG_DIVIDEN']
                                        +df_final5['JML_PPH_TERUTANG_PH_ISTRI']
                                        +df_final5['JML_PPH_TERUTANG_LAINNYA'])
df_final5 = df_final5.drop_duplicates(subset=['NPWP'], keep='last')
df_final5 = df_final5.set_index('NPWP')
df_sample.update(df_final5)
sum_terutang = df_sample['JML_PPH_TERUTANG_FINAL'].sum()
print('sum terutang: ', sum_terutang/1e9)
#OTHER INCOME
df_other = pd.read_csv("s2122p/SPT_OP_HIT_PH_NETO_DN_LAINNYA21.csv", sep= "|", on_bad_lines="warn")
df_other = df_other.drop(['DW_PROCESS_DATE', 'ID_MS_TH_PJK',
                                'ID_SPT', 'ID_SPT_FIELD', 'ID_TEMPLATE',
                                'ISVALID', 'JNS_SPT', 'KPPADM', 'REV_NO',
                                'TGL_SPT_TT'], axis=1)
df_other = df_other.drop_duplicates(subset=['NPWP'], keep='last')
df_other = df_other.set_index('NPWP')
df_sample = df_sample.join(df_other,how='left')

#INCOME FROM SALARY
df_salary = pd.read_csv("s2122p/SPT_OP_HIT_PH_NETO_DN_PEKERJAA21.csv", sep= "|", on_bad_lines="warn")
df_salary = df_salary.drop(['DW_PROCESS_DATE', 'ID_MS_TH_PJK',
                                'ID_SPT', 'ID_SPT_FIELD', 'ID_TEMPLATE',
                                'ISVALID', 'JNS_SPT', 'KPPADM', 'REV_NO',
                                'TGL_SPT_TT'], axis=1)
df_salary = df_salary.drop_duplicates(subset=['NPWP'], keep='last')
df_salary = df_salary.rename(columns={'JML_PH_NETO': 'JML_PH_NETO_SALARY'})
df_salary = df_salary.set_index('NPWP')
df_sample = df_sample.join(df_salary,how='left')
sum_terutang = df_sample['JML_PH_NETO_SALARY'].sum()
print('sum terutang: ', sum_terutang/1e9)

#BUSINESS INCOME WITH BOOK KEEPING
df_business_book = pd.read_csv("s2122p/SPT_OP_HIT_PH_NETO_DN_PEMBUKUAN21.csv", sep= "|", on_bad_lines="warn")
df_business_book = df_business_book.drop(['DW_PROCESS_DATE', 'ID_MS_TH_PJK',
                                'ID_SPT', 'ID_SPT_FIELD', 'ID_TEMPLATE',
                                'ISVALID', 'JNS_SPT', 'KPPADM', 'REV_NO',
                                'TGL_SPT_TT'], axis=1)
df_business_book = df_business_book.drop_duplicates(subset=['NPWP'], keep='last')
df_business_book = df_business_book.rename(columns={'JML_PH_NETO': 'JML_PH_NETO_BUS',
                                                    'JML_PU': 'JMLPU_WB'})
df_business_book = df_business_book.set_index('NPWP')
df_sample = df_sample.join(df_business_book,how='left')

#df_sample = pd.merge(df_sample, df_business_book, on = "NPWP", how = "left", indicator=True)

#BUSINESS INCOME WITHOUT BOOK KEEPING
df_business_deemed = pd.read_csv("s2122p/SPT_OP_HIT_PH_NETO_DN_PENCATATAN21.csv", sep= "|", on_bad_lines="warn")
df_business_deemed = df_business_deemed.drop(['DW_PROCESS_DATE', 'ID_MS_TH_PJK',
                                'ID_SPT', 'ID_SPT_FIELD', 'ID_TEMPLATE',
                                'ISVALID', 'JNS_SPT', 'KPPADM', 'REV_NO',
                                'TGL_SPT_TT'], axis=1)
df_business_deemed = df_business_deemed.drop_duplicates(subset=['NPWP'], keep='last')
df_business_deemed = df_business_deemed.set_index('NPWP')
df_sample = df_sample.join(df_business_deemed,how='left')


#FINAL INCOME FROM SMALL BUSINESS
df_msmb = pd.read_csv("s2122p/SPT_OP_PP4621.csv", sep= "|", on_bad_lines="warn")
df_msmb = df_msmb.drop(['DW_PROCESS_DATE', 'ID_MS_TH_PJK',
                                'ID_SPT', 'ID_SPT_FIELD', 'ID_TEMPLATE',
                                'ISVALID', 'JNS_SPT', 'KPPADM', 'REV_NO',
                                'TGL_SPT_TT'], axis=1)
df_msmb = df_msmb.drop_duplicates(subset=['NPWP'], keep='last')
df_msmb = df_msmb.set_index('NPWP')
df_sample = df_sample.join(df_msmb,how='left')


# NON TAXABLE INCOME
df_nti = pd.read_csv("s2122p/SPT_OP_TIDAK_OBJEK_PJK21.csv", sep= "|", on_bad_lines="warn")
df_nti = df_nti.drop(['DW_PROCESS_DATE', 'ID_MS_TH_PJK',
                                'ID_SPT', 'ID_SPT_FIELD', 'ID_TEMPLATE',
                                'ISVALID', 'JNS_SPT', 'KPPADM', 'REV_NO',
                                'TGL_SPT_TT'], axis=1)
df_nti = df_nti.drop_duplicates(subset=['NPWP'], keep='last')
df_nti = df_nti.rename(columns={'JML_PH_BRUTO_LAINNYA': 'JML_PH_BRUTO_LAINNYA_NTI'})
df_nti = df_nti.set_index('NPWP')
df_sample = df_sample.join(df_nti,how='left')


#writing the merged sample with appendix
#df_sample.to_csv('pit_sample_w_appendix_2021.csv')

# Make Small Sample

df_sample_big = pd.read_csv('pit_sample_w_appendix_2021.csv')
# Make small sample for verification
df_sample_small = df_sample_big.sample(n=100000, weights=df_sample_big['weight'])
df_sample_small['weight'] = df_sample_big['weight'].sum()/100000
df_sample_small.to_csv('pit_sample_2021_small_w_appendix.csv', index=False)

df_indo_weights = df_sample_small[['weight']]
df_indo_weights = df_indo_weights.rename(columns = {'weight': 'WT2021'})
df_indo_weights["WT2022"] = df_indo_weights["WT2021"]
df_indo_weights["WT2023"] = df_indo_weights["WT2021"]
df_indo_weights["WT2024"] = df_indo_weights["WT2021"]
df_indo_weights["WT2025"] = df_indo_weights["WT2021"]
df_indo_weights["WT2026"] = df_indo_weights["WT2021"]
df_indo_weights["WT2027"] = df_indo_weights["WT2021"]
df_indo_weights["WT2028"] = df_indo_weights["WT2021"]
df_indo_weights.to_csv("taxcalc/pit_weight_indo.csv")

#df_sample_small = pd.read_csv('taxcalc/pit_sample_2021_small_w_appendix.csv')
"""
main_salary_total = df_sample['JML_PH_NETO_DN_DR_PEKERJAAN'].sum()
appendix_salary_total = df_sample['JML_PH_NETO_SALARY'].sum()
print('sum main_salary_total: ', main_salary_total/1e9)
print('sum appendix_salary_total: ', appendix_salary_total/1e9)
"""

# verification



#next: mapping file 
