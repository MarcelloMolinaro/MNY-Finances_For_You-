"""
Creates sqlite table
Inserts into the table all records from Plaid API
To Do: Figure outn why I the splitwiseDB.db is locked and not the DBnew.db
    Write code for, if TABLE already is created, update the table
"""

import sqlite3
import sqlite_methods as sql_mthd
from pathlib import Path

#function called from plaid_api_access
def import_to_sqlite(plaid_df, table_name):
    #why can't I access the original splitwiseDB? Ugggg
    #This works sqlite3.connect('C:/Users/marcello/sqlite-tools/splitwiseDBnew.db')
    #this defintely works conn = sqlite3.connect('C:\\Users\\marcello\\sqlite-tools\\splitwiseDBnew.db')
    database_name = "splitwiseDBnew.db"
    folder_path = Path(r'C:\Users\marcello\sqlite-tools')
    full_path = str(folder_path / database_name)
    conn = sqlite3.connect(str(full_path))
    
    df0 = replace_square(plaid_df)
    temp_table = "temp_df_table"
    df0.to_sql(temp_table, conn, if_exists="replace")
    c = conn.cursor()
    
    tname = ("plaid_"+str(table_name) + "2",)
    c.execute('''SELECT count(name) 
                    FROM sqlite_master 
                    WHERE type = 'table' AND name =?''', tname)
    #if table exists...
    if c.fetchone()[0]==1:
        existing_row_count = sql_mthd.countRows(c, tname[0])
        sql_mthd.updateTable(c, tname[0], temp_table)
        current_row_count = sql_mthd.countRows(c, tname[0])
        print(tname[0] + " rows updated: " + str(current_row_count - existing_row_count) + "\n ")
    #if table does not exist                     
    else:
        sql_mthd.createTable(c, tname[0])
        sql_mthd.updateTable(c, tname[0], temp_table)
        print("Table Added to database: " + tname[0])
        print("Records now in " + tname[0] + " : " + str(sql_mthd.countRows(c, tname[0]))+ "\n ")
    conn.commit()
    conn.close()
    
#this is all necessary since I believe you cannot have a "[" square 
#bracket in s SQL string..it's a huge bummer
def replace_square(messy_df):
    count = 0
    if 'category' in messy_df.columns:
        for item in messy_df.loc[:, "category"]:
            messy_df.loc[count, "category"] = str(item).replace("[", "(").replace("]", ")")
            count = count + 1
    return messy_df
