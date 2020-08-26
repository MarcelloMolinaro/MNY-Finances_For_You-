require(ggplot2)
require(gridExtra)
require(lubridate)
setwd("C:/Users/marcello/Finance_app/R-files")
source("Clean_data.R")

#clean/transform categories
chase_cats <- chase_nopays
chase_cats$cleaned <- gsub("[()]", "", chase_cats$category)
chase_cats$split <- strsplit(chase_cats$cleaned, ",")

chase_cats$catSummary <- unlist(lapply(chase_cats$split, 
                          function(x) 
                              if(length(x) > 1){
                                  x[[2]]
                              } else {
                                  x[[1]]
                              } ))
chase_cats$cat1 <- unlist(lapply(chase_cats$split, function(x) x[[1]]))
chase_cats$cat2 <- unlist(lapply(chase_cats$split, 
                          function(x) 
                              if(length(x) > 1) {
                                  x[[2]]
                              } else {
                                  "No Second Category"
                              }))
chase_cats$cat3 <- unlist(lapply(chase_cats$split, 
                          function(x) 
                              if(length(x) > 2) {
                                x[[3]]
                              } else {
                                "No Thrid Category"
                              }))

#clean/transform data for YoY/Month comparisons
curr_month <- as.integer(format(Sys.Date(), "%m"))
curr_m <- curr_month

chase_m_Y_comp <- chase_cats
chase_m_Y_comp$month <- as.integer(chase_m_Y_comp$month)
chase_m_Y_comp <- chase_m_Y_comp %>%
      filter((month == curr_m & (year == "2020"| year =="2019")) | 
             (month == curr_m -1 & (year == "2020" | year =="2019")) |
             (month == curr_m -2 & (year == "2020" | year =="2019"))) %>%
      arrange(month_year)

#plot for spending by month               
plot1 <-ggplot(chase_cats, aes(x = month, y =amount)) +
            geom_col(aes(fill = cat1)) + #fill = month
            theme(legend.position = "none") +
            facet_grid(cols = vars(year))

#plot for spending YoY and curr Month vs Last Month
plot2<-ggplot(chase_m_Y_comp, aes(x = month, y =amount)) +
          geom_col(aes(fill = cat1)) + 
          #theme(legend.position = "none") +
          facet_grid( cols = vars(year)) + #cols = vars(month),
          labs(title = "Spending by Month: YoY vs Last Month")

#code for printing specific format
grid.arrange(plot1, plot2, nrow =2)

#plot for spendingby category by year (change cat1 to 2, 3 or summary (for 2 then 1))
ggplot(chase_cats, aes(x = cat1, y = amount)) + 
  geom_col(aes(fill = cat1)) +
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