#load financial data into R
library(DBI)
library(RSQLite)
setwd("C:/Users/marcello/sqlite-tools")
con <- dbConnect(SQLite(), 
                 "splitwiseDBnew.db")

#list of availble tables
as.data.frame(dbListTables(con))

#change this to be your table names!
split_users <- dbReadTable(con, 'split_users')
split_transactions <- dbReadTable(con, 'split_transactions')
plaid_chase <- dbReadTable(con, 'plaid_chase2')
plaid_wintrust <- dbReadTable(con, 'plaid_wintrust2')
plaid_accounts <- dbReadTable(con, 'plaid_accounts')

dbDisconnect(con)





