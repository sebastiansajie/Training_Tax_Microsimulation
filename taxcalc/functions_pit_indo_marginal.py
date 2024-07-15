"""
pitaxcalc-demo functions that calculate personal income tax liability.
"""
# CODING-STYLE CHECKS:
# pycodestyle functions.py
# pylint --disable=locally-disabled functions.py

import math
import copy
import pandas as pd
import numpy as np
from taxcalc.decorators import iterate_jit

"Calculation for Final Taxes"
@iterate_jit(nopython=True)
def cal_finaltaxes(rate_InterestSaving, threshold_InterestSaving, rate_InterestBonds, rate_SalesOfStocks, rate_Lottery,
                   rate1_SeverancePayment, tbrk1_SeverancePayment, rate2_SeverancePayment,
                   rate_Honoraria, rate_SalesOfAssets, rate_PropertyBOT, rate_Rent, rate_ConstructionFees,
                   rate_FuelDealers, rate1_CooperativeInterest, tbrk1_CooperativeInterest, rate2_CooperativeInterest, 
                   rate_DerivativeTransaction, rate_Dividend, 
                   rate1_WifeIncome, tbrk1_WifeIncome, rate2_WifeIncome, tbrk2_WifeIncome, rate3_WifeIncome, 
                   tbrk3_WifeIncome, rate4_WifeIncome, tbrk4_WifeIncome, rate5_WifeIncome,
                   rate_FinalOther,
                   JML_PH_BRUTO_DISKONTO_SBI, JML_PH_BRUTO_OBLIGASI, JML_PH_BRUTO_PENJUALAN_SAHAM, JML_PH_BRUTO_HADIAH_UNDIAN,
                   JML_PH_BRUTO_PESANGON, JML_PH_BRUTO_HONORARIUM_APBN, JML_PH_BRUTO_PHTB, JML_PH_BRUTO_BANGUN_GUNA_SERAH,                   
                   JML_PH_BRUTO_SEWA_TANAH_BANGUNAN, JML_PH_BRUTO_USAHA_JASKON, JML_PH_BRUTO_DEALER_BBM,
                   JML_PH_BRUTO_BUNGA_SIMPANAN_KOPERASI, JML_PH_BRUTO_TRANSAKSI_DERIVATIF, JML_PH_BRUTO_DIVIDEN,
                   JML_PH_BRUTO_PH_ISTRI, JML_PU, 
                   finaltax_InterestSaving, finaltax_InterestBonds, finaltax_SalesOfStocks, finaltax_Lottery, 
                   finaltax_SeverancePayment, finaltax_Honoraria, finaltax_SalesOfAssets, finaltax_PropertyBOT, finaltax_Rent, 
                   finaltax_FuelDealers, finaltax_DerivativeTransaction, finaltax_Dividend, finaltax_WifeIncome, finaltax_Other, 
                   finaltax_Total):

    savinginc = max(0, JML_PH_BRUTO_DISKONTO_SBI)    
    finaltax_InterestSaving = rate_InterestSaving * (savinginc-threshold_InterestSaving)   
    finaltax_InterestBonds = rate_InterestBonds * max(0, JML_PH_BRUTO_OBLIGASI) 
    finaltax_SalesOfStocks = rate_SalesOfStocks * max(0, JML_PH_BRUTO_PENJUALAN_SAHAM) 
    finaltax_Lottery = rate_Lottery * max(0, JML_PH_BRUTO_HADIAH_UNDIAN) 

    #pensioninc = JML_PH_BRUTO_PESANGON    
    # finaltax_Pension = (rate1_Pension * min(pensioninc, tbrk1_Pension) +
    #          rate2_Pension * min(tbrk2_Pension - tbrk1_Pension, max(0., pensioninc - tbrk1_Pension)) +
    #          rate3_Pension * min(tbrk3_Pension - tbrk2_Pension, max(0., pensioninc - tbrk2_Pension)) +
    #          rate4_Pension * min(tbrk4_Pension - tbrk3_Pension, max(0., pensioninc - tbrk3_Pension)) +
    #          rate5_Pension * max(0., pensioninc - tbrk4_Pension))
    
    severanceinc = max(0, JML_PH_BRUTO_PESANGON)
    finaltax_SeverancePayment = (rate1_SeverancePayment * min(severanceinc, tbrk1_SeverancePayment) 
                                  + rate2_SeverancePayment * max(0, severanceinc - tbrk1_SeverancePayment))
    finaltax_SeverancePayment = max(finaltax_SeverancePayment,0)

    finaltax_Honoraria = rate_Honoraria * max(0, JML_PH_BRUTO_HONORARIUM_APBN) 
    finaltax_SalesOfAssets = rate_SalesOfAssets * max(0, JML_PH_BRUTO_PHTB) 
    finaltax_PropertyBOT = rate_PropertyBOT * max(0, JML_PH_BRUTO_BANGUN_GUNA_SERAH) 
    finaltax_Rent = rate_Rent * max(0, JML_PH_BRUTO_SEWA_TANAH_BANGUNAN) 
    finaltax_ConstructionFees = rate_ConstructionFees * max(0, JML_PH_BRUTO_USAHA_JASKON) 
    finaltax_FuelDealers = rate_FuelDealers * max(0, JML_PH_BRUTO_DEALER_BBM) 

    cooperativeinc = JML_PH_BRUTO_BUNGA_SIMPANAN_KOPERASI
    finaltax_CooperativeInterest = (rate1_CooperativeInterest * min(cooperativeinc, tbrk1_CooperativeInterest)
                                    + rate2_CooperativeInterest * max(0, cooperativeinc - tbrk1_CooperativeInterest))
    finaltax_CooperativeInterest = max(finaltax_CooperativeInterest,0)

    finaltax_DerivativeTransaction = rate_DerivativeTransaction * max(0, JML_PH_BRUTO_TRANSAKSI_DERIVATIF) 
    finaltax_Dividend = rate_Dividend * max(0, JML_PH_BRUTO_DIVIDEN) 
    #finaltax_WifeIncome = rate_WifeIncome * max(0, JML_PH_BRUTO_PH_ISTRI) 
    wifeinc = max(0, JML_PH_BRUTO_PH_ISTRI)
    
    finaltax_WifeIncome = (rate1_WifeIncome * min(wifeinc, tbrk1_WifeIncome) +
                            rate2_WifeIncome * min(tbrk2_WifeIncome - tbrk1_WifeIncome, max(0., wifeinc - tbrk1_WifeIncome)) +
                            rate3_WifeIncome * min(tbrk3_WifeIncome - tbrk2_WifeIncome, max(0., wifeinc - tbrk2_WifeIncome)) +
                            rate4_WifeIncome * min(tbrk4_WifeIncome - tbrk3_WifeIncome, max(0., wifeinc - tbrk3_WifeIncome)) +
                            rate5_WifeIncome * max(0., wifeinc - tbrk4_WifeIncome))
    finaltax_WifeIncome = max(finaltax_WifeIncome,0)

    finaltax_Other = rate_FinalOther * max(0, JML_PU) 
    
    finaltax_Total = (finaltax_InterestSaving + finaltax_InterestBonds + finaltax_SalesOfStocks 
                      + finaltax_Lottery + finaltax_SeverancePayment + finaltax_Honoraria + finaltax_SalesOfAssets
                      + finaltax_PropertyBOT + finaltax_Rent + finaltax_ConstructionFees + finaltax_FuelDealers
                      + finaltax_CooperativeInterest + finaltax_DerivativeTransaction + finaltax_Dividend 
                      + finaltax_WifeIncome + finaltax_Other)
    finaltax_Total = max(finaltax_Total,0)
    # (finaltax_InterestSaving, finaltax_InterestBonds, finaltax_SalesOfStocks, finaltax_Lottery, 
    # finaltax_SeverancePayment, finaltax_Honoraria, finaltax_SalesOfAssets, finaltax_PropertyBOT, finaltax_Rent,
    # finaltax_ConstructionFees, finaltax_FuelDealers, finaltax_CooperativeInterest, finaltax_DerivativeTransaction, 
    # finaltax_Dividend, finaltax_WifeIncome, finaltax_Other, finaltax_Total) = [0]*17

    finaltax_InterestSaving = 0
    finaltax_InterestBonds = 0
    finaltax_Dividend = 0
     
    final_incomes_at_marginal_rates = JML_PH_BRUTO_DISKONTO_SBI + JML_PH_BRUTO_OBLIGASI + JML_PH_BRUTO_DIVIDEN

    return (finaltax_InterestSaving, finaltax_InterestBonds, finaltax_SalesOfStocks, finaltax_Lottery, 
            finaltax_SeverancePayment, finaltax_Honoraria, finaltax_SalesOfAssets, finaltax_PropertyBOT, finaltax_Rent,
            finaltax_ConstructionFees, finaltax_FuelDealers, finaltax_CooperativeInterest, finaltax_DerivativeTransaction, 
            finaltax_Dividend, finaltax_WifeIncome, finaltax_Other, final_incomes_at_marginal_rates, finaltax_Total)

