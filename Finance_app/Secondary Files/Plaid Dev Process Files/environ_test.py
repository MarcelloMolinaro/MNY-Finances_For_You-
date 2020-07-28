# -*- coding: utf-8 -*-
"""
Created on Sat Jun 13 11:46:11 2020
Some would call this the "settings.py" document
@author: marcello
"""

import os
from os.path import join, dirname
from dotenv import load_dotenv
import plaid_access_tokens as plaidToken

print(plaidToken.chase_access_token)

#throws an error if has not been run in the CLI yet, python environ_test.py
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

print(os.environ.get('PLAID_ENV'))
print(os.getenv('PLAID_CLIENT_ID')) # not a key yet

print("DEVELOPMENT secret: " + os.getenv('PLAID_SECRET_DEVELOPMENT'))
print("SANBOX secret: " + os.getenv('PLAID_SECRET_SANDBOX'))

print(os.getenv('PLAID_PUBLIC_KEY'))
print(os.getenv('PLAID_ENV', 'sandbox'))
print(os.getenv('PLAID_PRODUCTS', 'transactions'))
print(os.getenv('PLAID_COUNTRY_CODES', 'US'))

    #Path work
import os
print(os.getcwd())
from pathlib import Path

Path.cwd()
p = Path(r'C:\Users\marcello\sqlite-tools\create.txt')
p.read_text() #this works!! 

str(p)
#dynamically name variables. Instead do it in a dictionary.
a = {}
for i in range(1,4):
    key = "df" + str(i)
    value = i
    a[key] = value
    i += 1
    
for key in a:
    print(a[key], ": "+key)