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
#from stata_python import *

#'/Users/windi/Documents/SPRING 2024/Applied Tax Policy/Data/in_class_data/stata_python.py'

path = "/Users/windi/Documents/SPRING 2024/Applied Tax Policy/Data/raw_data_020724/o2122p/"
path2 = "/Users/windi/Documents/SPRING 2024/Applied Tax Policy/Microsimulation/Indonesia Microsimulation Model/taxcalc/"
path3 = "/Users/windi/Documents/SPRING 2024/Applied Tax Policy/Data/raw_data_020724/s2122p/"

#df1 = pd.read_csv("/Users/windi/Documents/SPRING 2024/Applied Tax Policy/Data/raw_data_020724/o2122p/_op21_01.csv", sep= "|", on_bad_lines="warn")

#reading csv datasets with pipe ("|") delimited
df1 = pd.read_csv(path+"_op21_01.csv", sep= "|", on_bad_lines="warn")
df2 = pd.read_csv(path+"_op21_23.csv", sep= "|", on_bad_lines="warn")
df3 = pd.read_csv(path+"_op21_45.csv", sep= "|", on_bad_lines="warn")
df4 = pd.read_csv(path+"_op21_67.csv", sep= "|", on_bad_lines="warn")
df5 = pd.read_csv(path+"_op21_89.csv", sep= "|", on_bad_lines="warn")

#concatinating cvs datasets
df_all = pd.concat([df1, df2, df3, df4, df5], axis = 0)

#df_all = pd.read_csv(path2+"pit21.csv")

#Creating a Year Field
df_all["Year"] = df_all["ID_MS_TH_PJK"]/100
df_all["Year"] = df_all["Year"].astype("int")

#Cleaning up invalid tax returns 
#(By the law, form 1770 SS is only for employees who has income less than IDR 60 millions. 
#But, in the 2021 we found 800+ 1770SS with income more than IDR 100 millions 
#and with some very huge number IDR 9,000 trilliun)
df_all.JNS_SPT = df_all.JNS_SPT.astype("string")
df_all=df_all.drop(df_all[(df_all.JML_PH_NETO > 1e8) & (df_all.JNS_SPT=="1770SS")].index)

# #9.83 trilliun entry for interest saving income is likely an error, so it will be dropped
# df_all=df_all.drop(df_all[(df_all.JML_PH_NETO > 1e8) & (df_all.JNS_SPT=="1770SS")].index)


#Cleaning up NaNs
df_all["JML_TANGGUNGAN"] = df_all["JML_TANGGUNGAN"].fillna(0)
df_all["JML_TANGGUNGAN"] = df_all["JML_TANGGUNGAN"].astype("int")

df_all["JML_PH_NETO_DN_DR_USAHA"] = df_all["JML_PH_NETO_DN_DR_USAHA"].fillna(0)
df_all["JML_PH_NETO_DN_DR_PEKERJAAN"] = df_all["JML_PH_NETO_DN_DR_PEKERJAAN"].fillna(0)
df_all["JML_PH_NETO_DN_LAINNYA"] = df_all["JML_PH_NETO_DN_LAINNYA"].fillna(0)
df_all["JML_PH_NETO_LN"] = df_all["JML_PH_NETO_LN"].fillna(0)
df_all["JML_ZAKAT"] = df_all["JML_ZAKAT"].fillna(0)
df_all["JML_KOM_RUGI"] = df_all["JML_KOM_RUGI"].fillna(0)
df_all["JML_TANGGUNGAN"] = df_all["JML_TANGGUNGAN"].fillna(0)
# df_all["JML_ZAKAT"] = df_all["JML_ZAKAT"].fillna(0)
# df_all["JML_ZAKAT"] = df_all["JML_ZAKAT"].fillna(0)
# df_all["JML_ZAKAT"] = df_all["JML_ZAKAT"].fillna(0)
# df_all["JML_ZAKAT"] = df_all["JML_ZAKAT"].fillna(0)

df_all["JNS_SPT_NUM"] = 0
df_all["JNS_SPT_NUM"] = np.where(df_all["JNS_SPT"] == "1770S", 1, df_all["JNS_SPT_NUM"])
df_all["JNS_SPT_NUM"] = np.where(df_all["JNS_SPT"] == "1770", 2, df_all["JNS_SPT_NUM"])

