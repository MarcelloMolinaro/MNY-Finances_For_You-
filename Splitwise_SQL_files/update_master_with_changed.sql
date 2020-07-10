--Code to import csv, must be done in sqlite3 command line I believe
-- Trying to bash script this...
/*
.open .../marcello/sqlite-tools/splitwiseDB.db
.mode csv
.import /marcello/splitwiseAPI/export_DF2.csv import3
.read updateMaster
.read update_master_with_changed--this file
*/

--Updates modified expenses
--Unfortunately, cannot use INNER JOIN and UPDATE so must use "replace into"
--Currently this adds the row, but does not delete the old row...?
REPLACE INTO testMaster (tableID, expenseID, description, cost, 
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
--Can i just do SELECT * FROM import3?
--I don't need to insert the expenseID, but I'll keep for now
SELECT testMaster.tableID, import3.expenseID, import3.description, import3.cost,
    import3.txnDate, import3.category, import3."Group",
    import3.updatedAt, import3.deletedAt,
    import3.userName1, import3.userBalance1,
    import3.userName2, import3.userBalance2,
    import3.userName3, import3.userBalance3,
    import3.userName4, import3.userBalance4,
    import3.userName5, import3.userBalance5,
    import3.userName6, import3.userBalance6,
    import3.userName7, import3.userBalance7,
    import3.userName8, import3.userBalance8,
    import3.userName9, import3.userBalance9
FROM import3
INNER JOIN testMaster ON import3.expenseID = testMaster.expenseID
WHERE testMaster.expenseID IN (
        SELECT expenseID FROM import3 WHERE import3.UpdatedAt > testMaster.updatedAt
);

DROP TABLE import3;
--BACKUP/COMMIT;

/* 2 notes: THis method runs into issues when PRAGMA foreign_keys=ON. Don't understand but there's the note.
I can chose to update only a few columns in the same way I didn't achange the PrimaryKey, 
pull data from the inserted into table itself, not thenew data */
