--Code to import csv, must be done in sqlite3 command line I believe
-- Trying to bash script this...
/*
.open .../marcello/sqlite-tools/splitwiseDB.db
.mode csv
.import /marcello/splitwiseAPI/export_DF2.csv import3
.read updateMaster
.read update_master_with_changed
.read remove_deleted_from_master--this file
*/

--Removes deleted expenses from master table
WITH del_data AS (
    SELECT * FROM import3
    WHERE deletedAt IS NOT "")
DELETE FROM testMaster
WHERE testMaster.expenseID IN (
    SELECT del_data.expenseID FROM del_data
);
--Adds THESE EXPENSES TO THE testDELETED TABLE
INSERT INTO testDeleted (expenseID, description, cost, 
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
WHERE deletedAt IS NOT "" 
    AND import3.expenseID NOT IN (SELECT expenseID FROM testDeleted);

DROP TABLE import3;
--BACKUP/COMMIT;