df_all.JNS_SPT_NUM = df_all.JNS_SPT_NUM.astype("int")
   
#df_all["JML_PH_NETO_DN_DR_PEKERJAAN"] = df_all["JML_PH_NETO_DN_DR_PEKERJAAN"].fillna(0)

df_all["JML_PH_NETO_DN_DR_PEKERJAAN_ADJ"] = np.where(df_all["JNS_SPT"] == "1770SS", df_all["JML_PH_NETO"], df_all["JML_PH_NETO_DN_DR_PEKERJAAN"])

df_all=df_all[["NPWP", "Year", "KPPADM", "JNS_SPT", "JNS_SPT_NUM", "JML_PH_NETO_DN_DR_USAHA","JML_PH_NETO_DN_DR_PEKERJAAN_ADJ","JML_PH_NETO_DN_LAINNYA",
                          "JML_PH_NETO_LN", "JML_PH_NETO", "JML_ZAKAT", "JML_PH_NETO_STLH_ZAKAT", "JML_KOM_RUGI", "JML_PH_NETO_STLH_KOM_RUGI", "FG_PTKP", "JML_TANGGUNGAN", "JML_PTKP",
                          "JML_PKP", "JML_PPH_TERUTANG", "JML_DPP_PH_FINAL", "JML_PPH_FINAL", "JML_PH_BUKAN_OBJEK_PJK", "JML_PENGURANGAN"]]

#Saving Complete Dataset without Appendix
#df_all.to_csv(path2+"pit21.csv", index = False)

df_all = pd.read_csv(path2+"pit21.csv")

#Creating Weights file for full dataset
df_weight = pd.DataFrame(index=range(len(df_all["NPWP"]))) 
df_weight["WT2021"]=1.0
df_weight["WT2022"]=1.0
df_weight["WT2023"]=1.0
df_weight["WT2024"]=1.0
df_weight["WT2025"]=1.0
df_weight["WT2026"]=1.0
df_weight["WT2027"]=1.0
df_weight["WT2028"]=1.0
df_weight.to_csv(path2+"pit21_weights.csv", index = False)

#sorting total income
# df_all = df_all.sort_values(by=['JML_PH_NETO'])

# #separate JML_PH_NETO = 0 
# df_0 = df_all[df_all['JML_PH_NETO'] <= 0]

# #separate JML_PH_NETO not 0
# df = df_all[df_all['JML_PH_NETO'] > 0] 

# #writing the concatinated and sorted file
# df.to_csv(path2+"pit21.csv", index = False)

#merging sample files and repeat for all appendixes files

#df = df_sample_big = pd.read_csv("pit_sample_2021.csv")
#df_sample_big = df_sample.drop('Unnamed: 0', axis=1)

# Make small sample for verification
#df_sample = df_sample_big.sample(n=100000)
#df_sample.to_csv('pit_sample_2021_small.csv', index=False)


#df_sample = pd.read_csv("pit_sample_2021_small.csv")

#df_sample = pd.read_csv("pit_sample_2021.csv")
#df_sample = df_sample.drop('Unnamed: 0', axis=1)
#df_sample = df_sample.set_index('NPWP')

#FINAL INCOME
df_final1 = pd.read_csv(path3+"SPT_OP_FINAL21_01.csv", sep= "|", on_bad_lines="warn")
df_final2 = pd.read_csv(path3+"SPT_OP_FINAL21_23.csv", sep= "|", on_bad_lines="warn")
df_final3 = pd.read_csv(path3+"SPT_OP_FINAL21_45.csv", sep= "|", on_bad_lines="warn")
df_final4 = pd.read_csv(path3+"SPT_OP_FINAL21_67.csv", sep= "|", on_bad_lines="warn")
df_final5 = pd.read_csv(path3+"SPT_OP_FINAL21_89.csv", sep= "|", on_bad_lines="warn")

df_final = pd.concat([df_final1, df_final2, df_final3, df_final4, df_final5], axis = 0)

