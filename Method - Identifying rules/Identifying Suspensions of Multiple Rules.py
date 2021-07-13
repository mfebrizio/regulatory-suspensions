#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import requests
import pandas as pd
import numpy as np
import json
import time
import os
import datetime
import re


# In[ ]:


# set file path
filePath = r'folder'


# # Check for Suspensions of Multiple Rules

# In[ ]:


# load csv file
filePathExtension = r"Data/Kai's Data/"
fileName = 'Suspended_Rules.csv'

with open(filePath+filePathExtension+fileName, 'r', encoding='utf-8') as loadfile:
    dfRS = pd.read_csv(loadfile)

dfRS.info()


# In[ ]:


# view details from specific documents
n = 115
print(dfRS.loc[n,'document_number'], dfRS.loc[n,'title'], dfRS.loc[n,'action'], dfRS.loc[n,'dates'], sep='\n')
print('\n'+dfRS.loc[n,'abstract'])


# In[ ]:


# use str.contains to identify obs containing regex pattern
# https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Series.str.contains.html

# define search terms and boolean array
##search = r'(effective|compliance)\s(\bdates\b|\beach\b)'
search = r'\bdates\b|\beach\b'
searchbool1 = dfRS['action'].str.contains(search, regex=True, case=False)
searchbool2 = dfRS['dates'].str.contains(search, regex=True, case=False)
searchbool = (searchbool1|searchbool2)

# filter results
dfDates = dfRS.loc[searchbool,:].reset_index()
print('Count: '+str(len(dfDates)))


# In[ ]:


for rule in range(len(dfDates)):
    print(dfDates.loc[rule,'document_number'],
          dfDates.loc[rule,'title'],
          dfDates.loc[rule,'action'],
          dfDates.loc[rule,'dates'],
          dfDates.loc[rule,'abstract']+'\n', sep='\n')


# In[ ]:


# manually reviewed each document and recorded number of rules suspended
dates_reviewed = [('01-6429',1), ('01-6430',1), ('2017-01822',30), ('2017-01976',1), ('2017-02056',3), 
                  ('2017-02711',1), ('2017-02860',2), ('2017-03337',1), ('2017-05462',5), ('2017-05518',2), 
                  ('2021-02035',1), ('2021-04881',1)]


# In[ ]:


# https://www.geeksforgeeks.org/creating-a-pandas-dataframe-using-list-of-tuples/
dfReviewed = pd.DataFrame(dates_reviewed, columns=['document_number','susp'])
dfReviewed


# # Revise data

# ## Suspended rules

# In[ ]:


# merge reviewed data with core dataset
dfSusp = dfRS.merge(dfReviewed, how='outer', on=['document_number'], indicator=True, validate='1:1')
print(str(dfSusp['_merge'].value_counts())+'\n')

# create bool to identify documents with multiple suspensions
bool_mult = dfSusp['susp_y'].notna()

# create new var with merged data
dfSusp.loc[~bool_mult,'susp'] = dfSusp.loc[~bool_mult,'susp_x']
dfSusp.loc[bool_mult,'susp'] = dfSusp.loc[bool_mult,'susp_y']

# drop columns
dfSusp = dfSusp.drop(columns=['susp_x','susp_y','_merge'])

# check values of new var
print(dfSusp['susp'].value_counts())


# In[ ]:


# load csv file
filePathExtension = r"Data/Data for analysis/"
fileName = 'suspended_rules_multiple.csv'

with open(filePath+filePathExtension+fileName, 'w', encoding='utf-8') as loadfile:
    dfSusp.to_csv(loadfile, index_label='index', line_terminator='\n')

print('Exported as CSV!')


# ## Raw rules

# In[ ]:


# load csv file
filePathExtension = r"Data/Kai's Data/"
fileName = 'Raw_Rules.csv'

with open(filePath+filePathExtension+fileName, 'r', encoding='utf-8') as loadfile:
    dfRaw = pd.read_csv(loadfile)

dfRaw.info()


# In[ ]:


# merge reviewed data with core dataset
dfRev = dfRaw.merge(dfReviewed, how='outer', on=['document_number'], indicator=True, validate='1:1')
print(str(dfRev['_merge'].value_counts())+'\n')

# create bool to identify documents with multiple suspensions
bool_mult = dfRev['susp_y'].notna()

# create new var with merged data
dfRev.loc[~bool_mult,'susp'] = dfRev.loc[~bool_mult,'susp_x']
dfRev.loc[bool_mult,'susp'] = dfRev.loc[bool_mult,'susp_y']

# drop columns
dfRev = dfRev.drop(columns=['susp_x','susp_y','_merge'])

# check values of new var
print(dfRev['susp'].value_counts())


# In[ ]:


# load csv file
filePathExtension = r"Data/Data for analysis/"
fileName = 'raw_rules_multiple.csv'

with open(filePath+filePathExtension+fileName, 'w', encoding='utf-8') as loadfile:
    dfSusp.to_csv(loadfile, index_label='index', line_terminator='\n')

print('Exported as CSV!')

