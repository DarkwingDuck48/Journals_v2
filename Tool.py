import json
import os
import time


# Structures in HFM
# MovProd
PR_07 = ["PR_"+str(x) for x in range(28, 67) if x not in [28, 37, 42, 46, 53, 59]]
PR_04 = ["PR_05", "PR_06"]
PR_08 = ["PR_09", "PR_10", "PR_11", "PR_12"]
PR_14 = ["PR_15", "PR_16", "PR_19"]
PR_18 = ["PR_21", "PR_22"]
PR_13 = ["PR_23", "PR_24", "PR_25", "PR_26", "PR_27"]

# MktOvr
MK_09 = ['[None]', 'MK_01', 'MK_02', 'MK_13', 'MK_14', 'MK_16', 'MK_17']
MK_03 = ['MK_04', 'MK_05', 'MK_06', 'MK_07', 'MK_08']

# End prepeared structures
# In future, find another way to do this
