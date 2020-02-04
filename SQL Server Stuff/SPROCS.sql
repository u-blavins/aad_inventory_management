USE [StoreManagement]
GO

/****** Object:  StoredProcedure [usr].[CreateUser]    Script Date: 03/02/2020 23:31:07 ******/
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

/****** Object:  StoredProcedure [usr].[getUser]    Script Date: 03/02/2020 23:31:07 ******/
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

/****** Object:  StoredProcedure [usr].[UserLogin]    Script Date: 03/02/2020 23:31:07 ******/
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


