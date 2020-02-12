USE [StoreManagement]
GO

/****** Object:  Trigger [itm].[UpdateStock]    Script Date: 12/02/2020 07:34:34 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO





CREATE TRIGGER [itm].[UpdateStock]
ON [itm].[TransactionInfo]
AFTER INSERT
NOT FOR REPLICATION
AS
BEGIN

DECLARE @ItemCode VARCHAR(10) = (SELECT TOP 1 [ItemCode] FROM inserted)
DECLARE @QuantityPurchased FLOAT = (SELECT TOP 1 [Quantity] FROM inserted WHERE ItemCode = @ItemCode)
DECLARE @UnitName VARCHAR(25) = (SELECT TOP 1 [UnitName] FROM inserted)
DECLARE @UnitValue FLOAT = (SELECT TOP 1 [Val] FROM [itm].[Unit] WHERE [UnitName] = @UnitName)
DECLARE @ConvertedVal FLOAT = @QuantityPurchased * @UnitValue
DECLARE @TransactionID UNIQUEIDENTIFIER = (SELECT TOP 1 [TransactionID] FROM inserted)

IF (SELECT TOP 1 [isRefund] FROM [itm].[Transaction] WHERE [TransactionID] = @TransactionID) = 0
BEGIN
	UPDATE 
		[itm].[Item]
	SET
		[Quantity] = [Quantity] - @ConvertedVal
	WHERE
		[Code] = @ItemCode
END
ELSE
BEGIN
	UPDATE 
		[itm].[Item]
	SET
		[Quantity] = [Quantity] + @ConvertedVal
	WHERE
		[Code] = @ItemCode
END
END
GO

ALTER TABLE [itm].[TransactionInfo] ENABLE TRIGGER [UpdateStock]
GO


USE [StoreManagement]
GO

/****** Object:  Trigger [itm].[RefreshStock]    Script Date: 12/02/2020 07:34:07 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO



CREATE TRIGGER [itm].[RefreshStock]
ON [itm].[PurchaseOrderInfo]
AFTER UPDATE
NOT FOR REPLICATION
AS
BEGIN

	DECLARE @isComplete BIT = (SELECT TOP 1 [isComplete] FROM inserted)
	IF @isComplete = 1
	BEGIN

		UPDATE
			[itm].[PurchaseOrderInfo]
		SET
			[completionDate] = GETDATE()
		WHERE
			[PurchaseOrderID] = (SELECT TOP 1 [PurchaseOrderID] FROM inserted)
			AND
			[ItemCode] = (SELECT TOP 1 [ItemCode] FROM inserted)

		UPDATE
			[itm].[Item]
		SET
			[Quantity] = [Quantity] + (SELECT TOP 1 [Quantity] FROM inserted)
		WHERE
			[Code] = (SELECT TOP 1 [ItemCode] FROM inserted)
		
		IF NOT EXISTS (
			SELECT
				[PurchaseOrderID],
				[isComplete]
			FROM
				[itm].[PurchaseOrderInfo]
			WHERE
				[IsComplete] = 0
			GROUP BY
				[PurchaseOrderID], [IsComplete])
		BEGIN
			UPDATE 
				[itm].[PurchaseOrder]
			SET
				[isComplete] = 1, [completionDate] = GETDATE()
			WHERE
				[PurchaseOrderID] = (SELECT TOP 1 [PurchaseOrderID] FROM inserted)
		END
	END	

END
GO

ALTER TABLE [itm].[PurchaseOrderInfo] ENABLE TRIGGER [RefreshStock]
GO


USE [StoreManagement]
GO

/****** Object:  UserDefinedFunction [itm].[DepartmentTransactionsByYearMonth]    Script Date: 12/02/2020 07:33:00 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO






CREATE FUNCTION [itm].[DepartmentTransactionsByYearMonth]
(
	@DepartmentCode VARCHAR(10),
	@Month INT,
	@Year INT,
	@Refund BIT
)
RETURNS TABLE
AS
RETURN(
	SELECT
		t.[TransactionID],
		t.[DepartmentCode],
		u.[Email],
		t.[Price],
		t.[TransactionDate],
		t.[IsRefund]
	FROM
		[itm].[Transaction] t
		INNER JOIN
		[usr].[User] u
	ON
		t.[UserID] = u.[ID]
	WHERE
		t.[DepartmentCode] = @DepartmentCode
		AND
		MONTH(t.[TransactionDate]) = @Month
		AND
		YEAR(t.[TransactionDate]) = @Year
		AND
		t.[isRefund] = @Refund
)
GO

/****** Object:  UserDefinedFunction [itm].[getUserTransactionInfo]    Script Date: 12/02/2020 07:33:00 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE FUNCTION [itm].[getUserTransactionInfo]
(
 @UserID VARCHAR(250)
)
RETURNS TABLE
AS
RETURN
(
	SELECT 
		ti.[TransactionID],
		ti.[ItemCode],
		ti.[Quantity],
		ti.[UnitName],
		t.[TransactionDate]
	FROM
		[itm].[TransactionInfo] ti
		INNER JOIN 
		[itm].[Transaction] t ON
		ti.[TransactionID] = t.[TransactionID]
	WHERE 
		t.[isRefund] = 0
		AND
		t.[UserID] = @UserID
)
GO

/****** Object:  UserDefinedFunction [itm].[viewPurchaseOrderInfo]    Script Date: 12/02/2020 07:33:00 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO



CREATE FUNCTION [itm].[viewPurchaseOrderInfo]
(
	@PurchaseOrderID VARCHAR(250)
)
RETURNS TABLE
AS
RETURN
(
	SELECT
		poi.[ItemCode],
		poi.[Quantity],
		poi.[isComplete],
		poi.[completionDate],
		u.[Email] as [ApprovedBy]
	FROM
		[itm].[PurchaseOrderInfo] poi
		LEFT OUTER JOIN
		[usr].[User] u 
	ON
		poi.[ApprovedBy] = u.[ID]
	WHERE
		[PurchaseOrderID] = @PurchaseOrderID
)
GO


USE [StoreManagement]
GO

/****** Object:  StoredProcedure [itm].[createPurchaseOrder]    Script Date: 12/02/2020 07:31:36 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO




CREATE PROCEDURE
	[itm].[createPurchaseOrder]
	(@UserID VARCHAR(250),
	@responseMessage VARCHAR(250) OUTPUT)
AS
BEGIN
	SET NOCOUNT ON
	BEGIN TRY
		DECLARE @PurchaseOrderID UNIQUEIDENTIFIER = NEWID()
		INSERT INTO 
			[itm].[PurchaseOrder]
			([PurchaseOrderID], [UserID],[GeneratedDate])
		VALUES
			(@PurchaseOrderID, @UserID, GETDATE())
		SET @responseMessage = @PurchaseOrderID
	END TRY
	BEGIN CATCH
		SET @responseMessage = 'Could not generate purchase order'
	END CATCH
END
GO

/****** Object:  StoredProcedure [itm].[createPurchaseOrderInfo]    Script Date: 12/02/2020 07:31:36 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO


CREATE PROCEDURE
	[itm].[createPurchaseOrderInfo]
	(@PurchaseOrderID VARCHAR(250),
	@ItemCode VARCHAR(10),
	@Quantity FLOAT,
	@responseMessage VARCHAR(250) OUTPUT)
AS
BEGIN
	SET NOCOUNT ON
	BEGIN TRY
		INSERT INTO 
			[itm].[PurchaseOrderInfo]
			([PurchaseOrderID], [ItemCode],[Quantity],[IsComplete])
		VALUES
			(@PurchaseOrderID, @ItemCode, @Quantity, 0)
		SET @responseMessage = 'Success'
	END TRY
	BEGIN CATCH
		SET @responseMessage = 'Failure'
	END CATCH
END
GO

/****** Object:  StoredProcedure [itm].[createTransaction]    Script Date: 12/02/2020 07:31:36 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO





CREATE PROCEDURE [itm].[createTransaction]
(
	@UserID VARCHAR(250),
	@Price FLOAT,
	@isRefund BIT,
	@responseMessage VARCHAR(250) OUTPUT
)
AS
BEGIN
	SET NOCOUNT ON

	DECLARE @TransactionID UNIQUEIDENTIFIER=NEWID()
	DECLARE @DepartmentCode CHAR(5)=(SELECT TOP 1 [DepartmentCode] FROM [usr].[User] WHERE ID = @UserID)
	INSERT INTO
		[itm].[Transaction]
		(TransactionID,
		UserID,
		DepartmentCode,
		Price,
		TransactionDate,
		isRefund)
	VALUES
		(@TransactionID, @UserID, @DepartmentCode,@Price,GETDATE(),@isRefund)
		
	SET @responseMessage = @TransactionID
END
GO

/****** Object:  StoredProcedure [itm].[createTransactionInfo]    Script Date: 12/02/2020 07:31:36 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO



CREATE PROCEDURE [itm].[createTransactionInfo]
(@ItemCode VARCHAR(10),
@TransactionID VARCHAR(250),
@UnitName VARCHAR(50),
@Quantity FLOAT,
@responseMessage NVARCHAR(250) OUTPUT)
AS
BEGIN
	SET NOCOUNT ON
	BEGIN TRY
		INSERT INTO 
			[itm].[TransactionInfo]
			(TransactionID,
			ItemCode,
			Quantity,
			UnitName)
		VALUES
			(@TransactionID,@ItemCode,@Quantity,@UnitName)
		SET @responseMessage = 'Success'
	END TRY
	BEGIN CATCH
		SET @responseMessage = 'Failure'
	END CATCH
END
GO

/****** Object:  StoredProcedure [itm].[GenerateFinanceReport]    Script Date: 12/02/2020 07:31:36 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO


CREATE PROCEDURE [itm].[GenerateFinanceReport]
(
	@StartDate DATE,
	@EndDate DATE
)
AS

	SELECT
		[DepartmentCode],
		SUM([Price]) AS [Total Price]
	FROM
		[itm].[Transaction]
	WHERE 
		[TransactionDate] >= @StartDate
		AND
		[TransactionDate] <= @EndDate
	GROUP BY
		[DepartmentCode]
GO

/****** Object:  StoredProcedure [usr].[CreateUser]    Script Date: 12/02/2020 07:31:36 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO



CREATE PROCEDURE [usr].[CreateUser]
(
    @Email VARCHAR(50), 
    @Password VARCHAR(50),
    @FirstName VARCHAR(40) = NULL, 
    @LastName VARCHAR(40) = NULL,
	@DepartmentCode CHAR(5),
	@Privileges INT = 0,
    @responseMessage NVARCHAR(250) OUTPUT
)
AS

BEGIN
    SET NOCOUNT ON

    DECLARE @salt UNIQUEIDENTIFIER=NEWID()
    BEGIN TRY
	IF NOT EXISTS (SELECT TOP 1 [Email] FROM [usr].[User] WHERE [Email] = @Email)
	BEGIN
       INSERT INTO [usr].[User] (Email, FirstName, LastName, Pass, Salt,DepartmentCode, Privileges)
       VALUES(@Email, @FirstName, @LastName, HASHBYTES('SHA2_512', @Password+CAST(@salt AS NVARCHAR(36))), @salt, @DepartmentCode,@Privileges)

       SET @responseMessage='User successfully registered'
	END
	ELSE
	BEGIN
		SET @responseMessage ='Email already has a registered account'
	END
    END TRY
    BEGIN CATCH
        SET @responseMessage='Failure due to exception'
    END CATCH

END
GO

/****** Object:  StoredProcedure [usr].[getUser]    Script Date: 12/02/2020 07:31:37 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO



CREATE PROCEDURE [usr].[getUser](
	@Email VARCHAR(50),
	@responseMessage NVARCHAR(250) OUTPUT
)
AS
BEGIN
	IF EXISTS (SELECT TOP 1 ID FROM [usr].[User] WHERE Email=@Email)
	BEGIN
		SELECT
			[ID],
			[Privileges]
		FROM [usr].[User]
		WHERE [Email] = @Email
		SET @responseMessage = 'Success'
	END
	ELSE
	BEGIN
		SET @responseMessage = 'False'
	END
END		
GO

/****** Object:  StoredProcedure [usr].[updatePassword]    Script Date: 12/02/2020 07:31:37 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO



CREATE PROCEDURE [usr].[updatePassword]
(
	@UserID VARCHAR(250),
	@Password VARCHAR(50),
	@responseMessage VARCHAR(250) OUTPUT
)
AS
BEGIN
	SET NOCOUNT ON
	BEGIN TRY
		DECLARE @Salt UNIQUEIDENTIFIER = (SELECT TOP 1 [Salt] FROM [usr].[User] WHERE [ID] = @UserID)
		DECLARE @newPassword BINARY(64) = HASHBYTES('SHA2_512', @Password+CAST(@salt AS NVARCHAR(36)))
		DECLARE @oldPassword BINARY(64) = (SELECT TOP 1 [Pass] FROM [usr].[User] WHERE [ID] = @UserID)
		IF @newPassword != @oldPassword
		BEGIN
			UPDATE
				[usr].[User]
			SET
				[Pass] = HASHBYTES('SHA2_512', @Password+CAST(@salt AS NVARCHAR(36)))
			WHERE
				[ID] = @UserID
			SET @responseMessage = 'Password changed successfully'
		END
		ELSE
		BEGIN
			SET @responseMessage = 'New password cannot be the same as an old password'
		END
	
	END TRY
	BEGIN CATCH
		SET @responseMessage = 'Failure due to exception'
	END CATCH
END
GO

/****** Object:  StoredProcedure [usr].[UserLogin]    Script Date: 12/02/2020 07:31:37 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO





CREATE PROCEDURE [usr].[UserLogin]
    @Email VARCHAR(50), 
    @Password VARCHAR(50),
    @responseMessage VARCHAR(50)='' OUTPUT
AS
BEGIN

    SET NOCOUNT ON

    DECLARE @userID UNIQUEIDENTIFIER

    IF EXISTS (SELECT TOP 1 ID FROM [usr].[User] WHERE Email=@Email)
    BEGIN
		IF (SELECT TOP 1 [isApproved] FROM [usr].[User] WHERE [Email] = @Email) = 1
		BEGIN
			SET @userID=(SELECT ID FROM [usr].[User] WHERE Email=@Email AND Pass=HASHBYTES('SHA2_512', @Password+CAST(Salt AS NVARCHAR(36))))

			IF(@userID IS NULL)
				SET @responseMessage='Incorrect password'
			ELSE 
				SET @responseMessage='Login successful'
		END
		ELSE
			SET @responseMessage='This account has not been approved'
    END
    ELSE
       SET @responseMessage='Invalid email address'

END
GO


USE [StoreManagement]
GO

/****** Object:  View [admin].[runningQueries]    Script Date: 12/02/2020 07:30:48 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE VIEW [admin].[runningQueries]
AS
SELECT sqltext.TEXT,
req.session_id,
req.status,
req.command,
req.cpu_time,
req.total_elapsed_time
FROM sys.dm_exec_requests req
CROSS APPLY sys.dm_exec_sql_text(sql_handle) AS sqltext
GO

/****** Object:  View [itm].[DepartmentCosts]    Script Date: 12/02/2020 07:30:48 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO




CREATE VIEW [itm].[DepartmentCosts]
AS

	SELECT
		t.[DepartmentCode],
		ISNULL((SELECT 
			SUM([Price]) 
		FROM 
			[itm].[Transaction] 
		WHERE 
			[isRefund] = 0 
			AND 
			[DepartmentCode] = t.[DepartmentCode] 
			AND
			MONTH([TransactionDate]) = MONTH(t.[TransactionDate])
			AND
			YEAR([TransactionDate]) = YEAR(t.[TransactionDate])
		GROUP BY 
			[DepartmentCode], MONTH([TransactionDate]), YEAR([TransactionDate])),0)
		- 
		ISNULL((SELECT 
			SUM([Price]) 
		FROM 
			[itm].[Transaction] 
		WHERE 
			[isRefund] = 1 AND [DepartmentCode] = t.[DepartmentCode]
			AND
			MONTH([TransactionDate]) = MONTH(t.[TransactionDate])
			AND
			YEAR([TransactionDate]) = YEAR(t.[TransactionDate])
		GROUP BY 
		[DepartmentCode], MONTH([TransactionDate]), YEAR([TransactionDate])),0) AS [Total Price],
		MONTH(t.[TransactionDate]) AS [BillingMonth],
		YEAR(t.[TransactionDate]) AS [BillingYear]
	FROM
		[itm].[Transaction] t
	GROUP BY
		t.[DepartmentCode], MONTH(t.[TransactionDate]), YEAR(t.[TransactionDate])

GO

/****** Object:  View [itm].[PendingPurchaseOrders]    Script Date: 12/02/2020 07:30:48 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE VIEW
	[itm].[PendingPurchaseOrders]
AS
	SELECT
		po.[PurchaseOrderID],
		u.[Email],
		po.[GeneratedDate]
	FROM
		[itm].[PurchaseOrder] po
		INNER JOIN
		[usr].[User] u ON
		po.[UserID] = u.[ID]
	WHERE
		[isComplete] = 0
GO

/****** Object:  View [itm].[PurchaseOrdersHistory]    Script Date: 12/02/2020 07:30:48 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE VIEW
	[itm].[PurchaseOrdersHistory]
AS
	SELECT
		po.[PurchaseOrderID],
		u.[Email],
		po.[GeneratedDate],
		po.[completionDate]
	FROM
		[itm].[PurchaseOrder] po
		INNER JOIN
		[usr].[User] u ON
		po.[UserID] = u.[ID]
	WHERE
		[isComplete] = 1
GO

/****** Object:  View [itm].[ViewPurchaseOrderStatus]    Script Date: 12/02/2020 07:30:48 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE VIEW [itm].[ViewPurchaseOrderStatus]
AS
	SELECT
		poi.[PurchaseOrderID],
		poi.[ItemCode],
		poi.[Quantity],
		po.[GeneratedDate],
		poi.[isComplete],
		poi.[completionDate]
	FROM
		[itm].[PurchaseOrderInfo] poi
		INNER JOIN
		[itm].[PurchaseOrder] po
	ON
		poi.[PurchaseOrderID] = po.[PurchaseOrderID]
GO

/****** Object:  View [usr].[WaitingForApproval]    Script Date: 12/02/2020 07:30:48 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO


CREATE VIEW [usr].[WaitingForApproval]
AS

SELECT
	[ID],
	[Email],
	[FirstName],
	[LastName],
	[DepartmentCode],
	[Privileges]
FROM
	[usr].[User]
WHERE
	[isApproved] = 0
GO


USE [StoreManagement]
GO

/****** Object:  Table [itm].[Item]    Script Date: 12/02/2020 07:29:13 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [itm].[Item](
	[Code] [varchar](10) NOT NULL,
	[Name] [varchar](25) NULL,
	[Risk] [bit] NULL,
	[Price] [float] NULL,
	[Quantity] [float] NULL,
	[MinThreshold] [float] NULL,
	[AutoPurchaseOrder] [bit] NULL,
	[onDisplay] [bit] NOT NULL,
PRIMARY KEY CLUSTERED 
(
	[Code] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
GO

/****** Object:  Table [itm].[ItemAssociatedUnitType]    Script Date: 12/02/2020 07:29:13 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [itm].[ItemAssociatedUnitType](
	[ItemCode] [varchar](10) NOT NULL,
	[UnitName] [varchar](50) NOT NULL,
 CONSTRAINT [pk_compositeUnitTypeConstraint] PRIMARY KEY CLUSTERED 
(
	[ItemCode] ASC,
	[UnitName] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
GO

/****** Object:  Table [itm].[PurchaseOrder]    Script Date: 12/02/2020 07:29:13 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [itm].[PurchaseOrder](
	[PurchaseOrderID] [uniqueidentifier] NOT NULL,
	[UserID] [uniqueidentifier] NULL,
	[GeneratedDate] [date] NULL,
	[isComplete] [bit] NOT NULL,
	[completionDate] [date] NULL,
PRIMARY KEY CLUSTERED 
(
	[PurchaseOrderID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
GO

/****** Object:  Table [itm].[PurchaseOrderInfo]    Script Date: 12/02/2020 07:29:13 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [itm].[PurchaseOrderInfo](
	[PurchaseOrderID] [uniqueidentifier] NOT NULL,
	[ItemCode] [varchar](10) NOT NULL,
	[Quantity] [float] NULL,
	[IsComplete] [bit] NULL,
	[completionDate] [date] NULL,
	[ApprovedBy] [uniqueidentifier] NULL,
 CONSTRAINT [pk_compositePurchaseInfoConstraint] PRIMARY KEY CLUSTERED 
(
	[PurchaseOrderID] ASC,
	[ItemCode] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
GO

/****** Object:  Table [itm].[Transaction]    Script Date: 12/02/2020 07:29:13 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [itm].[Transaction](
	[TransactionID] [uniqueidentifier] NOT NULL,
	[UserID] [uniqueidentifier] NOT NULL,
	[DepartmentCode] [char](5) NOT NULL,
	[Price] [float] NULL,
	[TransactionDate] [date] NULL,
	[IsRefund] [bit] NULL,
PRIMARY KEY CLUSTERED 
(
	[TransactionID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
GO

/****** Object:  Table [itm].[TransactionInfo]    Script Date: 12/02/2020 07:29:13 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [itm].[TransactionInfo](
	[TransactionID] [uniqueidentifier] NOT NULL,
	[ItemCode] [varchar](10) NOT NULL,
	[Quantity] [float] NULL,
	[UnitName] [varchar](50) NULL,
 CONSTRAINT [pk_compositeOrderConstraint] PRIMARY KEY CLUSTERED 
(
	[TransactionID] ASC,
	[ItemCode] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
GO

/****** Object:  Table [itm].[Unit]    Script Date: 12/02/2020 07:29:13 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [itm].[Unit](
	[UnitName] [varchar](50) NOT NULL,
	[Val] [float] NULL,
PRIMARY KEY CLUSTERED 
(
	[UnitName] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
GO

/****** Object:  Table [usr].[Department]    Script Date: 12/02/2020 07:29:13 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [usr].[Department](
	[Code] [char](5) NOT NULL,
	[Name] [varchar](25) NULL,
PRIMARY KEY CLUSTERED 
(
	[Code] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
GO

/****** Object:  Table [usr].[Privilege]    Script Date: 12/02/2020 07:29:13 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [usr].[Privilege](
	[AccessLevel] [int] NOT NULL,
	[Name] [varchar](25) NULL,
PRIMARY KEY CLUSTERED 
(
	[AccessLevel] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
GO

/****** Object:  Table [usr].[User]    Script Date: 12/02/2020 07:29:13 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [usr].[User](
	[ID] [uniqueidentifier] NOT NULL,
	[Email] [varchar](50) NOT NULL,
	[FirstName] [varchar](40) NOT NULL,
	[LastName] [varchar](40) NOT NULL,
	[Pass] [binary](64) NOT NULL,
	[Salt] [uniqueidentifier] NOT NULL,
	[DepartmentCode] [char](5) NOT NULL,
	[Privileges] [int] NOT NULL,
	[isApproved] [bit] NULL,
PRIMARY KEY CLUSTERED 
(
	[ID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY],
UNIQUE NONCLUSTERED 
(
	[Email] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
GO

ALTER TABLE [itm].[Item] ADD  DEFAULT ((0)) FOR [AutoPurchaseOrder]
GO

ALTER TABLE [itm].[Item] ADD  DEFAULT ((1)) FOR [onDisplay]
GO

ALTER TABLE [itm].[PurchaseOrder] ADD  DEFAULT (newid()) FOR [PurchaseOrderID]
GO

ALTER TABLE [itm].[PurchaseOrder] ADD  DEFAULT ((0)) FOR [isComplete]
GO

ALTER TABLE [itm].[Transaction] ADD  DEFAULT (newid()) FOR [TransactionID]
GO

ALTER TABLE [itm].[Transaction] ADD  DEFAULT ((0)) FOR [IsRefund]
GO

ALTER TABLE [usr].[User] ADD  DEFAULT (newid()) FOR [ID]
GO

ALTER TABLE [usr].[User] ADD  DEFAULT ((0)) FOR [isApproved]
GO

ALTER TABLE [itm].[ItemAssociatedUnitType]  WITH CHECK ADD FOREIGN KEY([ItemCode])
REFERENCES [itm].[Item] ([Code])
ON DELETE CASCADE
GO

ALTER TABLE [itm].[ItemAssociatedUnitType]  WITH CHECK ADD FOREIGN KEY([UnitName])
REFERENCES [itm].[Unit] ([UnitName])
GO

ALTER TABLE [itm].[PurchaseOrder]  WITH CHECK ADD FOREIGN KEY([UserID])
REFERENCES [usr].[User] ([ID])
GO

ALTER TABLE [itm].[PurchaseOrderInfo]  WITH CHECK ADD FOREIGN KEY([ApprovedBy])
REFERENCES [usr].[User] ([ID])
GO

ALTER TABLE [itm].[PurchaseOrderInfo]  WITH CHECK ADD FOREIGN KEY([ItemCode])
REFERENCES [itm].[Item] ([Code])
GO

ALTER TABLE [itm].[PurchaseOrderInfo]  WITH CHECK ADD FOREIGN KEY([PurchaseOrderID])
REFERENCES [itm].[PurchaseOrder] ([PurchaseOrderID])
GO

ALTER TABLE [itm].[Transaction]  WITH CHECK ADD FOREIGN KEY([DepartmentCode])
REFERENCES [usr].[Department] ([Code])
GO

ALTER TABLE [itm].[Transaction]  WITH CHECK ADD FOREIGN KEY([UserID])
REFERENCES [usr].[User] ([ID])
GO

ALTER TABLE [itm].[TransactionInfo]  WITH CHECK ADD FOREIGN KEY([TransactionID])
REFERENCES [itm].[Transaction] ([TransactionID])
GO

ALTER TABLE [itm].[TransactionInfo]  WITH CHECK ADD FOREIGN KEY([UnitName])
REFERENCES [itm].[Unit] ([UnitName])
GO

ALTER TABLE [usr].[User]  WITH CHECK ADD FOREIGN KEY([DepartmentCode])
REFERENCES [usr].[Department] ([Code])
GO

ALTER TABLE [usr].[User]  WITH CHECK ADD FOREIGN KEY([Privileges])
REFERENCES [usr].[Privilege] ([AccessLevel])
GO


