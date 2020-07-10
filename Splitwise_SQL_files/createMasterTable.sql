CREATE TABLE testMaster (
tableID INTEGER NOT NULL PRIMARY KEY,
expenseID INTEGER,
description VARCHAR (100),
cost NUMERIC,
txnDate DATE,
category VARCHAR (25),
groupName VARCHAR (50), 
updatedAt DATE,
deletedAt DATE,
userName1 VARCHAR (25),
userBalance1 NUMERIC,
userName2 VARCHAR (25),
userBalance2 NUMERIC,
userName3 VARCHAR (25),
userBalance3 NUMERIC,
userName4 VARCHAR (25),
userBalance4 NUMERIC,
userName5 VARCHAR (25),
userBalance5 NUMERIC,
userName6 VARCHAR (25),
userBalance6 NUMERIC,
userName7 VARCHAR (25),
userBalance7 NUMERIC,
userName8 VARCHAR (25),
userBalance8 NUMERIC,
userName9 VARCHAR (25),
userBalance9 NUMERIC
);

SELECT * FROM testMaster;
SELECT * FROM testMaster ORDER BY deletedAt DESC;

DROP TABLE testMaster;

CREATE TABLE testDeleted (
tableID INTEGER NOT NULL PRIMARY KEY,
expenseID INTEGER,
description VARCHAR (100),
cost NUMERIC,
txnDate DATE,
category VARCHAR (25),
groupName VARCHAR (50), 
updatedAt DATE,
deletedAt DATE,
userName1 VARCHAR (25),
userBalance1 NUMERIC,
userName2 VARCHAR (25),
userBalance2 NUMERIC,
userName3 VARCHAR (25),
userBalance3 NUMERIC,
userName4 VARCHAR (25),
userBalance4 NUMERIC,
userName5 VARCHAR (25),
userBalance5 NUMERIC,
userName6 VARCHAR (25),
userBalance6 NUMERIC,
userName7 VARCHAR (25),
userBalance7 NUMERIC,
userName8 VARCHAR (25),
userBalance8 NUMERIC,
userName9 VARCHAR (25),
userBalance9 NUMERIC
);