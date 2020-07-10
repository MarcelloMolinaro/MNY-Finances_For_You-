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

#assumes access token is accurate/up-to-date
accessdict = Access.accessdict

sObj = Splitwise(Config.consumer_key,Config.consumer_secret)
#if error, run get access token script, end, run this again somehow
sObj.setAccessToken(accessdict)
#parameterize the item and date limits?
#I used updated after to catch updates and new items, since update=getDate for un-modified expenses
expensesObj = sObj.getExpenses(limit=500, updated_after='01/06/2020') #DD/MM/YYYY

#Addresses the DeletedGroup Issue
groupsObj = sObj.getGroups()
groups = []
for group in groupsObj:
    groups.append(group.getId())

df = {  "expenseID": [],
        "Description": [],
        "Cost":[], 
        "TxnDate": [],
        "Category": [],
        "Group": [],
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
    txn_date_time = datetime.datetime.strptime(expense.getDate(), '%Y-%m-%dT%H:%M:%SZ')
    upd_date_time = datetime.datetime.strptime(expense.getUpdatedAt(), '%Y-%m-%dT%H:%M:%SZ')
  #cannot assign DeletedAt if no deleted date object
    if (expense.getDeletedAt()!= None):
        del_date_time = datetime.datetime.strptime(expense.getDeletedAt(), '%Y-%m-%dT%H:%M:%SZ')
        df.loc[df_row, "DeletedAt"] = del_date_time.date()
        deleted_items = deleted_items + 1
    else:
        df.loc[df_row, "DeletedAt"] = ""
  #cannot assign GroupName when group !Exist
    if (expense.getGroupId() not in groups ):
        df.loc[df_row, "Group"] = "Deleted_Group"
    else:
        df.loc[df_row, "Group"] = sObj.getGroup(expense.getGroupId()).getName()

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
             "Category","Group","UpdatedAt","DeletedAt"]
df = df[new_order]
#export to csv!
df.to_csv(r'C:\Users\marcello\splitwiseAPI\splitwise_export_trxn.csv', \
              index = False, header=True)
dfusers.to_csv(r'C:\Users\marcello\splitwiseAPI\splitwise_export_users.csv', \
              index = False, header=True)
print ("Number of expense records: " + str(df_row))
print ("Numer of deleted expenses: "+ str(deleted_items))
print ("Number of User Balances: " + str(dfusers_row))