"Calculation for Total Income"
@iterate_jit(nopython=True)
def cal_Total_Income(JNS_SPT_NUM, JML_PH_NETO_DN_DR_USAHA,JML_PH_NETO_DN_DR_PEKERJAAN_ADJ,JML_PH_NETO_DN_LAINNYA,
                          JML_PH_NETO_LN, JML_PH_NETO, final_incomes_at_marginal_rates, Calculated_Total_Income_1770, Calculated_Total_Income_1770S, Calculated_Total_Income_1770SS, Calculated_Total_Income):
    if (JNS_SPT_NUM == 0):
        JML_PH_NETO_DN_DR_USAHA_NEW = 0
        JML_PH_NETO_DN_LAINNYA_NEW = 0
        JML_PH_NETO_LN_NEW = 0
        
    JML_PH_NETO_DN_DR_USAHA_NEW = max(JML_PH_NETO_DN_DR_USAHA, 0)
    JML_PH_NETO_DN_DR_PEKERJAAN_NEW = max(JML_PH_NETO_DN_DR_PEKERJAAN_ADJ,0)
    JML_PH_NETO_DN_LAINNYA_NEW = max(JML_PH_NETO_DN_LAINNYA,0)
    JML_PH_NETO_LN_NEW = max(JML_PH_NETO_LN,0)
    #JML_PH_BRUTO_FINAL = max(JML_PH_BRUTO_FINAL,0)
    Calculated_Total_Income = JML_PH_NETO_DN_DR_USAHA_NEW + JML_PH_NETO_DN_DR_PEKERJAAN_NEW + JML_PH_NETO_DN_LAINNYA_NEW + JML_PH_NETO_LN_NEW + final_incomes_at_marginal_rates
    if (JNS_SPT_NUM == 0):    
        Calculated_Total_Income_1770SS = JML_PH_NETO_DN_DR_PEKERJAAN_NEW
        Calculated_Total_Income_1770S = 0
        Calculated_Total_Income_1770 = 0
    elif (JNS_SPT_NUM == 1):
        Calculated_Total_Income_1770S = Calculated_Total_Income  
        Calculated_Total_Income_1770SS = 0
        Calculated_Total_Income_1770 = 0
    else:
        Calculated_Total_Income_1770 = Calculated_Total_Income
        Calculated_Total_Income_1770S = 0
        Calculated_Total_Income_1770SS= 0
    return (Calculated_Total_Income_1770SS, Calculated_Total_Income_1770S, Calculated_Total_Income_1770, Calculated_Total_Income)

