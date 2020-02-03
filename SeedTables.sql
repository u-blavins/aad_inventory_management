INSERT INTO
	[itm].[Unit]
	(
		[UnitName],
		[Val]
	)
VALUES
	('Box',5)

INSERT INTO
	[itm].[Item]
	(
		[Code],
		[Name],
		[UnitName],
		[Risk],
		[Price]
	)
VALUES
	('Y33T','Pen','Box',1,0.95)

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
	('F19F9548-D9A8-407D-8E4F-4218B3ADED43','11111',0.95,GETDATE(),0)

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