#import the necessary packages
import requests
import pandas as pd
import numpy as np
import json
import time
import os
import datetime
import re

#first step, retrieve the raw data from the Federal Register API

# set file path
filePath =r'C:/Users/16192/OneDrive/Documents'

# endpoint: /documents.{format}

# define endpoint url
dcts_URL = 'https://www.federalregister.gov/api/v1/documents.json?'

# define parameters
exclude_corrections = 0 ## exclude corrections
res_per_page = 1000
page_offset = 0 ## both 0 and 1 return first page
sort_order = 'oldest'
cond_type = 'RULE'
fieldsList = ['publication_date', 'effective_on', 'agencies', 'agency_names', 'title', 'abstract', 'action',
              'type', 'president', 'dates',
              'citation', 'document_number', 'regulation_id_numbers', 'json_url', 'raw_text_url', 'html_url']
year = 2017 ## just to initialize params; will loop over list [2001, 2009, 2017, 2021]
gte_date = str(year)+'-01-20' ## greater than or equal to date
lte_date = str(year)+'-04-30' ## less than or equal to date

keywords = '("effective date" | "compliance date") & delay'

# dictionary of parameters
dcts_params = {'conditions[correction]': exclude_corrections,
               'per_page': res_per_page,
               'page': page_offset,
               'order': sort_order,
               'conditions[type][]': cond_type,
               'fields[]': fieldsList,
               'conditions[publication_date][gte]': gte_date,
               'conditions[publication_date][lte]': lte_date,
              }

print('Configured to retrieve rules published in Federal Register from '+gte_date+' to '+lte_date+'.')

# In[ ]:


# years of interest -- first year in presidential administration
years = [2001, 2009, 2017, 2021]

# set variable for holding results
dctsResults = []
dctsCount_all = 0

# loop over years
for y in years:
    gte_date = str(y) + '-01-20'
    lte_date = str(y) + '-04-30'
    dcts_params.update({'conditions[publication_date][gte]': gte_date,
                        'conditions[publication_date][lte]': lte_date})

    # get documents
    print('\n', '***** Retrieving results for rules published from ' + gte_date + ' to ' + lte_date + ' *****')
    dcts_response = requests.get(dcts_URL, params=dcts_params)
    print(dcts_response.status_code,
          dcts_response.headers['Date'],
          dcts_response.url, sep='\n')  ## print request URL

    # set variables
    dctsCount = dcts_response.json()['count']
    dctsPages = dcts_response.json()['total_pages']  ## number of pages to retrieve all results

    # for loop for grabbing results from multiple pages
    if dctsPages > 1:
        for page in range(1, dctsPages + 1):
            dcts_params.update({'page': page})
            dcts_response = requests.get(dcts_URL, params=dcts_params)
            results_this_page = dcts_response.json()['results']
            dctsResults.extend(results_this_page)
            print('Results retrieved = ' + str(len(dctsResults)))
    else:
        results_one_page = dcts_response.json()['results']
        dctsCount_all = dctsCount_all + dctsCount
        dctsResults.extend(results_one_page)

    print('Results retrieved this year = ' + str(dctsCount))

# save params for export with metadata
save_params = dcts_params
save_params.pop('page')
save_params.pop('per_page')
save_params.pop('conditions[publication_date][gte]')
save_params.pop('conditions[publication_date][lte]')

# create dictionary of data with retrieval date
dctsRules = {'dateRetrieved': str(datetime.date.today()),
             'params': save_params,
             'count': dctsCount_all,
             'results': dctsResults}
if dctsRules['count'] == len(dctsRules['results']):
    print('Dictionary with retrieval date created!',
          dctsRules.keys(),
          dctsRules['count'], sep='\n')
else:
    print('Error creating dictionary...')

# In[ ]:


# export json file
fileName = 'documents_endpoint_rules_population.json'

with open(filePath + fileName, 'w', encoding='utf-8') as outfile:
    json.dump(dctsRules, outfile, indent=4)

print('Exported as JSON!')

