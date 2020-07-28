# -*- coding: utf-8 -*

#accounts comes from plaid_api_access
#would be nice to normalize thatjson file and enter into 
#database but I did manually--See below

for dict in accounts:
    {k: str(v).encode("utf-8") for k,v in dict.items()}
    for key in dict:
     #   if isinstance(dict[key], str):
      #      print(key, dict[key])
        try:
            print(key, ": ", dict[key])
        except:
            try:
                print(dict[key].encode('utf-8'))
            except:    
                print("dictionary...") 
'''
CREATE TABLE plaid_accounts (
databaseID INTEGER PRIMARY KEY,
Timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
accountID TEXT,
accountName TEXT,
type TEXT,
mask TEXT);

INSERT INTO plaid_accounts (accountID, accountName, type, mask)
VALUES ('zqj1kJO19Rf6Qwyv3kvrTbjx55wzpDCOjrAea',
        'United Explorer',
        'credit',
        '0417'),
        ('YvxKL01KPMuAkqx83d8mHQ0J445n6VSQoOev3',
        'Chase Freedom Unlimited',
        'credit',
        '2610'),
        ('morOZBAOLjTo4PepvnpACy0obbL6ZruMKjrb9',
        'Chase Sapphire Preferred',
        'credit',
        '2901'),
        ('Mm70qmOm4asYejmwL6daSVmP6DqAQpFMZNdyk',
        'Checking',
        'depository',
        '0174'),
        ('OgNr3gmgxJcw90jagM6Jsxv4d5mYKgF8dAo1Z',
        'Savings',
        'depository',
        '2219');
'''
