setwd("C:/Users/marcello/Finance_app/R-files")
source("Connect_to_sqlite.R")

library(dplyr)

#Cleaning the data
    #Bank Data
wintrust <- plaid_wintrust %>% 
  left_join(plaid_accounts, 
            by = c("account_id" = "accountID")) %>%
  group_by(accountName) %>%
  #order_by(date) %>%
  arrange(date) %>%
  mutate(cumsum = order_by(date, cumsum(amount)))

wintrust$date <- as.POSIXlt.character(wintrust$date)

    #Credit Card Data
plaid_chase$date <- as.Date(plaid_chase$date)
chase <-plaid_chase %>%
  left_join(plaid_accounts, 
            by = c("account_id" = "accountID")) %>%
  mutate(month_year = format(date, "%Y-%m"),
         month = format(date, "%m"), 
         year = format(date, "%Y"))

chase_nopays <- chase %>% 
  filter(!grepl("thank you", 
                chase$name, 
                ignore.case = TRUE))

#check out data        
head(chase %>% select(amount, name) %>% arrange(amount))
head(wintrust %>% select(cumsum, amount, accountName, date))

