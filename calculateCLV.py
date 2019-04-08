#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec  4 22:03:23 2018.

Customer Analytics [ CLV Nigros Project ]
@author: Eray Ates, Sibel Gürbüz
"""

#%% [markdown]
# ## Import database connection libraries

#%%
from library.libx import *
import pandas as pd

#%% [markdown]
# ## Set connection parameters

#%%
config = jsonread("config.json")
con_config = config["connection"]

migros = MySQL(
    con_config["username"],
    con_config["password"],
    con_config["URL"],
    con_config["port"],
    con_config["db"]
    )

#%% [markdown]
# ## Set calculation for how many user

#%%
user_count = 50


#%%
# Customer average spend money from a few random users
ResultProxy = migros.connection.execute('select i.total_amount, a.id, i.invoice_date from     user_data as a, invoice as i     where i.user_id = a.id order by RAND() LIMIT {};'.format(user_count))
results = ResultProxy.fetchall()
df = pd.DataFrame(results, columns=['amount','id','date']).set_index('id').sort_index()
df = df.rename_axis("id", axis="columns").rename_axis(None)


#%%
df.head()


#%%
grouped = df.groupby(level=0)
grouped_avg_price = grouped['amount'].agg("mean")


#%%
avg_price = grouped_avg_price.values.mean(); avg_price

#%% [markdown]
# ## How many times a customer buy something in 1 year

#%%
from datetime import datetime, timedelta
now = datetime.now()


#%%
counts = df.loc[:, ['date']][df['date']> (now + timedelta(days=-365))].groupby(level=0)['date'].agg('count')


#%%
counts_frame = pd.DataFrame(counts)
counts_frame.head()

#%% [markdown]
# ## Put all in one dataframe

#%%
clv_frame = pd.DataFrame(grouped_avg_price)


#%%
clv_frame = pd.merge(clv_frame, counts_frame, left_index=True, right_index=True, how='outer').fillna(0)


#%%
clv_frame.head()

#%% [markdown]
# ## Average money spend per user in a year

#%%
clv_frame['mul'] = clv_frame['amount'] * clv_frame['date']


#%%
clv_frame.head()

#%% [markdown]
# Average count all users

#%%
result = clv_frame['mul'].mean(); result

#%% [markdown]
# So each of customer spendding average above count TL in a year
#%% [markdown]
# If we think our customer life time is 20 year

#%%
result * 20

#%% [markdown]
# ## So we can't spend more than (above count) TL above 20 year to gain a new customer.

