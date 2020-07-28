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

def updateTrxnRecords(cursor, table, temp, col_names):                
        #list of records needing updates, extracts expenseIDs for those records
        updated_records_sql = f'''
                SELECT {temp + ".*"}
                FROM {temp} 
                JOIN {table} ON {f"{table}.expenseID = {temp}.expenseID"}
                WHERE {f"{temp}.UpdatedAt > {table}.UpdatedAt"}'''                            
        cursor.execute(updated_records_sql)
        query = cursor.fetchall()
        print("updated transaction records adding...")
        for row in query: print(row)
        expenseIDs = [row[1] for row in query]
       
        #add the updated records to table
        replace_into_sql = f"REPLACE INTO {table} ({col_names}) " + \
                            updated_records_sql
        cursor.execute(replace_into_sql)
                       
        #delete the old, out-of-date records from table
        #list of removed records
        rank_by_updatedAt_From_sql = f'''
                FROM (SELECT *, rank() 
                        OVER (PARTITION BY expenseID 
                                  ORDER BY UpdatedAt DESC) as rankExpenseID 
                        FROM {table}) 
                WHERE rankExpenseID > 1'''
        cursor.execute("SELECT * " + rank_by_updatedAt_From_sql)
        print("old transaction records removing...")
        query = cursor.fetchall()
        for row in query: print(row)
        
        cursor.execute(f'''
                DELETE FROM {table}
                WHERE databaseID IN (
                    SELECT databaseID''' + \
                    rank_by_updatedAt_From_sql  + ")"                       
        )
        return expenseIDs

def updateUserRecords(cursor, table, temp, col_names, expenseIDs):
        expenseIDs_sql = "(" + ", ".join(str(idee) for idee in expenseIDs) + ")"
        temp = "temp_split_users"; table = "split_users"; col_names= col_names_user
        
        #list of update records expenseID in list
        updated_records_sql = f'''
                            SELECT * 
                            FROM {temp} 
                            WHERE expenseID IN {expenseIDs_sql}'''
        cursor.execute(updated_records_sql)
        query = cursor.fetchall()
        print("user balance records adding...")
        for row in query: print(row)
        
        #replace into split_users
        replace_into_sql = f'''
                            REPLACE INTO {table} ({col_names})
                            SELECT *
                            FROM {temp} 
                            WHERE expenseID IN {expenseIDs_sql}'''
        
        #delete old from split_users
        delete_from_sql = f'''
                            DELETE FROM {table} 
                            WHERE databaseID IN (
                                    SELECT databaseID
                                    FROM (SELECT *, rank() OVER (PARTITION BY expenseID
                                                ORDER BY Timestamp DESC) as rankExpenseID
                                          FROM {table})
                                    WHERE rankExpenseID > 1)'''
        cursor.execute(replace_into_sql)
        cursor.execute(f'''
                       SELECT * 
                       FROM (SELECT *, rank() OVER (PARTITION BY expenseID
                                                ORDER BY Timestamp DESC) as rankExpenseID
                             FROM {table})
                       WHERE rankExpenseID > 1''')
        print("removing user balance records...")
        query = cursor.fetchall()
        for row in query: print (row)
        cursor.execute(delete_from_sql)

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
        #can I change these to use ", ".join instead of 2 almost duplicates?
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
