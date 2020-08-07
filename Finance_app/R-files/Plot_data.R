library(ggplot2)
setwd("C:/Users/marcello/Finance_app/R-files")
source("Clean_data.R")

chase_cats <- chase_nopays
cats <- chase_cats$category
cats_cln <- gsub("[()]", "", cats)
cats_second_cat <- strsplit(cats_cln, ",")

#plot for spending by month               
ggplot(chase_nopays, aes(x = month, y =amount)) +
  geom_col(aes(fill = month)) + 
  facet_grid(cols = vars(year))

ggplot(chase_nopays, aes(x = category, y = amount)) + 
  geom_col() +
  facet_grid(cols = vars(year))

#plot for cumulative account value, starting from early 2019...it's not ideal
ggplot(wintrust, aes(x = as.factor(date), y = cumsum)) + 
  geom_point() +
  facet_grid(cols = vars(accountName))

#TO DO
#split Bank into payments and income
#   -Establish income
#build out expenses from:
#   -Bank
#   -Splitwise
#   -Venmo??
#Categorize everything?...eek!