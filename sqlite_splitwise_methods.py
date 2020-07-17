import sqlite3
#import sqlite_methods as sql_mthd
from pathlib import Path

#connects to hardcoded DB, creates a temp table with df contents, 
# creates & returns cursor
def connectDF(dataframe, temp_table):
        database_name = "splitwiseDBnew.db"
        folder_path = Path(r'C:\Users\marcello\sqlite-tools')
        full_path = str(folder_path / database_name)
        conn = sqlite3.connect(str(full_path)) 
        #df0 = replace_square(plaid_df)
        #temp_table = "temp_splitwise_table"
        dataframe.to_sql(temp_table, conn, if_exists="replace")
        cursor = conn.cursor()
        return cursor, conn
        
        #verbatim from sqlite_methods.py    
def createTable(cursor, table_name, col_nm_type):
                #unique to my database: ID and Timestamp
         cursor.execute( "CREATE TABLE " + table_name + '''
                (databaseID INTEGER PRIMARY KEY,
                Timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,''' + \
                col_nm_type + ")" )
         
         #verbatim from sqlite_methods.py                   
def addRecords(cursor, table_name, temp_table, col_names):
        cursor.execute( 
                "INSERT INTO " + table_name + \
                "(" + col_names + ")" + \
                "SELECT * FROM " + temp_table + \
                " WHERE expenseID NOT IN (SELECT expenseID FROM "+ table_name + ")"
                ) 
    #NEED TO MODIFY THIS method so that it DOES update records that have been modfied or deleted!
    #More likely, I need to make another method called refreshresults or something

def updateRecords(cursor, table_name, temp_tample, col_names):
        #list of transaction records to be updated
        #add the updated records to table
        database_name = "splitwiseDBnew.db"
        folder_path = Path(r'C:\Users\marcello\sqlite-tools')
        full_path = str(folder_path / database_name)
        conn = sqlite3.connect(str(full_path)) 
        cursor = conn.cursor()
        table = 'split_transactions'
        temp = 'temp_split_transactions'
        col_names = col_names_trxn
        
        #list of added records
        cursor.execute('''
                SELECT {}
                FROM {} 
                JOIN {} ON {}
                WHERE {}'''.format( \
                temp + ".*", \
                temp, \
                table, table + ".expenseID = " + temp + ".expenseID", \
                temp + ".UpdatedAt > " + table + ".UpdatedAt")
                )
        print("records adding...")
        for row in cursor.fetchall():
            print(row)
        
        cursor.execute('''
                REPLACE INTO {} ({})
                SELECT {}
                FROM {} 
                JOIN {} ON {}
                WHERE {}'''.format( \
                table, col_names, \
                temp + ".*", \
                temp, \
                table, table + ".expenseID = " + temp + ".expenseID", \
                temp + ".UpdatedAt > " + table + ".UpdatedAt")
                )
                
        conn.commit()
        conn.close()
       

        #delete the old, out-of-date records from table
        #list of removed records
        cursor.execute('''
                       SELECT databaseID 
                       FROM (SELECT *, rank() 
                       OVER (PARTITION BY expenseID 
                             ORDER BY UpdatedAt DESC) as rankExpenseID 
                        FROM '''+ table +''') 
                        WHERE rankExpenseID > 1''')
        print("removing records... \n" + str(cursor.fetchall()))
        
        
         #.format(table)
        
        
        cursor.execute('''
                        DELETE FROM {}
                        WHERE databaseID IN (
                             SELECT databaseID 
                             FROM (SELECT *, rank() 
                                 OVER (PARTITION BY expenseID 
                                       ORDER BY UpdatedAt DESC) as rankExpenseID 
                        FROM {}) 
                        WHERE rankExpenseID > 1  
                       )'''.format(table, table)
        )
           
    
def checkTable(cursor, table_name):
        cursor.execute('''SELECT count(name) 
                FROM sqlite_master 
                WHERE type = 'table' AND name =?''', table_name)
        return cursor.fetchone()[0]==1

def countRows(cursor, table_name):
        command = "SELECT count(*) FROM " + table_name
        cursor.execute(command)
        row_count = int(cursor.fetchone()[0])
        return row_count
 
        #I'd like to change IndexNum to importOrder
        #I'd like to change Timestamp to importDate
col_names_user_type= '''
        IndexNum INTEGER,   
        UserBalance DECIMAL,
        UserName TEXT,
        expenseID INTEGER'''

col_names_user = ''' 
        IndexNum,
        UserBalance,
        UserName,
        expenseID'''

col_names_trxn_type= '''
        IndexNum INTEGER,
        expenseID INTEGER,
        Description TEXT,
        Cost DECIMAL,
        TxnDate DATETIME,
        Category TEXT,
        GroupName TEXT,
        UpdatedAt DATETIME,
        DeletedAt DATETIME'''

col_names_trxn = '''
        IndexNum,
        expenseID,
        Description,
        Cost,
        TxnDate,
        Category,
        GroupName,
        UpdatedAt,
        DeletedAt'''
        