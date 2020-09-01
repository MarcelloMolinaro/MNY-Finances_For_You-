# MNY
### Finance API, ETL, and Visualization 
This is an application that gets Financial data from a variety of authenticated sources. It then cleans and imports that data into a single SQLite database hosted locally. Finally, using R, this database is accessed and the data are visualized.

## Who is this for?
This open source project is intended for anyone who is interested in owning and storing their financial data. This is for anyone tired of the same, static, ineffective visualizations provided by the standard personal finance services. This is for anyone who has ever tried to download more than 2 years of credit card transaction history!

## Why is this different?
Doesn't MINT do all of this and more? Well... yes. But MINT is owned by intuit and they are selling your data, though it is anonymized.
This program provides the framework to pull, store, and visualize your personal financial data. YOU own YOUR data. YOU store it. YOU chose how you want to visualize it, though I have also provided a framework for that. You can connect to any institution supported by PLAID (which does not sell or see your data) and any institution that has an API (Splitwise, Venmo, Coinbase, etc.)

## How do I use it?

#### Dependencies:

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

#### How To:

1. You must create a .env file in your "Plaid Files" folder that contains your plaid credentials
    - You do this by making a plaid account
    - Applying for the developer access gives 100 free access tokens rather than 5 I think, just explain why you want more!
    - You now have your client_ID, SECRET, etc which go into your file: *".env"*
2. You must modify your *"plaid_access_tokens.py"* file to reflect your own Bank Account access tokens
    - Run the PLAID sandbox tutorial first to see if it works
      -https://dashboard.plaid.com/overview/sandbox
    - Then run in the development environment to create bank account access-tokens
      - Create as many accounts as you wish. This can be bank accounts, investment accounts, and credit cards, etc.
    - Save those access tokens in the file: *"plaid_access_tokens"*
2. You must create a sqlite database
    - This is done rather easily in the sqlite3 program
    - after naming the sqlite3 path with the alias of "sqlite3", in BASH I run `sqlite3 .open "DatabaseName.db"`
    - This will create the database in your current directory
    - make sure to provide this same name and same directory to the file: *"plaid_data_to_sqlite.py"*
      - ```python
        database_name = "DatabaseName.db"
        folder_path = Path(r'C:\Users\marcello\sqlite-tools')
        ````
      - If you chose to use the Splitwise implementation as well, you'll need to add your Database path to the *"splitwise_sqlite_methods.py"* file as well!
3. Run the file *"plaid_get_data"*
    - Using python, run the file!
      - If you also have a splitwise account, you can use the splitwise files to import that data
          - there is a little more setup there...in progress
      - To get account names (in english) that is still in progress too
          -There is a file that has SQL code for all of my account names but that is manual as of right now.
          - File name: *"plaid_accounts_to_sqlite"*
4. Run the R file
        
## How does it work?
A Python script connects to the PLAID API `plaid_get_data.py`. Transaction data are then imported, cleaned, and loaded into a SQLite database. That database is then queried by an R script and after some more cleaning, the data are graphed and visualized.

Let me know if you use this! Submit pull requests!
Thank you.