df_final = df_final.drop(['DW_PROCESS_DATE',
                                'ID_SPT', 'ID_SPT_FIELD', 'ID_TEMPLATE',
                                'ISVALID', 'KPPADM', 'REV_NO',
                                'TGL_SPT_TT'], axis=1)

df_final.to_csv(path3+"final_tax_appendix_2021_1.csv", index = False)

df_final = pd.read_csv(path3+"final_tax_appendix_2021_1.csv")

df_final = df_final.drop_duplicates(subset=['NPWP'], keep='last')
df_all = pd.merge(df_all, df_final, on = "NPWP", how = "left")
#df_all.to_csv(path2+"pit21_with_final_tax.csv", index = False)

df_sb=pd.read_csv(path3+"SPT_OP_PP4621.csv", sep= "|", on_bad_lines="warn")
df_sb = df_sb.drop_duplicates(subset=['NPWP'], keep='last')

#Cleaning up invalid turnover inputs 
#(By the law, the small business turnover rate allowed only for those whose turnover are below IDR 4.8 billion 
#But, in the 2021 we found a lot of other final income with turnover of more than IDR 4.8 billion
#We assume 2x 4.8 billion are fine, and drop turnover of more than twice of 4.8 billion
df_sb=df_sb.drop(df_sb[(df_sb.JML_PU > 9.6E9)].index)


df_sb = df_sb[["NPWP", "JML_PU", "JML_PPH_FINAL_DIBYR" ]]
# df_sb["JML_PU"] = df_sb["JML_PU"].fillna(0)
# df_sb["JML_PPH_FINAL_DIBYR"] = df_sb["JML_PPH_FINAL_DIBYR"].fillna(0)

df_all = pd.merge(df_all, df_sb, on = "NPWP", how = "left")

#Cleaning up NaNs
df_all["JML_PH_BRUTO_DISKONTO_SBI"] = df_all["JML_PH_BRUTO_DISKONTO_SBI"].fillna(0)
df_all["JML_PH_BRUTO_OBLIGASI"] = df_all["JML_PH_BRUTO_OBLIGASI"].fillna(0)
df_all["JML_PH_BRUTO_PENJUALAN_SAHAM"] = df_all["JML_PH_BRUTO_PENJUALAN_SAHAM"].fillna(0)
df_all["JML_PH_BRUTO_HADIAH_UNDIAN"] = df_all["JML_PH_BRUTO_HADIAH_UNDIAN"].fillna(0)
df_all["JML_PH_BRUTO_PESANGON"] = df_all["JML_PH_BRUTO_PESANGON"].fillna(0)
df_all["JML_PH_BRUTO_HONORARIUM_APBN"] = df_all["JML_PH_BRUTO_HONORARIUM_APBN"].fillna(0)
df_all["JML_PH_BRUTO_PHTB"] = df_all["JML_PH_BRUTO_PHTB"].fillna(0)
df_all["JML_PH_BRUTO_BANGUN_GUNA_SERAH"] = df_all["JML_PH_BRUTO_BANGUN_GUNA_SERAH"].fillna(0)
df_all["JML_PH_BRUTO_SEWA_TANAH_BANGUNAN"] = df_all["JML_PH_BRUTO_SEWA_TANAH_BANGUNAN"].fillna(0)
df_all["JML_PH_BRUTO_USAHA_JASKON"] = df_all["JML_PH_BRUTO_USAHA_JASKON"].fillna(0)
df_all["JML_PH_BRUTO_DEALER_BBM"] = df_all["JML_PH_BRUTO_DEALER_BBM"].fillna(0)
df_all["JML_PH_BRUTO_BUNGA_SIMPANAN_KOPERASI"] = df_all["JML_PH_BRUTO_BUNGA_SIMPANAN_KOPERASI"].fillna(0)
df_all["JML_PH_BRUTO_TRANSAKSI_DERIVATIF"] = df_all["JML_PH_BRUTO_TRANSAKSI_DERIVATIF"].fillna(0)
df_all["JML_PH_BRUTO_DIVIDEN"] = df_all["JML_PH_BRUTO_DIVIDEN"].fillna(0)
df_all["JML_PH_BRUTO_PH_ISTRI"] = df_all["JML_PH_BRUTO_PH_ISTRI"].fillna(0)
df_all["JML_PH_BRUTO_LAINNYA"] = df_all["JML_PH_BRUTO_LAINNYA"].fillna(0)

