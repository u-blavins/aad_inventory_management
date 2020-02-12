USE [StoreManagement]
GO

/****** Object:  StoredProcedure [itm].[createTransaction]    Script Date: 05/02/2020 00:47:30 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO


CREATE PROCEDURE [itm].[createTransaction]
(
	@UserID VARCHAR(250),
	@Price FLOAT,
	@isRefund BIT,
	@responseMessage UNIQUEIDENTIFIER OUTPUT
)
AS
BEGIN
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

/****** Object:  StoredProcedure [itm].[createTransactionInfo]    Script Date: 05/02/2020 00:47:31 ******/
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

/****** Object:  StoredProcedure [usr].[CreateUser]    Script Date: 05/02/2020 00:47:31 ******/
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

        INSERT INTO [usr].[User] (Email, FirstName, LastName, Pass, Salt,DepartmentCode, Privileges)
        VALUES(@Email, @FirstName, @LastName, HASHBYTES('SHA2_512', @Password+CAST(@salt AS NVARCHAR(36))), @salt, @DepartmentCode,@Privileges)

       SET @responseMessage='Success'

    END TRY
    BEGIN CATCH
        SET @responseMessage='Failure'
    END CATCH

END
GO

/****** Object:  StoredProcedure [usr].[getUser]    Script Date: 05/02/2020 00:47:31 ******/
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

/****** Object:  StoredProcedure [usr].[UserLogin]    Script Date: 05/02/2020 00:47:32 ******/
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
        SET @userID=(SELECT ID FROM [usr].[User] WHERE Email=@Email AND Pass=HASHBYTES('SHA2_512', @Password+CAST(Salt AS NVARCHAR(36))))

       IF(@userID IS NULL)
           SET @responseMessage='Incorrect password'
       ELSE 
           SET @responseMessage='Login successful'
    END
    ELSE
       SET @responseMessage='Invalid username'

END
GO

/****** Object:  Trigger [itm].[RefreshStock]    Script Date: 05/02/2020 00:49:48 ******/
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

	DECLARE @isComplete BIT = (SELECT TOP 1 [isComplete] FROM updated)
	IF @isComplete = 1
	BEGIN
		UPDATE
			[itm].[Item]
		SET
			[Quantity] = [Quantity] + (SELECT TOP 1 [Quantity] FROM updated)
		WHERE
			[Code] = (SELECT TOP 1 [ItemCode] FROM updated)
	END	

END
GO

ALTER TABLE [itm].[PurchaseOrderInfo] ENABLE TRIGGER [RefreshStock]
GO

/****** Object:  Trigger [itm].[UpdateStock]    Script Date: 05/02/2020 00:50:03 ******/
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

UPDATE 
	[itm].[Item]
SET
	[Quantity] = [Quantity] - @ConvertedVal
WHERE
	[Code] = @ItemCode
END
GO

ALTER TABLE [itm].[TransactionInfo] ENABLE TRIGGER [UpdateStock]
GO