"Calculation for Income after Zakat or Compulsory Religious Donation"
"1770SS is not allowed to deduct zakat"
@iterate_jit(nopython=True)
def cal_Income_After_Zakat(JNS_SPT_NUM, JML_ZAKAT, JML_PH_NETO_STLH_ZAKAT, 
                           Calculated_Total_Income_1770SS, Calculated_Total_Income_1770S, Calculated_Total_Income_1770, 
                           Calculated_Income_After_Zakat_1770SS, Calculated_Income_After_Zakat_1770S, Calculated_Income_After_Zakat_1770, 
                           Calculated_Total_Income, Calculated_Income_After_Zakat):
    if (JNS_SPT_NUM == 0):
        JML_ZAKAT_NEW = 0
        Calculated_Income_After_Zakat_1770SS = Calculated_Total_Income_1770SS - JML_ZAKAT_NEW
        #Calculated_Income_After_Zakat_1770SS = 0
        Calculated_Income_After_Zakat_1770S = 0
        Calculated_Income_After_Zakat_1770 = 0
    elif (JNS_SPT_NUM == 1):
        JML_ZAKAT_NEW = np.nan_to_num(JML_ZAKAT) 
        Calculated_Income_After_Zakat_1770S = Calculated_Total_Income_1770S - JML_ZAKAT_NEW
        Calculated_Income_After_Zakat_1770SS = 0
        Calculated_Income_After_Zakat_1770 = 0
    else :
        JML_ZAKAT_NEW = np.nan_to_num(JML_ZAKAT) 
        Calculated_Income_After_Zakat_1770 = Calculated_Total_Income_1770 - JML_ZAKAT_NEW
        Calculated_Income_After_Zakat_1770S = 0
        Calculated_Income_After_Zakat_1770SS = 0
    Calculated_Income_After_Zakat = Calculated_Total_Income - JML_ZAKAT_NEW
    Calculated_Income_After_Zakat = max(Calculated_Income_After_Zakat, 0)
    
    #JML_PH_NETO_STLH_ZAKAT_NEW = np.nan_to_num(JML_PH_NETO_STLH_ZAKAT) 
    #Calculated_Income_After_Zakat = JML_PH_NETO_STLH_ZAKAT_NEW
    return (Calculated_Income_After_Zakat_1770SS, Calculated_Income_After_Zakat_1770S, 
            Calculated_Income_After_Zakat_1770, Calculated_Income_After_Zakat)