df_all["JML_PPH_TERUTANG_DISKONTO_SBI"] = df_all["JML_PPH_TERUTANG_DISKONTO_SBI"].fillna(0)
df_all["JML_PPH_TERUTANG_OBLIGASI"] = df_all["JML_PPH_TERUTANG_OBLIGASI"].fillna(0)
df_all["JML_PPH_TERUTANG_PENJUALAN_SAHAM"] = df_all["JML_PPH_TERUTANG_PENJUALAN_SAHAM"].fillna(0)
df_all["JML_PPH_TERUTANG_HADIAN_UNDIAN"] = df_all["JML_PPH_TERUTANG_HADIAN_UNDIAN"].fillna(0)
df_all["JML_PPH_TERUTANG_PESANGON"] = df_all["JML_PPH_TERUTANG_PESANGON"].fillna(0)
df_all["JML_PPH_TERUTANG_HONORARIUM_APBN"] = df_all["JML_PPH_TERUTANG_HONORARIUM_APBN"].fillna(0)
df_all["JML_PPH_TERUTANG_PHBTB"] = df_all["JML_PPH_TERUTANG_PHBTB"].fillna(0)
df_all["JML_PPH_TERUTANG_BANGUN_GUNA_SERAH"] = df_all["JML_PPH_TERUTANG_BANGUN_GUNA_SERAH"].fillna(0)
df_all["JML_PPH_TERUTANG_SEWA_TANAH_BANGUNAN"] = df_all["JML_PPH_TERUTANG_SEWA_TANAH_BANGUNAN"].fillna(0)
df_all["JML_PPH_TERUTANG_USAHA_JASKON"] = df_all["JML_PPH_TERUTANG_USAHA_JASKON"].fillna(0)
df_all["JML_PPH_TERUTANG_DEALER_BBM"] = df_all["JML_PPH_TERUTANG_DEALER_BBM"].fillna(0)
df_all["JML_PPH_TERUTANG_BUNGA_SIMPANAN_KOPERASI"] = df_all["JML_PPH_TERUTANG_BUNGA_SIMPANAN_KOPERASI"].fillna(0)
df_all["JML_PPH_TERUTANG_TRANSAKSI_DERIVATIF"] = df_all["JML_PPH_TERUTANG_TRANSAKSI_DERIVATIF"].fillna(0)
df_all["JML_PPH_TERUTANG_DIVIDEN"] = df_all["JML_PPH_TERUTANG_DIVIDEN"].fillna(0)
df_all["JML_PPH_TERUTANG_PH_ISTRI"] = df_all["JML_PPH_TERUTANG_PH_ISTRI"].fillna(0)
df_all["JML_PPH_TERUTANG_LAINNYA"] = df_all["JML_PPH_TERUTANG_LAINNYA"].fillna(0)

df_all["JML_PH_BRUTO_DISKONTO_SBI_ADJUSTED"] = np.where(df_all["JML_PPH_TERUTANG_DISKONTO_SBI"]>0,(df_all["JML_PPH_TERUTANG_DISKONTO_SBI"]/0.2)+7500000,0)

df_all["JML_PU"] = df_all["JML_PU"].fillna(0)
df_all["JML_PPH_FINAL_DIBYR"] = df_all["JML_PPH_FINAL_DIBYR"].fillna(0)

#margin for small business taken as 15% (data from SKDU statistics, Bank Indonesia https://www.bi.go.id/en/publikasi/laporan/Pages/SKDU-Triwulan-IV-2023.aspx)
df_all["JML_PH_BRUTO_PHTB_PROFIT"] = df_all["JML_PH_BRUTO_PHTB"]*0.15
df_all["JML_PH_BRUTO_PENJUALAN_SAHAM_PROFIT"] = df_all["JML_PH_BRUTO_PENJUALAN_SAHAM"]*0.15
df_all["JML_PH_BRUTO_BANGUN_GUNA_SERAH_PROFIT"] = df_all["JML_PH_BRUTO_BANGUN_GUNA_SERAH"]*0.15
df_all["JML_PH_BRUTO_USAHA_JASKON_PROFIT"] = df_all["JML_PH_BRUTO_USAHA_JASKON"]*0.15
df_all["JML_PH_BRUTO_DEALER_BBM_PROFIT"] = df_all["JML_PH_BRUTO_DEALER_BBM"]*0.15
df_all["JML_PROFIT_SB"] = df_all["JML_PU"]*0.15

