# Splitwise_API
This is an application that gets Financial data from a cariety of authenticated sources. It then cleans and imports that data into a single SQLite database hosted locally. Finally, using R, this database is accessed and the data are visualized. 
Could also integrate:
  Tableau
  Twilio
  Hosting Database online...like AWS

-To Do/note: Have I programmed the creation of the databse?
          :Does Plaid have access to my data?

## Dependencies

1. Packages
- Plaid
  -$ pip install plaid-python
  -https://github.com/plaid/plaid-python
- Splitwise
  -$ pip install splitwise
  -https://github.com/namaggarwal/splitwise
- dotenv
    -$ conda install -c conda-forge python-dotenv

2. Software 
- Sqlite3
-Python 3.7
-Anconda (for package management?)