"Calculation for Income after Loss Carry Forward"
@iterate_jit(nopython=True)
def cal_Income_After_LCF(JNS_SPT_NUM, JML_KOM_RUGI, Calculated_Income_After_Zakat, 
                         Calculated_Income_After_Zakat_1770SS, Calculated_Income_After_Zakat_1770S, Calculated_Income_After_Zakat_1770, 
                         Calculated_Income_After_LCF_1770SS, Calculated_Income_After_LCF_1770S, Calculated_Income_After_LCF_1770, 
                         Calculated_Income_After_LCF): 
    if (JNS_SPT_NUM == 0):
        JML_KOM_RUGI_NEW = 0
        Calculated_Income_After_LCF_1770SS = Calculated_Income_After_Zakat_1770SS - JML_KOM_RUGI_NEW
        #Calculated_Income_After_LCF_1770SS = 0
        Calculated_Income_After_LCF_1770S = 0
        Calculated_Income_After_LCF_1770 = 0
    elif (JNS_SPT_NUM == 1):
        #JML_KOM_RUGI_NEW = 0
        JML_KOM_RUGI_NEW = np.nan_to_num(JML_KOM_RUGI) 
        Calculated_Income_After_LCF_1770S = Calculated_Income_After_Zakat_1770S - JML_KOM_RUGI_NEW
        #Calculated_Income_After_LCF_1770S = 0
        Calculated_Income_After_LCF_1770SS = 0
        Calculated_Income_After_LCF_1770 = 0
    else :
        JML_KOM_RUGI_NEW = np.nan_to_num(JML_KOM_RUGI) 
        Calculated_Income_After_LCF_1770 = Calculated_Income_After_Zakat_1770 - JML_KOM_RUGI_NEW
        Calculated_Income_After_LCF_1770S = 0
        Calculated_Income_After_LCF_1770SS = 0   
    Calculated_Income_After_LCF = Calculated_Income_After_Zakat - JML_KOM_RUGI_NEW
    Calculated_Income_After_LCF = max(Calculated_Income_After_LCF, 0)
    return (Calculated_Income_After_LCF_1770SS, Calculated_Income_After_LCF_1770S, 
            Calculated_Income_After_LCF_1770, Calculated_Income_After_LCF)