df_all['JML_PH_BRUTO_FINAL']  = (df_all['JML_PH_BRUTO_DISKONTO_SBI_ADJUSTED']
                                        +df_all['JML_PH_BRUTO_OBLIGASI']
                                        +df_all['JML_PH_BRUTO_PENJUALAN_SAHAM_PROFIT']
                                        +df_all['JML_PH_BRUTO_HADIAH_UNDIAN']
                                        +df_all['JML_PH_BRUTO_PESANGON']
                                        +df_all['JML_PH_BRUTO_HONORARIUM_APBN']
                                        +df_all['JML_PH_BRUTO_PHTB_PROFIT']
                                        +df_all['JML_PH_BRUTO_BANGUN_GUNA_SERAH_PROFIT']
                                        +df_all['JML_PH_BRUTO_SEWA_TANAH_BANGUNAN']
                                        +df_all['JML_PH_BRUTO_USAHA_JASKON_PROFIT']
                                        +df_all['JML_PH_BRUTO_DEALER_BBM_PROFIT']
                                        +df_all['JML_PH_BRUTO_BUNGA_SIMPANAN_KOPERASI']
                                        +df_all['JML_PH_BRUTO_TRANSAKSI_DERIVATIF']
                                        +df_all['JML_PH_BRUTO_DIVIDEN']
                                        +df_all['JML_PH_BRUTO_PH_ISTRI']
                                        +df_all['JML_PROFIT_SB'])

df_all['JML_PPH_TERUTANG_FINAL']  = (df_all['JML_PPH_TERUTANG_DISKONTO_SBI']
                                        +df_all['JML_PPH_TERUTANG_OBLIGASI']
                                        +df_all['JML_PPH_TERUTANG_PENJUALAN_SAHAM']
                                        +df_all['JML_PPH_TERUTANG_HADIAN_UNDIAN']
                                        +df_all['JML_PPH_TERUTANG_PESANGON']
                                        +df_all['JML_PPH_TERUTANG_HONORARIUM_APBN']
                                        +df_all['JML_PPH_TERUTANG_PHBTB']
                                        +df_all['JML_PPH_TERUTANG_BANGUN_GUNA_SERAH']
                                        +df_all['JML_PPH_TERUTANG_SEWA_TANAH_BANGUNAN']
                                        +df_all['JML_PPH_TERUTANG_USAHA_JASKON']
                                        +df_all['JML_PPH_TERUTANG_DEALER_BBM']
                                        +df_all['JML_PPH_TERUTANG_BUNGA_SIMPANAN_KOPERASI']
                                        +df_all['JML_PPH_TERUTANG_TRANSAKSI_DERIVATIF']
                                        +df_all['JML_PPH_TERUTANG_DIVIDEN']
                                        +df_all['JML_PPH_TERUTANG_PH_ISTRI']
                                        +df_all['JML_PPH_FINAL_DIBYR'])

df_all["TOTAL_INCOME_WITH_FINAL"] = df_all["JML_PH_NETO"] + df_all['JML_PH_BRUTO_FINAL']
df_all["TOTAL_TAX_WITH_FINAL"] = df_all["JML_PPH_TERUTANG"] + df_all['JML_PPH_TERUTANG_FINAL']

df_all['weight']=1

df_all.to_csv(path2+"pit21_with_final_tax_2.csv", index = False)

#Creating Weights file for full dataset with final tax
df_weight = pd.DataFrame(index=range(len(df_all["NPWP"]))) 
df_weight["WT2021"]=1.0
df_weight["WT2022"]=1.0
df_weight["WT2023"]=1.0
df_weight["WT2024"]=1.0
df_weight["WT2025"]=1.0
df_weight["WT2026"]=1.0
df_weight["WT2027"]=1.0
df_weight["WT2028"]=1.0
df_weight.to_csv(path2+"pit21_with_final_tax_weights.csv", index = False)

