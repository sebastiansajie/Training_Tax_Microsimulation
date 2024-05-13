"""
app1.py illustrates use of pitaxcalc-demo release 2.0.0 (India version).
USAGE: python app2.py
"""
import pandas as pd
import json
import copy

# data_filename = "pit21.csv"
# weights_filename = "pit21_weights.csv"
# records_variables_filename = "records_variables_pit_indo.json"
# cit_data_filename = "cit_cross.csv"
# cit_weights_filename = "cit_cross_wgts1.csv"
# corprecords_variables_filename = "corprecords_variables.json"
# gst_data_filename = "gst.csv"
# gst_weights_filename = "gst_weights.csv"
# gstrecords_variables_filename = "gstrecords_variables.json"         
# policy_filename = "current_law_policy_pit_indo.json"
# growfactors_filename = "growfactors_pit_indo.csv"           
# benchmark_filename = "tax_incentives_benchmark.json"
# functions_filename = "functions_pit_indo.py"
# function_names = "function_names_pit_indo.json"
# start_year = 2021
# end_year=2028
# SALARY_VARIABLE = "SALARY"
# elasticity_filename = "elasticity_pit_srilanka.json"

"""
vars = {}
vars['DEFAULTS_FILENAME'] = policy_filename        
vars['GROWFACTORS_FILENAME'] = growfactors_filename
vars['pit_data_filename'] = data_filename
vars['pit_weights_filename'] = weights_filename
vars['records_variables_filename'] = records_variables_filename        
vars['cit_data_filename'] = cit_data_filename
vars['cit_weights_filename'] = cit_weights_filename
vars['corprecords_variables_filename'] = corprecords_variables_filename
vars['gst_data_filename'] = gst_data_filename
vars['gst_weights_filename'] = gst_weights_filename
vars['gstrecords_variables_filename'] = gstrecords_variables_filename        
vars['benchmark_filename'] = benchmark_filename
vars['functions_filename'] = functions_filename
vars['function_names'] = function_names
vars["start_year"] = start_year
vars["end_year"] = end_year
vars["SALARY_VARIABLE"] = SALARY_VARIABLE
vars['elasticity_filename'] = elasticity_filename
"""
vars = {}
vars['pit'] = 1
vars['cit'] = 0
vars['vat'] = 0
vars['DEFAULTS_FILENAME'] = "current_law_policy_pit_indo.json"
vars['GROWFACTORS_FILENAME'] = "growfactors_pit_indo.csv" 
#self.vars['pit_data_filename'] = "pit_sample_2021_small_w_appendix.csv"
#vars['pit_data_filename'] = "pit21_with_final_tax_2.csv"    
vars['pit_data_filename'] = "pit_sample_2021_with_final_tax.csv"    
#vars['pit_data_filename'] = "pit21_sample_small_2021_with_final_tax.csv"    
#self.vars['pit_weights_filename'] = "pit_weight_indo.csv"
#vars['pit_weights_filename'] = "pit21_with_final_tax_weights.csv"
vars['pit_weights_filename'] = "pit21_sample_2021_with_final_tax_weights_calibrated.csv"
#vars['pit_weights_filename'] = "pit21_sample_small_2021_with_final_tax_weights.csv"
vars['pit_records_variables_filename'] = "records_variables_pit_indo.json"
vars['pit_benchmark_filename'] = "tax_incentives_benchmark_pit_srilanka.json"
vars['pit_elasticity_filename'] = "elasticity_pit_srilanka.json"
vars['pit_functions_filename'] = "functions_pit_indo.py"
#vars['pit_functions_filename'] = "functions_pit_indo_marginal_1.py"
#vars['pit_functions_filename'] = "functions_pit_indo_without_final.py"
vars['pit_function_names_filename'] = "function_names_pit_indo.json"
vars['pit_distribution_json_filename'] = 'pit_distribution_indo.json'
vars['gdp_filename'] = 'gdp_nominal_srilanka.csv'  

# vars['DEFAULTS_FILENAME'] = "current_law_policy_pit_srilanka.json"
# vars['GROWFACTORS_FILENAME'] = "growfactors_pit_srilanka.csv"
# vars['pit_data_filename'] = "pit_srilanka.csv"
# vars['pit_weights_filename'] = "pit_weights_srilanka.csv"
# vars['pit_records_variables_filename'] = "records_variables_pit_srilanka.json"
# vars['pit_benchmark_filename'] = "tax_incentives_benchmark_pit_training.json"
# vars['pit_elasticity_filename'] = "elasticity_pit_training.json"
# vars['pit_functions_filename'] = "functions_pit_srilanka.py"
# vars['pit_function_names_filename'] = "function_names_pit_srilanka.json"
# vars['pit_distribution_json_filename'] = 'pit_distribution_srilanka.json'  
# vars['gdp_filename'] = 'gdp_nominal_training.csv'

