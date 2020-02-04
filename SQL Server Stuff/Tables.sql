CREATE DATABASE [StoreManagement]
GO

USE [StoreManagement]
GO

CREATE SCHEMA [itm]
GO

CREATE SCHEMA [usr]
GO

/****** Object:  Table [itm].[Item]    Script Date: 03/02/2020 23:24:31 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [itm].[Item](
	[Code] [varchar](10) NOT NULL,
	[Name] [varchar](25) NULL,
	[UnitName] [varchar](50) NULL,
	[Risk] [bit] NULL,
	[Price] [float] NULL,
	[StockCode] [varchar](10) NULL,
PRIMARY KEY CLUSTERED 
(
	[Code] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
GO

/****** Object:  Table [itm].[Stock]    Script Date: 03/02/2020 23:24:31 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [itm].[Stock](
	[StockCode] [varchar](10) NOT NULL,
	[Quantity] [float] NULL,
	[UnitName] [varchar](50) NULL,
	[MinThreshold] [float] NULL,
	[MaxThreshold] [float] NULL,
PRIMARY KEY CLUSTERED 
(
	[StockCode] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
GO

/****** Object:  Table [itm].[Transaction]    Script Date: 03/02/2020 23:24:31 ******/
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

/****** Object:  Table [itm].[TransactionInfo]    Script Date: 03/02/2020 23:24:31 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [itm].[TransactionInfo](
	[TransactionID] [uniqueidentifier] NOT NULL,
	[ItemCode] [varchar](10) NOT NULL,
	[UnitName] [varchar](50) NOT NULL,
	[Quantity] [varchar](10) NULL,
 CONSTRAINT [pk_compositeOrderConstraint] PRIMARY KEY CLUSTERED 
(
	[TransactionID] ASC,
	[ItemCode] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
GO

/****** Object:  Table [itm].[Unit]    Script Date: 03/02/2020 23:24:31 ******/
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

/****** Object:  Table [usr].[Department]    Script Date: 03/02/2020 23:24:31 ******/
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

/****** Object:  Table [usr].[Privilege]    Script Date: 03/02/2020 23:24:31 ******/
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

/****** Object:  Table [usr].[User]    Script Date: 03/02/2020 23:24:31 ******/
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
