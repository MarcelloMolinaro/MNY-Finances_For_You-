"""
Creates sqlite table
Inserts into the table all records from Plaid API
To Do: Figure outn why I the splitwiseDB.db is locked and not the DBnew.db
    Write code for, if TABLE already is created, update the table
"""

import sqlite3
from pathlib import Path

#df is currently coming from plaid_api_access...
#can use "**plaid_df_dict" or just a dict to pass multiple
def import_to_sqlite(plaid_df, token_num):
    #why can't I access the original splitwiseDB? Ugggg
    #This works sqlite3.connect('C:/Users/marcello/sqlite-tools/splitwiseDBnew.db')
    #this defintely works conn = sqlite3.connect('C:\\Users\\marcello\\sqlite-tools\\splitwiseDBnew.db')
    database_name = "splitwiseDBnew.db"
    tname = ("plaid_"+str(token_num),)
    folder_path = Path(r'C:\Users\marcello\sqlite-tools')
    full_path = str(folder_path / database_name)
    
    conn = sqlite3.connect(str(full_path))
    
    df0 = replace_square(plaid_df)
    
    df0.to_sql("temp_dataframe_table", conn, if_exists="replace")
    c = conn.cursor()

    c.execute(''' SELECT count(name) FROM sqlite_master WHERE type = 'table' AND name =?''', tname)
    if c.fetchone()[0]==1:
        print("UPDATE TABLE CODE HERE")
        #tname = 'lop'
        insert_cmnd = "INSERT INTO " + \
                str(tname[0]) + \
                " SELECT * FROM temp_dataframe_table WHERE transaction_id not in (SELECT transaction_id FROM "+ \
                str(tname[0]) + ")"
#AND NOT PENDING! Don't touch PENDING!
        c.execute(insert_cmnd)
        print("updated x rows!")
                         
    #elif:
    else:
        conn.execute(' Create TABLE ' + tname[0] +
                     ' AS SELECT * FROM temp_dataframe_table ')
        print("Table Added to database: " + str(tname) )
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
   
#import_to_sqlite(df, 0)


