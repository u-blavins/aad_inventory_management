USE [StoreManagement]
GO

/****** Object:  View [dbo].[GenerateReport]    Script Date: 03/02/2020 23:31:57 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE VIEW [dbo].[GenerateReport]
AS

SELECT
	[DepartmentCode],
	SUM([Price]) AS [Total Price]
FROM
	[itm].[Transaction]
WHERE 
	[TransactionDate] <= DATEADD(MONTH, DATEDIFF(MONTH, 0, GETDATE()), 0) 
	AND 
	[TransactionDate] > DATEADD(MONTH, DATEDIFF(MONTH, 0, GETDATE()) + 1, 0)
GROUP BY
	[DepartmentCode]

GO