#CREATING A SAMPLE OF THE DATASET
df_all = pd.read_csv(path2+"pit21_with_final_tax_2.csv")

#creating income orders
df_all = df_all.reset_index()

#df_all["TOTAL_INCOME"] = (df_all["JML_PH_NETO"] + df_all["JML_PH_BRUTO_FINAL"])
#df_all["TOTAL_TAX_WITH_FINAL"] = (df_all["JML_PPH_TERUTANG"] + df_all["JML_PPH_TERUTANG_FINAL"])

#sorting total income
df_all = df_all.sort_values(by=['TOTAL_INCOME_WITH_FINAL'])

num_records = len(df_all)

#separate JML_PH_NETO = 0 
df_0 = df_all[df_all['TOTAL_INCOME_WITH_FINAL'] <= 0]

num_records_zero_total_income = len(df_0)

#separate JML_PH_NETO not 0
df = df_all[df_all['TOTAL_INCOME_WITH_FINAL'] > 0] 

# allocate the income into 10 bins
df['bin'] = pd.qcut(df['TOTAL_INCOME_WITH_FINAL'], 10, labels=False)
df['weight']=1

#df_all['bin'] = pd.qcut(df_all['TOTAL_TAX'], 10, labels=False)

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

#df_sample = pd.concat(frames)


#Creating sample of 100000 records for zero Total Income
df_sample_0 = df_0.sample(n=100000)
df_sample_0['bin'] = -1
df_sample_0['weight'] = num_records_zero_total_income/100000
frames=frames+[df_sample_0]
df_sample = pd.concat(frames)
df_sample.to_csv(path2+'pit_sample_2021_with_final_tax.csv')

#2021 Tax collection as per MoF is 158.70 trillions
#2021 Tax collection as per sample is 118.46 trillions
#2022 Tax collection as per sample is 122.15 trillions
#calibration_factor_2021 = 1.0
calibration_factor_2021 = 158.70/118.46
calibration_factor_2022 = 1.0
calibration_factor_2023 = 1.0
calibration_factor_2024 = 1.0
calibration_factor_2025 = 1.0
calibration_factor_2026 = 1.0
calibration_factor_2027 = 1.0
calibration_factor_2028 = 1.0
#calibration_factor_2022 = 158.70/122.15
#calibration_factor_2022 = 183.70/219.22

#Creating Weights file for full dataset
df_weight = pd.DataFrame(index=range(len(df_sample["NPWP"]))) 
df_weight = df_sample[["weight"]].copy()
df_weight = df_weight.rename(columns={'weight':'WT2021'})
df_weight['WT2021'] = df_weight['WT2021']*calibration_factor_2021
df_weight['WT2022'] = df_weight['WT2021']*calibration_factor_2022
df_weight['WT2023'] = df_weight['WT2021']*calibration_factor_2023
df_weight['WT2024'] = df_weight['WT2021']*calibration_factor_2024
df_weight['WT2025'] = df_weight['WT2021']*calibration_factor_2025
df_weight['WT2026'] = df_weight['WT2021']*calibration_factor_2026
df_weight['WT2027'] = df_weight['WT2021']*calibration_factor_2027
df_weight['WT2028'] = df_weight['WT2021']*calibration_factor_2028

df_weight.to_csv(path2+"pit21_sample_2021_with_final_tax_weights_calibrated.csv", index = False)

#make a small sample of 100,000 data
#df_sample = pd.read_csv(path2+'pit_sample_2021_with_final_tax.csv')
df_sample_small = df_sample.sample(n = 100000, weights=df_sample["weight"])
df_sample_small["weight"]
num_records_sample = df_sample["weight"].sum()
num_records_small_sample = df_sample_small["weight"].sum()
df_sample_small["weight"] = df_sample_small["weight"]*num_records_sample/num_records_small_sample
df_sample_small["weight"].sum()
df_sample_small.to_csv(path2+"pit21_sample_small_2021_with_final_tax.csv", index = False)

