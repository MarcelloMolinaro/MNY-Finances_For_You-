--Creates master test table
CREATE TABLE table1master (
expenseID int,
amount int,
type varchar (3)
);
--Adds data to master test table
INSERT INTO table1master (expenseID, amount, type)
VALUES ("1", "10", "a"),
(2, 10, "b"),
(3, 15, "b"),
(4, 12, "c");

CREATE TABLE table1 (
expenseID int,
amount int,
type varchar (3)
);
INSERT INTO table1 (expenseID, amount, type)
VALUES (4, 12, "c"), (5, 11, "c");

SELECT * FROM table1master;
SELECT * FROM table1;