--https://www.sqlrelease.com/import-csv-file-into-sql-server-using-t-sql-query
--Code to import csv, must be done in sqlite3 command line I believe
-- Trying to bash script this...
/*
.open .../marcello/sqlite-tools/splitwiseDB.db
.mode csv
.import /marcello/splitwiseAPI/export_DF2.csv import3
.read ./Splitwise_SQL_files/updateMaster --this file
*/
--Inserts novel expenseID's into master table
INSERT INTO testMaster (expenseID, description, cost, 
    txnDate,category,groupName, updatedAt, deletedAt,
    userName1, userBalance1,
    userName2, userBalance2,
    userName3, userBalance3,
    userName4, userBalance4,
    userName5, userBalance5,
    userName6, userBalance6,
    userName7, userBalance7,
    userName8, userBalance8,
    userName9, userBalance9)
SELECT * FROM import3
WHERE expenseID NOT IN (SELECT expenseID FROM testMaster);


--Make sure new imports are not copying the Header Row into the master table!
    --SELECT * FROM import3 WHERE Description == 'Description';
    --SELECT count(*) FROM import3;
    
--When finished with table  
DROP TABLE import3;
--BACKUP/COMMIT;