df_weight = pd.DataFrame(index=range(len(df_sample_small["NPWP"]))) 
df_weight = df_sample_small[["weight"]].copy()
df_weight = df_weight.rename(columns={'weight':'WT2021'})
df_weight['WT2022'] = df_weight['WT2021']
df_weight['WT2023'] = df_weight['WT2021']
df_weight['WT2024'] = df_weight['WT2021']
df_weight['WT2025'] = df_weight['WT2021']
df_weight['WT2026'] = df_weight['WT2021']
df_weight['WT2027'] = df_weight['WT2021']
df_weight['WT2028'] = df_weight['WT2021']
df_weight.to_csv(path2+"pit21_sample_small_2021_with_final_tax_weights.csv", index = False)

#verify and comparing sample with the population
df_all["TOTAL_TAX_WITH_FINAL"] = df_all["JML_PPH_TERUTANG"] + df_all['JML_PPH_TERUTANG_FINAL']
df_sample["TOTAL_TAX_WITH_FINAL"] = df_sample["JML_PPH_TERUTANG"] + df_sample['JML_PPH_TERUTANG_FINAL']

varlist = ['TOTAL_INCOME_WITH_FINAL', 'TOTAL_TAX_WITH_FINAL']

total_weight_sample = df_sample['weight'].sum()
total_weight_population = df_all['weight'].sum()

#comparing the statistic of the population and sample
for var in varlist:
    df_sample['weighted_'+var] = df_sample[var]*df_sample['weight']
    sample_sum = df_sample['weighted_'+var].sum()
    population_sum = df_all[var].sum()
    print("            Sample Sum for ", var, " = ", sample_sum)
    print("        Population Sum for ", var, " = ", population_sum)
    print(" Sampling Error for Sum(%) ", var, " = ", "{:.2%}".format((population_sum-sample_sum)/population_sum))
    sample_mean = sample_sum/total_weight_sample
    population_mean = population_sum/total_weight_population
    print("           Sample Mean for ", var, " = ", sample_mean)
    print("       Population Mean for ", var, " = ", population_mean)
    print("Sampling Error for Mean(%) ", var, " = ", "{:.2%}".format((population_mean-sample_mean)/population_mean))    