vars['cit_data_filename'] = "cit_data_training.csv"
vars['cit_weights_filename'] = "cit_weights_training.csv"
vars['cit_records_variables_filename'] = "records_variables_cit_training.json"    
vars['cit_benchmark_filename'] = "tax_incentives_benchmark_cit.json"
vars['cit_elasticity_filename'] = "elasticity_cit_training.json"
vars['cit_functions_filename'] = "functions_cit_training.py"
vars['cit_function_names_filename'] = "function_names_cit_training.json"
vars['cit_distribution_json_filename'] = 'cit_distribution_training.json'

vars['cit_max_lag_years'] = 10

vars['vat_data_filename'] = "vat.csv"
vars['vat_weights_filename'] = "vat_weights.csv"
vars['vat_records_variables_filename'] = "vat_records_variables.json"   
vars['vat_benchmark_filename'] = "vat_tax_incentives_benchmark.json"
vars['vat_elasticity_filename'] = "vat_elasticity_macedonia.json"
vars['vat_functions_filename'] = "vat_functions.py"
vars['vat_function_names_filename'] = "vat_function_names.json"
vars['vat_distribution_json_filename'] = 'vat_distribution.json'
#vars['kakwani_list'] = []
vars['start_year'] = 2021
vars['end_year']=2028
vars['data_start_year'] = 2021
vars['pit_data_start_year'] = 2021
vars['cit_data_start_year'] = 2020
vars['vat_data_start_year'] = 2020
vars['show_error_log'] = 0
vars['verbose'] = 1
vars['SALARY_VARIABLE'] = "JML_PH_NETO_DN_DR_PEKERJAAN"
vars['pit_id_var'] = 'NPWP'

with open('global_vars.json', 'w') as f:
    f.write(json.dumps(vars, indent=2))
    
with open('global_vars.json', 'w') as f:
    json.dump(vars, f)

#from taxcalc import *
from taxcalc.growfactors import GrowFactors
from taxcalc.policy import Policy
from taxcalc.records import Records
#from taxcalc.gstrecords import GSTRecords
#from taxcalc.corprecords import CorpRecords
from taxcalc.parameters import ParametersBase
from taxcalc.calculator import Calculator
from taxcalc.utils import dist_variables
# create Records object containing pit.csv and pit_weights.csv input data
recs = Records()

# create Records object containing pit.csv and pit_weights.csv input data
#grecs = GSTRecords()

# create CorpRecords object containing cit.csv and cit_weights.csv input data
#crecs = CorpRecords()

# create Policy object containing current-law policy
pol = Policy()

# specify Calculator object for current-law policy
#calc1 = Calculator(policy=pol, records=recs, gstrecords=grecs,
#                   corprecords=crecs, verbose=False)

calc1 = Calculator(policy=pol, records=recs, verbose=False)
#calc1.adjust_behavior('SALARY', elasticity_dict)
# specify Calculator object for reform in JSON file
#reform = Calculator.read_json_param_objects('app_reform_srilanka.json', None)
#print(reform)
#pol2 = Policy()
#pol2.implement_reform(reform['policy'])
#calc2 = Calculator(policy=pol2, records=recs, verbose=False)
#calc2.adjust_behavior('SALARY', elasticity_dict)
      
