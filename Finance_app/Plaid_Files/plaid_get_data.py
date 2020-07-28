#Chase OAuth data
import pandas as pd
from os.path import join, dirname
from dotenv import load_dotenv
import plaid_access_tokens as plaidToken
import plaid_data_to_sqlite as py_to_sql
#import base64
import os
import datetime
import plaid

'''To DO
NEED TO RUN THIS PROGRAM IN GIT BASH-the client_id is weird otherwise
Use webhook and not a scheduled program run, to pull this info?
Tie R to sqlite and run analysis there
'''

#Defines the .env file
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)
print (os.getenv('PLAID_ENV'))

#fetches the variables necessary for interfacing with the API
PLAID_CLIENT_ID= os.environ.get('PLAID_CLIENT_ID')
PLAID_SECRET= os.environ.get('PLAID_SECRET_DEVELOPMENT') #Change for sandbox
PLAID_PUBLIC_KEY= os.environ.get('PLAID_PUBLIC_KEY')
PLAID_PRODUCTS= os.environ.get('PLAID_PRODUCTS', 'transactions')
PLAID_COUNTRY_CODES= os.environ.get('PLAID_COUNTRY_CODES', 'US')
PLAID_ENV= os.environ.get('PLAID_ENV', 'development') #Default to development
#PLAID_ENV='development'
#print(PLAID_CLIENT_ID, PLAID_SECRET, PLAID_PUBLIC_KEY, PLAID_PRODUCTS, PLAID_COUNTRY_CODES, PLAID_ENV)

#Call to the API. PLaid object stored in "client"
client = plaid.Client(client_id = PLAID_CLIENT_ID, 
                      secret= PLAID_SECRET, 
                      #public_key= PLAID_PUBLIC_KEY, This used to be needed...?
                      environment= PLAID_ENV, 
                      api_version= '2019-05-29')

#add all tokens here below
access_token_dict = {
                     "chase": plaidToken.chase_access_token, 
                     "wintrust": plaidToken.wintrust_access_token}

for key in access_token_dict:
    access_token= access_token_dict[key]
    #Chase CC only goes back ~25months, Wintrust only 19 months or 540 days
    start_date = '{:%Y-%m-%d}'.format(datetime.datetime.now() + \
        datetime.timedelta(-30))
    end_date = '{:%Y-%m-%d}'.format(datetime.datetime.now())
    response = client.Transactions.get(access_token, start_date, end_date)
    just_trxns = response['transactions']
    #DIRECT from the plaid python API docs: https://github.com/plaid/plaid-python#examples
    # the transactions in the response are paginated, so make multiple calls while increasing the offset to
    # retrieve all transactions
    while len(just_trxns) < response['total_transactions']:
        response = client.Transactions.get(access_token, start_date, end_date,
                                           offset=len(just_trxns))
        just_trxns.extend(response['transactions'])
    print("total records in " + str(key) + " API call: " + str(response['total_transactions']))
    
    accounts = response['accounts']#has info for account ID lookup to english names               
    #df_accounts = pd.json_normalize(accounts)   
    df = pd.json_normalize(just_trxns) #previously (pd.io.json.json_normalize())
    py_to_sql.import_to_sqlite(df, key)#THIS IS THE LINE THAT DOES ALLTHE SQLITE WORK    