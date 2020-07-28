# -*- coding: utf-8 -*-
"""This is the meat of extract data from the Splitwise API
as long as an access token exists:
    (dict comprised of oauth_token and oauth_token_secret)
This code then extracts all elements necessary for a csv.
"""
#from flask import Flask, render_template, redirect, session, url_for, request
from splitwise import Splitwise
import config as Config
import pandas as pd
import datetime
import access_token as Access

'''
accessdict = {
  "oauth_token": "KUlISlvNSKYHQ6RyUUqw4mOtAKJwzXbcmbqHo6fV",
  "oauth_token_secret": "JJ4jBfzJPSXu8BUmt9l0JWKaGaKHJqT9ZFLWfAim"}
'''
accessdict = Access.accessdict

sObj = Splitwise(Config.consumer_key,Config.consumer_secret)
#i think the below line will throw an error if the access_token in not up-todate
#so maybe this is an iferror: statement?
#   If error, then run the get/write accesstoken code
#   ...I'll need to automate that...
print ("establish sObj")
sObj.setAccessToken(accessdict)
print ("set sObj.Accesstoken")
#parameterize the item and date limits?
expensesObj = sObj.getExpenses(limit=30, dated_after='01/01/2020')
print ("expense Object established")

df = {  "Description": [],
        "Cost":[],
        "Date of txn": [],
        "Category": [],
        "UserName1": [], "UserBalance1":[],#"UserPaid1":[],#"UserOwed1":[],
        "UserName2": [], "UserBalance2":[] #"UserPaid2":[], #"UserOwed2":[],
        }
df = pd.DataFrame(data=df)
df_row = 0

for expense in expensesObj:
    date_time = datetime.datetime.strptime(expense.getDate(), '%Y-%m-%dT%H:%M:%SZ')
    print (expense.getDescription(), 
           expense.getCost(), 
           date_time.date(),
           expense.getCategory().getName())
    df.loc[df_row, "Description"] = expense.getDescription()
    df.loc[df_row, "Cost"] = expense.getCost()
    df.loc[df_row, "Date of txn"] = date_time.date()
    df.loc[df_row, "Category"] = expense.getCategory().getName()

    print (len(expense.getUsers()))
    usernum = 1
    if len(expense.getUsers()) > 2:
        #create another column(s), df only has 2 users
        print ("need more columns")
    for user in expense.getUsers():
        print (user.getFirstName(),
               "Paid: " + user.getPaidShare(),
               "Owed: "+ user.getOwedShare(),
               "Balance: " + user.getNetBalance()
               )
        df.loc[df_row, "UserName"+ str(usernum)] = user.getFirstName()
        #df.loc[df_row, "UserPaid"+ str(usernum)] = user.getPaidShare()
        #df.loc[df_row, "UserOwed"+ str(usernum)] = user.getOwedShare()
        df.loc[df_row, "UserBalance"+ str(usernum)] = user.getNetBalance()
        usernum = usernum + 1
    df_row = df_row + 1

df.to_csv(r'C:\Users\marcello\splitwiseAPI\export_DF2.csv', \
              index = True, header=True)