# loop through years 2017, 2018, and 2019 and print out pitax
for year in range(2021, 2028):
    calc1.advance_to_year(year)
    #calc2.advance_to_year(year)
    calc1.calc_all()
    #calc2.calc_all()
    weighted_tax1 = calc1.weighted_total_pit('op_tax')
    weighted_tax2 = calc1.weighted_total_pit('finaltax_InterestSaving')    
    weighted_tax3 = calc1.weighted_total_pit('finaltax_InterestBonds')    
    weighted_tax4 = calc1.weighted_total_pit('finaltax_SalesOfStocks')    
    weighted_tax5 = calc1.weighted_total_pit('finaltax_Lottery')    
    weighted_tax6 = calc1.weighted_total_pit('finaltax_SeverancePayment')    
    weighted_tax7 = calc1.weighted_total_pit('finaltax_Honoraria')    
    weighted_tax8 = calc1.weighted_total_pit('finaltax_SalesOfAssets')    
    weighted_tax9 = calc1.weighted_total_pit('finaltax_PropertyBOT')    
    weighted_tax10 = calc1.weighted_total_pit('finaltax_Rent')    
    weighted_tax11 = calc1.weighted_total_pit('finaltax_ConstructionFees')    
    weighted_tax12 = calc1.weighted_total_pit('finaltax_FuelDealers')    
    weighted_tax13 = calc1.weighted_total_pit('finaltax_CooperativeInterest')    
    weighted_tax14 = calc1.weighted_total_pit('finaltax_DerivativeTransaction')    
    weighted_tax15 = calc1.weighted_total_pit('finaltax_Dividend')    
    weighted_tax16 = calc1.weighted_total_pit('finaltax_WifeIncome')    
    weighted_tax17 = calc1.weighted_total_pit('finaltax_Other')    
    weighted_tax18 = calc1.weighted_total_pit('finaltax_Total')    
    weighted_tax19 = calc1.weighted_total_pit('pitax')
    weighted_tax20 = calc1.weighted_total_pit('JML_PPH_TERUTANG')
    weighted_tax21 = calc1.weighted_total_pit('JML_PPH_TERUTANG_FINAL')
    weighted_tax22 = calc1.weighted_total_pit('JML_PPH_TERUTANG_DISKONTO_SBI')    
    weighted_tax23 = calc1.weighted_total_pit('JML_PPH_FINAL_DIBYR')    
    #weighted_tax2 = calc2.weighted_total_pit('pitax')    
    #calc2_behv = copy.deepcopy(calc2)
    #print("without reform: ",calc1.array('SALARY'))
    #print("before adj: ",calc2.array('SALARY'))
    first_year=2021
    #print("starting behavior adjustment")
    #calc2_behv.adjust_behavior(first_year=2019, elasticity_filename=elasticity_filename)
    # Recalculate post-reform taxes incorporating behavioral responses
    #calc2_behv.calc_all()
    #weighted_tax3 = calc2_behv.weighted_total_pit('pitax')
    total_weights = calc1.total_weight_pit()
    print(f'Calculated OP Tax for {year}: {weighted_tax1 * 1e-12:,.2f} trill.')
    print(f'Calculated Total Final Tax for {year}: {weighted_tax18 * 1e-12:,.2f} trill.')
    print(f'Calculated Total Tax for {year}: {weighted_tax19 * 1e-12:,.2f} trill.')
    print(f'Total OP Tax for {year}: {weighted_tax20 * 1e-12:,.2f} trill.')
    print(f'Total Final Tax for {year}: {weighted_tax21 * 1e-12:,.2f} trill.')
    print(f'Total Taxpayers for {year}: {total_weights * 1e-6:,.1f} millions')

    print("################################")
    print(f'Final Tax on INTEREST OF DEPOSIT, SAVINGS, DISCOUNT ON BANK INDONESIA CERTIFICATES, STATE SECURITIES for {year}: {weighted_tax2 * 1e-12:,.2f} trill.')
    print(f'Final Tax on INTEREST from dataset for {year}: {weighted_tax22 * 1e-12:,.2f} trill.')
    print(f'Final Tax on INTEREST/DISCOUNT OF BOND for {year}: {weighted_tax3 * 1e-12:,.2f} trill.')
    print(f'Final Tax on SALES OF SHARES TRADED IN THE STOCK EXCHANGE for {year}: {weighted_tax4 * 1e-12:,.2f} trill.')
    print(f'Final Tax on LOTTERY PRIZES for {year}: {weighted_tax5 * 1e-12:,.2f} trill.')
    print(f'Final Tax on SEVERANCE PAYMENT, RETIREMENT ALLOWANCE AND PENSIONS PAID IN LUMP SUM for {year}: {weighted_tax6 * 1e-12:,.2f} trill.')
    print(f'Final Tax on HONORARIA DERIVED FROM STATE AND/OR LOCAL BUDGET for {year}: {weighted_tax7 * 1e-12:,.2f} trill.')
    print(f'Final Tax on TRANSFERS OF RIGHTS ON LAND AND BUILDING for {year}: {weighted_tax8 * 1e-12:,.2f} trill.')
    print(f'Final Tax on PROPERTY RECEIVED FROM BUILD OPERATE TRANSFER SCHEME for {year}: {weighted_tax9 * 1e-12:,.2f} trill.')
    print(f'Final Tax on LEASE/RENT ON LAND OR BUILDING for {year}: {weighted_tax10 * 1e-12:,.2f} trill.')
    print(f'Final Tax on CONSTRUCTION FEES for {year}: {weighted_tax11 * 1e-12:,.2f} trill.')
    print(f'Final Tax on DISTRIBUTOR/DEALER/AGENTS OF FUEL PRODUCTS for {year}: {weighted_tax12 * 1e-12:,.2f} trill.')
    print(f'Final Tax on SAVING INTEREST PAID BY COOPERATIVE TO ITS INDIVIDUAL MEMBER for {year}: {weighted_tax13 * 1e-12:,.2f} trill.')
    print(f'Final Tax on INCOME FROM DERIVATIVE TRANSACTION for {year}: {weighted_tax14 * 1e-12:,.2f} trill.')
    print(f'Final Tax on INCOME FROM DIVIDEND for {year}: {weighted_tax15 * 1e-12:,.2f} trill.')
    print(f'Final Tax on INCOME FROM WIFE INCOME FROM ONE EMPLOYER for {year}: {weighted_tax16 * 1e-12:,.2f} trill.')
    print(f'Final Tax on OTHER INCOME SUBJECT TO FINAL TAX AND OR FINAL IN NATURE for {year}: {weighted_tax17 * 1e-12:,.2f} trill.')
    print(f'Final Tax on OTHER INCOME from data set {year}: {weighted_tax23 * 1e-12:,.2f} trill.')
    print(f'Total Final Tax for {year}: {weighted_tax18 * 1e-12:,.2f} trill.')
    print("################################")
    #print(f'Total Tax for {year}: {weighted_tax19 * 1e-12:,.2f} trill.')
    #print(f'Tax 2 for {year}: {weighted_tax2 * 1e-9:,.2f}')
    #print(f'Tax 2 for {year} Adjusted: {weighted_tax3 * 1e-9:,.2f}')    
    #print(calc1.array('pitax'))
    #print(calc2.array('pitax'))
    #print(calc2_behv.array('pitax'))

