# -*- coding: utf-8 -*-
"""
Created on Fri Mar  4 17:06:20 2022

@author: RRQ1FYQ
"""

from AssetAllocation.datamanger import datamanger as dm
from AssetAllocation.analytics.liability_model import liabilityModel
import AssetAllocation.reporting.sheets as sheets
import AssetAllocation.reporting.reports as rp

import pandas as pd
import numpy as np
from scipy.optimize import fsolve

############################################################################################################################################################
# FUNCTIONS FOR COMPUTING LIAB RETURN                                                         
############################################################################################################################################################

def compute_pvs(pbo_cashflows, disc_factors, liab_curve=pd.DataFrame,disc_rates=pd.DataFrame):
    if disc_rates.empty:
        pv_dict={}
        for col in liab_curve.columns:
            temp_pv = 0
            for j in range (0,len(pbo_cashflows)):
                temp_pv += (pbo_cashflows[j]/((1+liab_curve[col][j]/100)**disc_factors[j]))
            pv_dict[col] = temp_pv
        return pd.DataFrame(pv_dict, index = ['Present Value']).transpose()
    else:
        disc_rates_pv_array = np.zeros(len(disc_rates))
        for i in range(len(disc_rates)):
            for j in range (0,len(pbo_cashflows)):
                disc_rates_pv_array[i] += (pbo_cashflows[j]/((1+disc_rates['IRR'][i])**disc_factors[j]))
            
        return pd.DataFrame(disc_rates_pv_array, columns=['Present Value'], index=disc_rates.index)
    
def npv(irr, cfs, yrs):  
    return np.sum(cfs / (1. + irr) ** yrs)

def irr(cfs, yrs, x0, **kwargs):
    return np.asscalar(fsolve(npv, x0=x0,args=(cfs,yrs), **kwargs))

def compute_irr(present_values,pbo_cashflows, disc_factors):
    irr_array = np.zeros(len(present_values))
    for j in range (len(present_values)):
        cashflows = np.append(np.negative(present_values['Present Value'][j]),pbo_cashflows)
        yrs = np.append(0, disc_factors)
        irr_array[j] += irr(cashflows, yrs, .03)
    return pd.DataFrame(irr_array, columns=['IRR'], index=present_values.index)

def compute_liab_ret(present_values, irr_df):
    liab_ret = np.zeros(len(present_values))

    for i in range (0,len(present_values)-1):
        liab_ret[i+1] += irr_df['IRR'][i]/12 + ((present_values['Present Value'][i+1])/present_values['Present Value'][i])-1
        
    return pd.DataFrame(liab_ret, columns=['Liability'], index=present_values.index)

def offset(pbo_cfs):
    #make a copy of the data
    data = pbo_cfs.copy()

    #loop through each period and offset first n rows of 0's to the end
    for i in range(0,len(data.columns)):
        #get discount factor for the period
        disc_rate = i+1
        #make a list of the cashflows
        cfs = list(data.iloc[:,i])
        #removes top discount amount of rows and adds to the bottom of the list
        cfs = cfs[disc_rate:] + cfs[:disc_rate] 
        #replaces column with new offset data
        data.iloc[:,i] = cfs
    return(data)

def get_liab_cfs(filename='UPS PBO Cash Flows YE18 to YE21 V5.xlsx',  plan_list = ['Retirement','Pension','IBT']):
    filepath = dm.TS_FP+filename
    data_dict = {}
    for key in plan_list:
        data_dict[key] = pd.read_excel(filepath, sheet_name = key, index_col=0)
        data_dict[key] = offset(data_dict[key])
            
    return(data_dict)

def get_pbo_plan(irr, pbo_cashflows ,plan= 'Retirement'):
    #get pbo cfs for specified plan
    cfs = pbo_cashflows[plan]
    #get yrs
    yrs = list(range(1,len(cfs)+1))
    plan_irr = irr[plan]
    pbo = []
    for i in list(range(0,len(cfs.columns))):
        month_irr = plan_irr.loc[cfs.columns[i]]/12
        month_cfs = list(cfs.iloc[:,i])
        pbo.append( npv(month_irr,month_cfs,yrs))
    return pbo

def get_liab_mv(irr, pbo_cashflows ,plan_list = ['Retirement','Pension','IBT']):
    df = pd.DataFrame()
    for plan in plan_list:
        #get pbo cfs for specified plan
        cfs = pbo_cashflows[plan]
        #get yrs
        yrs = list(range(1,len(cfs)+1))
        plan_irr = irr[plan]
        pbo = []
        for i in list(range(0,len(cfs.columns))):
            month_irr = plan_irr.loc[cfs.columns[i]]/12
            month_cfs = list(cfs.iloc[:,i])
            pbo.append( npv(month_irr,month_cfs,yrs))
        df[plan] = pbo
        df.set_index(pbo_cashflows['Retirement'].columns,inplace=True)
    return df



############################################################################################################################################################
#                                                            
############################################################################################################################################################
plan_list = ['Retirement','Pension','IBT']
pbo_cashflows = get_liab_cfs()

irr = pd.read_excel("C:/Users/RRQ1FYQ/Documents/UPS_MV/data/time_series/UPS PBO Cash Flows YE18 to YE21 V5.xlsx",sheet_name="irr_ftse" ,index_col=0)

pbo_df = get_liab_mv(irr, pbo_cashflows)

retirement_pbo = get_pbo_plan(irr, pbo_cashflows, plan = 'Retirement')
#todo: change get_pbo to plan list
#todo: change name of pbo to get liability mv
#todo change pbo list to pbo data frame with dates in the columns