"Calculation for Personal Exemptions"
@iterate_jit(nopython=True)
def cal_Personal_Exemptions(ptkp_self, ptkp_marriage, ptkp_dependant, max_dependant_allowed, 
                            JNS_SPT_NUM, JML_PTKP, FG_PTKP, JML_TANGGUNGAN, 
                            Calculated_Personal_Exemptions_1770SS, Calculated_Personal_Exemptions_1770S, 
                            Calculated_Personal_Exemptions_1770, Calculated_Personal_Exemptions):
    JML_TANGGUNGAN_NEW = np.nan_to_num(JML_TANGGUNGAN)    
    FG_PTKP_NEW = np.nan_to_num(FG_PTKP)
    #FG_PTKP_NEW = FG_PTKP
    JML_PTKP_NEW = np.nan_to_num(JML_PTKP)    
    if (FG_PTKP_NEW == 0) and (JML_TANGGUNGAN_NEW <=  max_dependant_allowed):
        Calculated_Personal_Exemptions = ptkp_self + (JML_TANGGUNGAN_NEW * ptkp_dependant)
    elif (FG_PTKP_NEW == 0) and (JML_TANGGUNGAN_NEW >  max_dependant_allowed):
        Calculated_Personal_Exemptions = ptkp_self + (max_dependant_allowed * ptkp_dependant)
    elif (FG_PTKP_NEW == 1) and (JML_TANGGUNGAN_NEW <=  max_dependant_allowed):
         Calculated_Personal_Exemptions = ptkp_self + ptkp_marriage + (JML_TANGGUNGAN_NEW * ptkp_dependant)  
    elif (FG_PTKP_NEW == 1) and (JML_TANGGUNGAN_NEW >  max_dependant_allowed):
        Calculated_Personal_Exemptions = ptkp_self + ptkp_marriage + (max_dependant_allowed * ptkp_dependant)
    elif (FG_PTKP_NEW == -1) and (JML_TANGGUNGAN_NEW <=  max_dependant_allowed):
        Calculated_Personal_Exemptions = ptkp_self + ptkp_marriage + (JML_TANGGUNGAN_NEW * ptkp_dependant)  
    elif (FG_PTKP_NEW == -1) and (JML_TANGGUNGAN_NEW >  max_dependant_allowed):
         Calculated_Personal_Exemptions = ptkp_self + ptkp_marriage + (max_dependant_allowed * ptkp_dependant)
    elif (FG_PTKP_NEW == 2) and (JML_TANGGUNGAN_NEW <=  max_dependant_allowed):
          Calculated_Personal_Exemptions = ptkp_self + ptkp_self + ptkp_marriage + (JML_TANGGUNGAN_NEW * ptkp_dependant)  
    elif (FG_PTKP_NEW == 2) and (JML_TANGGUNGAN_NEW >  max_dependant_allowed):
         Calculated_Personal_Exemptions = ptkp_self + ptkp_self + ptkp_marriage + (max_dependant_allowed * ptkp_dependant)
    else:
         #Calculated_Personal_Exemptions = ptkp_self + ptkp_marriage + (max_dependant_allowed * ptkp_dependant)  
         Calculated_Personal_Exemptions = JML_PTKP_NEW
    if (JNS_SPT_NUM == 0):
      Calculated_Personal_Exemptions_1770SS = Calculated_Personal_Exemptions
      Calculated_Personal_Exemptions_1770S = 0
      Calculated_Personal_Exemptions_1770 = 0
    elif (JNS_SPT_NUM == 1):
      Calculated_Personal_Exemptions_1770S = Calculated_Personal_Exemptions
      Calculated_Personal_Exemptions_1770SS = 0
      Calculated_Personal_Exemptions_1770 = 0
    else:
      Calculated_Personal_Exemptions_1770 = Calculated_Personal_Exemptions
      Calculated_Personal_Exemptions_1770S = 0
      Calculated_Personal_Exemptions_1770SS = 0       
    #Calculated_Personal_Exemptions = JML_PTKP_NEW
    return (Calculated_Personal_Exemptions_1770SS, Calculated_Personal_Exemptions_1770S, Calculated_Personal_Exemptions_1770, 
            Calculated_Personal_Exemptions)