# dump_vars = ['NPWP', 'JML_PH_NETO',  'JML_PH_BRUTO_DISKONTO_SBI', 'JML_PH_BRUTO_OBLIGASI',
#              'JML_PH_BRUTO_PENJUALAN_SAHAM','JML_PH_BRUTO_HADIAH_UNDIAN',
#              'JML_PH_BRUTO_PESANGON','JML_PH_BRUTO_HONORARIUM_APBN',
#              'JML_PH_BRUTO_PHTB','JML_PH_BRUTO_BANGUN_GUNA_SERAH',
#              'JML_PH_BRUTO_SEWA_TANAH_BANGUNAN', 'JML_PH_BRUTO_USAHA_JASKON',
#              'JML_PH_BRUTO_DEALER_BBM','JML_PH_BRUTO_BUNGA_SIMPANAN_KOPERASI',
#              'JML_PH_BRUTO_TRANSAKSI_DERIVATIF','JML_PH_BRUTO_DIVIDEN',
#              'JML_PH_BRUTO_PH_ISTRI','JML_PROFIT_SB','JML_PH_BRUTO_FINAL', 
#              'TOTAL_INCOME_WITH_FINAL', 'finaltax_InterestSaving',     
#              'finaltax_InterestBonds', 'finaltax_SalesOfStocks',  'finaltax_Lottery' ,
#              'finaltax_SeverancePayment' ,'finaltax_Honoraria' , 'finaltax_SalesOfAssets'    ,
#              'finaltax_PropertyBOT'    ,   'finaltax_Rent'    ,
#              'finaltax_ConstructionFees'    ,   'finaltax_FuelDealers'    ,   'finaltax_CooperativeInterest',
#              'finaltax_DerivativeTransaction'    ,   'finaltax_Dividend'    ,   'finaltax_WifeIncome',    
#              'finaltax_Other', 'op_tax', 'finaltax_Total', 'pitax']
# dumpdf = calc1.dataframe(dump_vars)
# column_order = dumpdf.columns

# assert len(dumpdf.index) == calc1.array_len

# dumpdf.to_csv('app0-dump.csv', columns=column_order,
#               index=False, float_format='%.0f')