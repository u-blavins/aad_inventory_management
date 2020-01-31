USE [StoreManagement]
GO
CREATE SCHEMA [usr]
GO
DROP TABLE [usr].[User]
GO
CREATE TABLE [usr].[User] (
	ID UNIQUEIDENTIFIER DEFAULT NEWID() PRIMARY KEY NOT NULL,
	Email VARCHAR(50) UNIQUE NOT NULL,
	FirstName VARCHAR(40) NOT NULL,
	LastName VARCHAR(40) NOT NULL,
	Pass BINARY(64) NOT NULL,
	Salt UNIQUEIDENTIFIER NOT NULL,
	DepartmentCode CHAR(5) NOT NULL,
	isStaff BIT NOT NULL DEFAULT 0
)
GO
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
	@isStaff BIT = 0,
    @responseMessage NVARCHAR(250) OUTPUT
)
AS

BEGIN
    SET NOCOUNT ON

    DECLARE @salt UNIQUEIDENTIFIER=NEWID()
    BEGIN TRY

        INSERT INTO [usr].[User] (Email, FirstName, LastName, Pass, Salt,DepartmentCode, isStaff)
        VALUES(@Email, @FirstName, @LastName, HASHBYTES('SHA2_512', @Password+CAST(@salt AS NVARCHAR(36))), @salt, @DepartmentCode,@isStaff)

       SET @responseMessage='Success'

    END TRY
    BEGIN CATCH
        SET @responseMessage='Failure'
    END CATCH

END
GO

ALTER PROCEDURE [usr].[UserLogin]
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

CREATE PROCEDURE [usr].[getUser](
	@Email VARCHAR(50)
)
AS
	IF EXISTS (SELECT TOP 1 ID FROM [usr].[User] WHERE Email=@Email)
	BEGIN
		SELECT
			[Email],
			[Firstname],
			[LastName],
			[DepartmentCode],
			[isStaff]
		FROM [usr].[User]
		WHERE [Email] = @Email
	END
		
GO

CREATE SCHEMA [itm]
GO

