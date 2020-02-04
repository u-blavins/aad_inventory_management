INSERT INTO
	[usr].[Privilege]
	([Name],
	[Level])
VALUES
	('Customer',0),
	('Privileged Customer',1),
	('Staff',2),
	('Admin',3),

INSERT INTO
	[itm].[Unit]
	(
		[UnitName],
		[Val]
	)
VALUES
	('Box',5),
	('Single',1)
INSERT INTO
	[itm].[Stock]
	(
		[StockCode],
		[Quantity],
		[UnitName],
		[MinThreshold],
		[MaxThreshold]
	)
VALUES
	('TUB3',100,'Single',35,100),
	('P3N5',50,'Box',20,60)

INSERT INTO
	[itm].[Item]
	(
		[Code],
		[Name],
		[UnitName],
		[Risk],
		[Price],
		[StockCode]
	)
VALUES
	('TUB3','Test Tubes','Single',1,0.95,'TUB3'),
	('R3D','Pen','Single',1,0.95,'P3N5'),
	('BLU3','Pen','Single',1,0.95,'P3N5'),
	('GR33N','Pen','Box',1,0.95,'P3N5')

INSERT INTO
	[itm].[Transaction]
	(
		[UserID],
		[DepartmentCode],
		[Price],
		[TransactionDate],
		[IsRefund]
	)
VALUES
	('F19F9548-D9A8-407D-8E4F-4218B3ADED43','11111',0.95,'2020-01-02',0)

INSERT INTO
	[itm].[TransactionInfo]
	(
		[TransactionID],
		[ItemCode],
		[UnitName],
		[Quantity]
	)
VALUES
	('32C37F98-DC67-4E41-BEA8-A6CC6A560D62','Y33T','Box',1)