"Calculation for Taxable Income"

@iterate_jit(nopython=True)
def cal_Taxable_Income(JNS_SPT_NUM, Calculated_Income_After_LCF, Calculated_Personal_Exemptions, 
                       Calculated_Taxable_Income_1770SS, Calculated_Taxable_Income_1770S, 
                       Calculated_Taxable_Income_1770, Calculated_Taxable_Income):
    if Calculated_Income_After_LCF - Calculated_Personal_Exemptions <= 0:
        Calculated_Taxable_Income = 0
    else: Calculated_Taxable_Income = Calculated_Income_After_LCF - Calculated_Personal_Exemptions
    if (JNS_SPT_NUM == 0):
      Calculated_Taxable_Income_1770SS = Calculated_Taxable_Income
      Calculated_Taxable_Income_1770S = 0
      Calculated_Taxable_Income_1770 = 0
    elif (JNS_SPT_NUM == 1):
      Calculated_Taxable_Income_1770S = Calculated_Taxable_Income
      Calculated_Taxable_Income_1770SS = 0
      Calculated_Taxable_Income_1770 = 0
    else:
      Calculated_Taxable_Income_1770 = Calculated_Taxable_Income
      Calculated_Taxable_Income_1770S = 0
      Calculated_Taxable_Income_1770SS = 0       
    Calculated_Taxable_Income = max(Calculated_Taxable_Income,0)
    return (Calculated_Taxable_Income_1770SS, Calculated_Taxable_Income_1770S, 
            Calculated_Taxable_Income_1770, Calculated_Taxable_Income)


"Calculation for Income Tax Payable"
@iterate_jit(nopython=True)
def cal_pit(rate1, rate2, rate3, rate4, rate5, tbrk1, tbrk2, tbrk3, tbrk4, 
            JNS_SPT_NUM, Calculated_Taxable_Income, pitax_1770SS, pitax_1770S, pitax_1770, op_tax):
    """
    Compute tax liability given the progressive tax rate schedule specified
    by the (marginal tax) rate* and (upper tax bracket) brk* parameters and
    given taxable income (taxinc)
    """
    # subtract TI_special_rates from TTI to get Aggregate_Income, which is
    # the portion of TTI that is taxed at normal rates
    
    taxinc = Calculated_Taxable_Income
    
    op_tax = (rate1 * min(taxinc, tbrk1) +
             rate2 * min(tbrk2 - tbrk1, max(0., taxinc - tbrk1)) +
             rate3 * min(tbrk3 - tbrk2, max(0., taxinc - tbrk2)) +
             rate4 * min(tbrk4 - tbrk3, max(0., taxinc - tbrk3)) +
             rate5 * max(0., taxinc - tbrk4))
    if (JNS_SPT_NUM == 0):
      pitax_1770SS = op_tax
      pitax_1770S = 0
      pitax_1770 = 0
    elif (JNS_SPT_NUM == 1):
      pitax_1770S = op_tax
      pitax_1770 = 0
      pitax_1770SS = 0
    else:
      pitax_1770 = op_tax
      pitax_1770S = 0
      pitax_1770SS = 0               
    return (pitax_1770SS, pitax_1770S, pitax_1770, op_tax)

    
"Calculation for Total Tax"
@iterate_jit(nopython=True)
def cal_tax_total(op_tax, finaltax_Total, pitax):
    pitax = op_tax+ finaltax_Total
    return (pitax)
    
    
    
    
    
    
    
    