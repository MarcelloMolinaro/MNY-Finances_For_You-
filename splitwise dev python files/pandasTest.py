import pandas as pd
import datetime

#the data
d = {"Letters": ["a", "b", "c"],
     "Numbers": [1, 2, 3 ],
     "Boolean": [True, True, False]}

#create the dataframe
df = pd.DataFrame(data=d)

#show us the dataframe
print (df)

#export dataframe to csv: Index provides indexes
#df.to_csv(r'C:\Users\marcello\splitwiseAPI\export_DF.csv', index = True, header=True)


x = {"description": ["table", "chair", "bench"]}
df2 = pd.DataFrame(data=x)

df2["description"]


x = "blahhhhh"
print ("the best", x, "is me")

y = "the best" + x + "is me2"
print (y)

a = "allegra"
b = 1
print(a + str(b))

a = "2020-02-28T08:00:00Z"
a = datetime.datetime.strptime(a, '%Y-%m-%dT%H:%M:%SZ')
#print (datetime.datetime.strptime(a, '%Y-%m-%dT%H:%M:%SZ'))
print (a.date(), a.time())