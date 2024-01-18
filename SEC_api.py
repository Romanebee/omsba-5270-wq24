"""
Romane Beeharry
OMSBA 5270 - Analytics for Financial Decisions & Market Insights
Week 3 Assignemnt: Connection to Public Data through Python API Call
January 18th 2024
"""

# import modules
import requests
import pandas as pd

# create a request header
headers = {'User-Agent':"beeharry@seattleu.edu"}

# get all companies data
companyTickers = requests.get("https://www.sec.gov/files/company_tickers.json", headers=headers)

# print(companyTickers.json()['0']['cik_str'])

companyCIK = pd.DataFrame.from_dict(companyTickers.json(), orient='index')

print(companyCIK)

companyCIK['cik_str'] = companyCIK['cik_str'].astype(str).str.zfill(10)

print(companyCIK)

# Get cik for Google
cik = companyCIK[2:3].cik_str[0]

print(cik)

# SEC Filing API
# https://data.sec.gov/submissions/CIK##########.json

# SEC Filing API call
companyFiling = requests.get(f"https://data.sec.gov/submissions/CIK{cik}.json", headers=headers)

print(companyFiling.json()['filings'].keys())

# Turn the dictionary into dataframe
allFilings = pd.DataFrame.from_dict(companyFiling.json()['filings']['recent'])

print(allFilings)

# Review columns 
print(allFilings.columns)
print(allFilings[['accessionNumber', 'reportDate', 'form']].head(100))

# Look at a specific form
allFilings.iloc[10]

# Get company facts
companyFacts = requests.get(f"https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json", headers=headers)

# Review company facts
print(companyFacts.json()['facts'].keys())

# Look at financial statements
# print(companyFacts.json()['facts']['us-gaap'].keys())

# Look at revenue data
companyRevenue = companyFacts.json()['facts']['us-gaap']['Revenues']

print(companyRevenue)

# Look at assets data
companyAssets = companyFacts.json()['facts']['us-gaap']['Assets']

print(companyAssets)

# Get company concept data for Revenue
companyConceptR = requests.get((f"https://data.sec.gov/api/xbrl/companyconcept/CIK{cik}" f"/us-gaap/Revenues.json"), headers=headers)

# Review data
print(companyConceptR.json()['units']['USD'])

# Turn dictinary into a dataframe
allRevenue = pd.DataFrame.from_dict(companyConceptR.json()['units']['USD'])

print(allRevenue)

# Filter the data to obtain only 10K forms 
revenue10K = allRevenue[allRevenue.form =='10-K']
revenue10K = revenue10K.reset_index(drop=True)

print(revenue10K)

# Plot the data for revenue from 10-K filings
print(revenue10K.plot(x='end', y='val'))

# Repeat the process for assets data
companyConceptA = requests.get((f"https://data.sec.gov/api/xbrl/companyconcept/CIK{cik}" f"/us-gaap/Assets.json"), headers=headers)

# Review data
print(companyConceptA.json()['units']['USD'])

# Turn dictinary into a dataframe
allAssets = pd.DataFrame.from_dict(companyConceptA.json()['units']['USD'])

print(allAssets)

# Filter the data to obtain only 10K forms 
Assets10K = allAssets[allAssets.form =='10-K']
Assets10K = Assets10K.reset_index(drop=True)

print(Assets10K)

# Plot the data for revenue from 10-K filings
print(Assets10K.plot(x='end', y='val'))