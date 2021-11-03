# -*- coding: utf-8 -*-
"""
Created on Sat Oct 30 11:38:48 2021

@author: Powis Forjoe
"""

###############################################################################
# IMPORT LIBRARIES                                                            #
###############################################################################
from AssetAllocation.datamanger import datamanger as dm
from AssetAllocation.analytics import summary
from AssetAllocation.reporting import plots, reports as rp
# import matplotlib.pyplot as plt
import numpy as np
import stochMV as stMV
import seaborn as sns

PLAN = 'IBT'

###############################################################################
# COMPUTE PLAN INPUTS                                                         #
###############################################################################
#get return
mv_inputs_dict = dm.get_mv_inputs_data('inputs_test.xlsx', plan=PLAN)
mv_inputs = summary.get_mv_inputs(mv_inputs_dict)
#get historical vol and correlation
ts_dict = dm.get_ts_data(plan=PLAN)
pp_inputs = summary.get_pp_inputs(mv_inputs, ts_dict)

###############################################################################
# INITIALIZE PLAN                                                             #
###############################################################################
plan = summary.get_plan_params(pp_inputs)
pp_dict = plan.get_pp_dict()

###############################################################################
# INITIALIZE STOCHMV                                                          #
###############################################################################
#initialize the stochastic mean variance
s = stMV.stochMV(plan, 120)
#generate the random returns Aand sample corr
s.generate_plans()
s.generate_resamp_corr_dict()
###############################################################################
# VIEW CORRELATIONS                                                           #
###############################################################################
for key in s.resamp_corr_dict:
    resamp_corr_fig = plots.get_resamp_corr_fig(s.resamp_corr_dict[key], key)
    resamp_corr_fig.show()
    
###############################################################################
# VIEW  RETURNS                                                               #
###############################################################################
#visualize the simulated returns
sns.pairplot(s.returns_df, corner=True)
# plt.savefig("sampling.jpeg")

###############################################################################
# DEFINE BOUNDS                                                               #
###############################################################################
bnds = dm.get_bounds(plan=PLAN)

###############################################################################
# DEFINE CONSTRAINTS TO OPTIMIZE FOR MIN AND MAX RETURN                       #
###############################################################################
cons = (
        # 45% <= sum of Fixed Income Assets <= 55%
        {'type': 'ineq', 'fun': lambda x: np.sum(x[1:3]) - 0.45},
        {'type': 'ineq', 'fun': lambda x: .55 - np.sum(x[1:3])},
        #sum of all plan assets (excluding Futures and Hedges) = Funded Status Difference    
        {'type': 'eq', 'fun': lambda x: np.sum(x[0:len(s.init_plan)-1]) - x[3] - (1-s.init_plan.funded_status)},
        # 50% of Equity and PE >= Hedges
        {'type': 'ineq', 'fun': lambda x: (x[4]+x[6])*.5 - x[len(s.init_plan)-1]},
        # STRIPS >= sum(50% of Futures and 25% of Hedges)
        {'type': 'ineq', 'fun': lambda x: x[1] - (x[3]/2+x[len(plan)-1]/4)}
        )

###############################################################################
# COMPUTE MV EFFICIENT FRONTIER PORTFOLIOS                                    #
###############################################################################
#Get data for MV efficient frontier portfolios
s.generate_efficient_frontiers(bnds, cons,num_ports=100)

###############################################################################
# DISPLAY MV ASSET ALLOCATION                                                 #
###############################################################################
#Asset Allocation Plot
aa_fig = plots.get_aa_fig(s.opt_ports_df)
aa_fig.show()

###############################################################################
# DISPLAY MV EFFICIENT FRONTIER                                               #
###############################################################################
#Plotly version of the Efficient Frontier plot
ef_fig = plots.get_ef_fig(s.opt_ports_df)
ef_fig.show()

###############################################################################
# EXPORT DATA TO EXCEL                                                        #
###############################################################################
#Export Efficient Frontier portfoio data to excel
rp.get_stochmv_ef_portfolios_report(PLAN+' stochmv_ef_report', s)