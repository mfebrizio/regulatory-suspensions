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
filePath =r'C:/Users/16192/OneDrive/Documents/'

# load json file
#fileName = 'clinton_bush_midnight_rules.json'
#fileName = 'bush_obama_midnight_rules.json'
#fileName = 'obama_trump_midnight_rules.json'
fileName = 'trump_biden_midnight_rules.json'

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
    string = dctsRules['results'][i]['regulation_id_numbers']
    dctsRules['results'][i]['regulation_id_numbers'] = ', '.join(string)
    #regular_list = dctsRules['results'][i]['regulation_id_numbers'] #need to flatten this list, https://stackabuse.com/python-how-to-flatten-list-of-lists/
    #flat_list = [item for sublist in regular_list for item in sublist]
    #dctsRules['results'][i]['regulation_id_numbers'] = ', '.join(flat_list)

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

#dfRules.to_excel(r'C:/Users/16192/OneDrive/clinton_bush_midnight_rules.xlsx', index = False, header=True)
#dfRules.to_excel(r'C:/Users/16192/OneDrive/bush_obama_midnight_rules.xlsx', index = False, header=True)
#dfRules.to_excel(r'C:/Users/16192/OneDrive/obama_trump_midnight_rules.xlsx', index = False, header=True)
dfRules.to_excel(r'C:/Users/16192/OneDrive/trump_biden_midnight_rules.xlsx', index = False, header=True)
