#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pandas as pd
import os
import refinitiv.data as rd
# reference: https://developers.refinitiv.com/en/api-catalog/refinitiv-data-platform/refinitiv-data-library-for-python
os.environ["RD_LIB_CONFIG_PATH"] = "../Configuration"

# Open the default Session
rd.open_session()

#
# Run your application code
#


# In[28]:


df_variable = pd.read_csv('Refinitiv_Codebook.csv')
formula_list = df_variable['Variable_Formula'].dropna().tolist()


# In[27]:


import refinitiv.data as rd

def api_history(instrument):
    df_temp = rd.get_history(
    universe=[instrument],
    fields=formula_list,
    interval="1Y",
    start="1995-01-01",
    end="2022-01-01",
    )
    try:
        df_temp = df_temp.groupby('Date').first()
    except:
        df_temp = df_temp
        f"Groupby Date error encountered at {instrument}"
    # replace blank values with NAs
    try:
        df_temp = df_temp.mask(df_temp == '')
    except:
        df_temp = df_temp
        f"Mask empty space error encountered at {instrument}"
    # drop rows with all NAs
    df_temp.dropna(axis = 0, how = 'all', inplace = True)
    # warnings regarding fragmentation
    df_temp.insert(0, 'Instrument', instrument)
    return df_temp

