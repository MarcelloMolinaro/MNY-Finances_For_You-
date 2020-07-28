import subprocess
import sqlite3
conn = sqlite3.connect('C:/Users/marcello/sqlite-tools/splitwiseDB.db')
cursor = conn.execute('select * from testDeleted_users')
for row in cursor:
    print ("ID= ", row[1], " Name= ", row[3], " Bal= ", row[2])


subprocess.call(["sqlite3"]) 
../../sqlite-tools/splitwiseDB.db"])
                 , 
                 ".mode csv",
                 ".import ])

#Ideally I run all of the sqlite code here, via SQL-Alchemy
Step 0
run the splitwiseAPI python program
"python export_data_2_tables.py"

Step 1
open database splitwiseDB.db use "/"
".open C:\Users\marcello\sqlite-tools\splitwiseDB.db"



Step 2
import 2 csv files use "/"
".mode csv"
".import C:\Users\marcello\splitwiseAPI\splitwise_export_trxn.csv import_trxn"
".import C:\Users\marcello\splitwiseAPI\splitwise_export_users.csv import_users"

Step 3
run SQL scripts (or bash script) using .read command
    Sub Step 1
    Addnew expenses to databases
    ".read ...updateMaster" --Needs edits
    Sub Step 2
    Update modified expenses since last time
    ".read ...update_master_with_changed" --Needs edits
    Sub Step 3
    Delete recrords that have since been deleted and move to deleted table
    ".read ...remove_deleted_from_master" --Needs edits
    
Step 4
create backup database? Use commit or backup commands? LEARN MORE

Step 5...
Create visualizations by accessing the database via R, Tableau, Python, Excel...