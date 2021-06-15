#import the necessary packages
import requests
import pandas as pd
import numpy as np
import json
import time
import os
import datetime
import re

def jprint(obj): #create function so it directly prints
    #created a formatted string of the Python object
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)

#second step, check the publication date and the Presidential ID
#exclude rules not under the incoming President

# set file path
filePath =r'C:/Users/16192/OneDrive/Documents'

# load json file
fileName = 'documents_endpoint_rules_population.json'

with open(filePath+fileName, 'r', encoding='utf-8') as loadfile:
    dctsRules = json.load(loadfile)

print('Retrieval date: '+dctsRules['dateRetrieved'])

# create df
#replace agency column with just agency names
for i in range(len(dctsRules['results'])):
    string = dctsRules['results'][i]['agency_names']
    dctsRules['results'][i]['agency_names'] = ', '.join(string)

#for i in range(len(dctsRules['results'])):
    #dctsRules['results'][i]['president'] = dctsRules['results'][i]['president']['name'] #replace president column with just the name

for i in range(len(dctsRules['results'])):
    regular_list = dctsRules['results'][i]['regulation_id_numbers'] #need to flatten this list, https://stackabuse.com/python-how-to-flatten-list-of-lists/
    flat_list = [item for sublist in regular_list for item in sublist]
    dctsRules['results'][i]['regulation_id_numbers'] = ''.join(flat_list)

for i in range(len(dctsRules['results'])): #need to turn the string or else Excel messes up the format (doesn't work for csv)
    dctsRules['results'][i]['document_number'] = str(dctsRules['results'][i]['document_number'])

#need to combine the names (sometimes multiple agencies) into a single string: https://stackoverflow.com/questions/12453580/how-to-concatenate-items-in-a-list-to-a-single-string
#to xlsx: https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.to_excel.html
dfRules = pd.DataFrame(dctsRules['results'])
dfRules.info()

# In[ ]:

# extract president identifier
dfRules['president_id'] = dfRules.apply(lambda x: x['president']['identifier'], axis=1)
president_list = list(set(dfRules['president_id'].values.tolist()))
print(', '.join(president_list))

# convert publication date to datetime format
dfRules['publication_dt'] = pd.to_datetime(dfRules['publication_date'])

# create year column
dfRules['publication_year'] = dfRules.apply(lambda x: x['publication_dt'].year, axis=1)
dfRules['publication_month'] = dfRules.apply(lambda x: x['publication_dt'].month, axis=1)

# match each president with incoming year
year_list = [2001, 2009, 2017, 2021]
president_list = ['george-w-bush', 'barack-obama', 'donald-trump', 'joe-biden']
incoming_list = list(zip(year_list,president_list))
print(incoming_list)

# In[ ]:

# eliminate rules not issued by incoming president

dfRules['incoming'] = 0 # create indicator variable

for i in incoming_list: # flag mismatched rules
    bool_incoming = (dfRules['publication_year']==i[0]) & (dfRules['president_id']==i[1])
    dfRules.loc[bool_incoming,'incoming'] = 1

print(dfRules['incoming'].value_counts())

# filter out mismatched rules
bool_incoming = dfRules['incoming']==1

dfDelays = dfRules.loc[bool_incoming,:] #dfDelays is the cleaned file without the mismatched rules
dfDelays['incoming'].value_counts()

print(dfDelays['incoming'].value_counts()) #all are 1's so there are no mismatched rules anymore

print(type(dfDelays)) #check object type, it is already pandas df

#export dfDelays

#third step, convert to usable dataframe (capable of being exported as .csv/.xlsx)
dfDelays.to_csv (r'C:/Users/16192/OneDrive/dfDelay.csv', index = False, header=True)
#to xlsx: https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.to_excel.html