"""
df_final1 = df_final1.drop_duplicates(subset=['NPWP'], keep='last')
df_final1 = df_final1.set_index('NPWP')
df_sample = df_sample.join(df_final1,how='left')
sum_terutang = df_sample['JML_PPH_TERUTANG_FINAL'].sum()
print('sum terutang: ', sum_terutang/1e9)

#df_sample = df_sample.drop('_merge', axis=1)


#OTHER INCOME
df_other = pd.read_csv(path3+"SPT_OP_HIT_PH_NETO_DN_LAINNYA21.csv", sep= "|", on_bad_lines="warn")
df_other = df_other.drop(['DW_PROCESS_DATE', 'ID_MS_TH_PJK',
                                'ID_SPT', 'ID_SPT_FIELD', 'ID_TEMPLATE',
                                'ISVALID', 'JNS_SPT', 'KPPADM', 'REV_NO',
                                'TGL_SPT_TT'], axis=1)
df_other = df_other.drop_duplicates(subset=['NPWP'], keep='last')
df_other = df_other.set_index('NPWP')
df_sample = df_sample.join(df_other,how='left')
df[df['bin']==i].sample(n=bin_size)
#INCOME FROM SALARY
df_salary = pd.read_csv(path3+"SPT_OP_HIT_PH_NETO_DN_PEKERJAA21.csv", sep= "|", on_bad_lines="warn")
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
df_business_book = pd.read_csv(path3+"SPT_OP_HIT_PH_NETO_DN_PEMBUKUAN21.csv", sep= "|", on_bad_lines="warn")
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
df_business_deemed = pd.read_csv(path3+"SPT_OP_HIT_PH_NETO_DN_PENCATATAN21.csv", sep= "|", on_bad_lines="warn")
df_business_deemed = df_business_deemed.drop(['DW_PROCESS_DATE', 'ID_MS_TH_PJK',
                                'ID_SPT', 'ID_SPT_FIELD', 'ID_TEMPLATE',
                                'ISVALID', 'JNS_SPT', 'KPPADM', 'REV_NO',
                                'TGL_SPT_TT'], axis=1)
df_business_deemed = df_business_deemed.drop_duplicates(subset=['NPWP'], keep='last')
df_business_deemed = df_business_deemed.set_index('NPWP')
df_sample = df_sample.join(df_business_deemed,how='left')


#FINAL INCOME FROM SMALL BUSINESS
df_msmb = pd.read_csv(path3+"SPT_OP_PP4621.csv", sep= "|", on_bad_lines="warn")
df_msmb = df_msmb.drop(['DW_PROCESS_DATE', 'ID_MS_TH_PJK',
                                'ID_SPT', 'ID_SPT_FIELD', 'ID_TEMPLATE',
                                'ISVALID', 'JNS_SPT', 'KPPADM', 'REV_NO',
                                'TGL_SPT_TT'], axis=1)
df_msmb = df_msmb.drop_duplicates(subset=['NPWP'], keep='last')
df_msmb = df_msmb.set_index('NPWP')
df_sample = df_sample.join(df_msmb,how='left')


# NON TAXABLE INCOME
df_nti = pd.read_csv(path3+"SPT_OP_TIDAK_OBJEK_PJK21.csv", sep= "|", on_bad_lines="warn")
df_nti = df_nti.drop(['DW_PROCESS_DATE', 'ID_MS_TH_PJK',
                                'ID_SPT', 'ID_SPT_FIELD', 'ID_TEMPLATE',
                                'ISVALID', 'JNS_SPT', 'KPPADM', 'REV_NO',
                                'TGL_SPT_TT'], axis=1)
df_nti = df_nti.drop_duplicates(subset=['NPWP'], keep='last')
df_nti = df_nti.rename(columns={'JML_PH_BRUTO_LAINNYA': 'JML_PH_BRUTO_LAINNYA_NTI'})
df_nti = df_nti.set_index('NPWP')
df_sample = df_sample.join(df_nti,how='left')


#writing the merged sample with appendix
df_sample.to_csv('pit_sample_w_appendix_2021.csv')

"""
# Make Small Sample
#path = "/Users/windi/Documents/SPRING/2024/Applied/Tax/Policy/Data/raw_data_020724/" 
df_sample_big = pd.read_csv("taxcalc/pit_sample_w_appendix_2021.csv")

df_sample_big["Year"] = df_sample_big["ID_MS_TH_PJK"]/100
df_sample_big["Year"] = df_sample_big["Year"].astype("int")
df_sample_big["JML_TANGGUNGAN"] = df_sample_big["JML_TANGGUNGAN"].fillna(0)
df_sample_big["JML_TANGGUNGAN"] = df_sample_big["JML_TANGGUNGAN"].astype("int")

df_all["JML_PH_NETO_DN_DR_USAHA"] = df_all["JML_PH_NETO_DN_DR_USAHA"].fillna(0)
df_all["JML_PH_NETO_DN_DR_PEKERJAAN"] = df_all["JML_PH_NETO_DN_DR_PEKERJAAN"].fillna(0)
df_all["JML_PH_NETO_DN_LAINNYA"] = df_all["JML_PH_NETO_DN_LAINNYA"].fillna(0)
df_all["JML_PH_NETO_LN"] = df_all["JML_PH_NETO_LN"].fillna(0)


# Make small sample for verification
df_sample_small = df_sample_big.sample(n=100000, weights=df_sample_big['weight'])
df_sample_small['weight'] = df_sample_big['weight'].sum()/100000
df_sample_small.JNS_SPT = df_sample_small.JNS_SPT.astype("string")
df_sample_small.to_csv('taxcalc/pit_sample_2021_small_w_appendix.csv', index=False)

df_sample_small = pd.read_csv('taxcalc/pit_sample_2021_small_w_appendix.csv')


main_salary_total = df_sample['JML_PH_NETO_DN_DR_PEKERJAAN'].sum()
appendix_salary_total = df_sample['JML_PH_NETO_SALARY'].sum()
print('sum main_salary_total: ', main_salary_total/1e9)
print('sum appendix_salary_total: ', appendix_salary_total/1e9)


# verification



#next: mapping file 
"""