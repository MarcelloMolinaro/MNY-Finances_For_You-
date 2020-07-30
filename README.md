# Finance_API_and_Visualization
This is an application that gets Financial data from a cariety of authenticated sources. It then cleans and imports that data into a single SQLite database hosted locally. Finally, using R, this database is accessed and the data are visualized. 

**Could also integrate:**
  - Tableau
  - Twilio- weekly confirmationthat rpogram ran sucessfully?
  - Hosting Database online...like AWS

**To Do/notes:**
- Have I programmed the creation of the databse? NO.
- Does Plaid have access to my data?

## Dependencies

1. Packages
- Plaid
  - $ pip install plaid-python
  - https://github.com/plaid/plaid-python
- Splitwise
  - $ pip install splitwise
  - https://github.com/namaggarwal/splitwise
- dotenv
    - $ conda install -c conda-forge python-dotenv

2. Software 
- Sqlite3
- Python 3.7
- Anconda (for package management?)

## HOW TO

1. You must create a .env file in your "Plaid Files" folder that contains all of your plaid credentials
  - You do this by making a plaid account
  - Applying for the developer access gives 100 free access tokens rather than 5 I think, just explain why you want more!
  - YOu now have your client_ID, SECRET, etc which go into your file: *".env"*
  - Run the sandbox tutorial and then run it in the development environment to create account access-tokens
  - Save those access tokens in the file: *"plaid_access_tokens"*
2. You must create a sqlite database
  - This is done rather easily in the sqlite3 program
  - after giving the alias of opening the sqlite3 program: sqlite3 run... 
  - `sqlite3 .open "DatabaseName.db"`
  - This will create the database in your current directory
  - make sure to provide this same name and same directory to the file: *"plaid_data_to_sqlite"*
