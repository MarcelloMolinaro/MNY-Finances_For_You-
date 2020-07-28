"""This is the meat of extract data from the Splitwise API
as long as an access token exists:
    (dict comprised of oauth_token and oauth_token_secret)
This code then extracts all elements necessary for a csv. """
#https://github.com/namaggarwal/splitwise
# TO DO case for A vs M as first payer, standardize it please? or handle in SQL
from splitwise import Splitwise
import config as Config
import pandas as pd
import datetime
import access_token as Access
import sqlite_splitwise_methods as sql_split_mthds

#assumes access token is accurate/up-to-date
accessdict = Access.accessdict

sObj = Splitwise(Config.consumer_key,Config.consumer_secret)
#if error, run get access token script, end, run this again somehow
sObj.setAccessToken(accessdict)
#parameterize the item and date limits?
#I used updated after to catch updates and new items, since update=getDate for un-modified expenses
expensesObj = sObj.getExpenses(limit=100, updated_after='07/15/2020') #DD/MM/YYYY

#Addresses the DeletedGroup Issue
groupsObj = sObj.getGroups()
groups = []
for group in groupsObj:
    groups.append(group.getId())
#The bulk of transactions
df = {  "expenseID": [],
        "Description": [],
        "Cost":[], 
        "TxnDate": [],
        "Category": [],
        "GroupName": [],
        "UpdatedAt": [],
        "DeletedAt": []}
dfusers = {"expenseID": [],
        "UserName": [],
        "UserBalance":[]}

df = pd.DataFrame(data=df); dfusers = pd.DataFrame(data=dfusers)
#set counts
df_row = 0; deleted_items = 0; dfusers_row = 0;

#iterate through each expense and then through each user
for expense in expensesObj:
    txn_date_time = datetime.datetime.strptime(expense.getDate(), \
                                               '%Y-%m-%dT%H:%M:%SZ')
    upd_date_time = datetime.datetime.strptime(expense.getUpdatedAt(), \
                                               '%Y-%m-%dT%H:%M:%SZ')
  #cannot assign DeletedAt if no deleted date object
    if (expense.getDeletedAt()!= None):
        del_date_time = datetime.datetime.strptime(expense.getDeletedAt(), '%Y-%m-%dT%H:%M:%SZ')
        df.loc[df_row, "DeletedAt"] = del_date_time.date()
        deleted_items = deleted_items + 1
    else:
        df.loc[df_row, "DeletedAt"] = ""
  #cannot assign GroupName when group !Exist
    if (expense.getGroupId() not in groups ):
        df.loc[df_row, "GroupName"] = "Deleted_Group"
    else:
        df.loc[df_row, "GroupName"] = sObj.getGroup(expense.getGroupId()).getName()

    df.loc[df_row, "expenseID"] = expense.getId()
    df.loc[df_row, "Description"] = expense.getDescription()
    df.loc[df_row, "Cost"] = expense.getCost()
    df.loc[df_row, "TxnDate"] = txn_date_time.date()
    df.loc[df_row, "Category"] = expense.getCategory().getName()
    df.loc[df_row, "UpdatedAt"] = upd_date_time.date()
    
    for user in expense.getUsers():
        dfusers.loc[dfusers_row, "expenseID"] = expense.getId()
        dfusers.loc[dfusers_row, "UserName"] = user.getFirstName()
        dfusers.loc[dfusers_row, "UserBalance"] = user.getNetBalance()
        dfusers_row = dfusers_row + 1
    df_row = df_row + 1

#code to reorder the columns from alphabetic   
new_order = ["expenseID","Description","Cost", "TxnDate", 
             "Category","GroupName","UpdatedAt","DeletedAt"]
df = df[new_order]

dict_of_dfs = {"transactions": (df, #index = 0
                                sql_split_mthds.col_names_trxn_type, 
                                sql_split_mthds.col_names_trxn),  
               "users": (dfusers, 
                         sql_split_mthds.col_names_user_type, 
                         sql_split_mthds.col_names_user)
               }          
            
for key in dict_of_dfs:
        tname = ("split_"+str(key),)
        temp_table= "temp_split_" + str(key)
        c, connection = sql_split_mthds.connectDF(dict_of_dfs[key][0], temp_table)
        #temp table now exists
        
        #if target table exists
        if sql_split_mthds.checkTable(c, tname):
            #count records existing
            old_row_total = sql_split_mthds.countRows(c, tname[0])
            #update table with records    
            sql_split_mthds.updateTable(c, tname[0], temp_table, dict_of_dfs[key][2])
        else:
            #make table
            sql_split_mthds.createTable(c, tname[0], dict_of_dfs[key][1])
            #update table with records
            sql_split_mthds.updateTable(c, tname[0], temp_table, dict_of_dfs[key][2])
            old_row_total = 0
        
        new_row_total = sql_split_mthds.countRows(c, tname[0])
        connection.commit()
        connection.close()
        print ("New {} added: {}".format(key, new_row_total - old_row_total))
        
print ("Expense records in API call: " + str(df_row))
print ("Deleted expenses in API call: "+ str(deleted_items))
print ("User-Balances in API call: " + str(dfusers_row))

#export to csv!
#df.to_csv(r'C:\Users\marcello\splitwiseAPI\splitwise_export_trxn.csv', \
#              index = False, header=True)
#dfusers.to_csv(r'C:\Users\marcello\splitwiseAPI\splitwise_export_users.csv', \
#              index = False, header=True)